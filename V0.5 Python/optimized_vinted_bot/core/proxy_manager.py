"""
Advanced Proxy Management System with rotation and health monitoring
"""

import asyncio
import random
import time
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import aiohttp
import json
from urllib.parse import urlparse

@dataclass
class ProxyInfo:
    """Information about a proxy server"""
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: str = "http"  # http, https, socks5
    success_count: int = 0
    failure_count: int = 0
    last_used: float = 0
    last_health_check: float = 0
    is_healthy: bool = True
    response_time: float = 0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate of the proxy"""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0
        
    @property
    def formatted_url(self) -> str:
        """Get formatted proxy URL with authentication"""
        if self.username and self.password:
            parsed = urlparse(self.url)
            return f"{parsed.scheme}://{self.username}:{self.password}@{parsed.netloc}"
        return self.url
        
    def record_success(self, response_time: float = 0):
        """Record a successful request"""
        self.success_count += 1
        self.last_used = time.time()
        self.response_time = response_time
        self.is_healthy = True
        
    def record_failure(self):
        """Record a failed request"""
        self.failure_count += 1
        self.last_used = time.time()
        if self.failure_count >= 5:  # Mark as unhealthy after 5 consecutive failures
            self.is_healthy = False

class ProxyRotator:
    """Smart proxy rotation with health monitoring"""
    
    def __init__(self, proxy_list_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.proxies: List[ProxyInfo] = []
        self.current_index = 0
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = 0
        self.proxy_list_file = proxy_list_file
        
        if proxy_list_file:
            self.load_proxies_from_file(proxy_list_file)
            
    def load_proxies_from_file(self, file_path: str):
        """Load proxies from a text file"""
        try:
            proxy_file = Path(file_path)
            if not proxy_file.exists():
                self.logger.warning(f"Proxy file not found: {file_path}")
                return
                
            with open(proxy_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    try:
                        proxy_info = self._parse_proxy_line(line)
                        if proxy_info:
                            self.proxies.append(proxy_info)
                    except Exception as e:
                        self.logger.error(f"Error parsing proxy line {line_num}: {e}")
                        
            self.logger.info(f"Loaded {len(self.proxies)} proxies from {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error loading proxy file: {e}")
            
    def _parse_proxy_line(self, line: str) -> Optional[ProxyInfo]:
        """Parse a single proxy line from the file"""
        # Support formats:
        # http://proxy:port
        # http://user:pass@proxy:port
        # proxy:port
        # user:pass@proxy:port
        
        if '://' not in line:
            # Add default protocol
            line = f"http://{line}"
            
        parsed = urlparse(line)
        
        if not parsed.hostname or not parsed.port:
            return None
            
        return ProxyInfo(
            url=f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
            username=parsed.username,
            password=parsed.password,
            proxy_type=parsed.scheme
        )
        
    def add_proxy(self, proxy_url: str, username: str = None, password: str = None, proxy_type: str = "http"):
        """Add a proxy to the rotation pool"""
        proxy_info = ProxyInfo(
            url=proxy_url,
            username=username,
            password=password,
            proxy_type=proxy_type
        )
        self.proxies.append(proxy_info)
        self.logger.info(f"Added proxy: {proxy_url}")
        
    def get_next_proxy(self) -> Optional[ProxyInfo]:
        """Get the next proxy in rotation (round-robin with health check)"""
        if not self.proxies:
            return None
            
        # Filter healthy proxies
        healthy_proxies = [p for p in self.proxies if p.is_healthy]
        
        if not healthy_proxies:
            self.logger.warning("No healthy proxies available, using any available proxy")
            healthy_proxies = self.proxies
            
        # Use round-robin rotation
        if self.current_index >= len(healthy_proxies):
            self.current_index = 0
            
        proxy = healthy_proxies[self.current_index]
        self.current_index += 1
        
        return proxy
        
    def get_random_proxy(self) -> Optional[ProxyInfo]:
        """Get a random healthy proxy"""
        healthy_proxies = [p for p in self.proxies if p.is_healthy]
        
        if not healthy_proxies:
            healthy_proxies = self.proxies
            
        if not healthy_proxies:
            return None
            
        return random.choice(healthy_proxies)
        
    def get_best_proxy(self) -> Optional[ProxyInfo]:
        """Get the proxy with the best success rate and lowest response time"""
        healthy_proxies = [p for p in self.proxies if p.is_healthy]
        
        if not healthy_proxies:
            return None
            
        # Sort by success rate (desc) and response time (asc)
        best_proxy = max(
            healthy_proxies,
            key=lambda p: (p.success_rate, -p.response_time)
        )
        
        return best_proxy
        
    async def health_check_proxy(self, proxy: ProxyInfo) -> bool:
        """Check if a proxy is healthy"""
        test_url = "https://httpbin.org/ip"
        timeout = aiohttp.ClientTimeout(total=10)
        
        try:
            connector = aiohttp.TCPConnector()
            proxy_url = proxy.formatted_url
            
            start_time = time.time()
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            ) as session:
                async with session.get(test_url, proxy=proxy_url) as response:
                    if response.status == 200:
                        response_time = time.time() - start_time
                        proxy.record_success(response_time)
                        proxy.last_health_check = time.time()
                        self.logger.debug(f"Proxy {proxy.url} health check: OK ({response_time:.2f}s)")
                        return True
                        
        except Exception as e:
            proxy.record_failure()
            proxy.last_health_check = time.time()
            self.logger.debug(f"Proxy {proxy.url} health check failed: {e}")
            return False
            
        return False
        
    async def health_check_all_proxies(self):
        """Run health checks on all proxies"""
        if not self.proxies:
            return
            
        self.logger.info(f"Running health check on {len(self.proxies)} proxies")
        
        tasks = []
        for proxy in self.proxies:
            # Only check proxies that haven't been checked recently
            if time.time() - proxy.last_health_check > self.health_check_interval:
                tasks.append(self.health_check_proxy(proxy))
            else:
                tasks.append(asyncio.sleep(0))  # Skip but maintain order
                
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        healthy_count = sum(1 for p in self.proxies if p.is_healthy)
        self.logger.info(f"Health check complete: {healthy_count}/{len(self.proxies)} proxies healthy")
        
    def get_proxy_stats(self) -> Dict:
        """Get statistics about proxy pool"""
        if not self.proxies:
            return {"total": 0, "healthy": 0, "unhealthy": 0, "average_success_rate": 0}
            
        healthy = sum(1 for p in self.proxies if p.is_healthy)
        unhealthy = len(self.proxies) - healthy
        avg_success_rate = sum(p.success_rate for p in self.proxies) / len(self.proxies)
        
        return {
            "total": len(self.proxies),
            "healthy": healthy,
            "unhealthy": unhealthy,
            "average_success_rate": avg_success_rate,
            "proxies": [
                {
                    "url": p.url,
                    "is_healthy": p.is_healthy,
                    "success_rate": p.success_rate,
                    "response_time": p.response_time,
                    "success_count": p.success_count,
                    "failure_count": p.failure_count
                }
                for p in self.proxies
            ]
        }
        
    def remove_unhealthy_proxies(self, min_success_rate: float = 0.1):
        """Remove proxies with very low success rates"""
        initial_count = len(self.proxies)
        
        self.proxies = [
            p for p in self.proxies 
            if p.success_rate >= min_success_rate or (p.success_count + p.failure_count) < 10
        ]
        
        removed_count = initial_count - len(self.proxies)
        if removed_count > 0:
            self.logger.info(f"Removed {removed_count} unhealthy proxies")
            
    async def start_health_monitoring(self):
        """Start background health monitoring"""
        self.logger.info("Starting proxy health monitoring")
        
        while True:
            try:
                await self.health_check_all_proxies()
                self.remove_unhealthy_proxies()
                await asyncio.sleep(self.health_check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying


class ProxyManager:
    """Main proxy manager with advanced features"""
    
    def __init__(self, proxy_list_file: Optional[str] = None, enable_rotation: bool = True):
        self.logger = logging.getLogger(__name__)
        self.enable_rotation = enable_rotation
        self.rotator = ProxyRotator(proxy_list_file) if enable_rotation else None
        self.request_count = 0
        self.last_rotation = time.time()
        self.rotation_interval = 10  # Rotate every 10 requests
        
        # Start health monitoring task
        if self.rotator:
            asyncio.create_task(self.rotator.start_health_monitoring())
            
    async def get_proxy_for_request(self, strategy: str = "round_robin") -> Optional[Tuple[str, Dict]]:
        """
        Get a proxy for making a request
        
        Args:
            strategy: "round_robin", "random", "best", or "none"
            
        Returns:
            Tuple of (proxy_url, proxy_config) or None
        """
        if not self.enable_rotation or not self.rotator or strategy == "none":
            return None
            
        proxy_info = None
        
        if strategy == "round_robin":
            proxy_info = self.rotator.get_next_proxy()
        elif strategy == "random":
            proxy_info = self.rotator.get_random_proxy()
        elif strategy == "best":
            proxy_info = self.rotator.get_best_proxy()
            
        if not proxy_info:
            return None
            
        proxy_config = {
            "http": proxy_info.formatted_url,
            "https": proxy_info.formatted_url,
        }
        
        return proxy_info.formatted_url, proxy_config
        
    def record_request_result(self, proxy_url: str, success: bool, response_time: float = 0):
        """Record the result of a request for proxy statistics"""
        if not self.rotator:
            return
            
        for proxy in self.rotator.proxies:
            if proxy.formatted_url == proxy_url:
                if success:
                    proxy.record_success(response_time)
                else:
                    proxy.record_failure()
                break
                
    def get_stats(self) -> Dict:
        """Get proxy manager statistics"""
        if not self.rotator:
            return {"proxy_rotation": False, "total_requests": self.request_count}
            
        stats = self.rotator.get_proxy_stats()
        stats["proxy_rotation"] = True
        stats["total_requests"] = self.request_count
        
        return stats
