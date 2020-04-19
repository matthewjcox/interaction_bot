#source for most of this: https://realpython.com/how-to-make-a-discord-bot-python/

import discord
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

interaction_role= 'wants-random-interaction'

client = discord.Client()

def get_name(member):
    if member.nick is not None:
        return member.nick
    return member.name

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

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

    #Message each person about who else they bumped into:
    for group in groups_who_bumped_into_eachother:
        for member in group:
            group_minus_member=[get_name(i) for i in group if i != member]
            try:
                await member.create_dm()
                if (len(group) == 2):
                    people_bumped_into=group_minus_member[0]
                elif (len(group) == 3):
                    people_bumped_into=f"{group_minus_member[0]} and {group_minus_member[1]}"
                else:
                    raise ValueError

                message = f'Hi {get_name(member)}! You just bumped into {people_bumped_into} - say hi to them! (They also got a message that they bumped into you.)'
                await member.dm_channel.send(message)
            except:
                pass


client.run(TOKEN)