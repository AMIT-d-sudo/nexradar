#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ScriptScan:
    def __init__(self):
        self.commands = {
            # Basic Script Options
            "-sC": "Equivalent to --script=default (safe default scripts)",
            "--script": "Run specific Lua scripts (e.g., default, vuln, http-title)",
            "--script-args": "Arguments for scripts (n1=v1,n2=v2)",
            "--script-args-file": "Load script arguments from file",
            "--script-trace": "Show all data sent/received by scripts",
            "--script-updatedb": "Update script database from online repository",
            
            # Web/HTTP Scripts
            "--script=http-brute": "Brute force HTTP authentication",
            "--script=http-title": "Get webpage title",
            "--script=http-enum": "Enumerate web directories and files",
            "--script=http-headers": "Get HTTP headers",
            "--script=http-methods": "Test HTTP methods (GET, POST, etc.)",
            "--script=http-shellshock": "Test for Shellshock vulnerability",
            "--script=http-sql-injection": "Test for SQL injection",
            "--script=http-xss": "Test for Cross-Site Scripting",
            "--script=http-wordpress-enum": "Enumerate WordPress installation",
            
            # Vulnerability Scripts
            "--script=vuln": "Run vulnerability detection scripts",
            "--script=vulners": "Check vulnerabilities in Vulners database",
            "--script=exploit": "Run exploit scripts",
            "--script=malware": "Scan for malware",
            
            # Category Scripts
            "--script=default": "Run default script category (safe scripts)",
            "--script=safe": "Run safe (non-intrusive) scripts",
            "--script=discovery": "Run host/service discovery scripts",
            "--script=auth": "Run authentication bypass scripts",
            "--script=brute": "Run brute force password scripts",
            "--script=dos": "Run denial of service scripts",
            "--script=fuzzer": "Run fuzzing scripts",
            "--script=version": "Advanced version detection",
            "--script=intrusive": "Run intrusive (potentially dangerous) scripts",
            
            # SMB/Windows Scripts
            "--script=smb-enum-shares": "Enumerate SMB shares",
            "--script=smb-os-discovery": "Discover SMB OS information",
            "--script=smb-security-mode": "Check SMB security mode",
            "--script=smb-vuln-ms17-010": "Check for EternalBlue vulnerability",
            "--script=smb-brute": "Brute force SMB passwords",
            
            # SSH Scripts
            "--script=ssh-auth-methods": "List SSH authentication methods",
            "--script=ssh-hostkey": "Show SSH host keys",
            "--script=ssh-brute": "Brute force SSH passwords",
            "--script=ssh2-enum-algos": "Enumerate SSH2 algorithms",
            
            # Database Scripts
            "--script=mysql-info": "Get MySQL information",
            "--script=mysql-brute": "Brute force MySQL passwords",
            "--script=mysql-empty-password": "Check for empty MySQL password",
            "--script=mysql-databases": "List MySQL databases",
            "--script=mysql-query": "Run SQL query on MySQL",
            "--script=mysql-users": "List MySQL users",
            
            "--script=pgsql-brute": "Brute force PostgreSQL passwords",
            "--script=redis-info": "Get Redis information",
            "--script=mongodb-info": "Get MongoDB information",
            
            # FTP Scripts
            "--script=ftp-anon": "Check for anonymous FTP access",
            "--script=ftp-brute": "Brute force FTP passwords",
            "--script=ftp-syst": "Get FTP system information",
            "--script=ftp-vsftpd-backdoor": "Check for vsftpd backdoor",
            
            # SNMP Scripts
            "--script=snmp-info": "Get SNMP information",
            "--script=snmp-brute": "Brute force SNMP community strings",
            "--script=snmp-win32-services": "Enumerate Windows services via SNMP",
            "--script=snmp-interfaces": "Enumerate network interfaces",
            
            # DNS Scripts
            "--script=dns-brute": "Brute force DNS subdomains",
            "--script=dns-zone-transfer": "Test for DNS zone transfer",
            "--script=dns-recursion": "Check for DNS recursion",
            "--script=dns-nsid": "Get DNS nameserver ID",
            
            # SSL/TLS Scripts
            "--script=ssl-heartbleed": "Check for Heartbleed vulnerability",
            "--script=ssl-cert": "Get SSL certificate information",
            "--script=ssl-enum-ciphers": "Enumerate SSL ciphers",
            "--script=ssl-poodle": "Check for POODLE vulnerability",
            "--script=ssl-ccs-injection": "Check for CCS injection",
            
            # Telnet Scripts
            "--script=telnet-brute": "Brute force Telnet passwords",
            "--script=telnet-encryption": "Check Telnet encryption",
            
            # RDP Scripts
            "--script=rdp-brute": "Brute force RDP passwords",
            "--script=rdp-ntlm-info": "Get RDP NTLM information",
            "--script=rdp-vuln-ms12-020": "Check for MS12-020 vulnerability",
            
            # NFS Scripts
            "--script=nfs-showmount": "Show NFS exports",
            "--script=nfs-ls": "List NFS directory contents",
            "--script=nfs-statfs": "Get NFS filesystem statistics",
            
            # UPnP Scripts
            "--script=upnp-info": "Get UPnP information",
            "--script=upnp-msearch": "Search for UPnP devices",
            
            # Other Scripts
            "--script=broadcast-dhcp-discover": "Discover DHCP servers",
            "--script=broadcast-ping": "Discover hosts via broadcast ping",
            "--script=whois-domain": "Perform WHOIS lookup",
            "--script=asn-query": "Query ASN information"
        }
        
    def get_commands(self):
        return self.commands
        
    def get_command_help(self, command):
        help_texts = {
            "-sC": "Run default set of safe scripts (equivalent to --script=default)",
            "--script": "Run specific scripts. Examples:\n   --script default\n   --script vuln\n   --script http-title\n   --script ssh-*",
            "--script-args": "Pass arguments to scripts. Example: userdb=users.txt,passdb=pass.txt",
            "--script-args-file": "Load script arguments from a file (one argument per line)",
            "--script-trace": "Trace script execution for debugging purposes",
            "--script-updatedb": "Update the Nmap script database from online repository",
            "--script=http-brute": "Brute force HTTP login pages (requires userdb/passdb)",
            "--script=http-title": "Extract webpage title from HTTP services",
            "--script=vuln": "Check for known vulnerabilities (CVEs)",
            "--script=http-enum": "Enumerate web directories and files",
            "--script=smb-enum-shares": "List available SMB shares",
            "--script=ftp-anon": "Check if anonymous FTP login is allowed",
            "--script=ssl-heartbleed": "Test for the Heartbleed vulnerability (CVE-2014-0160)",
            "--script=smb-vuln-ms17-010": "Test for EternalBlue vulnerability (CVE-2017-0144)",
            "--script=dns-brute": "Brute force subdomains using a wordlist"
        }
        return help_texts.get(command, self.commands.get(command, "No help available"))
