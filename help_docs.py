class HelpDocs:
    def __init__(self):
        self.docs = {
            "Host Discovery": {
                "-sL": "List Scan - simply list targets to scan without sending any packets",
                "-sn": "Ping Scan - disable port scan. Only performs host discovery",
                "-Pn": "Treat all hosts as online -- skip host discovery",
                "-PS": "TCP SYN ping to specified ports (default 80)",
                "-PA": "TCP ACK ping to specified ports (default 80)",
                "-PU": "UDP ping to specified ports (default 40125)",
                "-PY": "SCTP INIT ping to specified ports (default 80)",
                "-PO": "IP protocol ping - send IP packets with specified protocol number",
                "--traceroute": "Trace hop path to each host",
                "--dns-server": "Use specified DNS server for reverse lookups"
            },
            "Port Specification": {
                "-p": "Specify ports (single: 80, range: 1-65535, multiple: 22,80,443)",
                "-F": "Fast scan - only scan top 100 most common ports",
                "-r": "Scan ports consecutively - don't randomize port order",
                "--top-ports": "Scan the n most common ports (--top-ports 1000)"
            },
            "Scan Techniques": {
                "-sS": "TCP SYN scan - half-open scanning, fast and stealthy",
                "-sT": "TCP connect scan - full TCP connection, less stealthy",
                "-sU": "UDP scan - can be slow but finds UDP services",
                "-sA": "TCP ACK scan - used to map firewall rulesets",
                "-sW": "TCP Window scan - examines TCP window field",
                "-sM": "TCP Maimon scan - FIN/ACK probe",
                "-sN": "TCP Null scan - all flags off",
                "-sF": "FIN scan - only FIN flag set",
                "-sX": "Xmas scan - FIN, PSH, URG flags set"
            },
            "Service/Version Detection": {
                "-sV": "Version detection - determines service and version info",
                "--version-intensity": "Set intensity level 0-9 (higher = more probes)",
                "--version-all": "Use every probe for version detection (intensity 9)",
                "--version-trace": "Show detailed version scan events"
            },
            "OS Detection": {
                "-O": "Enable OS detection using TCP/IP fingerprinting",
                "--osscan-limit": "Only run OS detection on promising targets",
                "--osscan-guess": "Guess OS more aggressively when uncertain"
            },
            "Timing and Performance": {
                "-T0": "Paranoid - extremely slow, IDS evasion",
                "-T1": "Sneaky - quite slow, IDS evasion",
                "-T2": "Polite - slower to use less bandwidth",
                "-T3": "Normal - default timing template",
                "-T4": "Aggressive - fast, assumes good network",
                "-T5": "Insane - very fast, may miss ports",
                "--host-timeout": "Give up on slow hosts after time",
                "--max-retries": "Maximum port scan probe retransmissions",
                "--min-rate": "Minimum packet sending rate"
            },
            "Firewall/IDS Evasion": {
                "-f": "Fragment packets to avoid packet filters",
                "--mtu": "Set specific MTU for fragmentation",
                "-D": "Decoy scan - hide real IP among decoys",
                "-S": "Spoof source IP address",
                "-g": "Use given source port number",
                "--data-length": "Append random data to packets",
                "--ttl": "Set IP time-to-live field",
                "--spoof-mac": "Spoof MAC address",
                "--badsum": "Send packets with invalid checksum"
            },
            "Output Options": {
                "-oN": "Normal output to file",
                "-oX": "XML output for parsing",
                "-oG": "Grepable output for text processing",
                "-oA": "Output in all formats",
                "-v": "Increase verbosity level",
                "-d": "Increase debugging level",
                "--reason": "Show reason each port is in state",
                "--open": "Only show open ports",
                "--packet-trace": "Show all packets sent and received"
            }
        }
        
    def get_all_docs(self):
        doc_text = "=== NMAP TOOL HELP DOCUMENTATION ===\n\n"
        for category, commands in self.docs.items():
            doc_text += f"\n{category}:\n"
            doc_text += "-" * 50 + "\n"
            for cmd, desc in commands.items():
                doc_text += f"{cmd:<15} - {desc}\n"
        return doc_text
        
    def get_command_doc(self, command):
        for category, commands in self.docs.items():
            if command in commands:
                return commands[command]
        return "No documentation available for this command"
