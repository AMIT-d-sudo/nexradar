#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Interface Module
Web-based dashboard, Mobile responsive, Real-time collaboration
Live streaming, Cloud backup
"""

import json
import os
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class WebInterface:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.port = 8080
        self.scan_data = {}
        self.active_users = []
        self.cloud_backup_enabled = False
        
    # ========== 1. WEB-BASED DASHBOARD ==========
    
    def start_web_server(self, port=8080):
        """Start web server for dashboard"""
        self.port = port
        self.is_running = True
        
        handler = self.create_handler()
        self.server = HTTPServer(('0.0.0.0', port), handler)
        
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        return True, f"Web server started at http://localhost:{port}"
    
    def stop_web_server(self):
        """Stop web server"""
        if self.server:
            self.server.shutdown()
            self.is_running = False
            return True, "Web server stopped"
        return False, "Server not running"
    
    def create_handler(self):
        """Create HTTP request handler"""
        
        class DashboardHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress logging
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(self.get_dashboard_html().encode())
                elif self.path == '/api/status':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(self.get_status_json().encode())
                elif self.path == '/api/scans':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(self.get_scans_json().encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def get_dashboard_html(self):
                return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>T-8 Scanner AI - Web Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #00ff41;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #00ff41;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 2em;
            text-shadow: 0 0 10px #00ff41;
        }
        .status-bar {
            background: #1a1a1a;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
        }
        .card {
            background: #1a1a1a;
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .card h3 {
            margin-bottom: 15px;
            color: #ffcc00;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat {
            text-align: center;
            padding: 15px;
            background: #0a0a0a;
            border-radius: 5px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00ff41;
        }
        .stat-label {
            font-size: 0.8em;
            color: #00ccff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #00ff41;
            padding: 8px;
            text-align: left;
        }
        th {
            background: #00ff41;
            color: #0a0a0a;
        }
        .risk-critical { color: #ff3333; }
        .risk-high { color: #ff6600; }
        .risk-medium { color: #ffcc00; }
        .risk-low { color: #00ff41; }
        button {
            background: #0a0a0a;
            color: #00ff41;
            border: 1px solid #00ff41;
            padding: 8px 16px;
            cursor: pointer;
            border-radius: 5px;
            font-family: monospace;
        }
        button:hover {
            background: #00ff41;
            color: #0a0a0a;
        }
        .footer {
            text-align: center;
            padding: 20px;
            border-top: 1px solid #00ff41;
            margin-top: 20px;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .status-bar {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 T-8 Scanner AI</h1>
            <p>Advanced Network Security Scanner</p>
        </div>
        
        <div class="status-bar">
            <span>🟢 System Status: <span id="systemStatus">Online</span></span>
            <span>👥 Active Users: <span id="activeUsers">0</span></span>
            <span>📡 Last Scan: <span id="lastScan">Never</span></span>
        </div>
        
        <div class="grid">
            <div class="stat">
                <div class="stat-value" id="totalScans">0</div>
                <div class="stat-label">Total Scans</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="criticalVulns">0</div>
                <div class="stat-label">Critical Vulnerabilities</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="avgRisk">0</div>
                <div class="stat-label">Average Risk Score</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="hostsFound">0</div>
                <div class="stat-label">Hosts Discovered</div>
            </div>
        </div>
        
        <div class="card">
            <h3>📊 Recent Scans</h3>
            <div style="overflow-x: auto;">
                <table id="scansTable">
                    <thead>
                        <tr><th>Target</th><th>Date</th><th>Risk Score</th><th>Open Ports</th><th>Status</th></tr>
                    </thead>
                    <tbody id="scansBody">
                        <tr><td colspan="5">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="card">
            <h3>🎯 Quick Actions</h3>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button onclick="window.open('/api/scans', '_blank')">📊 Export Data</button>
                <button onclick="location.reload()">🔄 Refresh</button>
            </div>
        </div>
        
        <div class="footer">
            <p>T-8 Scanner AI v1.0 | Web Dashboard | Real-time Monitoring</p>
        </div>
    </div>
    
    <script>
        function fetchData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('totalScans').innerText = data.totalScans || 0;
                    document.getElementById('criticalVulns').innerText = data.criticalVulns || 0;
                    document.getElementById('avgRisk').innerText = data.avgRisk || 0;
                    document.getElementById('hostsFound').innerText = data.hostsFound || 0;
                    document.getElementById('activeUsers').innerText = data.activeUsers || 0;
                    document.getElementById('lastScan').innerText = data.lastScan || 'Never';
                });
            
            fetch('/api/scans')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('scansBody');
                    tbody.innerHTML = '';
                    if (data.scans && data.scans.length > 0) {
                        data.scans.forEach(scan => {
                            const row = tbody.insertRow();
                            row.insertCell(0).innerText = scan.target;
                            row.insertCell(1).innerText = scan.date;
                            row.insertCell(2).innerHTML = `<span class="risk-${scan.riskLevel}">${scan.riskScore}</span>`;
                            row.insertCell(3).innerText = scan.openPorts;
                            row.insertCell(4).innerText = scan.status;
                        });
                    } else {
                        tbody.innerHTML = '<tr><td colspan="5">No scans available</td></tr>';
                    }
                });
        }
        
        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>"""
            
            def get_status_json(self):
                # This will be populated by main class
                return json.dumps({
                    "totalScans": 0,
                    "criticalVulns": 0,
                    "avgRisk": 0,
                    "hostsFound": 0,
                    "activeUsers": 0,
                    "lastScan": "Never"
                })
            
            def get_scans_json(self):
                return json.dumps({"scans": []})
        
        return DashboardHandler
    
    def update_status(self, total_scans, critical_vulns, avg_risk, hosts_found, active_users, last_scan):
        """Update status data"""
        self.status_data = {
            "totalScans": total_scans,
            "criticalVulns": critical_vulns,
            "avgRisk": avg_risk,
            "hostsFound": hosts_found,
            "activeUsers": active_users,
            "lastScan": last_scan
        }
    
    # ========== 2. MOBILE RESPONSIVE ==========
    
    def get_mobile_html(self):
        """Mobile-optimized HTML"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>T-8 Scanner - Mobile</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff41;
            padding: 15px;
        }
        .card {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        button {
            width: 100%;
            padding: 15px;
            background: #0a0a0a;
            color: #00ff41;
            border: 1px solid #00ff41;
            border-radius: 10px;
            font-size: 16px;
            margin-top: 10px;
        }
        input {
            width: 100%;
            padding: 12px;
            background: #0a0a0a;
            color: #00ff41;
            border: 1px solid #00ff41;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔍 T-8 Scanner</h2>
        <p>Mobile Security Scanner</p>
    </div>
    
    <div class="card">
        <div class="stat-row">
            <span>📊 Total Scans:</span>
            <span id="totalScans">0</span>
        </div>
        <div class="stat-row">
            <span>⚠️ Critical Vulns:</span>
            <span id="criticalVulns">0</span>
        </div>
        <div class="stat-row">
            <span>📡 Hosts Found:</span>
            <span id="hostsFound">0</span>
        </div>
    </div>
    
    <div class="card">
        <input type="text" id="target" placeholder="Enter target IP or domain">
        <button onclick="startScan()">▶ START SCAN</button>
    </div>
    
    <script>
        function fetchData() {
            fetch('/api/status')
                .then(r => r.json())
                .then(d => {
                    document.getElementById('totalScans').innerText = d.totalScans || 0;
                    document.getElementById('criticalVulns').innerText = d.criticalVulns || 0;
                    document.getElementById('hostsFound').innerText = d.hostsFound || 0;
                });
        }
        function startScan() {
            const target = document.getElementById('target').value;
            alert('Scan started for: ' + target);
        }
        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>"""
    
    # ========== 3. REAL-TIME COLLABORATION ==========
    
    def add_active_user(self, username):
        """Add active user for collaboration"""
        if username not in self.active_users:
            self.active_users.append(username)
        return len(self.active_users)
    
    def remove_active_user(self, username):
        """Remove active user"""
        if username in self.active_users:
            self.active_users.remove(username)
        return len(self.active_users)
    
    def broadcast_scan_result(self, scan_data):
        """Broadcast scan result to all active users"""
        # In real implementation, this would push to WebSocket
        return {"broadcast": True, "data": scan_data, "users": len(self.active_users)}
    
    # ========== 4. LIVE STREAMING ==========
    
    def start_live_stream(self, scan_id):
        """Start live streaming of scan progress"""
        def stream():
            progress = 0
            while progress < 100:
                time.sleep(0.5)
                progress += 5
                # In real implementation, send via WebSocket
        thread = threading.Thread(target=stream)
        thread.daemon = True
        thread.start()
        return True
    
    def get_live_status(self, scan_id):
        """Get live scan status"""
        return {
            "scan_id": scan_id,
            "progress": 50,
            "status": "running",
            "ports_scanned": 500,
            "total_ports": 1000,
            "open_ports_found": 5
        }
    
    # ========== 5. CLOUD BACKUP ==========
    
    def enable_cloud_backup(self, api_key=None):
        """Enable cloud backup"""
        self.cloud_backup_enabled = True
        return True, "Cloud backup enabled"
    
    def disable_cloud_backup(self):
        """Disable cloud backup"""
        self.cloud_backup_enabled = False
        return True, "Cloud backup disabled"
    
    def backup_to_cloud(self, data):
        """Backup data to cloud"""
        if not self.cloud_backup_enabled:
            return False, "Cloud backup not enabled"
        
        # In real implementation, upload to cloud storage
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return True, f"Data backed up with ID: {backup_id}"
    
    def restore_from_cloud(self, backup_id):
        """Restore data from cloud"""
        if not self.cloud_backup_enabled:
            return False, "Cloud backup not enabled"
        
        # In real implementation, download from cloud storage
        return True, f"Data restored from backup: {backup_id}"
    
    # ========== FORMAT OUTPUT ==========
    
    def format_output(self, data_type, data):
        """Format output for display"""
        output = []
        output.append("\n" + "="*70)
        output.append(f"🌐 {data_type.upper()}")
        output.append("="*70)
        
        if isinstance(data, dict):
            for key, value in data.items():
                output.append(f"   • {key}: {value}")
        elif isinstance(data, list):
            for item in data:
                output.append(f"   • {item}")
        else:
            output.append(f"   {data}")
        
        return "\n".join(output)
