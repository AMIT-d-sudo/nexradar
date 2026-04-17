import random
import re

class AIAssistant:
    def __init__(self):
        self.scan_patterns = {
            'web_server': ['80', '443', '8080', '8443'],
            'database': ['3306', '5432', '27017', '6379'],
            'ssh': ['22'],
            'ftp': ['21'],
            'smtp': ['25', '587', '465'],
            'dns': ['53'],
            'windows': ['135', '139', '445', '3389']
        }
        
        self.recommendations = {
            'quick': ['-F', '-T4', '--max-retries 2', '--min-rate 100'],
            'stealth': ['-T2', '-f', '-D RND:10', '--max-retries 1', '--scan-delay 1s'],
            'full': ['-p-', '-sS', '-sV', '-O', '-A', '-T4'],
            'vulnerability': ['-sV', '--script=vuln', '-T4'],
            'os_detection': ['-O', '--osscan-guess', '-sV']
        }
        
    def get_recommendation(self, target, ports, selected_cmds):
        """Get AI recommendation based on target and selected options"""
        recommendation = []
        recommendation.append("🤖 AI SCAN ANALYSIS\n")
        recommendation.append("="*50 + "\n\n")
        
        # Analyze target
        if target:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
                recommendation.append(f"📡 Target: {target} (IPv4 Address)\n")
            elif ':' in target:
                recommendation.append(f"📡 Target: {target} (IPv6 Address)\n")
            else:
                recommendation.append(f"📡 Target: {target} (Domain Name)\n")
        else:
            recommendation.append("⚠ No target specified. Using scanme.nmap.org\n")
            
        # Port analysis
        if ports:
            recommendation.append(f"\n🔌 Ports specified: {ports}\n")
            if '-' in ports:
                start, end = ports.split('-')
                total_ports = int(end) - int(start) + 1
                recommendation.append(f"   → Scanning {total_ports} ports\n")
                if total_ports > 10000:
                    recommendation.append("   ⚠ Large port range detected. Consider using -T4 for speed\n")
        else:
            recommendation.append("\n⚠ No ports specified. Scanning default ports (1-1000)\n")
            
        # Command analysis
        if selected_cmds:
            recommendation.append(f"\n📋 Selected options: {len(selected_cmds)}\n")
            if '-sS' in selected_cmds:
                recommendation.append("   ✓ SYN scan selected (fast & stealthy)\n")
            if '-sV' in selected_cmds:
                recommendation.append("   ✓ Version detection enabled\n")
            if '-O' in selected_cmds:
                recommendation.append("   ✓ OS detection enabled\n")
            if '-A' in selected_cmds:
                recommendation.append("   ✓ Aggressive scan enabled\n")
                
        # Recommendations
        recommendation.append("\n💡 AI RECOMMENDATIONS:\n")
        recommendation.append("-"*40 + "\n")
        
        if not ports:
            recommendation.append("→ Use -F for fast scan (top 100 ports)\n")
            recommendation.append("→ Use -p- for full port scan (all 65535 ports)\n")
            
        if not selected_cmds:
            recommendation.append("→ Try: -sS -sV -O for comprehensive scan\n")
            recommendation.append("→ Try: -T4 for faster scanning\n")
            
        # Scenario-based recommendations
        if ports == '22' or '22' in ports if isinstance(ports, str) else False:
            recommendation.append("\n🎯 SSH detected! Recommendations:\n")
            recommendation.append("   → Use --script=ssh-* for SSH enumeration\n")
            recommendation.append("   → Try: -sV --script=ssh2-enum-algos\n")
            
        if ports and ('80' in ports or '443' in ports):
            recommendation.append("\n🌐 Web ports detected! Recommendations:\n")
            recommendation.append("   → Use --script=http-* for web enumeration\n")
            recommendation.append("   → Try: --script=http-title,http-headers\n")
            
        # Performance recommendations
        recommendation.append("\n⚡ Performance Tips:\n")
        recommendation.append("   • Use -T4 for fast networks\n")
        recommendation.append("   • Use --min-rate 100 for faster scanning\n")
        recommendation.append("   • Use --max-retries 1 to reduce time\n")
        
        # Stealth recommendations
        recommendation.append("\n🛡 Stealth Recommendations:\n")
        recommendation.append("   • Use -T1 or -T2 for IDS evasion\n")
        recommendation.append("   • Use -f for packet fragmentation\n")
        recommendation.append("   • Use -D RND:10 for decoy scans\n")
        
        return ''.join(recommendation)
        
    def analyze_output(self, output):
        """Analyze scan output and provide insights"""
        analysis = []
        analysis.append("📊 AI OUTPUT ANALYSIS\n")
        analysis.append("="*40 + "\n\n")
        
        # Check for open ports
        open_ports = re.findall(r'(\d+)/tcp\s+open', output)
        if open_ports:
            analysis.append(f"✓ Found {len(open_ports)} open ports\n")
            analysis.append(f"  Open ports: {', '.join(open_ports[:10])}\n")
            
            # Service detection
            services = re.findall(r'(\d+)/tcp\s+open\s+(\w+)', output)
            if services:
                analysis.append("\n📡 Detected Services:\n")
                for port, service in services[:5]:
                    analysis.append(f"  • Port {port}: {service}\n")
                    
        # Check for OS detection
        os_match = re.search(r'OS guess:\s+(.+?)(?:\n|$)', output)
        if os_match:
            analysis.append(f"\n💻 OS Detection: {os_match.group(1)}\n")
            
        # Check for vulnerabilities
        if 'VULNERABLE' in output or 'CVE-' in output:
            analysis.append("\n⚠ POTENTIAL VULNERABILITIES DETECTED!\n")
            vulns = re.findall(r'CVE-\d{4}-\d{4,}', output)
            if vulns:
                analysis.append(f"  CVEs found: {', '.join(set(vulns[:5]))}\n")
                
        # Performance analysis
        scan_time = re.search(r'Nmap done:.*?(\d+\.\d+) seconds', output)
        if scan_time:
            analysis.append(f"\n⏱ Scan completed in {scan_time.group(1)} seconds\n")
            
        if not open_ports:
            analysis.append("\n⚠ No open ports found!\n")
            analysis.append("  Suggestions:\n")
            analysis.append("  • Check if firewall is blocking\n")
            analysis.append("  • Try different scan techniques (-sS, -sT, -sU)\n")
            analysis.append("  • Increase timing template (-T4)\n")
            
        return ''.join(analysis)
