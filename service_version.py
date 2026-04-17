class ServiceVersion:
    def __init__(self):
        self.commands = {
            "-sV": "Probe open ports to determine service/version info",
            "--version-intensity": "Set version detection intensity (0-9)",
            "--version-all": "Try every single probe for version detection",
            "--version-trace": "Show detailed version scan events"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
