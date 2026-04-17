#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report Summarization
Long scan outputs को छोटा और समझने योग्य बनाता है
"""

import re
from datetime import datetime

class ReportSummarizer:
    def __init__(self):
        self.summary = {}
        
    def summarize(self, scan_output, target, scan_time):
        """Summarize scan output"""
        summary = {
            "target": target,
            "scan_time": scan_time,
            "total_hosts": 0,
            "hosts_up": 0,
            "open_ports": [],
            "services": [],
            "critical_findings": [],
            "high_findings": [],
            "recommendations": []
        }
        
        # Parse host information
        host_matches = re.findall(r'Nmap scan report for (.+?)\n', scan_output)
        summary["total_hosts"] = len(host_matches)
        summary["hosts_up"] = len(re.findall(r'Host is up', scan_output))
        
        # Parse open ports
        port_matches = re.findall(r'(\d+)/tcp\s+open\s+(\w+)', scan_output)
        for port, service in port_matches:
            summary["open_ports"].append({"port": port, "service": service})
            if service not in summary["services"]:
                summary["services"].append(service)
        
        # Identify critical findings
        critical_ports = [445, 3389, 23, 21, 513, 514, 512, 1524]
        for port_info in summary["open_ports"]:
            if int(port_info["port"]) in critical_ports:
                summary["critical_findings"].append(port_info)
            elif int(port_info["port"]) in [22, 3306, 5432, 5900]:
                summary["high_findings"].append(port_info)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary)
        summary["recommendations"] = recommendations
        
        self.summary = summary
        return summary
    
    def _generate_recommendations(self, summary):
        """Generate recommendations based on findings"""
        recommendations = []
        
        for port in summary["critical_findings"]:
            if port["port"] == "445":
                recommendations.append("🔴 CRITICAL: Disable SMBv1 and patch against EternalBlue")
            elif port["port"] == "3389":
                recommendations.append("🔴 CRITICAL: Patch RDP against BlueKeep (CVE-2019-0708)")
            elif port["port"] == "23":
                recommendations.append("🔴 CRITICAL: Disable Telnet - Use SSH instead")
            elif port["port"] == "21":
                recommendations.append("🟠 HIGH: Disable anonymous FTP access")
            elif port["port"] == "1524":
                recommendations.append("🔴 CRITICAL: ingreslock backdoor detected!")
        
        for port in summary["high_findings"]:
            if port["port"] == "22":
                recommendations.append("🟡 MEDIUM: Update SSH and disable root login")
            elif port["port"] == "3306":
                recommendations.append("🟡 MEDIUM: Change MySQL default root password")
            elif port["port"] == "5900":
                recommendations.append("🟡 MEDIUM: Secure VNC with strong password")
        
        if not recommendations:
            recommendations.append("✅ No immediate security concerns detected")
        
        return recommendations
    
    def generate_executive_summary(self):
        """Generate executive-friendly summary"""
        exec_summary = []
        exec_summary.append("\n" + "="*70)
        exec_summary.append("📊 EXECUTIVE SUMMARY")
        exec_summary.append("="*70)
        
        exec_summary.append(f"\n🎯 Target: {self.summary['target']}")
        exec_summary.append(f"⏱ Scan Time: {self.summary['scan_time']}")
        exec_summary.append(f"📡 Hosts Found: {self.summary['hosts_up']}/{self.summary['total_hosts']}")
        exec_summary.append(f"🔌 Open Ports: {len(self.summary['open_ports'])}")
        exec_summary.append(f"🛠 Services: {', '.join(self.summary['services'][:10])}")
        
        exec_summary.append(f"\n{'─'*50}")
        exec_summary.append("⚠️ CRITICAL FINDINGS:")
        
        if self.summary['critical_findings']:
            for finding in self.summary['critical_findings']:
                exec_summary.append(f"  🔴 Port {finding['port']} - {finding['service']}")
        else:
            exec_summary.append("  ✅ No critical findings")
        
        exec_summary.append(f"\n{'─'*50}")
        exec_summary.append("📋 RECOMMENDATIONS:")
        
        for rec in self.summary['recommendations']:
            exec_summary.append(f"  {rec}")
        
        exec_summary.append("\n" + "="*70)
        return "\n".join(exec_summary)
    
    def generate_technical_summary(self):
        """Generate detailed technical summary"""
        tech_summary = []
        tech_summary.append("\n" + "="*70)
        tech_summary.append("🔧 TECHNICAL DETAILS")
        tech_summary.append("="*70)
        
        tech_summary.append(f"\n📡 Open Ports Details:")
        for port in self.summary['open_ports']:
            tech_summary.append(f"  • {port['port']}/tcp - {port['service']}")
        
        if self.summary['critical_findings']:
            tech_summary.append(f"\n{'─'*50}")
            tech_summary.append("🔴 CRITICAL VULNERABILITIES:")
            for finding in self.summary['critical_findings']:
                tech_summary.append(f"  • Port {finding['port']} ({finding['service']}) - Requires immediate action")
        
        tech_summary.append("\n" + "="*70)
        return "\n".join(tech_summary)
    
    def format_output(self, summary_type="executive"):
        """Format summary output"""
        if summary_type == "executive":
            return self.generate_executive_summary()
        elif summary_type == "technical":
            return self.generate_technical_summary()
        else:
            return self.generate_executive_summary()
