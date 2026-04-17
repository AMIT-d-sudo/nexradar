class PortSpecification:
    def __init__(self):
        self.commands = {
            "-p": "Specify ports (single: 80, range: 1-65535, multiple: 22,80,443)",
            "-F": "Fast scan - only top 100 ports",
            "-r": "Scan ports consecutively - don't randomize",
            "--top-ports": "Scan most common ports"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
