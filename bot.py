#source for most of this: https://realpython.com/how-to-make-a-discord-bot-python/
import asyncio

import discord
import random
import os
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

def get_name(member):
    if member.nick is not None:
        return member.nick
    return member.name

interaction_role= 'wants-random-interaction'

class InteractionBot(discord.Client):
    def __init__(self, intents, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.background_task = self.loop.create_task(self.match_loop())

    async def match_loop(self):
        await self.wait_until_ready()

        #Chooses a time from 19:00 to 23:59 EDT to match people up
        next_match_hour=random.randint(19,23)
        next_match_minute=random.randint(0,59)

        # Use for debugging to force a match at a time very soon
        # next_match_hour=21
        # next_match_minute=20

        while not self.is_closed():
            now = time.localtime()
            if next_match_hour==now.tm_hour and next_match_minute==now.tm_min:
                print(f"it is now {now.tm_hour:02d}:{now.tm_min:02d}; sending matches!")
                await self.match_people()
                next_match_hour = random.randint(19, 23)
                next_match_minute = random.randint(0, 59)
                print(f'Will send next matches tomorrow at {next_match_hour:02d}:{next_match_minute:02d}')
                await asyncio.sleep(12*60*60) # Wait 12 hours

                # Note that new matches will be sent at the first instance of the next match time.
                # e.g. if the new notification time is later than the current time, the new matches
                # will be sent on the same day; if the new time is before the current time, the new
                # matches will be sent on the next day.
            else:
                print(f"it is now {now.tm_hour:02d}:{now.tm_min:02d}; waiting until {next_match_hour:02d}:{next_match_minute:02d}")

            await asyncio.sleep(30) # check every 30 seconds


    async def match_people(self):
        # print('Matching!')
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        else:
            return

        members_to_contact=[member for member in guild.members if interaction_role in [i.name for i in member.roles]]
        random.shuffle(members_to_contact)
        groups_who_bumped_into_eachother=[]


        #Figure out the groups who bumped into each other:
        while members_to_contact:
            if len(members_to_contact)<=1:
                break
            if len(members_to_contact)==3:
                groups_who_bumped_into_eachother.append((members_to_contact[0],members_to_contact[1],members_to_contact[2]))
                break
            groups_who_bumped_into_eachother.append((members_to_contact[0],members_to_contact[1]))
            members_to_contact=members_to_contact[2:]
        # print('Matches made!')

        #Message each person about who else they bumped into:
        for group in groups_who_bumped_into_eachother:
            for member in group:
                group_minus_member=[get_name(i) for i in group if i != member]
                try:
                    await member.create_dm()
                    if (len(group) == 2):
                        people_bumped_into=str(group_minus_member[0])
                    elif (len(group) == 3):
                        people_bumped_into=f"{group_minus_member[0]} and {group_minus_member[1]}"
                    else:
                        raise ValueError

                    message = f'Hi {get_name(member)}! You just bumped into {people_bumped_into} - say hi to them! (They also got a message that they bumped into you.)'
                    await member.dm_channel.send(message)
                except:
                    pass
        # print('Match messages sent!')


intents = discord.Intents.default()
intents.members = True
client = InteractionBot(intents)
client.run(TOKEN)