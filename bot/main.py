import datetime
from smite_html_parser import SmiteHTMLParser
from enum import Enum

import discord
import pyrez
import os

from smite_vgs import VGS


class MessageType(Enum):
    # Enum for determining message type
    NONE = 0,
    HELP = 1,
    LIST = 2,
    SMITE = 3,
    SAY_HI = 4,
    MOTD = 5


devId = os.getenv("SMITE_DEV_ID")
authKey = os.getenv("SMITE_AUTH_KEY")
vgs = VGS()


def validate_message(self, message: discord.Message):
    if message.author == self.user:
        return False
    if message.content[0] != "!":
        print(message.author.mention)
        print("Message {} does not start with '!'".format(message.content))
        return False
    return True


def determine_message_type(message: discord.Message):
    # When adding a new message type, add the content here
    message_command = message.content[1:]
    if message_command.lower() == "help":
        return MessageType.HELP
    if message_command.lower() == "list_commands":
        return MessageType.LIST
    if vgs.is_command(message_command):
        return MessageType.SMITE
    if message_command == "hi":
        return MessageType.SAY_HI
    if message_command == "motd":
        return MessageType.MOTD
    return MessageType.NONE


async def send_message(message_type, message: discord.Message):
    # When adding a new message type, add the content here too
    message_command = message.content[1:]
    if message_type == MessageType.SMITE:
        channel_message = "{} - {}".format(vgs.get_response(message_command), message.author.mention)
        channel = message.channel
        await channel.send(channel_message)
        await message.delete()
    if message_type == MessageType.HELP:
        await message.channel.send("Available commands: list_commands, hi")
    if message_type == MessageType.LIST:
        fin_string = "You can use the following smite keywords: "
        keys = ", ".join(vgs.keys())
        await message.channel.send(fin_string + keys)
    if message_type == MessageType.SAY_HI:
        await message.channel.send("Hello, {}".format(message.author.mention))
    if message_type == MessageType.MOTD:
        await message.channel.send(get_match_of_the_day())


class QuickChatClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: discord.Message):
        if not validate_message(self, message):
            return
        # Determine a message type to send
        message_type = determine_message_type(message)
        # Send corresponding message to channel
        await send_message(message_type, message)


def is_today(item):
    time_format = '%m/%d/%Y %I:%M:%S %p'
    today = datetime.datetime.now()
    start_date = datetime.datetime.strptime(item['startDateTime'], time_format)
    return today.date() == start_date.date()


def get_todays_motd(matches):
    return list(filter(is_today, matches))

def get_filtered_description(match):
    parser = SmiteHTMLParser()
    parser.feed(match.description)
    filtered = "*{}*\n\n**Map: {}**\n\n".format(parser.smite_object.description, parser.smite_object.map_data)
    for data in parser.smite_object.additional_data:
        filtered += "- {}\n".format(data)
    return filtered


client = QuickChatClient()
print("Created quick chat client")


def get_match_of_the_day():
    with pyrez.SmiteAPI(devId, authKey) as smite_api:
        motd = smite_api.getMotd()
        todays_motd = get_todays_motd(motd)
        if (len(todays_motd) > 1):
            print("[ERROR] Today should only contain 1 match of the day!")
        todays_motd = todays_motd[0]
        filtered_description = get_filtered_description(todays_motd)
        ret = "Today's Smite MOTD is **{}**.\n\n> {}".format(todays_motd.name, filtered_description)
        return ret


client.run(os.getenv('DISCORD_BOT_TOKEN'))
