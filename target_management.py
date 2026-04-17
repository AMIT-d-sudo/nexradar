#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Target Management Module
Target groups/projects, Asset inventory, Change detection
Whitelist/blacklist, Import from multiple sources
"""

import json
import csv
import os
import hashlib
from datetime import datetime

class TargetManagement:
    def __init__(self):
        self.projects = {}
        self.assets = {}
        self.whitelist = []
        self.blacklist = []
        self.data_dir = "target_management_data"
        
        # Create data directory if not exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.load_all_data()
    
    def load_all_data(self):
        """Load all saved data"""
        # Load projects
        projects_file = f"{self.data_dir}/projects.json"
        if os.path.exists(projects_file):
            try:
                with open(projects_file, 'r') as f:
                    self.projects = json.load(f)
                print(f"[*] Loaded {len(self.projects)} projects")
            except Exception as e:
                print(f"[!] Error loading projects: {e}")
                self.projects = {}
        
        # Load assets
        assets_file = f"{self.data_dir}/assets.json"
        if os.path.exists(assets_file):
            try:
                with open(assets_file, 'r') as f:
                    self.assets = json.load(f)
                print(f"[*] Loaded {len(self.assets)} assets")
            except:
                self.assets = {}
        
        # Load whitelist
        whitelist_file = f"{self.data_dir}/whitelist.json"
        if os.path.exists(whitelist_file):
            try:
                with open(whitelist_file, 'r') as f:
                    self.whitelist = json.load(f)
            except:
                self.whitelist = []
        
        # Load blacklist
        blacklist_file = f"{self.data_dir}/blacklist.json"
        if os.path.exists(blacklist_file):
            try:
                with open(blacklist_file, 'r') as f:
                    self.blacklist = json.load(f)
            except:
                self.blacklist = []
    
    def save_all_data(self):
        """Save all data"""
        try:
            with open(f"{self.data_dir}/projects.json", 'w') as f:
                json.dump(self.projects, f, indent=4)
            print(f"[*] Saved {len(self.projects)} projects")
        except Exception as e:
            print(f"[!] Error saving projects: {e}")
        
        try:
            with open(f"{self.data_dir}/assets.json", 'w') as f:
                json.dump(self.assets, f, indent=4)
        except:
            pass
        
        try:
            with open(f"{self.data_dir}/whitelist.json", 'w') as f:
                json.dump(self.whitelist, f, indent=4)
        except:
            pass
        
        try:
            with open(f"{self.data_dir}/blacklist.json", 'w') as f:
                json.dump(self.blacklist, f, indent=4)
        except:
            pass
    
    # ========== 1. TARGET GROUPS/PROJECTS ==========
    
    def create_project(self, name, description=""):
        """Create a new project"""
        import time
        project_id = f"project_{int(time.time())}"
        self.projects[project_id] = {
            'id': project_id,
            'name': name,
            'description': description,
            'targets': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.save_all_data()
        return project_id
    
    def add_target_to_project(self, project_id, target):
        """Add target to project"""
        if project_id in self.projects:
            if target not in self.projects[project_id]['targets']:
                self.projects[project_id]['targets'].append(target)
                self.projects[project_id]['updated_at'] = datetime.now().isoformat()
                self.save_all_data()
                return True
        return False
    
    def get_all_projects(self):
        """Get all projects"""
        return self.projects
    
    def get_project_targets(self, project_id):
        """Get all targets in a project"""
        if project_id in self.projects:
            return self.projects[project_id]['targets']
        return []
    
    # ========== 2. ASSET INVENTORY ==========
    
    def add_asset(self, ip, hostname="", os="", services=None):
        """Add asset to inventory"""
        asset_id = hashlib.md5(ip.encode()).hexdigest()[:8]
        
        if asset_id not in self.assets:
            self.assets[asset_id] = {
                'id': asset_id,
                'ip': ip,
                'hostname': hostname,
                'os': os,
                'services': services or [],
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'scan_history': []
            }
        else:
            self.assets[asset_id]['last_seen'] = datetime.now().isoformat()
            if hostname:
                self.assets[asset_id]['hostname'] = hostname
            if os:
                self.assets[asset_id]['os'] = os
        
        self.save_all_data()
        return asset_id
    
    def get_all_assets(self):
        """Get all assets"""
        return self.assets
    
    # ========== 3. CHANGE DETECTION ==========
    
    def detect_changes(self, asset_id, new_services):
        """Detect changes since last scan"""
        if asset_id not in self.assets:
            return {'error': 'Asset not found', 'added': [], 'removed': []}
        
        asset = self.assets[asset_id]
        old_services = asset.get('services', [])
        
        changes = {
            'added': [],
            'removed': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Find added services
        for service in new_services:
            if service not in old_services:
                changes['added'].append(service)
        
        # Find removed services
        for service in old_services:
            if service not in new_services:
                changes['removed'].append(service)
        
        # Update asset
        asset['services'] = new_services
        asset['last_seen'] = datetime.now().isoformat()
        
        # Add to scan history
        asset['scan_history'].append({
            'date': datetime.now().isoformat(),
            'services': new_services,
            'changes': changes
        })
        
        self.save_all_data()
        return changes
    
    # ========== 4. WHITELIST/BLACKLIST ==========
    
    def add_to_whitelist(self, ip_range, reason=""):
        """Add IP range to whitelist"""
        entry = {
            'ip_range': ip_range,
            'reason': reason,
            'added_at': datetime.now().isoformat()
        }
        self.whitelist.append(entry)
        self.save_all_data()
        return True
    
    def add_to_blacklist(self, ip_range, reason=""):
        """Add IP range to blacklist"""
        entry = {
            'ip_range': ip_range,
            'reason': reason,
            'added_at': datetime.now().isoformat()
        }
        self.blacklist.append(entry)
        self.save_all_data()
        return True
    
    def get_whitelist(self):
        """Get whitelist"""
        return self.whitelist
    
    def get_blacklist(self):
        """Get blacklist"""
        return self.blacklist
    
    # ========== 5. IMPORT FROM MULTIPLE SOURCES ==========
    
    def import_from_csv(self, filename):
        """Import targets from CSV file"""
        targets = []
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'target' in row:
                        targets.append(row['target'])
                    elif 'ip' in row:
                        targets.append(row['ip'])
                    elif 'host' in row:
                        targets.append(row['host'])
            return targets
        except Exception as e:
            return {'error': str(e)}
    
    def import_from_json(self, filename):
        """Import targets from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'targets' in data:
                    return data['targets']
                else:
                    return []
        except Exception as e:
            return {'error': str(e)}
    
    def import_from_nessus(self, filename):
        """Import from Nessus scan file"""
        targets = []
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('.//ReportHost'):
                hostname = host.get('name')
                if hostname:
                    targets.append(hostname)
            
            return targets
        except Exception as e:
            return {'error': str(e)}
    
    def import_from_openvas(self, filename):
        """Import from OpenVAS scan file"""
        targets = []
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('.//host'):
                ip = host.get('ip', '')
                if ip:
                    targets.append(ip)
            
            return targets
        except Exception as e:
            return {'error': str(e)}
    
    # ========== FORMAT OUTPUT ==========
    
    def format_projects_output(self):
        """Format projects for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("📁 PROJECTS")
        output.append("="*70)
        
        if not self.projects:
            output.append("   No projects found")
            output.append("   Create a project using the form above")
        else:
            for proj_id, proj in self.projects.items():
                output.append(f"\n📌 {proj.get('name', 'Unknown')}")
                output.append(f"   ID: {proj_id}")
                output.append(f"   Description: {proj.get('description', 'No description')}")
                output.append(f"   Targets: {len(proj.get('targets', []))}")
                output.append(f"   Created: {proj.get('created_at', 'Unknown')}")
        
        return "\n".join(output)
    
    def format_assets_output(self):
        """Format assets for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("💾 ASSET INVENTORY")
        output.append("="*70)
        
        if not self.assets:
            output.append("   No assets found")
            output.append("   Add an asset using the form above")
        else:
            for asset_id, asset in self.assets.items():
                output.append(f"\n📡 {asset.get('ip', 'Unknown')}")
                output.append(f"   ID: {asset_id}")
                output.append(f"   Hostname: {asset.get('hostname', 'Unknown')}")
                output.append(f"   OS: {asset.get('os', 'Unknown')}")
                output.append(f"   Services: {len(asset.get('services', []))}")
                output.append(f"   First Seen: {asset.get('first_seen', 'Unknown')}")
                output.append(f"   Last Seen: {asset.get('last_seen', 'Unknown')}")
        
        return "\n".join(output)
    
    def format_changes_output(self, changes):
        """Format changes for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("🔄 CHANGE DETECTION")
        output.append("="*70)
        
        if changes.get('error'):
            output.append(f"   ❌ {changes['error']}")
        else:
            if changes.get('added'):
                output.append("\n✅ ADDED SERVICES:")
                for service in changes['added']:
                    output.append(f"   • {service}")
            
            if changes.get('removed'):
                output.append("\n❌ REMOVED SERVICES:")
                for service in changes['removed']:
                    output.append(f"   • {service}")
            
            if not changes.get('added') and not changes.get('removed'):
                output.append("\n   No changes detected")
        
        return "\n".join(output)
    
    def format_lists_output(self):
        """Format whitelist/blacklist for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("✅ WHITELIST")
        output.append("="*70)
        
        if not self.whitelist:
            output.append("   No entries")
        else:
            for i, entry in enumerate(self.whitelist):
                output.append(f"   {i+1}. {entry.get('ip_range', 'Unknown')} - {entry.get('reason', 'No reason')}")
        
        output.append("\n" + "="*70)
        output.append("🚫 BLACKLIST")
        output.append("="*70)
        
        if not self.blacklist:
            output.append("   No entries")
        else:
            for i, entry in enumerate(self.blacklist):
                output.append(f"   {i+1}. {entry.get('ip_range', 'Unknown')} - {entry.get('reason', 'No reason')}")
        
        return "\n".join(output)
