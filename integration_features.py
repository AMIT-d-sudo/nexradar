#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integration Features Module
Mobile app API, Browser extension, IDE plugin
CI/CD integration, SIEM integration
"""

import json
import os
import subprocess
import threading
import time
from datetime import datetime
import hashlib

class IntegrationFeatures:
    def __init__(self):
        self.data_dir = "integration_data"
        self.api_port = 5000
        self.api_key = None
        self.webhook_urls = []
        self.siem_config = {}
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.load_config()
    
    def load_config(self):
        """Load integration configuration"""
        config_file = f"{self.data_dir}/config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    self.webhook_urls = config.get('webhook_urls', [])
                    self.siem_config = config.get('siem_config', {})
            except:
                pass
        
        if not self.api_key:
            self.api_key = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
            self.save_config()
    
    def save_config(self):
        """Save integration configuration"""
        config = {
            'api_key': self.api_key,
            'webhook_urls': self.webhook_urls,
            'siem_config': self.siem_config
        }
        with open(f"{self.data_dir}/config.json", 'w') as f:
            json.dump(config, f, indent=4)
    
    # ========== 1. MOBILE APP API ==========
    
    def start_mobile_api_server(self, port=5000):
        """Start REST API server for mobile app"""
        self.api_port = port
        self.api_server_running = True
        
        def run_server():
            from http.server import HTTPServer, BaseHTTPRequestHandler
            
            class MobileAPIHandler(BaseHTTPRequestHandler):
                def log_message(self, format, *args):
                    pass
                
                def do_GET(self):
                    if self.path == '/api/status':
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'status': 'online', 'version': '1.0'}).encode())
                    elif self.path == '/api/scans':
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(self.get_scans_data()).encode())
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def do_POST(self):
                    if self.path == '/api/scan':
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data)
                        result = self.start_scan(data.get('target'), data.get('ports'))
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode())
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def get_scans_data(self):
                    return {'scans': [], 'total': 0}
                
                def start_scan(self, target, ports):
                    return {'scan_id': 'scan_001', 'status': 'started', 'target': target}
            
            server = HTTPServer(('0.0.0.0', port), MobileAPIHandler)
            server.serve_forever()
        
        thread = threading.Thread(target=run_server)
        thread.daemon = True
        thread.start()
        return True, f"Mobile API server started on port {port}"
    
    def stop_mobile_api_server(self):
        """Stop mobile API server"""
        self.api_server_running = False
        return True, "Mobile API server stopped"
    
    def get_api_key(self):
        """Get API key for mobile app authentication"""
        return self.api_key
    
    def generate_new_api_key(self):
        """Generate new API key"""
        self.api_key = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        self.save_config()
        return self.api_key
    
    def get_mobile_app_config(self):
        """Get mobile app configuration"""
        return {
            'api_url': f'http://localhost:{self.api_port}',
            'api_key': self.api_key,
            'version': '1.0'
        }
    
    # ========== 2. BROWSER EXTENSION ==========
    
    def generate_browser_extension(self):
        """Generate browser extension files"""
        extension_dir = f"{self.data_dir}/browser_extension"
        if not os.path.exists(extension_dir):
            os.makedirs(extension_dir)
        
        # Manifest.json
        manifest = {
            "manifest_version": 3,
            "name": "T-8 Scanner",
            "version": "1.0",
            "description": "One-click security scan from browser",
            "permissions": ["activeTab", "storage", "notifications"],
            "action": {
                "default_popup": "popup.html",
                "default_icon": {
                    "16": "icon16.png",
                    "48": "icon48.png",
                    "128": "icon128.png"
                }
            },
            "background": {
                "service_worker": "background.js"
            }
        }
        
        with open(f"{extension_dir}/manifest.json", 'w') as f:
            json.dump(manifest, f, indent=4)
        
        # Popup HTML
        popup_html = '''<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            width: 300px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff41;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #0a0a0a;
            color: #00ff41;
            border: 1px solid #00ff41;
            cursor: pointer;
            margin: 5px 0;
            font-family: monospace;
        }
        button:hover {
            background: #00ff41;
            color: #0a0a0a;
        }
        input {
            width: 100%;
            padding: 8px;
            background: #0a0a0a;
            color: #00ff41;
            border: 1px solid #00ff41;
            margin: 5px 0;
            font-family: monospace;
        }
        .status {
            margin-top: 10px;
            padding: 5px;
            background: #1a1a1a;
            text-align: center;
        }
    </style>
</head>
<body>
    <h3>🔍 T-8 Scanner</h3>
    <input type="text" id="target" placeholder="Enter target IP or domain">
    <input type="text" id="ports" placeholder="Ports (e.g., 80,443)" value="80,443">
    <button id="scanBtn">▶ START SCAN</button>
    <div id="status" class="status">Ready</div>
    
    <script>
        document.getElementById('scanBtn').addEventListener('click', () => {
            const target = document.getElementById('target').value;
            const ports = document.getElementById('ports').value;
            const status = document.getElementById('status');
            
            if (!target) {
                status.textContent = 'Please enter target';
                return;
            }
            
            status.textContent = 'Scanning ' + target + '...';
            
            fetch('http://localhost:5000/api/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target, ports: ports})
            })
            .then(response => response.json())
            .then(data => {
                status.textContent = 'Scan started: ' + data.scan_id;
            })
            .catch(error => {
                status.textContent = 'Error: ' + error.message;
            });
        });
    </script>
</body>
</html>'''
        
        with open(f"{extension_dir}/popup.html", 'w') as f:
            f.write(popup_html)
        
        return extension_dir
    
    # ========== 3. IDE PLUGIN ==========
    
    def generate_vscode_extension(self):
        """Generate VS Code extension"""
        vscode_dir = f"{self.data_dir}/vscode_extension"
        if not os.path.exists(vscode_dir):
            os.makedirs(vscode_dir)
        
        # Package.json
        package_json = {
            "name": "t8-scanner",
            "displayName": "T-8 Scanner",
            "description": "Security scanner for VS Code",
            "version": "1.0.0",
            "publisher": "t8-scanner",
            "engines": {"vscode": "^1.80.0"},
            "categories": ["Other"],
            "activationEvents": ["onCommand:t8-scanner.scan"],
            "main": "./extension.js",
            "contributes": {
                "commands": [
                    {
                        "command": "t8-scanner.scan",
                        "title": "T-8 Scanner: Scan Current File"
                    },
                    {
                        "command": "t8-scanner.scanIP",
                        "title": "T-8 Scanner: Scan Selected IP"
                    }
                ],
                "menus": {
                    "editor/context": [
                        {
                            "command": "t8-scanner.scanIP",
                            "when": "editorHasSelection"
                        }
                    ]
                }
            }
        }
        
        with open(f"{vscode_dir}/package.json", 'w') as f:
            json.dump(package_json, f, indent=4)
        
        # Extension.js
        extension_js = '''const vscode = require('vscode');
const axios = require('axios');

function activate(context) {
    let disposable = vscode.commands.registerCommand('t8-scanner.scan', async function () {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            const text = document.getText();
            
            vscode.window.showInformationMessage('T-8 Scanner: Analyzing code...');
            // Send to T-8 Scanner API
        }
    });
    
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };'''
        
        with open(f"{vscode_dir}/extension.js", 'w') as f:
            f.write(extension_js)
        
        return vscode_dir
    
    def generate_pycharm_plugin(self):
        """Generate PyCharm plugin configuration"""
        pycharm_dir = f"{self.data_dir}/pycharm_plugin"
        if not os.path.exists(pycharm_dir):
            os.makedirs(pycharm_dir)
        
        plugin_xml = '''<idea-plugin>
    <id>com.t8.scanner</id>
    <name>T-8 Scanner</name>
    <version>1.0</version>
    <vendor email="support@t8-scanner.com">T-8 Scanner</vendor>
    
    <description><![CDATA[
        Security scanner integration for PyCharm
    ]]></description>
    
    <depends>com.intellij.modules.lang</depends>
    
    <extensions defaultExtensionNs="com.intellij">
        <toolWindow id="T-8 Scanner" secondary="false" anchor="right"
                    factoryClass="com.t8.scanner.ToolWindowFactory"/>
    </extensions>
    
    <actions>
        <action id="T8Scanner.Scan" class="com.t8.scanner.ScanAction" text="Scan with T-8 Scanner">
            <add-to-group group-id="EditorPopupMenu" anchor="first"/>
        </action>
    </actions>
</idea-plugin>'''
        
        with open(f"{pycharm_dir}/plugin.xml", 'w') as f:
            f.write(plugin_xml)
        
        return pycharm_dir
    
    # ========== 4. CI/CD INTEGRATION ==========
    
    def generate_jenkins_pipeline(self):
        """Generate Jenkins pipeline script"""
        jenkinsfile = '''pipeline {
    agent any
    
    tools {
        maven 'Maven-3'
    }
    
    stages {
        stage('Security Scan') {
            steps {
                script {
                    // Run T-8 Scanner
                    sh 'python3 main.py --scan --target scanme.nmap.org --output report.json'
                }
            }
        }
        
        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Security Scan Report'
                ])
            }
        }
    }
    
    post {
        always {
            echo 'Scan completed'
        }
    }
}'''
        
        jenkins_file = f"{self.data_dir}/Jenkinsfile"
        with open(jenkins_file, 'w') as f:
            f.write(jenkinsfile)
        
        return jenkins_file
    
    def generate_github_action(self):
        """Generate GitHub Actions workflow"""
        github_action = '''name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily scan

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install T-8 Scanner
      run: |
        pip install -r requirements.txt
    
    - name: Run Security Scan
      run: |
        python3 main.py --scan --target scanme.nmap.org --output scan_results.json
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: scan-results
        path: scan_results.json
    
    - name: Comment PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const results = JSON.parse(fs.readFileSync('scan_results.json'));
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## 🔍 Security Scan Results\\nRisk Score: ${results.risk_score}/100\\nOpen Ports: ${results.open_ports}`
          });'''
        
        github_dir = f"{self.data_dir}/.github/workflows"
        if not os.path.exists(github_dir):
            os.makedirs(github_dir)
        
        workflow_file = f"{github_dir}/security-scan.yml"
        with open(workflow_file, 'w') as f:
            f.write(github_action)
        
        return workflow_file
    
    def add_webhook(self, url, event_type="scan_complete"):
        """Add webhook for CI/CD integration"""
        webhook = {
            'url': url,
            'event_type': event_type,
            'created_at': datetime.now().isoformat()
        }
        self.webhook_urls.append(webhook)
        self.save_config()
        return True
    
    def trigger_webhook(self, event_type, data):
        """Trigger webhook for event"""
        import requests
        for webhook in self.webhook_urls:
            if webhook['event_type'] == event_type:
                try:
                    requests.post(webhook['url'], json=data, timeout=10)
                except:
                    pass
    
    # ========== 5. SIEM INTEGRATION ==========
    
    def configure_siem(self, siem_type, config):
        """Configure SIEM integration"""
        self.siem_config = {
            'type': siem_type,
            'config': config,
            'enabled': True,
            'configured_at': datetime.now().isoformat()
        }
        self.save_config()
        return True
    
    def send_to_splunk(self, data):
        """Send data to Splunk"""
        if self.siem_config.get('type') != 'splunk':
            return False
        
        try:
            import requests
            splunk_config = self.siem_config.get('config', {})
            url = f"{splunk_config.get('url', '')}/services/collector"
            headers = {'Authorization': f"Splunk {splunk_config.get('token', '')}"}
            requests.post(url, json=data, headers=headers, timeout=10)
            return True
        except:
            return False
    
    def send_to_elasticsearch(self, data):
        """Send data to Elasticsearch (ELK stack)"""
        if self.siem_config.get('type') != 'elasticsearch':
            return False
        
        try:
            import requests
            es_config = self.siem_config.get('config', {})
            url = f"{es_config.get('url', '')}/t8-scanner/_doc"
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json=data, headers=headers, timeout=10)
            return True
        except:
            return False
    
    def send_to_qradar(self, data):
        """Send data to QRadar"""
        if self.siem_config.get('type') != 'qradar':
            return False
        
        try:
            import requests
            qradar_config = self.siem_config.get('config', {})
            url = f"{qradar_config.get('url', '')}/api/events"
            headers = {'Authorization': f"Bearer {qradar_config.get('token', '')}"}
            requests.post(url, json=data, headers=headers, timeout=10)
            return True
        except:
            return False
    
    def send_scan_to_siem(self, scan_data):
        """Send scan results to SIEM"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'scan_completed',
            'source': 'T-8 Scanner',
            'data': scan_data
        }
        
        if self.siem_config.get('type') == 'splunk':
            return self.send_to_splunk(event)
        elif self.siem_config.get('type') == 'elasticsearch':
            return self.send_to_elasticsearch(event)
        elif self.siem_config.get('type') == 'qradar':
            return self.send_to_qradar(event)
        
        return False
    
    # ========== FORMAT OUTPUT ==========
    
    def format_output(self, data_type, data):
        output = []
        output.append("\n" + "="*70)
        output.append(f"📱 {data_type.upper()}")
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

