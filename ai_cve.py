#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CVE Database Integration
Known vulnerabilities के लिए automatic check
"""

import json
import re
from datetime import datetime

class CVEDatabase:
    def __init__(self):
        # Built-in CVE database (can be updated from online sources)
        self.cve_database = {
            # SMB/EternalBlue
            "smb": {
                "CVE-2017-0144": {
                    "name": "EternalBlue",
                    "description": "Remote code execution in SMBv1",
                    "severity": "CRITICAL",
                    "cvss": 9.8,
                    "affected_versions": ["SMBv1"],
                    "fix": "Install MS17-010 patch or disable SMBv1"
                },
                "CVE-2020-0796": {
                    "name": "SMBGhost",
                    "description": "SMBv3 compression vulnerability",
                    "severity": "CRITICAL",
                    "cvss": 10.0,
                    "affected_versions": ["Windows 10 v1903", "Server v1903"],
                    "fix": "Install patch or disable SMB compression"
                }
            },
            
            # SSH
            "ssh": {
                "CVE-2016-6210": {
                    "name": "OpenSSH User Enumeration",
                    "description": "Information disclosure via timing attack",
                    "severity": "MEDIUM",
                    "cvss": 5.0,
                    "affected_versions": ["OpenSSH < 7.3"],
                    "fix": "Upgrade to OpenSSH 7.3 or later"
                },
                "CVE-2018-15473": {
                    "name": "SSH User Enumeration",
                    "description": "Username enumeration vulnerability",
                    "severity": "MEDIUM",
                    "cvss": 5.0,
                    "affected_versions": ["OpenSSH < 7.7"],
                    "fix": "Upgrade to OpenSSH 7.7 or later"
                }
            },
            
            # Apache
            "apache": {
                "CVE-2021-41773": {
                    "name": "Apache Path Traversal",
                    "description": "Path traversal and RCE in Apache 2.4.49",
                    "severity": "HIGH",
                    "cvss": 7.5,
                    "affected_versions": ["Apache 2.4.49"],
                    "fix": "Upgrade to Apache 2.4.50"
                },
                "CVE-2017-5638": {
                    "name": "Struts2 RCE",
                    "description": "Remote code execution in Apache Struts2",
                    "severity": "CRITICAL",
                    "cvss": 9.8,
                    "affected_versions": ["Struts 2.3.x", "2.5.x"],
                    "fix": "Upgrade to Struts 2.5.10.1"
                }
            },
            
            # MySQL
            "mysql": {
                "CVE-2012-2122": {
                    "name": "MySQL Authentication Bypass",
                    "description": "Authentication bypass vulnerability",
                    "severity": "HIGH",
                    "cvss": 7.5,
                    "affected_versions": ["MySQL 5.1", "5.5", "5.6"],
                    "fix": "Upgrade to MySQL 5.6.6 or later"
                },
                "CVE-2016-6662": {
                    "name": "MySQL Privilege Escalation",
                    "description": "Privilege escalation via my.cnf",
                    "severity": "HIGH",
                    "cvss": 7.8,
                    "affected_versions": ["MySQL < 5.7.15"],
                    "fix": "Upgrade to MySQL 5.7.15 or later"
                }
            },
            
            # RDP
            "rdp": {
                "CVE-2019-0708": {
                    "name": "BlueKeep",
                    "description": "Remote code execution in RDP",
                    "severity": "CRITICAL",
                    "cvss": 9.8,
                    "affected_versions": ["Windows 7", "Server 2008", "XP"],
                    "fix": "Install security patch KB4499164"
                }
            },
            
            # Heartbleed
            "openssl": {
                "CVE-2014-0160": {
                    "name": "Heartbleed",
                    "description": "Information disclosure in OpenSSL",
                    "severity": "HIGH",
                    "cvss": 7.5,
                    "affected_versions": ["OpenSSL 1.0.1-1.0.1f"],
                    "fix": "Upgrade to OpenSSL 1.0.1g"
                }
            }
        }
    
    def check_vulnerabilities(self, service, version=None):
        """Check for known CVEs for a service"""
        vulnerabilities = []
        
        service_lower = service.lower()
        
        # Find matching service
        for service_key, vulns in self.cve_database.items():
            if service_key in service_lower:
                for cve_id, cve_info in vulns.items():
                    # Check version if provided
                    if version:
                        if self._version_affected(version, cve_info.get("affected_versions", [])):
                            vulnerabilities.append({
                                "cve": cve_id,
                                **cve_info
                            })
                    else:
                        vulnerabilities.append({
                            "cve": cve_id,
                            **cve_info
                        })
        
        return vulnerabilities
    
    def _version_affected(self, version, affected_versions):
        """Check if version is affected by CVE"""
        for affected in affected_versions:
            if affected.lower() in version.lower():
                return True
            if version.lower() in affected.lower():
                return True
        return False
    
    def get_all_vulnerabilities(self, services):
        """Get vulnerabilities for multiple services"""
        all_vulns = []
        
        for service in services:
            vulns = self.check_vulnerabilities(service)
            all_vulns.extend(vulns)
        
        return all_vulns
    
    def calculate_risk_score(self, vulnerabilities):
        """Calculate overall risk score"""
        if not vulnerabilities:
            return 0
        
        total_cvss = 0
        for vuln in vulnerabilities:
            total_cvss += vuln.get("cvss", 0)
        
        avg_cvss = total_cvss / len(vulnerabilities)
        return min(100, int(avg_cvss * 10))
    
    def format_output(self, vulnerabilities, risk_score):
        """Format CVE output"""
        output = []
        output.append("\n" + "="*70)
        output.append("📚 CVE DATABASE INTEGRATION")
        output.append("="*70)
        
        if not vulnerabilities:
            output.append("\n✅ No known CVEs found for detected services")
            output.append("="*70)
            return "\n".join(output)
        
        output.append(f"\n📊 OVERALL RISK SCORE: {risk_score}/100")
        
        if risk_score >= 70:
            output.append("🔴 CRITICAL - Multiple high-risk vulnerabilities found!")
        elif risk_score >= 50:
            output.append("🟠 HIGH - Significant vulnerabilities detected")
        elif risk_score >= 30:
            output.append("🟡 MEDIUM - Some vulnerabilities to address")
        else:
            output.append("🟢 LOW - Minor vulnerabilities found")
        
        output.append(f"\n🔍 Found {len(vulnerabilities)} known vulnerabilities:")
        
        for vuln in vulnerabilities:
            output.append(f"\n{'─'*50}")
            
            # Severity emoji
            severity_emoji = {
                "CRITICAL": "🔴",
                "HIGH": "🟠",
                "MEDIUM": "🟡",
                "LOW": "🟢"
            }.get(vuln["severity"], "⚪")
            
            output.append(f"{severity_emoji} {vuln['cve']} - {vuln['name']}")
            output.append(f"   Severity: {vuln['severity']} (CVSS: {vuln['cvss']})")
            output.append(f"   Description: {vuln['description']}")
            output.append(f"   💡 Fix: {vuln['fix']}")
        
        output.append("\n" + "="*70)
        return "\n".join(output)
