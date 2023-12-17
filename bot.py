import discord

with open('bot_token.txt', 'r') as file:
    token = file.readline()

TOKEN = token
CHANNEL_ID = '1175798021104095302'
 
 
class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send('Hello World')
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
