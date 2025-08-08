"""
Discord Bot implementation with advanced features
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

import discord
from discord.ext import commands, tasks

try:
    from ..core.vinted_api import VintedAPIClient, VintedItem
    from ..core.proxy_manager import ProxyManager
    from ..core.database import DatabaseManager
    from ..config.settings import settings
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from core.vinted_api import VintedAPIClient, VintedItem
    from core.proxy_manager import ProxyManager
    from core.database import DatabaseManager
    from config.settings import settings

class VintedDiscordBot:
    """Advanced Vinted Discord Bot"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.proxy_manager = ProxyManager(
            proxy_list_file=settings.proxy.proxy_list_file,
            enable_rotation=settings.proxy.rotation_enabled
        ) if settings.proxy.enabled else None
        
        self.vinted_client = VintedAPIClient(self.proxy_manager)
        self.database = DatabaseManager()
        
        # Discord bot setup
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(
            command_prefix=settings.discord.command_prefix,
            intents=intents,
            help_command=None
        )
        
        # Bot state
        self.is_running = False
        self.monitor_tasks = {}
        self.stats = {
            "items_published": 0,
            "total_checks": 0,
            "errors": 0,
            "start_time": time.time()
        }
        
        # Setup bot events and commands
        self._setup_events()
        self._setup_commands()
        
    def _setup_events(self):
        """Setup Discord bot events"""
        
        @self.bot.event
        async def on_ready():
            self.logger.info(f'Bot logged in as {self.bot.user}')
            self.is_running = True
            
            # Start background tasks
            if not self.monitor_all_channels.is_running():
                self.monitor_all_channels.start()
                
            if settings.monitoring.enabled and not self.health_check_task.is_running():
                self.health_check_task.start()
                
            # Start Vinted API client
            await self.vinted_client.start_session()
            
            # Start database cleanup task
            asyncio.create_task(self.database.start_cleanup_task())
            
        @self.bot.event
        async def on_disconnect():
            self.logger.warning("Bot disconnected from Discord")
            
        @self.bot.event
        async def on_resumed():
            self.logger.info("Bot reconnected to Discord")
            
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return  # Ignore unknown commands
                
            self.logger.error(f"Command error in {ctx.command}: {error}")
            
            # Log to database
            self.database.log_error(
                error_type="command_error",
                error_message=str(error),
                context=f"Command: {ctx.command}, User: {ctx.author}",
                channel_id=ctx.channel.id if ctx.channel else None
            )
            
            try:
                await ctx.send(f"❌ Une erreur s'est produite: {error}")
            except:
                pass  # Channel might be unavailable
                
    def _setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='addlink')
        async def add_link(ctx, *, search_url: str):
            """Add a Vinted search URL to monitor for new items"""
            try:
                channel_id = ctx.channel.id
                
                # Validate URL
                if "vinted.com" not in search_url or "catalog" not in search_url:
                    await ctx.send("❌ URL invalide. Veuillez fournir une URL de recherche Vinted valide.")
                    return
                    
                # Check if channel already has a search configured
                existing_config = self.database.get_search_config(channel_id)
                if existing_config:
                    await ctx.send(f"⚠️ Ce canal surveille déjà: `{existing_config['search_url']}`\n"
                                 f"Utilisez `{settings.discord.command_prefix}removelink` pour le supprimer d'abord.")
                    return
                    
                # Test the search URL
                await ctx.send("🔄 Test de l'URL de recherche...")
                
                try:
                    items = await self.vinted_client.get_latest_items(search_url, max_items=1)
                    if not items:
                        await ctx.send("⚠️ Aucun article trouvé avec cette URL. Vérifiez que l'URL est correcte.")
                        return
                except Exception as e:
                    self.logger.error(f"Error testing search URL: {e}")
                    await ctx.send("❌ Erreur lors du test de l'URL. Vérifiez qu'elle est correcte.")
                    return
                    
                # Add to database
                if self.database.add_search_config(channel_id, search_url):
                    await ctx.send(f"✅ URL ajoutée avec succès!\n"
                                 f"Le bot surveillera maintenant: `{search_url}`\n"
                                 f"Les nouveaux articles seront postés dans ce canal.")
                    
                    # Start monitoring for this channel
                    await self._start_channel_monitoring(channel_id, search_url)
                else:
                    await ctx.send("❌ Erreur lors de l'ajout de l'URL.")
                    
            except Exception as e:
                self.logger.error(f"Error in add_link command: {e}")
                await ctx.send("❌ Une erreur s'est produite lors de l'ajout de l'URL.")
                
        @self.bot.command(name='removelink')
        async def remove_link(ctx):
            """Remove the monitored search URL from this channel"""
            try:
                channel_id = ctx.channel.id
                
                config = self.database.get_search_config(channel_id)
                if not config:
                    await ctx.send("❌ Aucune URL configurée pour ce canal.")
                    return
                    
                if self.database.remove_search_config(channel_id):
                    await ctx.send(f"✅ URL supprimée: `{config['search_url']}`")
                    
                    # Stop monitoring for this channel
                    if channel_id in self.monitor_tasks:
                        self.monitor_tasks[channel_id].cancel()
                        del self.monitor_tasks[channel_id]
                else:
                    await ctx.send("❌ Erreur lors de la suppression de l'URL.")
                    
            except Exception as e:
                self.logger.error(f"Error in remove_link command: {e}")
                await ctx.send("❌ Une erreur s'est produite.")
                
        @self.bot.command(name='viewlink')
        async def view_link(ctx):
            """View the current search URL for this channel"""
            try:
                channel_id = ctx.channel.id
                config = self.database.get_search_config(channel_id)
                
                if not config:
                    await ctx.send("❌ Aucune URL configurée pour ce canal.")
                    return
                    
                embed = discord.Embed(
                    title="🔗 Configuration du canal",
                    color=0x00ff00 if config["is_active"] else 0xff0000
                )
                
                embed.add_field(
                    name="URL de recherche",
                    value=f"`{config['search_url']}`",
                    inline=False
                )
                
                embed.add_field(
                    name="Statut",
                    value="✅ Actif" if config["is_active"] else "❌ Inactif",
                    inline=True
                )
                
                embed.add_field(
                    name="Articles trouvés",
                    value=str(config["items_found_count"]),
                    inline=True
                )
                
                embed.add_field(
                    name="Erreurs",
                    value=str(config["errors_count"]),
                    inline=True
                )
                
                if config["last_check"]:
                    last_check = datetime.fromtimestamp(config["last_check"])
                    embed.add_field(
                        name="Dernière vérification",
                        value=last_check.strftime("%d/%m/%Y %H:%M:%S"),
                        inline=False
                    )
                    
                await ctx.send(embed=embed)
                
            except Exception as e:
                self.logger.error(f"Error in view_link command: {e}")
                await ctx.send("❌ Une erreur s'est produite.")
                
        @self.bot.command(name='test')
        async def test_search(ctx, *, search_url: str = None):
            """Test a search URL and show the latest item"""
            try:
                if not search_url:
                    # Use configured URL for this channel
                    config = self.database.get_search_config(ctx.channel.id)
                    if not config:
                        await ctx.send("❌ Aucune URL configurée. Utilisez: `!test <url>` ou configurez une URL avec `!addlink`")
                        return
                    search_url = config["search_url"]
                    
                await ctx.send("🔄 Test de la recherche...")
                
                items = await self.vinted_client.get_latest_items(search_url, max_items=1)
                
                if not items:
                    await ctx.send("❌ Aucun article trouvé.")
                    return
                    
                item = items[0]
                embed = self._create_item_embed(item)
                view = self._create_item_view(item)
                
                await ctx.send("✅ Test réussi! Voici le dernier article trouvé:", embed=embed, view=view)
                
            except Exception as e:
                self.logger.error(f"Error in test command: {e}")
                await ctx.send("❌ Erreur lors du test.")
                
        @self.bot.command(name='stats')
        async def show_stats(ctx):
            """Show bot statistics"""
            try:
                embed = discord.Embed(
                    title="📊 Statistiques du Bot",
                    color=0x0099ff
                )
                
                # Bot stats
                uptime = time.time() - self.stats["start_time"]
                uptime_str = f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m"
                
                embed.add_field(name="⏱️ Uptime", value=uptime_str, inline=True)
                embed.add_field(name="📦 Articles publiés", value=str(self.stats["items_published"]), inline=True)
                embed.add_field(name="🔍 Vérifications totales", value=str(self.stats["total_checks"]), inline=True)
                embed.add_field(name="❌ Erreurs", value=str(self.stats["errors"]), inline=True)
                
                # Active channels
                configs = self.database.get_all_search_configs()
                embed.add_field(name="📺 Canaux actifs", value=str(len(configs)), inline=True)
                
                # API stats
                api_stats = self.vinted_client.get_stats()
                if api_stats["total_requests"] > 0:
                    success_rate = (api_stats["successful_requests"] / api_stats["total_requests"]) * 100
                    embed.add_field(name="📡 Taux de succès API", value=f"{success_rate:.1f}%", inline=True)
                    
                # Proxy stats
                if self.proxy_manager:
                    proxy_stats = self.proxy_manager.get_stats()
                    if proxy_stats.get("total") > 0:
                        embed.add_field(
                            name="🔄 Proxies",
                            value=f"{proxy_stats['healthy']}/{proxy_stats['total']} sains",
                            inline=True
                        )
                        
                # Database stats
                db_stats = self.database.get_database_stats()
                embed.add_field(
                    name="💾 Base de données",
                    value=f"{db_stats.get('published_items_count', 0)} articles\n{db_stats.get('database_size_mb', 0):.1f} MB",
                    inline=True
                )
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                self.logger.error(f"Error in stats command: {e}")
                await ctx.send("❌ Erreur lors de l'affichage des statistiques.")
                
        @self.bot.command(name='help')
        async def show_help(ctx):
            """Show help information"""
            embed = discord.Embed(
                title="🤖 Aide - Bot Vinted",
                description="Bot pour surveiller les nouveaux articles Vinted",
                color=0x0099ff
            )
            
            commands_info = [
                (f"`{settings.discord.command_prefix}addlink <url>`", "Ajouter une URL de recherche Vinted à surveiller"),
                (f"`{settings.discord.command_prefix}removelink`", "Supprimer l'URL configurée pour ce canal"),
                (f"`{settings.discord.command_prefix}viewlink`", "Voir la configuration actuelle du canal"),
                (f"`{settings.discord.command_prefix}test [url]`", "Tester une URL de recherche"),
                (f"`{settings.discord.command_prefix}stats`", "Afficher les statistiques du bot"),
                (f"`{settings.discord.command_prefix}help`", "Afficher cette aide"),
            ]
            
            for cmd, desc in commands_info:
                embed.add_field(name=cmd, value=desc, inline=False)
                
            embed.add_field(
                name="📝 Comment utiliser",
                value=(
                    "1. Allez sur vinted.com et effectuez votre recherche\n"
                    "2. Copiez l'URL de la page de résultats\n"
                    f"3. Utilisez `{settings.discord.command_prefix}addlink <url>` dans le canal souhaité\n"
                    "4. Le bot publiera automatiquement les nouveaux articles!"
                ),
                inline=False
            )
            
            await ctx.send(embed=embed)
            
    def _create_item_embed(self, item: VintedItem) -> discord.Embed:
        """Create a Discord embed for a Vinted item"""
        embed = discord.Embed(
            title=item.title[:256],  # Discord title limit
            url=item.url,
            color=0x00a651  # Vinted green
        )
        
        # Add fields
        if item.price:
            embed.add_field(name="💰 Prix", value=f"{item.price} {item.currency}", inline=True)
        if item.brand:
            embed.add_field(name="🏷️ Marque", value=item.brand, inline=True)
        if item.size:
            embed.add_field(name="📏 Taille", value=item.size, inline=True)
        if item.condition:
            embed.add_field(name="✨ État", value=item.condition, inline=True)
        if item.user_login:
            embed.add_field(name="👤 Vendeur", value=item.user_login, inline=True)
        if item.location:
            embed.add_field(name="📍 Localisation", value=item.location, inline=True)
            
        # Add image
        if item.photo_url:
            embed.set_image(url=item.photo_url)
            
        # Add footer
        embed.set_footer(text="Vinted Bot", icon_url="https://www.vinted.com/favicon.ico")
        embed.timestamp = datetime.now()
        
        return embed
        
    def _create_item_view(self, item: VintedItem) -> discord.ui.View:
        """Create a Discord view with buttons for a Vinted item"""
        view = discord.ui.View(timeout=None)
        
        # Add "View Item" button
        view.add_item(discord.ui.Button(
            label="Voir l'article",
            url=item.url,
            style=discord.ButtonStyle.link,
            emoji="👀"
        ))
        
        return view
        
    async def _start_channel_monitoring(self, channel_id: int, search_url: str):
        """Start monitoring a specific channel"""
        if channel_id in self.monitor_tasks:
            self.monitor_tasks[channel_id].cancel()
            
        task = asyncio.create_task(self._monitor_channel(channel_id, search_url))
        self.monitor_tasks[channel_id] = task
        
    async def _monitor_channel(self, channel_id: int, search_url: str):
        """Monitor a channel for new items"""
        self.logger.info(f"Starting monitoring for channel {channel_id}")
        
        while True:
            try:
                # Get latest items
                items = await self.vinted_client.get_latest_items(search_url, max_items=10)
                
                if items:
                    new_items = []
                    for item in items:
                        if not self.database.is_item_published(item.id, channel_id):
                            new_items.append(item)
                            
                    if new_items:
                        channel = self.bot.get_channel(channel_id)
                        if channel:
                            for item in new_items:
                                try:
                                    embed = self._create_item_embed(item)
                                    view = self._create_item_view(item)
                                    
                                    await channel.send(embed=embed, view=view)
                                    
                                    # Mark as published
                                    self.database.mark_item_published(item, channel_id, search_url)
                                    self.stats["items_published"] += 1
                                    
                                    # Small delay between messages
                                    await asyncio.sleep(1)
                                    
                                except Exception as e:
                                    self.logger.error(f"Error sending item to channel {channel_id}: {e}")
                                    
                    # Update stats
                    self.database.update_search_config_stats(channel_id, len(new_items))
                else:
                    # Update stats even if no items found
                    self.database.update_search_config_stats(channel_id, 0)
                    
                self.stats["total_checks"] += 1
                
            except Exception as e:
                self.logger.error(f"Error monitoring channel {channel_id}: {e}")
                self.database.update_search_config_stats(channel_id, error_occurred=True)
                self.database.log_error(
                    error_type="monitoring_error",
                    error_message=str(e),
                    context=f"Channel monitoring",
                    channel_id=channel_id,
                    search_url=search_url
                )
                self.stats["errors"] += 1
                
            # Wait before next check (with some randomization)
            import random
            wait_time = random.uniform(30, 60)  # 30-60 seconds
            await asyncio.sleep(wait_time)
            
    @tasks.loop(minutes=5)
    async def monitor_all_channels(self):
        """Monitor all configured channels"""
        try:
            configs = self.database.get_all_search_configs()
            
            for config in configs:
                channel_id = config["channel_id"]
                search_url = config["search_url"]
                
                # Start monitoring if not already running
                if channel_id not in self.monitor_tasks or self.monitor_tasks[channel_id].done():
                    await self._start_channel_monitoring(channel_id, search_url)
                    
        except Exception as e:
            self.logger.error(f"Error in monitor_all_channels: {e}")
            
    @tasks.loop(minutes=30)
    async def health_check_task(self):
        """Periodic health check and statistics saving"""
        try:
            # Save statistics
            stats = {
                "total_requests": self.vinted_client.request_count,
                "successful_requests": self.vinted_client.success_count,
                "failed_requests": self.vinted_client.error_count,
                "items_published": self.stats["items_published"],
                "active_channels": len(self.database.get_all_search_configs())
            }
            
            if self.proxy_manager:
                stats["proxy_stats"] = self.proxy_manager.get_stats()
                
            self.database.save_bot_stats(stats)
            
            self.logger.info(f"Health check: {stats}")
            
        except Exception as e:
            self.logger.error(f"Error in health check: {e}")
            
    async def start(self):
        """Start the bot"""
        self.logger.info("Starting Vinted Discord Bot...")
        
        if not settings.discord.token:
            self.logger.error("Discord bot token not provided!")
            return
            
        try:
            await self.bot.start(settings.discord.token)
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            raise
            
    async def stop(self):
        """Stop the bot gracefully"""
        self.logger.info("Stopping bot...")
        
        # Cancel all monitoring tasks
        for task in self.monitor_tasks.values():
            task.cancel()
            
        # Stop background tasks
        if self.monitor_all_channels.is_running():
            self.monitor_all_channels.cancel()
            
        if self.health_check_task.is_running():
            self.health_check_task.cancel()
            
        # Close API client
        if self.vinted_client:
            await self.vinted_client.close_session()
            
        # Close bot
        if not self.bot.is_closed():
            await self.bot.close()
            
        self.is_running = False
        self.logger.info("Bot stopped successfully")
