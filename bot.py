import discord
 
TOKEN = 'MTE3NTM2OTA2NzU2MjAyOTA4Nw.GYaSTZ.wLCykJ6IiAWlJbciZYNTz7bKaE1Ur1Edyr1_Lo'
CHANNEL_ID = '1175798021104095302'
 
 
class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send('Hello World')
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
