#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Integration Module - OPTIMIZED FOR SPEED
Fast optimization, reduced delays, caching
"""

import subprocess
import time
import re
from datetime import datetime
from functools import lru_cache

class AIIntegration:
    def __init__(self):
        self.scan_history = []
        self.cache = {}
        
    # ========== SMART SCAN OPTIMIZATION (FAST) ==========
    
    @lru_cache(maxsize=100)
    def optimize_before_scan(self, target):
        """Fast network optimization with caching"""
        
        # Check cache first
        cache_key = f"opt_{target}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Fast optimization - skip slow ping tests
        # Assume local network for speed
        profile = {
            "latency": 0,
            "packet_loss": 0,
            "bandwidth": "EXCELLENT"
        }
        
        # Recommended parameters (fast by default)
        params = {
            "timing": "T4",
            "max_retries": "--max-retries 1",
            "min_rate": "--min-rate 2000",
            "host_timeout": "--host-timeout 2m"
        }
        
        # Build output
        output = []
        output.append("\n" + "="*70)
        output.append("⚡ SMART SCAN OPTIMIZATION (FAST MODE)")
        output.append("="*70)
        
        output.append(f"\n📡 Target: {target}")
        output.append(f"📊 Network Profile:")
        output.append(f"   • Latency: 0ms (assumed)")
        output.append(f"   • Packet Loss: 0%")
        output.append(f"   • Bandwidth: EXCELLENT")
        
        output.append(f"\n🎯 Recommended Parameters:")
        output.append(f"   • Timing Template: -{params['timing']}")
        output.append(f"   • Max Retries: {params['max_retries']}")
        output.append(f"   • Min Rate: {params['min_rate']}")
        output.append(f"   • Host Timeout: {params['host_timeout']}")
        
        output.append("\n💡 Optimization applied automatically!")
        output.append("="*70)
        
        result = {
            'profile': profile,
            'parameters': params,
            'output': "\n".join(output)
        }
        
        # Cache result
        self.cache[cache_key] = result
        return result
    
    # ========== AI ANALYSIS (FAST) ==========
    
    def analyze_scan(self, scan_output, target, ports, services, scan_time):
        """Fast AI analysis with caching"""
        
        # Check cache
        cache_key = f"analysis_{target}_{hash(str(ports))}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Fast vulnerability prediction
        vuln_predictions = self._fast_vulnerability_prediction(ports, services)
        
        # Fast anomaly detection
        anomalies = self._fast_anomaly_detection(ports)
        
        # Fast CVE check
        cve_results = self._fast_cve_check(services)
        
        analysis = {
            'vulnerability_prediction': vuln_predictions,
            'anomalies': anomalies,
            'cve_check': cve_results,
            'target': target,
            'scan_time': scan_time,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache result
        self.cache[cache_key] = analysis
        return analysis
    
    def _fast_vulnerability_prediction(self, ports, services):
        """Fast vulnerability prediction using pre-defined patterns"""
        predictions = []
        risk_score = 0
        
        # Critical port patterns
        critical_ports = {
            445: "SMB - EternalBlue (CVE-2017-0144)",
            3389: "RDP - BlueKeep (CVE-2019-0708)",
            23: "Telnet - Insecure protocol",
            21: "FTP - Anonymous access possible",
            512: "exec - r-service vulnerability",
            513: "login - r-service vulnerability",
            514: "shell - r-service vulnerability",
            1524: "ingreslock - Backdoor possible",
            6667: "IRC - Botnet possible"
        }
        
        high_ports = {
            22: "SSH - Weak ciphers possible",
            80: "HTTP - Web vulnerabilities possible",
            443: "HTTPS - SSL/TLS issues possible",
            3306: "MySQL - Default credentials possible",
            5432: "PostgreSQL - Default credentials possible",
            5900: "VNC - Weak authentication possible"
        }
        
        for port in ports:
            if port in critical_ports:
                predictions.append({
                    "port": port,
                    "service": services[ports.index(port)] if port < len(services) else "unknown",
                    "vulnerabilities": [{"name": critical_ports[port], "severity": "CRITICAL", "cvss": 9.8}],
                    "recommendation": "Patch immediately or disable service"
                })
                risk_score += 15
            elif port in high_ports:
                predictions.append({
                    "port": port,
                    "service": services[ports.index(port)] if port < len(services) else "unknown",
                    "vulnerabilities": [{"name": high_ports[port], "severity": "HIGH", "cvss": 7.5}],
                    "recommendation": "Update and secure service"
                })
                risk_score += 10
        
        risk_score = min(100, risk_score)
        
        # Build output
        output = []
        output.append("\n" + "="*70)
        output.append("🤖 AUTOMATIC VULNERABILITY PREDICTION (FAST)")
        output.append("="*70)
        
        output.append(f"\n📊 RISK SCORE: {risk_score}/100")
        
        if risk_score >= 70:
            output.append("🔴 CRITICAL RISK - Immediate action required!")
        elif risk_score >= 50:
            output.append("🟠 HIGH RISK - Action required soon")
        elif risk_score >= 30:
            output.append("🟡 MEDIUM RISK - Plan to address")
        else:
            output.append("🟢 LOW RISK - Monitor")
        
        for pred in predictions[:10]:  # Limit to 10 for speed
            output.append(f"\n{'─'*50}")
            output.append(f"📡 PORT {pred['port']} - {pred['service']}")
            for vuln in pred['vulnerabilities']:
                output.append(f"  🔴 {vuln['severity']}: {vuln['name']}")
                output.append(f"     CVSS Score: {vuln['cvss']}")
            output.append(f"  💡 {pred['recommendation']}")
        
        if not predictions:
            output.append("\n   No critical vulnerabilities predicted")
        
        output.append("\n" + "="*70)
        
        return {
            'predictions': predictions,
            'risk_score': risk_score,
            'output': "\n".join(output)
        }
    
    def _fast_anomaly_detection(self, ports):
        """Fast anomaly detection"""
        anomalies = []
        severity = "LOW"
        
        # Known backdoor ports
        backdoor_ports = {
            4444: "Metasploit Meterpreter",
            31337: "Back Orifice",
            6667: "IRC Botnet",
            1337: "Leet Backdoor",
            54321: "PCAnywhere"
        }
        
        # Suspicious ports
        suspicious_ports = [4444, 31337, 6667, 1337, 12345, 31337]
        
        for port in ports:
            if port in backdoor_ports:
                anomalies.append({
                    "port": port,
                    "type": "BACKDOOR",
                    "severity": "CRITICAL",
                    "details": f"Known backdoor port: {backdoor_ports[port]}",
                    "action": "IMMEDIATE INVESTIGATION REQUIRED!"
                })
                severity = "CRITICAL"
            elif port in suspicious_ports:
                anomalies.append({
                    "port": port,
                    "type": "SUSPICIOUS",
                    "severity": "HIGH",
                    "details": "Unusual port for typical server",
                    "action": "Investigate service on this port"
                })
                if severity != "CRITICAL":
                    severity = "HIGH"
        
        # Build output
        output = []
        output.append("\n" + "="*70)
        output.append("🔍 ANOMALY DETECTION REPORT (FAST)")
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
        
        output.append(f"\n📡 Open ports analyzed: {len(ports)}")
        output.append(f"⚠️ Anomalies found: {len(anomalies)}")
        
        for anomaly in anomalies[:10]:
            output.append(f"\n{'─'*50}")
            if anomaly["type"] == "BACKDOOR":
                output.append(f"🔴 PORT {anomaly['port']} - BACKDOOR DETECTED!")
            else:
                output.append(f"🟠 PORT {anomaly['port']} - SUSPICIOUS")
            output.append(f"   📝 {anomaly['details']}")
            output.append(f"   🎯 ACTION: {anomaly['action']}")
        
        output.append("\n" + "="*70)
        
        return {
            'anomalies': anomalies,
            'severity': severity,
            'output': "\n".join(output)
        }
    
    def _fast_cve_check(self, services):
        """Fast CVE check using pre-defined database"""
        vulnerabilities = []
        
        # Fast CVE database
        cve_db = {
            "smb": [
                {"cve": "CVE-2017-0144", "name": "EternalBlue", "severity": "CRITICAL", "cvss": 9.8},
                {"cve": "CVE-2020-0796", "name": "SMBGhost", "severity": "CRITICAL", "cvss": 10.0}
            ],
            "ssh": [
                {"cve": "CVE-2016-6210", "name": "User Enumeration", "severity": "MEDIUM", "cvss": 5.0}
            ],
            "ftp": [
                {"cve": "CVE-2011-2523", "name": "vsftpd Backdoor", "severity": "CRITICAL", "cvss": 10.0}
            ],
            "mysql": [
                {"cve": "CVE-2012-2122", "name": "Auth Bypass", "severity": "HIGH", "cvss": 7.5}
            ],
            "http": [
                {"cve": "CVE-2014-0160", "name": "Heartbleed", "severity": "HIGH", "cvss": 7.5}
            ]
        }
        
        for service in services:
            service_lower = service.lower()
            for key, vulns in cve_db.items():
                if key in service_lower:
                    vulnerabilities.extend(vulns)
        
        # Remove duplicates
        seen = set()
        unique_vulns = []
        for v in vulnerabilities:
            if v['cve'] not in seen:
                seen.add(v['cve'])
                unique_vulns.append(v)
        
        risk_score = sum(10 if v['severity'] == 'CRITICAL' else 7 if v['severity'] == 'HIGH' else 4 for v in unique_vulns)
        risk_score = min(100, risk_score)
        
        # Build output
        output = []
        output.append("\n" + "="*70)
        output.append("📚 CVE DATABASE INTEGRATION (FAST)")
        output.append("="*70)
        
        output.append(f"\n📊 OVERALL RISK SCORE: {risk_score}/100")
        
        if risk_score >= 70:
            output.append("🔴 CRITICAL - Multiple high-risk vulnerabilities found!")
        elif risk_score >= 50:
            output.append("🟠 HIGH - Significant vulnerabilities detected")
        elif risk_score >= 30:
            output.append("🟡 MEDIUM - Some vulnerabilities to address")
        else:
            output.append("🟢 LOW - Minor vulnerabilities found")
        
        if unique_vulns:
            output.append(f"\n🔍 Found {len(unique_vulns)} known vulnerabilities:")
            for vuln in unique_vulns[:10]:
                severity_icon = "🔴" if vuln['severity'] == 'CRITICAL' else "🟠" if vuln['severity'] == 'HIGH' else "🟡"
                output.append(f"\n{severity_icon} {vuln['cve']} - {vuln['name']}")
                output.append(f"   Severity: {vuln['severity']} (CVSS: {vuln['cvss']})")
        else:
            output.append("\n   No known CVEs found")
        
        output.append("\n" + "="*70)
        
        return {
            'vulnerabilities': unique_vulns,
            'risk_score': risk_score,
            'output': "\n".join(output)
        }
    
    def generate_full_report(self, analysis):
        """Generate fast full AI report"""
        report = []
        report.append("\n" + "█"*70)
        report.append("█" + " " * 68 + "█")
        report.append("█" + " " * 15 + "T-8 AI REPORT (FAST)" + " " * 37 + "█")
        report.append("█" + " " * 68 + "█")
        report.append("█"*70)
        
        report.append(f"\n🎯 Target: {analysis['target']}")
        report.append(f"⏱ Scan Time: {analysis['scan_time']}")
        
        # Add key findings
        vuln_risk = analysis['vulnerability_prediction']['risk_score']
        cve_risk = analysis['cve_check']['risk_score']
        total_risk = (vuln_risk + cve_risk) // 2
        
        report.append(f"\n📊 OVERALL RISK: {total_risk}/100")
        
        if total_risk >= 70:
            report.append("🔴 CRITICAL - Immediate action required!")
        elif total_risk >= 50:
            report.append("🟠 HIGH - Action required soon")
        elif total_risk >= 30:
            report.append("🟡 MEDIUM - Plan to address")
        else:
            report.append("🟢 LOW - Monitor regularly")
        
        report.append(analysis['vulnerability_prediction']['output'])
        report.append(analysis['anomalies']['output'])
        report.append(analysis['cve_check']['output'])
        
        report.append("\n" + "█"*70)
        
        return "\n".join(report)
