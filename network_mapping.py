#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Network Mapping Module - OPTIMIZED FOR SPEED
Parallel scanning, faster discovery
"""

import subprocess
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class NetworkMapper:
    def __init__(self):
        self.hosts = []
        self.topology = {}
        
    def discover_hosts(self, network_range, max_workers=10):
        """Parallel host discovery - FAST"""
        print(f"[*] Fast discovering hosts in {network_range}...")
        
        try:
            # Fast ping scan with timing
            cmd = f"nmap -sn -T4 --min-rate 1000 {network_range}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            # Parse IP addresses
            ip_pattern = r'Nmap scan report for (?:.*? )?(\d+\.\d+\.\d+\.\d+)'
            ips = re.findall(ip_pattern, result.stdout)
            
            # Parse MAC addresses
            mac_pattern = r'MAC Address: ([0-9A-F:]+)'
            macs = re.findall(mac_pattern, result.stdout)
            
            for i, ip in enumerate(ips):
                host = {
                    'ip': ip,
                    'mac': macs[i] if i < len(macs) else 'Unknown',
                    'status': 'up',
                    'last_seen': datetime.now().isoformat()
                }
                self.hosts.append(host)
                
            return self.hosts
            
        except subprocess.TimeoutExpired:
            return [{'error': 'Scan timeout'}]
        except Exception as e:
            return [{'error': str(e)}]
    
    def scan_topology(self, target):
        """Fast topology discovery"""
        print(f"[*] Fast mapping topology to {target}...")
        
        try:
            # Fast traceroute with timing
            cmd = f"nmap --traceroute -T4 --min-rate 1000 {target}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            # Parse hops
            hop_pattern = r'(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)'
            hops = re.findall(hop_pattern, result.stdout)
            
            topology = []
            for hop in hops[:20]:  # Limit hops for speed
                topology.append({
                    'hop': int(hop[0]),
                    'rtt': float(hop[1]),
                    'ip': hop[2]
                })
            
            self.topology[target] = topology
            return topology
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def parallel_scan_hosts(self, hosts, ports="1-1000", scan_type="-sS", max_workers=5):
        """Parallel scan multiple hosts - FAST"""
        results = {}
        
        def scan_host(host):
            cmd = f"nmap {scan_type} -T4 --min-rate 2000 --max-retries 1 -p {ports} {host}"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                return host, result.stdout
            except:
                return host, None
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_host = {executor.submit(scan_host, host): host for host in hosts}
            for future in as_completed(future_to_host):
                host, output = future.result()
                if output:
                    results[host] = output
        
        return results
    
    def format_output(self, hosts, topology, subdomains):
        """Fast formatted output"""
        output = []
        output.append("\n" + "="*70)
        output.append("🌐 NETWORK MAPPING REPORT (FAST)")
        output.append("="*70)
        
        output.append(f"\n📡 LIVE HOSTS FOUND: {len(hosts)}")
        for host in hosts[:20]:  # Limit for speed
            output.append(f"   • {host.get('ip', 'Unknown')} - MAC: {host.get('mac', 'Unknown')}")
        
        if hosts and len(hosts) > 20:
            output.append(f"   ... and {len(hosts) - 20} more")
        
        if topology:
            output.append(f"\n🗺️ NETWORK TOPOLOGY")
            for hop in topology[:10]:
                output.append(f"   Hop {hop['hop']}: {hop['ip']} ({hop['rtt']}ms)")
        
        output.append("\n" + "="*70)
        return "\n".join(output)
    
    def generate_topology_graph(self, topology_data, filename="network_topology.html"):
        """Fast topology graph generation"""
        # Simplified fast HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Network Topology - T-8 Scanner</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .hop {{ background: #1a1a1a; margin: 5px; padding: 10px; border-left: 3px solid #00ff41; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Network Topology</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        if 'hops' in topology_data:
            for hop in topology_data['hops'][:20]:
                html_content += f"""
        <div class="hop">
            <strong>Hop {hop['hop']}</strong><br>
            IP: {hop['ip']}<br>
            RTT: {hop['rtt']}ms
        </div>
"""
        html_content += """
    </div>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def generate_attack_surface(self, scan_data, filename="attack_surface.html"):
        """Fast attack surface generation"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Attack Surface - T-8 Scanner</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .critical {{ color: #ff4444; }}
        .high {{ color: #ff8844; }}
        .medium {{ color: #ffcc44; }}
        .low {{ color: #44ff44; }}
    </style>
</head>
<body>
    <h1>🎯 Attack Surface Analysis</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <pre>
{scan_data.get('vulnerability_prediction', {}).get('output', 'No data')[:2000]}
    </pre>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def generate_dependency_map(self, services, filename="dependency_map.html"):
        """Fast dependency map generation"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Service Dependency - T-8 Scanner</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
    </style>
</head>
<body>
    <h1>🔗 Service Dependencies</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <ul>
"""
        for service in services[:20]:
            html_content += f"        <li>{service.get('service', 'unknown')} on port {service.get('port', '?')}</li>\n"
        
        html_content += """
    </ul>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def live_host_tracking(self, hosts, interval=5):
        """Fast live host tracking"""
        print(f"\n[*] Fast live tracking (interval: {interval} seconds)")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"\n{'='*50}")
                print(f"Live Host Status - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*50}")
                
                for host in hosts[:20]:  # Limit for speed
                    ip = host['ip']
                    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                           capture_output=True)
                    
                    if result.returncode == 0:
                        print(f"  {ip} - ✅ UP")
                    else:
                        print(f"  {ip} - ❌ DOWN")
                
                import time
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n[*] Live tracking stopped")
