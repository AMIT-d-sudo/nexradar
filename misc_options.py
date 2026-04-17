class MiscOptions:
    def __init__(self):
        self.commands = {
            "-6": "Enable IPv6 scanning (scan IPv6 addresses)",
            "-A": "Enable aggressive scanning: OS detection, version detection, script scanning, and traceroute"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        help_texts = {
            "-6": "Enable IPv6 scanning. Use with IPv6 addresses like: nmap -6 2001:db8::1",
            "-A": "Enable aggressive scan - combines -O, -sC, -sV, and --traceroute"
        }
        return help_texts.get(command, self.commands.get(command, "No help available"))
