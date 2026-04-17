class TargetSpecification:
    def __init__(self):
        self.commands = {
            "--exclude": "Exclude specified hosts (comma-separated list or file path)",
            "--excludefile": "Exclude hosts from file (one host per line)",
            "-iL": "Input from list of hosts file (one host per line)"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        help_texts = {
            "--exclude": "Exclude specific hosts from scan. Example: --exclude 192.168.1.1,192.168.1.2 or --exclude /path/to/exclude.txt",
            "--excludefile": "Read exclusion list from file. Each host/IP on new line. Example: --excludefile exclude.txt",
            "-iL": "Read target list from file. Each target on new line. Example: -iL targets.txt"
        }
        return help_texts.get(command, self.commands.get(command, "No help available"))
