#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess

def check_dependencies():
    print("\n" + "="*70)
    print("🔍 CHECKING DEPENDENCIES...")
    print("="*70)
    
    missing_deps = []
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    else:
        print("✅ Python version OK")
    
    # Check nmap
    print("\n📡 Checking Nmap...")
    try:
        result = subprocess.run(['nmap', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
        else:
            print("❌ Nmap is not installed!")
            missing_deps.append("nmap")
    except FileNotFoundError:
        print("❌ Nmap not found!")
        missing_deps.append("nmap")
    
    # Check tkinter
    print("\n🖥️ Checking Tkinter...")
    try:
        import tkinter
        print("✅ Tkinter is installed")
    except ImportError:
        print("❌ Tkinter is not installed!")
        missing_deps.append("tkinter")
    
    if missing_deps:
        print("\n⚠️ MISSING DEPENDENCIES:")
        for dep in missing_deps:
            print(f"   • {dep}")
        return False
    
    print("\n✅ ALL DEPENDENCIES SATISFIED!")
    return True

def show_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║   ███╗   ██╗██╗███╗   ██╦╗     ███████╗ ██████╗ █████╗ ███╗   ██╗            ║
    ║   ████╗  ██║██║████╗  ██║║     ██╔════╝██╔════╝██╔══██╗████╗  ██║            ║
    ║   ██╔██╗ ██║██║██╔██╗ ██║║     ███████╗██║     ███████║██╔██╗ ██║            ║
    ║   ██║╚██╗██║██║██║╚██╗██║║     ╚════██║██║     ██╔══██║██║╚██╗██║            ║
    ║   ██║ ╚████║██║██║ ╚████║██████╗███████║╚██████╗██║  ██║██║ ╚████║            ║
    ║   ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝╚═════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝            ║
    ║                                                                              ║
    ║                         N-VERSION 1 - NETWORK SCANNER                        ║
    ║                              [ FAST | STEALTH | PROFESSIONAL ]               ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_banner()
        
        if not check_dependencies():
            sys.exit(1)
        
        print("\n🚀 LOADING N-VERSION 1...")
        print("="*70)
        from gui import NmapGUI
        
        print("\n✨ INITIALIZING INTERFACE...")
        print("="*70 + "\n")
        
        app = NmapGUI()
        app.run()
        
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if os.name == 'posix' and os.geteuid() != 0:
        print("\n⚠️ Running without root privileges! Some features may not work.\n")
    main()
