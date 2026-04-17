#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Evasion Techniques Module
Proxy chains, VPN rotation, MAC randomization, Traffic shaping, IDS/IPS fingerprinting
"""

import subprocess
import random
import time
import re
import socket
import requests
from datetime import datetime

class EvasionTechniques:
    def __init__(self):
        self.proxy_list = []
        self.current_proxy = None
        self.vpn_status = False
        self.original_mac = None
        self.traffic_stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'scan_duration': 0
        }
        
    # ========== 1. PROXY CHAINS ==========
    
    def setup_tor_proxy(self):
        """Setup Tor proxy for anonymous scanning"""
        try:
            # Check if Tor is installed
            result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if result.returncode != 0:
                return False, "Tor is not installed. Install with: sudo apt install tor"
            
            # Start Tor service
            subprocess.run(['sudo', 'systemctl', 'start', 'tor'], capture_output=True)
            
            # Configure proxy
            self.current_proxy = {
                'type': 'socks5',
                'host': '127.0.0.1',
                'port': 9050,
                'name': 'Tor'
            }
            
            return True, f"Tor proxy configured at {self.current_proxy['host']}:{self.current_proxy['port']}"
        except Exception as e:
            return False, f"Error setting up Tor: {e}"
    
    def setup_socks_proxy(self, host, port, username=None, password=None):
        """Setup SOCKS5 proxy"""
        self.current_proxy = {
            'type': 'socks5',
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'name': f'SOCKS5@{host}:{port}'
        }
        return True, f"SOCKS5 proxy configured: {host}:{port}"
    
    def setup_http_proxy(self, host, port, username=None, password=None):
        """Setup HTTP/HTTPS proxy"""
        self.current_proxy = {
            'type': 'http',
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'name': f'HTTP@{host}:{port}'
        }
        return True, f"HTTP proxy configured: {host}:{port}"
    
    def test_proxy(self):
        """Test if proxy is working"""
        try:
            test_url = "https://api.ipify.org?format=json"
            proxies = {}
            if self.current_proxy:
                proxy_url = f"{self.current_proxy['type']}://{self.current_proxy['host']}:{self.current_proxy['port']}"
                proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
            
            response = requests.get(test_url, proxies=proxies, timeout=10)
            return True, f"Proxy working. IP: {response.json().get('ip', 'Unknown')}"
        except Exception as e:
            return False, f"Proxy test failed: {e}"
    
    def get_nmap_proxy_command(self):
        """Get nmap command with proxy settings"""
        if self.current_proxy:
            if self.current_proxy['type'] == 'socks5':
                return f"--proxies {self.current_proxy['type']}://{self.current_proxy['host']}:{self.current_proxy['port']}"
            elif self.current_proxy['type'] == 'http':
                return f"--proxies http://{self.current_proxy['host']}:{self.current_proxy['port']}"
        return ""
    
    # ========== 2. VPN ROTATION ==========
    
    def check_vpn_status(self):
        """Check if VPN is connected"""
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            vpn_interfaces = ['tun', 'tap', 'openvpn', 'wireguard', 'ppp']
            for interface in vpn_interfaces:
                if interface in result.stdout:
                    self.vpn_status = True
                    return True, f"VPN detected on interface: {interface}"
            
            current_ip = self.get_public_ip()
            if current_ip != self.get_original_ip():
                self.vpn_status = True
                return True, f"VPN active. Current IP: {current_ip}"
            
            return False, "No VPN detected"
        except:
            return False, "Could not check VPN status"
    
    def rotate_vpn(self, vpn_config_path=None):
        """Rotate VPN connection"""
        try:
            subprocess.run(['sudo', 'pkill', 'openvpn'], capture_output=True)
            subprocess.run(['sudo', 'pkill', 'wireguard'], capture_output=True)
            time.sleep(2)
            
            if vpn_config_path:
                subprocess.Popen(['sudo', 'openvpn', '--config', vpn_config_path], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(5)
                return True, f"VPN rotated to new server"
            else:
                return False, "No VPN config provided"
        except Exception as e:
            return False, f"VPN rotation failed: {e}"
    
    def get_public_ip(self):
        """Get current public IP address"""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text.strip()
        except:
            return "Unknown"
    
    def get_original_ip(self):
        """Get original IP (without VPN)"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unknown"
    
    # ========== 3. MAC RANDOMIZATION ==========
    
    def get_current_mac(self, interface="eth0"):
        """Get current MAC address"""
        try:
            result = subprocess.run(['ip', 'link', 'show', interface], capture_output=True, text=True)
            mac_match = re.search(r'link/ether\s+([0-9a-f:]{17})', result.stdout)
            if mac_match:
                return mac_match.group(1)
            return None
        except:
            return None
    
    def generate_random_mac(self):
        """Generate random MAC address"""
        first_byte = random.randint(0, 254)
        if first_byte % 2 != 0:
            first_byte += 1
        mac = [first_byte] + [random.randint(0, 255) for _ in range(5)]
        return ':'.join(f'{b:02x}' for b in mac)
    
    def change_mac_address(self, interface="eth0", new_mac=None):
        """Change MAC address"""
        try:
            if not new_mac:
                new_mac = self.generate_random_mac()
            
            if not self.original_mac:
                self.original_mac = self.get_current_mac(interface)
            
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'address', new_mac], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], capture_output=True)
            
            return True, f"MAC changed to {new_mac}"
        except Exception as e:
            return False, f"MAC change failed: {e}"
    
    def restore_mac_address(self, interface="eth0"):
        """Restore original MAC address"""
        if self.original_mac:
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'address', self.original_mac], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], capture_output=True)
            return True, f"MAC restored to {self.original_mac}"
        return False, "No original MAC stored"
    
    # ========== 4. TRAFFIC SHAPING ==========
    
    def get_default_interface(self):
        """Get default network interface"""
        try:
            result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
            interface_match = re.search(r'dev\s+(\w+)', result.stdout)
            if interface_match:
                return interface_match.group(1)
            return "eth0"
        except:
            return "eth0"
    
    def setup_traffic_shaping(self, rate_limit="100kbit", burst="200kbit"):
        """Setup traffic shaping"""
        try:
            interface = self.get_default_interface()
            subprocess.run(['sudo', 'tc', 'qdisc', 'add', 'dev', interface, 'root', 'handle', '1:', 'htb'], 
                          capture_output=True)
            subprocess.run(['sudo', 'tc', 'class', 'add', 'dev', interface, 'parent', '1:', 'classid', '1:1', 
                          'htb', 'rate', rate_limit, 'burst', burst], capture_output=True)
            return True, f"Traffic shaping enabled: rate={rate_limit}, burst={burst}"
        except Exception as e:
            return False, f"Traffic shaping failed: {e}"
    
    def set_scan_delay(self, delay_ms=1000):
        """Set delay between packets"""
        return f"--scan-delay {delay_ms}ms"
    
    def remove_traffic_shaping(self):
        """Remove traffic shaping"""
        try:
            interface = self.get_default_interface()
            subprocess.run(['sudo', 'tc', 'qdisc', 'del', 'dev', interface, 'root'], capture_output=True)
            return True, "Traffic shaping removed"
        except:
            return False, "Could not remove traffic shaping"
    
    # ========== 5. IDS/IPS FINGERPRINTING ==========
    
    def detect_firewall(self, target):
        """Detect if firewall/IDS is present"""
        results = []
        try:
            result = subprocess.run(['nmap', '-sS', '-p', '80,443', target], 
                                   capture_output=True, text=True, timeout=30)
            if 'filtered' in result.stdout:
                results.append("Ports appear FILTERED - Firewall likely present")
            else:
                results.append("Ports appear OPEN - No obvious firewall")
        except:
            results.append("Could not test ports")
        
        try:
            result = subprocess.run(['nmap', '-sA', '-p', '80', target], 
                                   capture_output=True, text=True, timeout=30)
            if 'unfiltered' in result.stdout:
                results.append("ACK scan shows unfiltered - Stateful firewall likely")
        except:
            pass
        
        return results
    
    def get_evasion_commands(self):
        """Get all evasion commands"""
        return [
            "-f (Fragment packets)",
            "--mtu 8 (Set MTU to 8)",
            "-D RND:10 (Random decoys)",
            "-g 53 (Source port 53)",
            "--source-port 53 (Source port spoofing)",
            "-T0 (Paranoid timing)",
            "--scan-delay 1s (1 second delay)",
            "--max-retries 1 (Fewer retries)",
            "--data-length 200 (Random data length)",
            "--ttl 128 (Set TTL)",
            "--spoof-mac 0 (Random MAC)",
            "--badsum (Bad checksum)"
        ]
    
    def format_output(self, data_type, data):
        """Format output"""
        output = []
        output.append("\n" + "="*70)
        output.append(f"🛡 {data_type.upper()}")
        output.append("="*70)
        
        if isinstance(data, list):
            for item in data:
                output.append(f"   • {item}")
        elif isinstance(data, dict):
            for key, value in data.items():
                output.append(f"   • {key}: {value}")
        else:
            output.append(f"   {data}")
        
        return "\n".join(output)
