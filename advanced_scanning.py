#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Scanning Features Module
IPv6 scanning, Bluetooth scanning, WiFi scanning
IoT device scanning, Industrial protocols scanning
"""

import subprocess
import re
import json
import os
import time
from datetime import datetime

class AdvancedScanning:
    def __init__(self):
        self.data_dir = "advanced_scan_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    # ========== 1. IPv6 FULL SUPPORT ==========
    
    def scan_ipv6_hosts(self, ipv6_range="fe80::/64"):
        """Discover IPv6 hosts on network"""
        results = []
        try:
            cmd = f"nmap -6 -sn {ipv6_range}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            ipv6_pattern = r'([0-9a-f:]+)'
            ips = re.findall(ipv6_pattern, result.stdout)
            
            for ip in ips:
                if ':' in ip and len(ip) > 5 and ' ' not in ip:
                    results.append({
                        'ip': ip,
                        'type': 'IPv6',
                        'status': 'discovered'
                    })
            
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    def scan_ipv6_ports(self, ipv6_target, ports="1-1000"):
        """Scan ports on IPv6 target"""
        try:
            cmd = f"nmap -6 -p {ports} {ipv6_target}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            port_pattern = r'(\d+)/tcp\s+open\s+(\w+)'
            open_ports = []
            for port, service in re.findall(port_pattern, result.stdout):
                open_ports.append({'port': int(port), 'service': service})
            
            return open_ports
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_ipv6_neighbors(self):
        """Get IPv6 neighbors using ND protocol"""
        try:
            result = subprocess.run(['ip', '-6', 'neigh', 'show'], 
                                   capture_output=True, text=True, timeout=10)
            neighbors = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        neighbors.append({
                            'ip': parts[0],
                            'mac': parts[4] if len(parts) > 4 else 'Unknown',
                            'state': parts[1] if len(parts) > 1 else 'Unknown'
                        })
            return neighbors
        except:
            return []
    
    # ========== 2. BLUETOOTH SCANNING (FIXED) ==========
    
    def scan_bluetooth_devices(self, timeout=15):
        """Discover Bluetooth devices - FIXED version"""
        results = []
        try:
            # Check if bluetoothctl is available
            result = subprocess.run(['which', 'bluetoothctl'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return [{'error': 'bluetoothctl not found. Install bluez package'}]
            
            # Check if Bluetooth adapter is available
            result = subprocess.run(['hciconfig'], capture_output=True, text=True, timeout=5)
            if 'DOWN' in result.stdout or 'No such file' in result.stdout:
                return [{'error': 'Bluetooth adapter not found or disabled. Enable Bluetooth first.'}]
            
            # Method 1: Using bluetoothctl with proper timeout
            try:
                # Start scan in background
                scan_process = subprocess.Popen(['bluetoothctl', 'scan', 'on'], 
                                                stdout=subprocess.DEVNULL, 
                                                stderr=subprocess.DEVNULL)
                
                # Wait for scan to initialize
                time.sleep(3)
                
                # Get devices
                result = subprocess.run(['bluetoothctl', 'devices'], 
                                       capture_output=True, text=True, timeout=timeout)
                
                # Stop scan
                subprocess.run(['bluetoothctl', 'scan', 'off'], 
                              capture_output=True, timeout=5)
                
                # Terminate scan process
                scan_process.terminate()
                
            except subprocess.TimeoutExpired:
                # If timeout, try to stop scan and continue
                subprocess.run(['bluetoothctl', 'scan', 'off'], capture_output=True)
                result = subprocess.run(['bluetoothctl', 'devices'], 
                                       capture_output=True, text=True, timeout=5)
            
            # Parse devices
            for line in result.stdout.split('\n'):
                if line.strip() and 'Device' in line:
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        results.append({
                            'mac': parts[1],
                            'name': parts[2],
                            'type': 'Bluetooth',
                            'status': 'discovered'
                        })
            
            # Method 2: Alternative using hcitool (if available)
            if not results:
                try:
                    result = subprocess.run(['sudo', 'hcitool', 'scan'], 
                                           capture_output=True, text=True, timeout=15)
                    for line in result.stdout.split('\n'):
                        if line.strip() and ':' in line:
                            parts = line.split('\t')
                            if len(parts) >= 2:
                                results.append({
                                    'mac': parts[0].strip(),
                                    'name': parts[1].strip() if parts[1].strip() else 'Unknown',
                                    'type': 'Bluetooth',
                                    'status': 'discovered'
                                })
                except:
                    pass
            
            return results if results else [{'info': 'No Bluetooth devices found. Make sure devices are in range and discoverable.'}]
            
        except subprocess.TimeoutExpired:
            return [{'error': 'Bluetooth scan timeout. Try again or check Bluetooth adapter.'}]
        except Exception as e:
            return [{'error': f'Bluetooth scan failed: {str(e)}'}]
    
    def get_bluetooth_device_info(self, mac_address):
        """Get detailed info about Bluetooth device"""
        try:
            result = subprocess.run(['bluetoothctl', 'info', mac_address], 
                                   capture_output=True, text=True, timeout=10)
            
            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            return info
        except:
            return {}
    
    # ========== 3. WIFI SCANNING ==========
    
    def scan_wifi_networks(self, interface=None):
        """Discover WiFi access points - FIXED version"""
        results = []
        try:
            # Check if iwlist is available
            result = subprocess.run(['which', 'iwlist'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return [{'error': 'iwlist not found. Install wireless-tools'}]
            
            # Get wireless interface if not specified
            if not interface:
                interface = self.get_wifi_interface()
            
            if not interface:
                return [{'error': 'No wireless interface found'}]
            
            # Scan WiFi
            cmd = f"sudo iwlist {interface} scan"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            # Parse WiFi networks
            current_network = {}
            for line in result.stdout.split('\n'):
                if 'ESSID:' in line:
                    ssid = line.split('ESSID:')[1].strip().strip('"')
                    if ssid and ssid != '':
                        current_network['ssid'] = ssid
                elif 'Address:' in line:
                    current_network['bssid'] = line.split('Address:')[1].strip()
                elif 'Channel:' in line:
                    current_network['channel'] = line.split('Channel:')[1].strip()
                elif 'Quality=' in line:
                    quality = re.search(r'Quality=(\d+)/(\d+)', line)
                    if quality:
                        current_network['signal'] = f"{int(quality.group(1)) * 100 // int(quality.group(2))}%"
                elif 'Encryption key:on' in line:
                    current_network['encrypted'] = True
                elif 'Encryption key:off' in line:
                    current_network['encrypted'] = False
                
                if current_network.get('ssid') and current_network.get('bssid'):
                    results.append(current_network.copy())
                    current_network = {}
            
            return results if results else [{'info': 'No WiFi networks found. Make sure WiFi adapter is enabled.'}]
            
        except subprocess.TimeoutExpired:
            return [{'error': 'WiFi scan timeout'}]
        except Exception as e:
            return [{'error': f'WiFi scan failed: {str(e)}'}]
    
    def get_wifi_interface(self):
        """Get wireless interface name"""
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line:
                    return line.split()[0]
            return None
        except:
            return None
    
    # ========== 4. IoT DEVICE SCANNING ==========
    
    def scan_iot_devices(self, ip_range="192.168.79.0/24"):
        """Discover IoT devices on network"""
        results = []
        try:
            iot_ports = [1883, 8883, 5683, 5684, 4840, 47808, 502, 9600]
            iot_services = {
                1883: 'MQTT',
                8883: 'MQTT TLS',
                5683: 'CoAP',
                5684: 'CoAPS',
                4840: 'OPC UA',
                47808: 'BACnet',
                502: 'Modbus',
                9600: 'Z-Wave'
            }
            
            for port in iot_ports:
                try:
                    cmd = f"nmap -sS -p {port} {ip_range}"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                    
                    ip_pattern = r'Nmap scan report for ([\d.]+)'
                    ips = re.findall(ip_pattern, result.stdout)
                    
                    for ip in ips:
                        if port in iot_services:
                            results.append({
                                'ip': ip,
                                'port': port,
                                'service': iot_services[port],
                                'type': 'IoT Device'
                            })
                except:
                    pass
            
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    def detect_zigbee_devices(self):
        """Detect ZigBee devices"""
        return [{'info': 'ZigBee detection requires compatible hardware dongle (CC2531, CC1352, etc.)'}]
    
    def detect_zwave_devices(self):
        """Detect Z-Wave devices"""
        return [{'info': 'Z-Wave detection requires compatible hardware dongle (Aeotec, Zooz, etc.)'}]
    
    # ========== 5. INDUSTRIAL PROTOCOLS SCANNING ==========
    
    def scan_modbus_devices(self, ip_range="192.168.79.0/24"):
        """Scan for Modbus devices"""
        results = []
        try:
            cmd = f"nmap -sS -p 502 {ip_range}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            ip_pattern = r'Nmap scan report for ([\d.]+)'
            ips = re.findall(ip_pattern, result.stdout)
            
            for ip in ips:
                results.append({
                    'ip': ip,
                    'protocol': 'Modbus/TCP',
                    'port': 502,
                    'type': 'Industrial Control'
                })
            
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    def scan_bacnet_devices(self, ip_range="192.168.79.0/24"):
        """Scan for BACnet devices"""
        results = []
        try:
            cmd = f"nmap -sS -p 47808 {ip_range}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            ip_pattern = r'Nmap scan report for ([\d.]+)'
            ips = re.findall(ip_pattern, result.stdout)
            
            for ip in ips:
                results.append({
                    'ip': ip,
                    'protocol': 'BACnet',
                    'port': 47808,
                    'type': 'Building Automation'
                })
            
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    def scan_scada_devices(self, ip_range="192.168.79.0/24"):
        """Scan for SCADA devices"""
        results = []
        scada_ports = {
            502: 'Modbus',
            44818: 'CIP',
            2222: 'EtherNet/IP',
            4840: 'OPC UA',
            47808: 'BACnet',
            1962: 'IEC 60870-5-104'
        }
        
        for port, protocol in scada_ports.items():
            try:
                cmd = f"nmap -sS -p {port} {ip_range}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                
                ip_pattern = r'Nmap scan report for ([\d.]+)'
                ips = re.findall(ip_pattern, result.stdout)
                
                for ip in ips:
                    results.append({
                        'ip': ip,
                        'port': port,
                        'protocol': protocol,
                        'type': 'SCADA/ICS'
                    })
            except:
                pass
        
        return results
    
    # ========== FORMAT OUTPUT ==========
    
    def format_ipv6_output(self, data):
        output = []
        output.append("\n" + "="*70)
        output.append("🌐 IPv6 SCAN RESULTS")
        output.append("="*70)
        
        if not data:
            output.append("   No IPv6 hosts found")
        else:
            for item in data:
                if 'error' in item:
                    output.append(f"   ❌ {item['error']}")
                else:
                    output.append(f"\n📡 IPv6 Host: {item.get('ip', 'Unknown')}")
                    output.append(f"   Type: {item.get('type', 'IPv6')}")
                    output.append(f"   Status: {item.get('status', 'Unknown')}")
        
        return "\n".join(output)
    
    def format_bluetooth_output(self, data):
        output = []
        output.append("\n" + "="*70)
        output.append("🔵 BLUETOOTH DEVICES")
        output.append("="*70)
        
        if not data:
            output.append("   No Bluetooth devices found")
        else:
            for item in data:
                if 'error' in item:
                    output.append(f"\n   ❌ {item['error']}")
                elif 'info' in item:
                    output.append(f"\n   ℹ️ {item['info']}")
                else:
                    output.append(f"\n📱 Device: {item.get('name', 'Unknown')}")
                    output.append(f"   MAC: {item.get('mac', 'Unknown')}")
                    output.append(f"   Type: {item.get('type', 'Bluetooth')}")
                    output.append(f"   Status: {item.get('status', 'Discovered')}")
        
        output.append("\n💡 Tips for better results:")
        output.append("   • Make sure Bluetooth is enabled")
        output.append("   • Put devices in pairing mode")
        output.append("   • Bring devices closer")
        output.append("   • Run: sudo systemctl start bluetooth")
        
        return "\n".join(output)
    
    def format_wifi_output(self, data):
        output = []
        output.append("\n" + "="*70)
        output.append("📶 WIFI NETWORKS")
        output.append("="*70)
        
        if not data:
            output.append("   No WiFi networks found")
        else:
            for item in data:
                if 'error' in item:
                    output.append(f"\n   ❌ {item['error']}")
                elif 'info' in item:
                    output.append(f"\n   ℹ️ {item['info']}")
                else:
                    output.append(f"\n🛜 SSID: {item.get('ssid', 'Hidden Network')}")
                    output.append(f"   BSSID: {item.get('bssid', 'Unknown')}")
                    output.append(f"   Channel: {item.get('channel', 'Unknown')}")
                    output.append(f"   Signal: {item.get('signal', 'Unknown')}")
                    output.append(f"   Encrypted: {'Yes' if item.get('encrypted') else 'No'}")
        
        return "\n".join(output)
    
    def format_iot_output(self, data):
        output = []
        output.append("\n" + "="*70)
        output.append("🤖 IoT DEVICES")
        output.append("="*70)
        
        if not data:
            output.append("   No IoT devices found")
        else:
            for item in data:
                if 'error' in item:
                    output.append(f"\n   ❌ {item['error']}")
                elif 'info' in item:
                    output.append(f"\n   ℹ️ {item['info']}")
                else:
                    output.append(f"\n📡 Device: {item.get('ip', 'Unknown')}")
                    output.append(f"   Port: {item.get('port', 'Unknown')}")
                    output.append(f"   Service: {item.get('service', 'Unknown')}")
                    output.append(f"   Type: {item.get('type', 'IoT')}")
        
        return "\n".join(output)
    
    def format_industrial_output(self, data):
        output = []
        output.append("\n" + "="*70)
        output.append("🏭 INDUSTRIAL PROTOCOLS")
        output.append("="*70)
        
        if not data:
            output.append("   No industrial devices found")
        else:
            protocols = {}
            for item in data:
                if 'error' in item:
                    output.append(f"\n   ❌ {item['error']}")
                else:
                    proto = item.get('protocol', 'Unknown')
                    if proto not in protocols:
                        protocols[proto] = []
                    protocols[proto].append(item)
            
            for proto, devices in protocols.items():
                output.append(f"\n📡 {proto} Devices:")
                for device in devices:
                    output.append(f"   • {device.get('ip', 'Unknown')} (Port: {device.get('port', 'Unknown')})")
        
        return "\n".join(output)
