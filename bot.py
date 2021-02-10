import os
import discord
from discord.ext.tasks import loop
from dotenv import load_dotenv
from record import Record
from datetime import datetime

class Bot:

    # Constructor
    def __init__(self):
        load_dotenv()
        token = os.getenv("BOT_TOKEN")

        if not token:
            raise Exception("ERROR : no token found in .env file. Create a .env file with BOT_TOKEN variable")

        self.token = token

        self.client = discord.Client()

        self._setup_events()

        self.reminders = []

        # self.client.bg_task = self.client.loop.create_task(self._bg_check_reminders())

    # Called once in constructor. Here are Discord events
    def _setup_events(self):

        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            self._bg_check_reminders.start()

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('$rm'):
                arg = message.content[3:]
                print('message received')
                try:
                    rec = Record(message.author, arg, message.channel)
                
                    self.reminders.append(rec)
                    self.reminders.sort(key=lambda r : r.datetime)

                    await message.channel.send('{0.mention} - Reminder set to {1} !'.format(rec.user, rec.get_datetime_as_str()))

                except Exception as ex:
                    await message.channel.send('***Error : {}***'.format(ex))
    
    @loop(seconds=5)
    async def _bg_check_reminders(self):
        now = datetime.now()
        while len(self.reminders) > 0:
            reminder = self.reminders[0]
            if reminder.datetime > now:
                break
            await reminder.channel.send('{0.mention} - You have a reminder ! '.format(reminder.user))
            self.reminders.remove(reminder)

    @_bg_check_reminders.before_loop
    async def _bg_before_check_reminders(self):
        await self.client.wait_until_ready()

    
    # Called to run server
    def run(self):
        self.client.run(self.token)
    