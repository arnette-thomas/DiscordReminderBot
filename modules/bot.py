from modules.record import Record

import os
import discord
from discord.ext.tasks import loop
from dotenv import load_dotenv
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

        # Triggered when bot ready
        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            self._bg_check_reminders.start()

        # Triggered when a new message is received
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('$rm'):
                print('Message received')

                # Get args
                args = message.content.strip().split(' ', 2)

                if len(args) < 2:
                    await self._send_help(message)
                    return
                
                try:

                    rec = Record(message.author, args[1], message.channel)
                    if len(args) >= 3:
                        rec.set_description(args[2])
                
                    self.reminders.append(rec)
                    self.reminders.sort(key=lambda r : r.datetime)

                    await message.channel.send('{0.mention} - Reminder set to {1} !'.format(rec.user, rec.get_datetime_as_str()))

                except Exception as ex:
                    await message.channel.send('***Error : {}***'.format(ex))

    async def _send_help(self, msg):
        channel = msg.channel
        help_str = """
** Reminder Bot **

*Syntax : * `$rm [date] [time] [description]

*Parameters : *
__date and time__ --- Mandatory --- Indicates the datetime for the reminder. Format : dd/mm/yyyy-HH:MM:SS
                                    If date is empty, current day will be considered.
                                    If time is empty, current time will be considered.
                                    Minutes and seconds can be ommitted
                                    examples : 18/01/2021-10:34:45 | 18/01/2021 | 10:34 

__description__   --- Optional  --- Inidcates the text to display when reminder is triggered
        """

        await channel.send(help_str)
    
    @loop(seconds=5)
    async def _bg_check_reminders(self):
        now = datetime.now()

        while len(self.reminders) > 0:
            reminder = self.reminders[0]

            if reminder.datetime > now:
                break

            to_send = '{0.mention} - You have a reminder ! '.format(reminder.user)
            if reminder.description != '':
                to_send += "\n \n {}".format(reminder.description)

            await reminder.channel.send(to_send)

            self.reminders.remove(reminder)

    @_bg_check_reminders.before_loop
    async def _bg_before_check_reminders(self):
        await self.client.wait_until_ready()

    
    # Called to run server
    def run(self):
        self.client.run(self.token)
    