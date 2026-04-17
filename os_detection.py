class OSDetection:
    def __init__(self):
        self.commands = {
            "-O": "Enable OS detection",
            "--osscan-limit": "Limit OS detection to promising targets",
            "--osscan-guess": "Guess OS more aggressively"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
