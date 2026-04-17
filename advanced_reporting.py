#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Reporting Module
PDF/HTML/CSV/JSON/XML reports generation
Executive summaries, comparison reports, timeline views
"""

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re

class AdvancedReporting:
    def __init__(self):
        self.report_history = []
        
    def generate_html_report(self, scan_data, filename="scan_report.html"):
        """Generate HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NINJA SCAN AI - Security Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #00ff41;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #0d0d0d;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0,255,65,0.2);
        }}
        .header {{
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #00ff41;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #00ff41;
            text-shadow: 0 0 10px #00ff41;
        }}
        .risk-critical {{ background: #8b0000; color: white; padding: 10px; border-radius: 5px; }}
        .risk-high {{ background: #cc5500; color: white; padding: 10px; border-radius: 5px; }}
        .risk-medium {{ background: #886600; color: white; padding: 10px; border-radius: 5px; }}
        .risk-low {{ background: #006400; color: white; padding: 10px; border-radius: 5px; }}
        .port-card {{
            background: #1a1a1a;
            border-left: 4px solid #00ff41;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .vulnerability {{ margin: 5px 0; padding-left: 20px; }}
        .critical {{ color: #ff4444; }}
        .high {{ color: #ff8844; }}
        .medium {{ color: #ffcc44; }}
        .low {{ color: #44ff44; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #00ff41;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background: #00ff41;
            color: #0a0a0a;
        }}
        .summary-box {{
            background: #1a1a1a;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            border-top: 1px solid #00ff41;
            margin-top: 20px;
            font-size: 0.8em;
        }}
        button {{
            background: #00ff41;
            color: #0a0a0a;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            border-radius: 5px;
            font-weight: bold;
        }}
        button:hover {{
            background: #00cc33;
        }}
        .chart {{
            background: #1a1a1a;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .progress-bar {{
            background: #333;
            border-radius: 10px;
            overflow: hidden;
            margin: 5px 0;
        }}
        .progress-fill {{
            background: #00ff41;
            height: 20px;
            text-align: center;
            color: #0a0a0a;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 NINJA SCAN AI</h1>
            <h2>Advanced Security Assessment Report</h2>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Target: {scan_data.get('target', 'Unknown')}</p>
        </div>
        
        <div class="summary-box">
            <h3>📊 Executive Summary</h3>
            {self._generate_executive_summary_html(scan_data)}
        </div>
        
        <div class="summary-box">
            <h3>🎯 Risk Assessment</h3>
            {self._generate_risk_chart_html(scan_data)}
        </div>
        
        <div class="summary-box">
            <h3>🔓 Open Ports & Vulnerabilities</h3>
            {self._generate_ports_table_html(scan_data)}
        </div>
        
        <div class="summary-box">
            <h3>📋 Recommendations</h3>
            {self._generate_recommendations_html(scan_data)}
        </div>
        
        <div class="footer">
            <p>NINJA SCAN AI v5.0 - Professional Security Assessment Tool</p>
            <p>This report is generated automatically by AI-powered scanning engine</p>
        </div>
    </div>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def _generate_executive_summary_html(self, scan_data):
        """Generate executive summary for HTML"""
        risk_score = scan_data.get('risk_score', 0)
        if risk_score >= 70:
            risk_class = "risk-critical"
            risk_text = "CRITICAL RISK - Immediate Action Required"
        elif risk_score >= 50:
            risk_class = "risk-high"
            risk_text = "HIGH RISK - Action Required Soon"
        elif risk_score >= 30:
            risk_class = "risk-medium"
            risk_text = "MEDIUM RISK - Plan to Address"
        else:
            risk_class = "risk-low"
            risk_text = "LOW RISK - Monitor Regularly"
        
        return f"""
        <div class="{risk_class}">
            <strong>Overall Risk Level: {risk_text}</strong><br>
            Risk Score: {risk_score}/100<br>
            Open Ports: {len(scan_data.get('open_ports', []))}<br>
            Critical Vulnerabilities: {scan_data.get('critical_count', 0)}<br>
            Scan Duration: {scan_data.get('scan_time', 'Unknown')}
        </div>
        """
    
    def _generate_risk_chart_html(self, scan_data):
        """Generate risk chart for HTML"""
        critical = scan_data.get('critical_count', 0)
        high = scan_data.get('high_count', 0)
        medium = scan_data.get('medium_count', 0)
        low = scan_data.get('low_count', 0)
        total = critical + high + medium + low
        if total == 0:
            total = 1
        
        return f"""
        <div class="chart">
            <h4>Vulnerability Distribution</h4>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(critical/total)*100}%; background: #ff0000;">
                    Critical: {critical}
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(high/total)*100}%; background: #ff6600;">
                    High: {high}
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(medium/total)*100}%; background: #ffcc00;">
                    Medium: {medium}
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(low/total)*100}%; background: #00ff00;">
                    Low: {low}
                </div>
            </div>
        </div>
        """
    
    def _generate_ports_table_html(self, scan_data):
        """Generate ports table for HTML"""
        html = '<table><tr><th>Port</th><th>Service</th><th>Vulnerabilities</th><th>Risk</th></tr>'
        for port in scan_data.get('open_ports', []):
            vulns = port.get('vulnerabilities', [])
            vuln_text = '<br>'.join([f"{v.get('severity', '')}: {v.get('name', '')}" for v in vulns[:3]])
            risk_class = "critical" if any(v.get('severity') == 'CRITICAL' for v in vulns) else "high" if any(v.get('severity') == 'HIGH' for v in vulns) else "medium" if vulns else "low"
            html += f'<tr><td>{port.get("port", "")}</td><td>{port.get("service", "")}</td><td>{vuln_text}</td><td class="{risk_class}">{risk_class.upper()}</td></tr>'
        html += '</table>'
        return html
    
    def _generate_recommendations_html(self, scan_data):
        """Generate recommendations for HTML"""
        recs = scan_data.get('recommendations', [])
        if not recs:
            return "<p>No specific recommendations at this time.</p>"
        html = "<ul>"
        for rec in recs:
            html += f"<li>{rec}</li>"
        html += "</ul>"
        return html
    
    def generate_csv_report(self, scan_data, filename="scan_report.csv"):
        """Generate CSV report"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Port', 'Service', 'Vulnerability', 'Severity', 'CVSS', 'CVE', 'Fix'])
            for port in scan_data.get('open_ports', []):
                for vuln in port.get('vulnerabilities', []):
                    writer.writerow([
                        port.get('port', ''),
                        port.get('service', ''),
                        vuln.get('name', ''),
                        vuln.get('severity', ''),
                        vuln.get('cvss', ''),
                        vuln.get('cve', ''),
                        vuln.get('fix', '')
                    ])
        return filename
    
    def generate_json_report(self, scan_data, filename="scan_report.json"):
        """Generate JSON report"""
        with open(filename, 'w') as f:
            json.dump(scan_data, f, indent=4)
        return filename
    
    def generate_xml_report(self, scan_data, filename="scan_report.xml"):
        """Generate XML report"""
        root = ET.Element("scan_report")
        root.set("timestamp", datetime.now().isoformat())
        root.set("target", scan_data.get('target', 'Unknown'))
        
        summary = ET.SubElement(root, "summary")
        ET.SubElement(summary, "risk_score").text = str(scan_data.get('risk_score', 0))
        ET.SubElement(summary, "total_ports").text = str(len(scan_data.get('open_ports', [])))
        
        ports_elem = ET.SubElement(root, "open_ports")
        for port in scan_data.get('open_ports', []):
            port_elem = ET.SubElement(ports_elem, "port")
            ET.SubElement(port_elem, "number").text = str(port.get('port', ''))
            ET.SubElement(port_elem, "service").text = port.get('service', '')
            vulns_elem = ET.SubElement(port_elem, "vulnerabilities")
            for vuln in port.get('vulnerabilities', []):
                vuln_elem = ET.SubElement(vulns_elem, "vulnerability")
                ET.SubElement(vuln_elem, "name").text = vuln.get('name', '')
                ET.SubElement(vuln_elem, "severity").text = vuln.get('severity', '')
                ET.SubElement(vuln_elem, "cve").text = vuln.get('cve', '')
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        return filename
    
    def generate_executive_summary(self, scan_data):
        """Generate simple executive summary (non-technical)"""
        risk_score = scan_data.get('risk_score', 0)
        
        if risk_score >= 70:
            risk_level = "🔴 CRITICAL"
            action = "IMMEDIATE action required!"
        elif risk_score >= 50:
            risk_level = "🟠 HIGH"
            action = "Action required soon"
        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM"
            action = "Plan to address"
        else:
            risk_level = "🟢 LOW"
            action = "Monitor regularly"
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    EXECUTIVE SECURITY SUMMARY                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Target: {scan_data.get('target', 'Unknown')}
║  Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║                                                                  ║
║  📊 RISK ASSESSMENT:                                             ║
║     Overall Risk Level: {risk_level}
║     Risk Score: {risk_score}/100
║     Status: {action}
║                                                                  ║
║  🔍 KEY FINDINGS:                                                ║
║     • Open Ports Found: {len(scan_data.get('open_ports', []))}
║     • Critical Issues: {scan_data.get('critical_count', 0)}
║     • High Risk Issues: {scan_data.get('high_count', 0)}
║                                                                  ║
║  ⚠️ TOP 3 RISKS:                                                 ║
"""
        for i, risk in enumerate(scan_data.get('top_risks', [])[:3], 1):
            summary += f"║     {i}. {risk}\n"
        
        summary += f"""
║                                                                  ║
║  ✅ RECOMMENDATIONS:                                             ║
"""
        for rec in scan_data.get('recommendations', [])[:5]:
            summary += f"║     • {rec[:50]}\n"
        
        summary += """
║                                                                  ║
║  📞 CONTACT: IT Security Team for detailed report               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return summary
    
    def generate_comparison_report(self, before_scan, after_scan, filename="comparison_report.html"):
        """Generate before/after comparison report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Comparison Report - NINJA SCAN AI</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: #0d0d0d; padding: 20px; }}
        .good {{ color: #00ff00; }}
        .bad {{ color: #ff4444; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #00ff41; padding: 8px; text-align: left; }}
        th {{ background: #00ff41; color: #0a0a0a; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Security Comparison Report</h1>
        <p>Before vs After Security Assessment</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Risk Score Comparison</h2>
        <table>
            <tr><th>Metric</th><th>Before</th><th>After</th><th>Change</th></tr>
            <tr>
                <td>Risk Score</td>
                <td>{before_scan.get('risk_score', 0)}</td>
                <td>{after_scan.get('risk_score', 0)}</td>
                <td class="{'good' if after_scan.get('risk_score', 0) < before_scan.get('risk_score', 0) else 'bad'}">
                    {before_scan.get('risk_score', 0) - after_scan.get('risk_score', 0)} points
                </td>
            </tr>
            <tr>
                <td>Open Ports</td>
                <td>{len(before_scan.get('open_ports', []))}</td>
                <td>{len(after_scan.get('open_ports', []))}</td>
                <td>{len(before_scan.get('open_ports', [])) - len(after_scan.get('open_ports', []))}</td>
            </tr>
            <tr>
                <td>Critical Vulnerabilities</td>
                <td>{before_scan.get('critical_count', 0)}</td>
                <td>{after_scan.get('critical_count', 0)}</td>
                <td>{before_scan.get('critical_count', 0) - after_scan.get('critical_count', 0)}</td>
            </tr>
        </table>
        
        <h2>Improvement Summary</h2>
        <div class="summary-box">
            {self._generate_improvement_summary(before_scan, after_scan)}
        </div>
    </div>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def _generate_improvement_summary(self, before, after):
        """Generate improvement summary for comparison"""
        risk_improvement = before.get('risk_score', 0) - after.get('risk_score', 0)
        if risk_improvement > 0:
            return f"✅ Security improved! Risk reduced by {risk_improvement} points."
        elif risk_improvement < 0:
            return f"⚠️ Security degraded! Risk increased by {abs(risk_improvement)} points."
        else:
            return "ℹ️ No significant change in security posture."
    
    def generate_timeline_view(self, scan_history, filename="timeline_report.html"):
        """Generate timeline view with graphs"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Scan Timeline - NINJA SCAN AI</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: #0d0d0d; padding: 20px; }}
        canvas {{ background: #1a1a1a; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Scan History Timeline</h1>
        <p>Security Trend Analysis</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Risk Score Trend</h2>
        <canvas id="riskChart" width="800" height="400"></canvas>
        
        <h2>Vulnerabilities Over Time</h2>
        <canvas id="vulnChart" width="800" height="400"></canvas>
        
        <h2>Scan History</h2>
        <table>
            <tr><th>Date</th><th>Target</th><th>Risk Score</th><th>Critical</th><th>High</th><th>Medium</th></tr>
"""
        for scan in scan_history[-20:]:  # Last 20 scans
            html_content += f"""
            <tr>
                <td>{scan.get('date', '')}</td>
                <td>{scan.get('target', '')}</td>
                <td>{scan.get('risk_score', 0)}</td>
                <td>{scan.get('critical_count', 0)}</td>
                <td>{scan.get('high_count', 0)}</td>
                <td>{scan.get('medium_count', 0)}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
    
    <script>
        // Risk Score Chart
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        new Chart(riskCtx, {
            type: 'line',
            data: {
                labels: [""" + ','.join([f"'{s.get('date', '')}'" for s in scan_history[-20:]]) + """],
                datasets: [{
                    label: 'Risk Score',
                    data: [""" + ','.join([str(s.get('risk_score', 0)) for s in scan_history[-20:]]) + """],
                    borderColor: '#00ff41',
                    backgroundColor: 'rgba(0, 255, 65, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
        
        // Vulnerabilities Chart
        const vulnCtx = document.getElementById('vulnChart').getContext('2d');
        new Chart(vulnCtx, {
            type: 'bar',
            data: {
                labels: [""" + ','.join([f"'{s.get('date', '')}'" for s in scan_history[-20:]]) + """],
                datasets: [
                    { label: 'Critical', data: [""" + ','.join([str(s.get('critical_count', 0)) for s in scan_history[-20:]]) + """], backgroundColor: '#ff0000' },
                    { label: 'High', data: [""" + ','.join([str(s.get('high_count', 0)) for s in scan_history[-20:]]) + """], backgroundColor: '#ff6600' },
                    { label: 'Medium', data: [""" + ','.join([str(s.get('medium_count', 0)) for s in scan_history[-20:]]) + """], backgroundColor: '#ffcc00' }
                ]
            },
            options: { responsive: true, scales: { y: { beginAtZero: true } } }
        });
    </script>
</body>
</html>
"""
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename
    
    def export_all_formats(self, scan_data, basename="scan_report"):
        """Export to all formats at once"""
        reports = {
            'html': self.generate_html_report(scan_data, f"{basename}.html"),
            'csv': self.generate_csv_report(scan_data, f"{basename}.csv"),
            'json': self.generate_json_report(scan_data, f"{basename}.json"),
            'xml': self.generate_xml_report(scan_data, f"{basename}.xml")
        }
        return reports
