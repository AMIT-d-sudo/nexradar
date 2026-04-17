class ScanTechniques:
    def __init__(self):
        self.commands = {
            "-sS": "TCP SYN scan",
            "-sT": "TCP connect scan",
            "-sA": "TCP ACK scan",
            "-sW": "TCP Window scan",
            "-sM": "TCP Maimon scan",
            "-sU": "UDP scan",
            "-sN": "TCP Null scan",
            "-sF": "FIN scan",
            "-sX": "Xmas scan",
            "--scanflags": "Custom TCP scan flags",
            "-sZ": "SCTP COOKIE ECHO scan",
            "-sI": "Idle scan with zombie host",
            "-sO": "IP protocol scan",
            "-b": "FTP bounce scan"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
