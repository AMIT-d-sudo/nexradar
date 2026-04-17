#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
from datetime import datetime
import queue
import re
import os

# Import AI Dashboard
from ai_dashboard import AIDashboard

class NmapGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ NEXRADAR v2.0 - Ultimate Network Scanner ⚡")
        self.root.geometry("1600x950")
        self.root.configure(bg='#0a0a0a')
        
        # Colors
        self.bg_dark = '#0a0a0a'
        self.bg_medium = '#0d0d0d'
        self.bg_light = '#1a1a1a'
        self.green = '#00ff41'
        self.red = '#ff3333'
        self.yellow = '#ffcc00'
        self.blue = '#3399ff'
        self.cyan = '#00ccff'
        self.purple = '#9b00ff'
        self.orange = '#ff6600'
        self.white = '#ffffff'
        
        self.current_process = None
        self.is_scanning = False
        self.output_queue = queue.Queue()
        self.last_scan_output = ""
        self.scan_history = []
        
        # Command variables
        self.cmd_vars = {}
        self.cmd_entries = {}
        
        # Import modules
        from target_spec import TargetSpecification
        from host_discovery import HostDiscovery
        from scan_techniques import ScanTechniques
        from port_spec import PortSpecification
        from service_version import ServiceVersion
        from os_detection import OSDetection
        from timing_performance import TimingPerformance
        from firewall_evasion import FirewallEvasion
        from output_options import OutputOptions
        from misc_options import MiscOptions
        from script_scan import ScriptScan
        from help_docs import HelpDocs
        from ai_integration import AIIntegration
        from advanced_reporting import AdvancedReporting
        from network_mapping import NetworkMapper
        from advanced_discovery import AdvancedDiscovery
        
        self.target_spec = TargetSpecification()
        self.host_discovery = HostDiscovery()
        self.scan_techniques = ScanTechniques()
        self.port_spec = PortSpecification()
        self.service_version = ServiceVersion()
        self.os_detection = OSDetection()
        self.timing_perf = TimingPerformance()
        self.firewall = FirewallEvasion()
        self.output = OutputOptions()
        self.misc = MiscOptions()
        self.script_scan = ScriptScan()
        self.help_docs = HelpDocs()
        self.ai = AIIntegration()
        self.reporting = AdvancedReporting()
        self.network_mapper = NetworkMapper()
        self.advanced_discovery = AdvancedDiscovery()
        
        self.setup_ui()
        self.update_output_queue()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== TOP BANNER ==========
        banner_frame = tk.Frame(main_frame, bg=self.bg_medium, height=80, relief=tk.RIDGE, bd=2)
        banner_frame.pack(fill=tk.X, padx=5, pady=5)
        banner_frame.pack_propagate(False)
        
        banner_text = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         NEXRADAR v2.0 - ULTIMATE NETWORK SCANNER                                     ║
║                                   [ FAST | STEALTH | PROFESSIONAL | AI-POWERED ]                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """
        tk.Label(banner_frame, text=banner_text, bg=self.bg_medium, 
                fg=self.green, font=('Courier', 9, 'bold')).pack()
        
        # ========== FAST SCAN BUTTONS ==========
        fast_frame = tk.Frame(main_frame, bg=self.bg_light, relief=tk.RIDGE, bd=2)
        fast_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(fast_frame, text="⚡ QUICK ACTIONS:", bg=self.bg_light, 
                fg=self.yellow, font=('Courier', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.ultra_btn = tk.Button(fast_frame, text="🚀 ULTRA FAST SCAN", command=self.ultra_fast_scan,
                                   bg='#ff6600', fg='white', font=('Courier', 9, 'bold'),
                                   padx=15, pady=3, cursor='hand2')
        self.ultra_btn.pack(side=tk.LEFT, padx=5)
        
        self.fast_btn = tk.Button(fast_frame, text="⚡ FAST PORT SCAN", command=self.fast_scan,
                                  bg='#006600', fg='white', font=('Courier', 9, 'bold'),
                                  padx=15, pady=3, cursor='hand2')
        self.fast_btn.pack(side=tk.LEFT, padx=5)
        
        self.list_btn = tk.Button(fast_frame, text="📋 LIST SCAN (no ports)", command=self.list_scan,
                                  bg='#004466', fg='white', font=('Courier', 9, 'bold'),
                                  padx=15, pady=3, cursor='hand2')
        self.list_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(fast_frame, text="⚡ ULTRA FAST: 1 sec | FAST: 2-3 sec | LIST: <1 sec", 
                bg=self.bg_light, fg=self.cyan, font=('Courier', 8)).pack(side=tk.RIGHT, padx=10)
        
        # ========== TARGET SECTION ==========
        control_frame = tk.Frame(main_frame, bg=self.bg_light, relief=tk.RIDGE, bd=2)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        target_frame = tk.Frame(control_frame, bg=self.bg_light)
        target_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(target_frame, text="🎯 TARGET:", bg=self.bg_light, 
                fg=self.cyan, font=('Courier', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.target_entry = tk.Entry(target_frame, width=50, bg=self.bg_dark, 
                                      fg=self.green, font=('Courier', 11), 
                                      insertbackground=self.green, relief=tk.SUNKEN, bd=3)
        self.target_entry.pack(side=tk.LEFT, padx=10)
        self.target_entry.insert(0, "192.168.79.129")
        
        tk.Button(target_frame, text="📂 LOAD FILE", command=self.load_targets_from_file,
                 bg=self.bg_dark, fg=self.yellow, font=('Courier', 9, 'bold'),
                 cursor='hand2', relief=tk.RAISED, bd=2, padx=10).pack(side=tk.LEFT, padx=5)
        
        # ========== BUTTONS ROW ==========
        button_frame = tk.Frame(control_frame, bg=self.bg_light)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("▶ RUN", self.run_scan, self.green),
            ("⏹ STOP", self.stop_scan, self.red),
            ("🗑 CLEAR", self.clear_output, self.yellow),
            ("🔨 BUILD", self.build_command, self.blue),
            ("💾 SAVE", self.save_output, self.purple),
            ("🤖 AI ANALYZE", self.ai_analyze, self.cyan),
            ("🎮 AI DASHBOARD", self.open_ai_dashboard, self.orange),
            ("❓ HELP", self.show_help, self.white)
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(button_frame, text=text, command=cmd,
                           bg=self.bg_dark, fg=color, font=('Courier', 9, 'bold'),
                           padx=10, pady=5, cursor='hand2', relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
            if text == "⏹ STOP":
                self.stop_btn = btn
                btn.config(state=tk.DISABLED)
            elif text == "▶ RUN":
                self.run_btn = btn
        
        # Status Bar
        status_frame = tk.Frame(main_frame, bg=self.bg_dark)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_indicator = tk.Label(status_frame, text="●", bg=self.bg_dark, 
                                          fg=self.green, font=('Courier', 12))
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_bar = tk.Label(status_frame, 
                                   text="NEXRADAR v2.0 READY | 60+ FEATURES | AI ASSISTANT ONLINE", 
                                   bg=self.bg_dark, fg=self.green,
                                   font=('Courier', 9, 'bold'))
        self.status_bar.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress_frame = tk.Frame(main_frame, bg=self.bg_dark)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = tk.Label(self.progress_frame, text="", bg=self.bg_dark, 
                                        fg=self.cyan, font=('Courier', 8))
        self.progress_label.pack()
        
        self.progress = ttk.Progressbar(self.progress_frame, mode='indeterminate', length=500)
        self.progress.pack(pady=5)
        
        # ========== MAIN CONTENT ==========
        content_frame = tk.Frame(main_frame, bg=self.bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ========== LEFT PANEL ==========
        left_panel = tk.Frame(content_frame, bg=self.bg_medium, relief=tk.RIDGE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_panel, text="⚡ SCAN OPTIONS (11 TABS)", bg=self.bg_medium, 
                fg=self.yellow, font=('Courier', 10, 'bold')).pack(pady=5)
        
        self.notebook = ttk.Notebook(left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create all command tabs
        self.create_command_tab("🎯 TARGET", self.target_spec.get_commands(), 'target')
        self.create_command_tab("🔍 HOST", self.host_discovery.get_commands(), 'host')
        self.create_command_tab("⚡ SCAN", self.scan_techniques.get_commands(), 'scan')
        self.create_command_tab("🔌 PORT", self.port_spec.get_commands(), 'port')
        self.create_command_tab("🛠 SERVICE", self.service_version.get_commands(), 'service')
        self.create_command_tab("💻 OS", self.os_detection.get_commands(), 'os')
        self.create_command_tab("📜 SCRIPT", self.script_scan.get_commands(), 'script')
        self.create_command_tab("⏱ TIMING", self.timing_perf.get_commands(), 'timing')
        self.create_command_tab("🛡 FIREWALL", self.firewall.get_commands(), 'firewall')
        self.create_command_tab("📄 OUTPUT", self.output.get_commands(), 'output')
        self.create_command_tab("🔧 MISC", self.misc.get_commands(), 'misc')
        
        # ========== RIGHT PANEL ==========
        right_panel = tk.Frame(content_frame, bg=self.bg_medium, relief=tk.RIDGE, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Command Display
        cmd_frame = tk.LabelFrame(right_panel, text="📝 GENERATED COMMAND", 
                                   bg=self.bg_light, fg=self.yellow,
                                   font=('Courier', 10, 'bold'), relief=tk.RIDGE, bd=2)
        cmd_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.command_text = scrolledtext.ScrolledText(cmd_frame, height=4,
                                                       bg=self.bg_dark, fg=self.yellow,
                                                       font=('Courier', 10), relief=tk.SUNKEN)
        self.command_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Output Display
        output_frame = tk.LabelFrame(right_panel, text="📊 SCAN OUTPUT", 
                                      bg=self.bg_light, fg=self.green,
                                      font=('Courier', 11, 'bold'), relief=tk.RIDGE, bd=2)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=35,
                                                      bg=self.bg_dark, fg=self.green,
                                                      font=('Courier', 10), relief=tk.SUNKEN,
                                                      wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure text tags
        self.output_text.tag_config('info', foreground=self.cyan)
        self.output_text.tag_config('output', foreground=self.green)
        self.output_text.tag_config('error', foreground=self.red)
        self.output_text.tag_config('warning', foreground=self.yellow)
        self.output_text.tag_config('success', foreground=self.green)
        self.output_text.tag_config('ai', foreground=self.purple)
        
        self.blink_status()
        self.print_welcome()
    
    def print_welcome(self):
        welcome = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                      ║
║  🚀 NEXRADAR v2.0 READY                                                                                             ║
║                                                                                                                      ║
║  ✅ QUICK ACTIONS: ULTRA FAST SCAN | FAST PORT SCAN | LIST SCAN (no ports)                                          ║
║  ✅ AI ASSISTANT ONLINE                                                                                             ║
║  ✅ 60+ FEATURES LOADED                                                                                             ║
║                                                                                                                      ║
║  📌 QUICK START:                                                                                                    ║
║     1. Enter target IP or domain                                                                                    ║
║     2. Use QUICK ACTION buttons or select options from LEFT PANEL                                                   ║
║     3. Click RUN to start scanning                                                                                  ║
║     4. Click AI ANALYZE for vulnerability report                                                                    ║
║     5. Click AI DASHBOARD for advanced features                                                                     ║
║                                                                                                                      ║
║  ⚡ QUICK ACTION BUTTONS:                                                                                           ║
║     • ULTRA FAST SCAN - -T5 -F --min-rate 10000 -n (1 second)                                                       ║
║     • FAST PORT SCAN - -T4 -F --min-rate 5000 -n (2-3 seconds)                                                      ║
║     • LIST SCAN - -sL -n (No ports, just IP list, <1 second)                                                        ║
║                                                                                                                      ║
║  ⚠️  USE RESPONSIBLY - ONLY ON AUTHORIZED SYSTEMS                                                                  ║
║                                                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

"""
        self.output_text.insert(tk.END, welcome, 'info')
    
    def create_command_tab(self, title, commands, tab_name):
        """Create a scrollable tab with all commands and entry boxes"""
        tab_frame = tk.Frame(self.notebook, bg=self.bg_medium)
        self.notebook.add(tab_frame, text=title)
        
        canvas = tk.Canvas(tab_frame, bg=self.bg_medium, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_medium)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        if tab_name not in self.cmd_vars:
            self.cmd_vars[tab_name] = {}
        if tab_name not in self.cmd_entries:
            self.cmd_entries[tab_name] = {}
        
        row = 0
        for cmd, desc in commands.items():
            frame = tk.Frame(scrollable_frame, bg=self.bg_medium)
            frame.grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=cmd, variable=var,
                                 bg=self.bg_medium, fg=self.green,
                                 selectcolor=self.bg_medium, font=('Courier', 8))
            chk.pack(side=tk.LEFT)
            
            short_desc = desc[:50] + "..." if len(desc) > 50 else desc
            tk.Label(frame, text=f"- {short_desc}", bg=self.bg_medium, 
                    fg=self.cyan, font=('Courier', 7)).pack(side=tk.LEFT, padx=5)
            
            entry_widget = None
            
            # Port specification
            if cmd == '-p':
                entry_frame = tk.Frame(frame, bg=self.bg_medium)
                entry_frame.pack(side=tk.LEFT, padx=5)
                entry = tk.Entry(entry_frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT)
                entry.insert(0, "1-1000")
                tk.Label(entry_frame, text="(e.g., 80, 1-1000, 22,80,443)", 
                        bg=self.bg_medium, fg=self.cyan, font=('Courier', 7)).pack(side=tk.LEFT, padx=5)
                entry_widget = entry
            
            # Script options
            elif cmd == '--script':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "default,vuln")
                entry_widget = entry
            
            elif cmd == '--script-args':
                entry = tk.Entry(frame, width=25, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "userdb=users.txt,passdb=pass.txt")
                entry_widget = entry
            
            elif cmd == '--script-args-file':
                entry_frame = tk.Frame(frame, bg=self.bg_medium)
                entry_frame.pack(side=tk.LEFT, padx=5)
                entry = tk.Entry(entry_frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT)
                tk.Button(entry_frame, text="📂", command=lambda e=entry: self.browse_file(e),
                         bg=self.bg_dark, fg=self.cyan, font=('Courier', 7), width=2).pack(side=tk.LEFT, padx=2)
                entry_widget = entry
            
            # DNS options
            elif cmd == '--dns-servers':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "8.8.8.8,1.1.1.1")
                entry_widget = entry
            
            elif cmd == '--dns-server':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "8.8.8.8")
                entry_widget = entry
            
            # Scan flags
            elif cmd == '--scanflags':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "SYN,ACK,FIN")
                entry_widget = entry
            
            # Zombie host
            elif cmd == '-sI':
                entry = tk.Entry(frame, width=25, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "192.168.79.1:80")
                entry_widget = entry
            
            # FTP relay
            elif cmd == '-b':
                entry = tk.Entry(frame, width=25, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "192.168.79.1:21")
                entry_widget = entry
            
            # Exclude ports
            elif cmd == '--exclude-ports':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "139,445,3389")
                entry_widget = entry
            
            # Version intensity
            elif cmd == '--version-intensity':
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "7")
                entry_widget = entry
            
            # Exclude hosts
            elif cmd == '--exclude':
                entry = tk.Entry(frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "192.168.79.1,192.168.79.2")
                entry_widget = entry
            
            # File options
            elif cmd in ['--excludefile', '-iL']:
                entry_frame = tk.Frame(frame, bg=self.bg_medium)
                entry_frame.pack(side=tk.LEFT, padx=5)
                entry = tk.Entry(entry_frame, width=20, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT)
                tk.Button(entry_frame, text="📂", command=lambda e=entry: self.browse_file(e),
                         bg=self.bg_dark, fg=self.cyan, font=('Courier', 7), width=2).pack(side=tk.LEFT, padx=2)
                entry_widget = entry
            
            # Timing options
            elif cmd == '--min-rate':
                entry = tk.Entry(frame, width=10, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "5000")
                entry_widget = entry
            
            elif cmd == '--max-retries':
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "1")
                entry_widget = entry
            
            elif cmd == '--host-timeout':
                entry = tk.Entry(frame, width=10, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "30s")
                entry_widget = entry
            
            elif cmd == '--max-scan-delay':
                entry = tk.Entry(frame, width=10, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "10ms")
                entry_widget = entry
            
            # Top ports
            elif cmd == '--top-ports':
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "1000")
                entry_widget = entry
            
            # MTU
            elif cmd == '--mtu':
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "8")
                entry_widget = entry
            
            # Decoy
            elif cmd == '-D':
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "RND:10")
                entry_widget = entry
            
            # Spoof IP
            elif cmd == '-S':
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "192.168.79.100")
                entry_widget = entry
            
            # Interface
            elif cmd == '-e':
                entry = tk.Entry(frame, width=10, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "eth0")
                entry_widget = entry
            
            # Source port
            elif cmd in ['-g', '--source-port']:
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "53")
                entry_widget = entry
            
            # Data options
            elif cmd in ['--data-string', '--data-length']:
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                if cmd == '--data-string':
                    entry.insert(0, "GET / HTTP/1.0")
                else:
                    entry.insert(0, "200")
                entry_widget = entry
            
            # IP options
            elif cmd == '--ip-options':
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "LSRR")
                entry_widget = entry
            
            # TTL
            elif cmd == '--ttl':
                entry = tk.Entry(frame, width=8, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "128")
                entry_widget = entry
            
            # Spoof MAC
            elif cmd == '--spoof-mac':
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "0")
                entry_widget = entry
            
            # Output options
            elif cmd in ['-oN', '-oX', '-oS', '-oG', '-oA']:
                entry = tk.Entry(frame, width=15, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "scan_report")
                entry_widget = entry
            
            # Stylesheet
            elif cmd == '--stylesheet':
                entry = tk.Entry(frame, width=25, bg=self.bg_dark, fg=self.yellow, font=('Courier', 7))
                entry.pack(side=tk.LEFT, padx=5)
                entry.insert(0, "https://nmap.org/data/nmap.xsl")
                entry_widget = entry
                    
            self.cmd_vars[tab_name][cmd] = var
            self.cmd_entries[tab_name][cmd] = entry_widget
            row += 1
    
    # ========== QUICK ACTION FUNCTIONS ==========
    
    def ultra_fast_scan(self):
        """Ultra fast scan - <1 second - clears all previous selections"""
        target = self.target_entry.get().strip()
        if not target:
            self.output_text.insert(tk.END, "\n[!] Enter target first\n", 'warning')
            return
        
        # Clear ALL previous selections
        for tab in self.cmd_vars:
            for cmd in self.cmd_vars[tab]:
                self.cmd_vars[tab][cmd].set(False)
        
        # Set ultra fast options
        if 'timing' in self.cmd_vars:
            if '-T5' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['-T5'].set(True)
            if '--min-rate' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['--min-rate'].set(True)
                entry = self.cmd_entries['timing'].get('--min-rate')
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, "10000")
            if '--max-retries' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['--max-retries'].set(True)
                entry = self.cmd_entries['timing'].get('--max-retries')
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, "0")
        
        if 'port' in self.cmd_vars and '-F' in self.cmd_vars['port']:
            self.cmd_vars['port']['-F'].set(True)
        
        if 'misc' in self.cmd_vars and '-n' in self.cmd_vars['misc']:
            self.cmd_vars['misc']['-n'].set(True)
        
        self.output_text.insert(tk.END, "\n⚡ ULTRA FAST SCAN STARTED (<1 sec expected)\n", 'info')
        self.run_scan()
    
    def fast_scan(self):
        """Fast scan - 2-3 seconds - clears all previous selections"""
        target = self.target_entry.get().strip()
        if not target:
            self.output_text.insert(tk.END, "\n[!] Enter target first\n", 'warning')
            return
        
        # Clear ALL previous selections
        for tab in self.cmd_vars:
            for cmd in self.cmd_vars[tab]:
                self.cmd_vars[tab][cmd].set(False)
        
        # Set fast options
        if 'timing' in self.cmd_vars:
            if '-T4' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['-T4'].set(True)
            if '--min-rate' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['--min-rate'].set(True)
                entry = self.cmd_entries['timing'].get('--min-rate')
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, "5000")
            if '--max-retries' in self.cmd_vars['timing']:
                self.cmd_vars['timing']['--max-retries'].set(True)
                entry = self.cmd_entries['timing'].get('--max-retries')
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, "1")
        
        if 'port' in self.cmd_vars and '-F' in self.cmd_vars['port']:
            self.cmd_vars['port']['-F'].set(True)
        
        if 'misc' in self.cmd_vars and '-n' in self.cmd_vars['misc']:
            self.cmd_vars['misc']['-n'].set(True)
        
        self.output_text.insert(tk.END, "\n⚡ FAST PORT SCAN STARTED (2-3 sec expected)\n", 'info')
        self.run_scan()
    
    def list_scan(self):
        """List scan - no ports, just IP list - <1 second"""
        target = self.target_entry.get().strip()
        if not target:
            self.output_text.insert(tk.END, "\n[!] Enter target first\n", 'warning')
            return
        
        # Clear ALL previous selections
        for tab in self.cmd_vars:
            for cmd in self.cmd_vars[tab]:
                self.cmd_vars[tab][cmd].set(False)
        
        # Set list scan options (NO port scan parameters!)
        if 'host' in self.cmd_vars and '-sL' in self.cmd_vars['host']:
            self.cmd_vars['host']['-sL'].set(True)
        
        if 'misc' in self.cmd_vars and '-n' in self.cmd_vars['misc']:
            self.cmd_vars['misc']['-n'].set(True)
        
        self.output_text.insert(tk.END, "\n📋 LIST SCAN STARTED (no ports, <1 sec expected)\n", 'info')
        self.run_scan()
    
    # ========== HELPER FUNCTIONS ==========
    
    def blink_status(self):
        if self.is_scanning:
            current = self.status_indicator.cget('fg')
            new_color = self.red if current == self.green else self.green
            self.status_indicator.config(fg=new_color)
        else:
            self.status_indicator.config(fg=self.green)
        self.root.after(500, self.blink_status)
    
    def browse_file(self, entry_widget):
        filename = filedialog.askopenfilename(title="Select File", filetypes=[("Text files", "*.txt")])
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)
            self.output_text.insert(tk.END, f"\n✓ File: {filename}\n", 'success')
    
    def load_targets_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as f:
                self.target_entry.delete(0, tk.END)
                self.target_entry.insert(0, f.read().strip().replace('\n', ' '))
            self.output_text.insert(tk.END, f"\n✓ Loaded: {filename}\n", 'success')
    
    def build_command(self):
        cmd = ["nmap"]
        target = self.target_entry.get().strip()
        
        # Check if list scan is selected (NO port scan parameters allowed)
        is_list_scan = False
        if 'host' in self.cmd_vars and '-sL' in self.cmd_vars['host']:
            if self.cmd_vars['host']['-sL'].get():
                is_list_scan = True
        
        for tab, vars_dict in self.cmd_vars.items():
            entries_dict = self.cmd_entries.get(tab, {})
            for c, var in vars_dict.items():
                if var.get():
                    # Skip port scan parameters if list scan is selected
                    if is_list_scan and c in ['-p', '-F', '--top-ports', '--exclude-ports', '-T0', '-T1', '-T2', '-T3', '-T4', '-T5', '--min-rate', '--max-retries', '--host-timeout', '--max-scan-delay']:
                        continue
                    entry = entries_dict.get(c)
                    if entry and entry.get():
                        file_path = entry.get()
                        if ' ' in file_path:
                            file_path = '"' + file_path + '"'
                        cmd.append(f"{c} {file_path}")
                    else:
                        cmd.append(c)
                        
        if target:
            cmd.append(target)
        else:
            cmd.append("scanme.nmap.org")
            
        cmd_str = " ".join(cmd)
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, cmd_str)
        return cmd_str
    
    def update_output_queue(self):
        try:
            while True:
                text, tag = self.output_queue.get_nowait()
                self.output_text.insert(tk.END, text, tag)
                self.output_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.update_output_queue)
    
    # ========== AI FUNCTIONS ==========
    
    def open_ai_dashboard(self):
        try:
            dashboard = AIDashboard(self.root, self.ai, self.reporting, self.network_mapper, self.advanced_discovery)
            dashboard.open_dashboard()
        except Exception as e:
            self.output_text.insert(tk.END, f"\n[!] Opening AI Dashboard...\n", 'info')
    
    def ai_analyze(self):
        if not self.last_scan_output:
            self.output_text.insert(tk.END, "\n[!] Run a scan first\n", 'warning')
            return
        
        target = self.target_entry.get().strip()
        ports = []
        services = []
        matches = re.findall(r'(\d+)/tcp\s+open\s+(\w+)', self.last_scan_output)
        for port, service in matches:
            ports.append(int(port))
            services.append(service)
        
        if not ports:
            self.output_text.insert(tk.END, "\n[!] No open ports found\n", 'warning')
            return
        
        self.output_text.insert(tk.END, "\n🤖 AI ANALYSIS...\n", 'ai')
        
        risk_score = 0
        critical_ports = [445, 3389, 23, 21, 512, 513, 514, 1524, 6667]
        high_ports = [22, 80, 443, 3306, 5432, 5900]
        
        for port in ports:
            if port in critical_ports:
                risk_score += 15
            elif port in high_ports:
                risk_score += 8
        
        risk_score = min(100, risk_score)
        
        self.output_text.insert(tk.END, f"\n📊 RISK SCORE: {risk_score}/100\n", 'ai')
        
        if risk_score >= 70:
            self.output_text.insert(tk.END, "🔴 CRITICAL RISK - Immediate action required!\n", 'error')
        elif risk_score >= 50:
            self.output_text.insert(tk.END, "🟠 HIGH RISK - Action required soon\n", 'warning')
        elif risk_score >= 30:
            self.output_text.insert(tk.END, "🟡 MEDIUM RISK - Plan to address\n", 'warning')
        else:
            self.output_text.insert(tk.END, "🟢 LOW RISK - Monitor\n", 'success')
        
        self.output_text.insert(tk.END, f"\n📡 Open Ports Found: {len(ports)}\n", 'info')
        for port in ports[:30]:
            self.output_text.insert(tk.END, f"   • Port {port}\n", 'output')
        
        if 445 in ports:
            self.output_text.insert(tk.END, "\n📋 RECOMMENDATION: Port 445 (SMB) - Disable SMBv1, patch EternalBlue\n", 'warning')
        if 23 in ports:
            self.output_text.insert(tk.END, "📋 RECOMMENDATION: Port 23 (Telnet) - DISABLE, use SSH\n", 'warning')
        if 21 in ports:
            self.output_text.insert(tk.END, "📋 RECOMMENDATION: Port 21 (FTP) - Disable anonymous access\n", 'warning')
    
    # ========== CORE FUNCTIONS ==========
    
    def run_scan(self):
        if self.is_scanning:
            return
        
        cmd = self.build_command()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n" + "="*80 + "\n", 'info')
        self.output_text.insert(tk.END, f"[*] SCAN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", 'info')
        self.output_text.insert(tk.END, f"[*] COMMAND: {cmd}\n", 'info')
        self.output_text.insert(tk.END, "="*80 + "\n\n", 'info')
        
        def scan():
            try:
                start_time = datetime.now()
                self.is_scanning = True
                self.run_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.status_bar.config(text="🔥 SCANNING...", fg=self.red)
                self.progress.start()
                self.progress_label.config(text="Scanning target...")
                
                self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
                lines = []
                for line in iter(self.current_process.stdout.readline, ''):
                    if line:
                        self.output_queue.put((line, 'output'))
                        lines.append(line)
                stdout, stderr = self.current_process.communicate()
                if stdout:
                    self.output_queue.put((stdout, 'output'))
                    lines.append(stdout)
                if stderr:
                    self.output_queue.put((f"\n[!] {stderr}\n", 'error'))
                self.last_scan_output = ''.join(lines)
                
                elapsed = (datetime.now() - start_time).total_seconds()
                
                self.progress.stop()
                self.progress_label.config(text="")
                self.output_queue.put(("\n" + "="*80 + "\n", 'info'))
                self.output_queue.put((f"[✓] SCAN COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", 'success'))
                self.output_queue.put((f"[*] SCAN TIME: {elapsed:.2f} seconds\n", 'info'))
                self.output_queue.put(("="*80 + "\n", 'info'))
                self.status_bar.config(text="✅ READY", fg=self.green)
            except Exception as e:
                self.progress.stop()
                self.output_queue.put((f"\n[✗] ERROR: {str(e)}\n", 'error'))
                self.status_bar.config(text="❌ FAILED", fg=self.red)
            finally:
                self.is_scanning = False
                self.run_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.current_process = None
        threading.Thread(target=scan, daemon=True).start()
    
    def stop_scan(self):
        if self.current_process and self.is_scanning:
            try:
                self.current_process.terminate()
                self.output_queue.put(("\n[!] STOPPED\n", 'warning'))
                self.status_bar.config(text="⏹ STOPPED", fg=self.yellow)
                self.progress.stop()
                self.is_scanning = False
                self.run_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
            except:
                pass
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.command_text.delete(1.0, tk.END)
        self.last_scan_output = ""
        self.print_welcome()
        self.status_bar.config(text="✅ CLEARED", fg=self.green)
    
    def save_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, 'w') as f:
                f.write(self.output_text.get(1.0, tk.END))
            self.output_text.insert(tk.END, f"\n✓ Saved: {filename}\n", 'success')
    
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("NEXRADAR HELP")
        help_window.geometry("800x600")
        help_window.configure(bg=self.bg_dark)
        
        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, bg=self.bg_dark, fg=self.green, font=('Courier', 10))
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
NEXRADAR v2.0 - HELP GUIDE

⚡ QUICK ACTION BUTTONS:
   • ULTRA FAST SCAN - -T5 -F --min-rate 10000 -n (1 second)
   • FAST PORT SCAN - -T4 -F --min-rate 5000 -n (2-3 seconds)
   • LIST SCAN - -sL -n (No ports, just IP list, <1 second)

🤖 AI FEATURES:
   • AI ANALYZE - Vulnerability detection and risk scoring
   • AI DASHBOARD - Advanced features (13 TABS)

📌 BASIC USAGE:
   1. Enter target IP or domain
   2. Use QUICK ACTION buttons OR select options from LEFT PANEL
   3. Click RUN to start scanning
   4. Click AI ANALYZE for vulnerability report

🎯 SCAN OPTIONS (11 TABS):
   • TARGET - Target specification
   • HOST - Host discovery (-sn, -Pn, -PS, -PA, -PU, -sL)
   • SCAN - Scan techniques (-sS, -sT, -sU, -sA)
   • PORT - Port specification (-p, -F, --top-ports, --exclude-ports)
   • SERVICE - Service version detection (-sV, --version-intensity)
   • OS - OS detection (-O)
   • SCRIPT - Script scanning (-sC, --script, --script-args)
   • TIMING - Timing templates (-T0 to -T5, --min-rate, --max-retries)
   • FIREWALL - Evasion techniques (-f, -D, --mtu, --scanflags)
   • OUTPUT - Output options (-oN, -oX, -oG, -oA)
   • MISC - Miscellaneous (-6, -A, -n)

⚠️ LEGAL: Only scan authorized systems!
"""
        help_text.insert(1.0, help_content)
    
    def run(self):
        self.root.mainloop()
