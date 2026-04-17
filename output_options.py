import tkinter as tk
from tkinter import filedialog

class OutputOptions:
    def __init__(self, parent=None):
        self.parent = parent
        self.commands = {
            "-oN": "Normal output to file",
            "-oX": "XML output to file", 
            "-oS": "Script kiddie output",
            "-oG": "Grepable output",
            "-oA": "Output in all major formats (Normal, XML, Grepable)",
            "-v": "Increase verbosity level 1 (more detailed output)",
            "-vv": "Increase verbosity level 2",
            "-vvv": "Increase verbosity level 3 (maximum verbosity)",
            "-d": "Debugging level 1 (show debug information)",
            "-d1": "Debugging level 1",
            "-d2": "Debugging level 2", 
            "-d3": "Debugging level 3",
            "-d4": "Debugging level 4",
            "-d5": "Debugging level 5",
            "-d6": "Debugging level 6",
            "-d7": "Debugging level 7",
            "-d8": "Debugging level 8",
            "-d9": "Debugging level 9 (maximum debugging)",
            "--reason": "Display reason for each port state (open/closed/filtered)",
            "--open": "Only show open ports in output",
            "--packet-trace": "Show all packets sent and received (detailed trace)",
            "--iflist": "List host network interfaces and routes",
            "--append-output": "Append to output file instead of overwriting",
            "--stylesheet": "Set XSL stylesheet for XML output"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        return self.commands.get(command, "No help available")
        
    def browse_output_file(self, cmd):
        """Browse for output file location"""
        if self.parent:
            filename = filedialog.asksaveasfilename(title=f"Save {cmd} output file",
                                                    defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt"), 
                                                              ("XML files", "*.xml"),
                                                              ("All files", "*.*")])
            if filename:
                return filename
        return None
