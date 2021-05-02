import discord
import os
from smite_vgs import VGS
from enum import Enum


class MessageType(Enum):
    NONE = 0,
    HELP = 1,
    LIST = 2,
    SMITE = 3,
    SAY_HI = 4


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
    message_command = message.content[1:]
    if message_command.lower() == "help":
        return MessageType.HELP
    if message_command.lower() == "list_commands":
        return MessageType.LIST
    if vgs.is_command(message_command):
        return MessageType.SMITE
    if message_command == "hi":
        return MessageType.SAY_HI
    return MessageType.NONE


async def send_message(message_type, message: discord.Message):
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


class QuickChatClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: discord.Message):
        if not validate_message(self, message):
            return
        # Determine a message type to send
        message_type = determine_message_type(message)
        # Send corresponding message to channel
        send_message(message_type, message)


client = QuickChatClient()
client.run(os.getenv('DISCORD_BOT_TOKEN'))
