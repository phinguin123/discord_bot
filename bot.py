import discord
from datetime import datetime, time, timedelta
import asyncio
import pytz
from discord.ext import commands
from time import sleep

with open('/home/ubuntu/discord_bot/bot_token.txt', 'r') as file:
    token = file.readline()

TOKEN = token
CHANNEL_ID = '1175798021104095302'

users = []

MIDNIGHT = datetime(2023,12,18,0,0)
seoul_timezone = pytz.timezone('Asia/Seoul')
def get_current_time():
    # Get the current time
    current_time = datetime.now(seoul_timezone)

    time_in_seconds = (current_time.hour * 3600) + (current_time.minute * 60) + current_time.second

    return time_in_seconds

class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.total_time = 0
        self.start = 0
    
    def reset(self):
        self.total_time = 0
        self.start = 0


class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send('Bot started')
        await self.background_task()

    async def on_message(self, message):
        #print('inside on message')
        if message.author == self.user:
            #await message.channel.send("hello {0.author.mention}".format(message))
            return

        for user in users:
            if message.content == "!"+user.name.lower():

                await message.channel.send("{0}    {1:.2f} / 6시간".format(user.name,user.total_time/3600))
                return

    async def on_voice_state_update(self, member, before, after):
        for user in users:
            if user.id == member.id:
                channel = self.get_channel(int(CHANNEL_ID))
                if before.channel is None and after.channel is not None:
                    user.start = get_current_time()
 #                   await channel.send("You entered the channel")
                else:
                    user.total_time += get_current_time() - user.start
                    await channel.send("current_time",user.total_time,"start time",user.start)
#                    await channel.send("You left the channel")
                    
    
    async def called_once_a_day(self):
        #print(self)
        #await self.wait_until_ready()
        #print("Inside called once a day")
        channel = self.get_channel(int(CHANNEL_ID))
        allowed_mentions = discord.AllowedMentions(everyone = True)
        await channel.send(content = "everyone", allowed_mentions = allowed_mentions)
        await channel.send("Past Midnight")
        for user in users:
            await channel.send("start {0} total {1}".format(user.start,user.total_time))
            user.total_time += 86400 - user.start
            await channel.send("{0}    {1:.2f} / 6시간".format(user.name,user.total_time/3600))
            user.reset()
    
    async def background_task(self):
        now = datetime.now(seoul_timezone).replace(tzinfo=None)
        if now.time() > MIDNIGHT.time():  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
            print("Inside if statement")
            print(now.time(),MIDNIGHT.time())
            tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
            seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
            await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
        while True:

            now = datetime.now(seoul_timezone).replace(tzinfo=None) # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
            target_time = datetime.combine(now.date(), MIDNIGHT.time())  # 6:00 PM today (In UTC)
            seconds_until_target = (target_time - now).total_seconds()
            print(seconds_until_target)
            await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
            await self.called_once_a_day()  # Call the helper function that sends the message
            tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
            seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
            await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration
        
        """for user in users:
            if name == user.name:
                channel = self.get_channel(1175368705715208255)
                await channel.send("{0}    {1} / 6시간".format(user.name,user.total_time/3600))
"""
# creating users
# phinguin
user1 = User(624839394117025793, "phinguin")
users.append(user1)
user2 = User(269673731721396225, "민댜")
users.append(user2)
user3 = User(352786596317233152, "Uniguri")
users.append(user3)
user4 = User(543004181842362379, "msh1307")
users.append(user4)
user5 = User(372665460032012288, "kio")
users.append(user5)



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = MyClient(intents=intents)
client.run(TOKEN)
