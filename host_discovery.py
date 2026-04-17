class HostDiscovery:
    def __init__(self):
        self.commands = {
            "-sL": "List Scan - simply list targets to scan",
            "-sn": "Ping Scan - disable port scan",
            "-Pn": "Treat all hosts as online -- skip host discovery",
            "-PS": "TCP SYN ping to specified ports",
            "-PA": "TCP ACK ping to specified ports", 
            "-PU": "UDP ping to specified ports",
            "-PY": "SCTP INIT ping",
            "-PO": "IP protocol ping",
            "--traceroute": "Trace hop path to each host",
            "--dns-server": "Use specified DNS server"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
