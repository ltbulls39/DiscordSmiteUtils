import discord
import os
from enum import Enum

class MessageType(Enum):
    NONE = 0,
    HELP = 1,
    LIST = 2,
    SMITE = 3,
    SAY_HI = 4

smite_commands = {
    "vvgt": "That's too bad!",
    "vvgw": "You're welcome!",
    "vvgr": "No Problem!",
    "vvgq": "Quiet!",
    "vvgl": "Good luck!",
    "vvgg": "Good game!",
    "vvgb": "Bye!",
    "vea": "Awesome!",
    "veg": "I'm the Greatest!",
    "ver": "You Rock!",
    "vva": "Ok!",
    "vvb": "Be right back!",
    "vvn": "No!",
    "vvp": "Please?",
    "vvs": "Sorry!",
    "vvt": "Thanks!",
    "vvx": "Cancel that!",
    "vvy": "Yes!"
}
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
    if message_command in smite_commands:
        return MessageType.SMITE
    if message_command == "hi":
        return MessageType.SAY_HI
    return MessageType.NONE

class QuickChatClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: discord.Message):
        if not validate_message(self, message):
            return
        message_command = message.content[1:]
        message_type = determine_message_type(message)
        if message_type == MessageType.SMITE:
            channel_message = "{} - {}".format(smite_commands[message_command], message.author.mention)
            channel = message.channel
            await channel.send(channel_message)
            await message.delete()
        if message_type == MessageType.HELP:
            await message.channel.send("Available commands: list_commands")
        if message_type == MessageType.LIST:
            fin_string = "You can use the following smite keywords: "
            keys = ", ".join(smite_commands.keys())
            await message.channel.send(fin_string + keys)
        if message_type == MessageType.SAY_HI:
            await message.channel.send("Hello, {}".format(message.author.mention))



client = QuickChatClient()
client.run(os.getenv('DISCORD_BOT_TOKEN'))