class VGS:
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

    def get_response(self, message):
        if message not in self.smite_commands:
            return None
        return self.smite_commands[message]

    def is_command(self, message):
        return True if message in self.smite_commands else False

    def keys(self):
        return self.smite_commands.keys()