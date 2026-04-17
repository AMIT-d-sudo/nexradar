class FirewallEvasion:
    def __init__(self):
        self.commands = {
            "-f": "Fragment packets",
            "--mtu": "Set MTU value",
            "-D": "IP decoy scan",
            "-S": "Spoof source IP address",
            "-e": "Use specified interface",
            "-g": "Use given source port number",
            "--source-port": "Set source port",
            "--data-string": "Append custom string to sent packets",
            "--data-length": "Append random data to sent packets",
            "--ip-options": "Send packets with specified ip options",
            "--ttl": "Set IP time-to-live field",
            "--spoof-mac": "Spoof MAC address",
            "--badsum": "Send packets with bad checksum"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
