#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Anomaly Detection
Unusual open ports detect करता है
"""

class AnomalyDetector:
    def __init__(self):
        # Normal port profiles for different server types
        self.profiles = {
            "web_server": {
                "expected": [80, 443],
                "optional": [22, 3306, 5432],
                "suspicious": [4444, 31337, 6667, 1337, 12345]
            },
            "database_server": {
                "expected": [3306, 5432, 1433, 1521],
                "optional": [22, 80, 443],
                "suspicious": [4444, 31337]
            },
            "file_server": {
                "expected": [139, 445, 2049],
                "optional": [22, 21, 873],
                "suspicious": [4444, 31337]
            },
            "mail_server": {
                "expected": [25, 110, 143, 587, 993, 995],
                "optional": [22, 80, 443],
                "suspicious": [4444, 31337]
            },
            "dns_server": {
                "expected": [53],
                "optional": [22, 953],
                "suspicious": [4444, 31337]
            },
            "default": {
                "expected": [22, 80, 443],
                "optional": [21, 25, 53, 3306],
                "suspicious": [4444, 31337, 6667, 1337, 12345, 54321, 31337]
            }
        }
        
        # Known backdoor ports
        self.backdoor_ports = {
            4444: "Metasploit Meterpreter",
            31337: "Back Orifice / Elite",
            6667: "IRC Botnet",
            1337: "Leet Backdoor",
            12345: "NetBus",
            54321: "PCAnywhere",
            31337: "Elite (Back Orifice)",
            65534: "Linux Backdoor",
            4443: "A-Squared Backdoor",
            8080: "Proxy (possible malware)"
        }
    
    def detect(self, open_ports, server_type="default"):
        """Detect anomalies in open ports"""
        anomalies = []
        severity = "LOW"
        
        profile = self.profiles.get(server_type, self.profiles["default"])
        
        for port in open_ports:
            # Check for backdoors
            if port in self.backdoor_ports:
                anomalies.append({
                    "port": port,
                    "type": "BACKDOOR",
                    "severity": "CRITICAL",
                    "details": f"Known backdoor port: {self.backdoor_ports[port]}",
                    "action": "IMMEDIATE INVESTIGATION REQUIRED!"
                })
                severity = "CRITICAL"
            
            # Check for suspicious ports
            elif port in profile["suspicious"]:
                anomalies.append({
                    "port": port,
                    "type": "SUSPICIOUS",
                    "severity": "HIGH",
                    "details": f"Unusual port for {server_type}",
                    "action": "Investigate service on this port"
                })
                if severity != "CRITICAL":
                    severity = "HIGH"
            
            # Check for unexpected but not suspicious
            elif port not in profile["expected"] and port not in profile["optional"]:
                anomalies.append({
                    "port": port,
                    "type": "UNEXPECTED",
                    "severity": "MEDIUM",
                    "details": f"Not expected on {server_type}",
                    "action": "Verify if this service should be running"
                })
                if severity not in ["CRITICAL", "HIGH"]:
                    severity = "MEDIUM"
        
        return anomalies, severity
    
    def detect_service_anomaly(self, service_name, version, expected_version=None):
        """Detect anomalies in service versions"""
        anomalies = []
        
        # Check for end-of-life versions
        eol_versions = {
            "Windows": ["XP", "7", "2003", "2008"],
            "Linux": ["2.4", "2.6", "3.x"],
            "Apache": ["2.2", "2.0"],
            "MySQL": ["5.0", "5.1", "5.5"],
            "OpenSSH": ["4.x", "5.x", "6.x"]
        }
        
        for service, versions in eol_versions.items():
            if service.lower() in service_name.lower():
                for eol in versions:
                    if eol in version:
                        anomalies.append({
                            "service": service_name,
                            "version": version,
                            "type": "END_OF_LIFE",
                            "severity": "HIGH",
                            "details": f"{service} version {version} is end-of-life",
                            "action": "Upgrade to supported version immediately"
                        })
        
        return anomalies
    
    def format_output(self, anomalies, severity, open_ports):
        """Format anomaly detection output"""
        output = []
        output.append("\n" + "="*70)
        output.append("🔍 ANOMALY DETECTION REPORT")
        output.append("="*70)
        
        output.append(f"\n📊 OVERALL SEVERITY: {severity}")
        
        if severity == "CRITICAL":
            output.append("🔴 CRITICAL ANOMALIES DETECTED!")
        elif severity == "HIGH":
            output.append("🟠 HIGH RISK ANOMALIES DETECTED")
        elif severity == "MEDIUM":
            output.append("🟡 MEDIUM RISK ANOMALIES DETECTED")
        else:
            output.append("🟢 No significant anomalies detected")
        
        if not anomalies:
            output.append("\n✅ No anomalies detected in open ports")
            output.append("="*70)
            return "\n".join(output)
        
        output.append(f"\n📡 Open ports analyzed: {len(open_ports)}")
        output.append(f"⚠️ Anomalies found: {len(anomalies)}")
        
        for anomaly in anomalies:
            output.append(f"\n{'─'*50}")
            
            if anomaly["type"] == "BACKDOOR":
                output.append(f"🔴 PORT {anomaly['port']} - BACKDOOR DETECTED!")
            elif anomaly["type"] == "SUSPICIOUS":
                output.append(f"🟠 PORT {anomaly['port']} - SUSPICIOUS")
            else:
                output.append(f"🟡 PORT {anomaly['port']} - UNEXPECTED")
            
            output.append(f"   📝 {anomaly['details']}")
            output.append(f"   🎯 ACTION: {anomaly['action']}")
        
        output.append("\n" + "="*70)
        return "\n".join(output)
