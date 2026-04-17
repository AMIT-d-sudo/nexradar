class TimingPerformance:
    def __init__(self):
        self.commands = {
            "-T0": "Paranoid (0) idle scan",
            "-T1": "Sneaky (1) slow scan",
            "-T2": "Polite (2) slower scan",
            "-T3": "Normal (3) default speed",
            "-T4": "Aggressive (4) fast scan",
            "-T5": "Insane (5) very fast scan",
            "--min-hostgroup": "Parallel host scan group sizes",
            "--max-hostgroup": "Parallel host scan group sizes",
            "--min-parallelism": "Number of probes outstanding",
            "--max-parallelism": "Number of probes outstanding",
            "--max-retries": "Number of retransmissions",
            "--host-timeout": "Time to wait for a host",
            "--max-scan-delay": "Maximum delay between probes",
            "--min-rate": "Minimum packet sending rate"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
