import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!addlink'):
        channel = discord.MessageReference.channel_id
        print(channel)
        await message.channel.send('Hello!')

client.run('MTE1MTg5MDg0ODM4NTA4NTUyMw.G1CWu5.ehGimOTqhjIZ_h1bGjkMhwuC7fOdTX7WIu_mmY')



