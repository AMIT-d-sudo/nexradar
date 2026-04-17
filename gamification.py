#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gamification Features Module
Achievements system, Leaderboards, Training mode
Challenge targets, Certification tracking
"""

import json
import os
from datetime import datetime
import hashlib

class Gamification:
    def __init__(self):
        self.data_dir = "gamification_data"
        self.achievements_file = f"{self.data_dir}/achievements.json"
        self.leaderboard_file = f"{self.data_dir}/leaderboard.json"
        self.training_data_file = f"{self.data_dir}/training.json"
        self.certifications_file = f"{self.data_dir}/certifications.json"
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.load_data()
        self.init_achievements()
    
    def load_data(self):
        """Load all gamification data"""
        # Load achievements
        if os.path.exists(self.achievements_file):
            with open(self.achievements_file, 'r') as f:
                self.achievements = json.load(f)
        else:
            self.achievements = {}
        
        # Load leaderboard
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r') as f:
                self.leaderboard = json.load(f)
        else:
            self.leaderboard = []
        
        # Load training data
        if os.path.exists(self.training_data_file):
            with open(self.training_data_file, 'r') as f:
                self.training_data = json.load(f)
        else:
            self.training_data = {}
        
        # Load certifications
        if os.path.exists(self.certifications_file):
            with open(self.certifications_file, 'r') as f:
                self.certifications = json.load(f)
        else:
            self.certifications = {}
    
    def save_data(self):
        """Save all gamification data"""
        with open(self.achievements_file, 'w') as f:
            json.dump(self.achievements, f, indent=4)
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard, f, indent=4)
        with open(self.training_data_file, 'w') as f:
            json.dump(self.training_data, f, indent=4)
        with open(self.certifications_file, 'w') as f:
            json.dump(self.certifications, f, indent=4)
    
    # ========== 1. ACHIEVEMENTS SYSTEM ==========
    
    def init_achievements(self):
        """Initialize achievements list"""
        self.achievements_list = {
            "first_scan": {
                "name": "🎯 First Blood",
                "description": "Complete your first scan",
                "points": 10,
                "icon": "🎯",
                "unlocked": False
            },
            "scan_10": {
                "name": "🔍 Curious Explorer",
                "description": "Complete 10 scans",
                "points": 50,
                "icon": "🔍",
                "unlocked": False
            },
            "scan_50": {
                "name": "⚡ Scan Master",
                "description": "Complete 50 scans",
                "points": 200,
                "icon": "⚡",
                "unlocked": False
            },
            "scan_100": {
                "name": "🏆 Legendary Scanner",
                "description": "Complete 100 scans",
                "points": 500,
                "icon": "🏆",
                "unlocked": False
            },
            "vuln_finder": {
                "name": "🐛 Bug Hunter",
                "description": "Find your first vulnerability",
                "points": 25,
                "icon": "🐛",
                "unlocked": False
            },
            "critical_finder": {
                "name": "💀 Critical Strike",
                "description": "Find a critical vulnerability",
                "points": 100,
                "icon": "💀",
                "unlocked": False
            },
            "stealth_master": {
                "name": "👻 Ghost Mode",
                "description": "Complete a scan with stealth options",
                "points": 75,
                "icon": "👻",
                "unlocked": False
            },
            "fast_scanner": {
                "name": "⚡ Speed Demon",
                "description": "Complete a scan in under 1 second",
                "points": 50,
                "icon": "⚡",
                "unlocked": False
            },
            "port_master": {
            "name": "🔌 Port Master",
                "description": "Discover 50+ open ports",
                "points": 100,
                "icon": "🔌",
                "unlocked": False
            },
            "network_explorer": {
                "name": "🌐 Network Explorer",
                "description": "Scan an entire subnet",
                "points": 150,
                "icon": "🌐",
                "unlocked": False
            },
            "os_detector": {
                "name": "💻 OS Detective",
                "description": "Successfully detect operating system",
                "points": 75,
                "icon": "💻",
                "unlocked": False
            },
            "service_master": {
                "name": "🛠️ Service Master",
                "description": "Identify 20+ services",
                "points": 100,
                "icon": "🛠️",
                "unlocked": False
            },
            "vulnerability_hunter": {
                "name": "🔓 Vulnerability Hunter",
                "description": "Find 10+ vulnerabilities",
                "points": 200,
                "icon": "🔓",
                "unlocked": False
            },
            "compliance_guru": {
                "name": "✅ Compliance Guru",
                "description": "Achieve 90%+ compliance score",
                "points": 150,
                "icon": "✅",
                "unlocked": False
            },
            "team_player": {
                "name": "👥 Team Player",
                "description": "Collaborate with other users",
                "points": 50,
                "icon": "👥",
                "unlocked": False
            },
            "expert_scanner": {
                "name": "🎓 Expert Scanner",
                "description": "Earn expert certification",
                "points": 500,
                "icon": "🎓",
                "unlocked": False
            }
        }
        
        # Merge with saved data
        for ach_id, ach_data in self.achievements_list.items():
            if ach_id in self.achievements:
                self.achievements_list[ach_id]['unlocked'] = self.achievements[ach_id].get('unlocked', False)
                self.achievements_list[ach_id]['unlocked_at'] = self.achievements[ach_id].get('unlocked_at')
    
    def check_achievement(self, user_id, event_type, data):
        """Check and unlock achievements"""
        unlocked = []
        total_points = self.get_user_points(user_id)
        
        if event_type == 'scan_completed':
            scans = self.get_user_scans(user_id)
            
            if scans == 1 and not self.achievements_list['first_scan']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'first_scan'))
            
            if scans >= 10 and not self.achievements_list['scan_10']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'scan_10'))
            
            if scans >= 50 and not self.achievements_list['scan_50']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'scan_50'))
            
            if scans >= 100 and not self.achievements_list['scan_100']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'scan_100'))
            
            if data.get('scan_time', 0) < 1 and not self.achievements_list['fast_scanner']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'fast_scanner'))
            
            if data.get('is_subnet', False) and not self.achievements_list['network_explorer']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'network_explorer'))
            
            if data.get('stealth_used', False) and not self.achievements_list['stealth_master']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'stealth_master'))
        
        elif event_type == 'vulnerability_found':
            vuln_count = self.get_user_vulns(user_id)
            
            if vuln_count >= 1 and not self.achievements_list['vuln_finder']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'vuln_finder'))
            
            if vuln_count >= 10 and not self.achievements_list['vulnerability_hunter']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'vulnerability_hunter'))
            
            if data.get('is_critical', False) and not self.achievements_list['critical_finder']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'critical_finder'))
        
        elif event_type == 'port_discovered':
            ports = self.get_user_ports(user_id)
            
            if ports >= 50 and not self.achievements_list['port_master']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'port_master'))
        
        elif event_type == 'os_detected':
            if not self.achievements_list['os_detector']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'os_detector'))
        
        elif event_type == 'service_detected':
            services = self.get_user_services(user_id)
            
            if services >= 20 and not self.achievements_list['service_master']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'service_master'))
        
        elif event_type == 'compliance_achieved':
            if data.get('score', 0) >= 90 and not self.achievements_list['compliance_guru']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'compliance_guru'))
        
        elif event_type == 'team_collab':
            if not self.achievements_list['team_player']['unlocked']:
                unlocked.append(self.unlock_achievement(user_id, 'team_player'))
        
        return unlocked
    
    def unlock_achievement(self, user_id, achievement_id):
        """Unlock an achievement for user"""
        if achievement_id in self.achievements_list:
            self.achievements_list[achievement_id]['unlocked'] = True
            self.achievements_list[achievement_id]['unlocked_at'] = datetime.now().isoformat()
            
            if user_id not in self.achievements:
                self.achievements[user_id] = {}
            
            self.achievements[user_id][achievement_id] = {
                'unlocked': True,
                'unlocked_at': datetime.now().isoformat(),
                'points': self.achievements_list[achievement_id]['points']
            }
            
            self.save_data()
            self.update_leaderboard(user_id, self.achievements_list[achievement_id]['points'])
            
            return self.achievements_list[achievement_id]
        
        return None
    
    def get_user_achievements(self, user_id):
        """Get all achievements for a user"""
        user_achs = []
        for ach_id, ach_data in self.achievements_list.items():
            user_achs.append({
                'id': ach_id,
                'name': ach_data['name'],
                'description': ach_data['description'],
                'points': ach_data['points'],
                'icon': ach_data['icon'],
                'unlocked': ach_data['unlocked'],
                'unlocked_at': ach_data.get('unlocked_at')
            })
        return user_achs
    
    def get_user_points(self, user_id):
        """Get total points for a user"""
        total = 0
        if user_id in self.achievements:
            for ach_id, ach_data in self.achievements[user_id].items():
                total += ach_data.get('points', 0)
        return total
    
    def get_user_scans(self, user_id):
        """Get total scans count for user"""
        if user_id in self.training_data:
            return self.training_data[user_id].get('total_scans', 0)
        return 0
    
    def get_user_vulns(self, user_id):
        """Get total vulnerabilities found"""
        if user_id in self.training_data:
            return self.training_data[user_id].get('total_vulns', 0)
        return 0
    
    def get_user_ports(self, user_id):
        """Get total open ports discovered"""
        if user_id in self.training_data:
            return self.training_data[user_id].get('total_ports', 0)
        return 0
    
    def get_user_services(self, user_id):
        """Get total services identified"""
        if user_id in self.training_data:
            return self.training_data[user_id].get('total_services', 0)
        return 0
    
    # ========== 2. LEADERBOARDS ==========
    
    def update_leaderboard(self, user_id, points):
        """Update leaderboard with user points"""
        # Find user in leaderboard
        user_found = False
        for entry in self.leaderboard:
            if entry['user_id'] == user_id:
                entry['points'] += points
                entry['last_updated'] = datetime.now().isoformat()
                user_found = True
                break
        
        if not user_found:
            self.leaderboard.append({
                'user_id': user_id,
                'username': user_id,
                'points': points,
                'achievements': len(self.get_user_achievements(user_id)),
                'last_updated': datetime.now().isoformat()
            })
        
        # Sort by points (descending)
        self.leaderboard.sort(key=lambda x: x['points'], reverse=True)
        self.save_data()
    
    def get_leaderboard(self, limit=10):
        """Get top users from leaderboard"""
        return self.leaderboard[:limit]
    
    def get_user_rank(self, user_id):
        """Get user's rank in leaderboard"""
        for i, entry in enumerate(self.leaderboard):
            if entry['user_id'] == user_id:
                return i + 1
        return None
    
    # ========== 3. TRAINING MODE ==========
    
    def start_training(self, user_id, module):
        """Start training module"""
        if user_id not in self.training_data:
            self.training_data[user_id] = {
                'completed_modules': [],
                'current_module': None,
                'score': 0,
                'total_scans': 0,
                'total_vulns': 0,
                'total_ports': 0,
                'total_services': 0,
                'started_at': datetime.now().isoformat()
            }
        
        self.training_data[user_id]['current_module'] = module
        self.save_data()
        
        return self.get_training_module(module)
    
    def complete_training_module(self, user_id, module, score):
        """Complete a training module"""
        if user_id not in self.training_data:
            return False
        
        if module not in self.training_data[user_id]['completed_modules']:
            self.training_data[user_id]['completed_modules'].append(module)
            self.training_data[user_id]['score'] += score
        
        self.training_data[user_id]['current_module'] = None
        self.save_data()
        
        # Check for expert achievement
        if len(self.training_data[user_id]['completed_modules']) >= 5:
            self.unlock_achievement(user_id, 'expert_scanner')
        
        return True
    
    def get_training_module(self, module):
        """Get training module content"""
        modules = {
            "basics": {
                "name": "📚 Security Scanning Basics",
                "description": "Learn the fundamentals of network scanning",
                "duration": "15 minutes",
                "lessons": [
                    "What is network scanning?",
                    "Types of scans (SYN, TCP, UDP)",
                    "Understanding open ports",
                    "Interpreting scan results"
                ],
                "challenge": "Scan scanme.nmap.org and identify open ports",
                "points": 50
            },
            "vulnerability": {
                "name": "🐛 Vulnerability Detection",
                "description": "Learn to identify security vulnerabilities",
                "duration": "20 minutes",
                "lessons": [
                    "Common vulnerabilities (EternalBlue, Heartbleed)",
                    "CVE database usage",
                    "Risk assessment",
                    "Remediation strategies"
                ],
                "challenge": "Find a vulnerability on the test target",
                "points": 100
            },
            "stealth": {
                "name": "👻 Stealth Scanning Techniques",
                "description": "Master undetectable scanning methods",
                "duration": "25 minutes",
                "lessons": [
                    "Evading IDS/IPS",
                    "Using decoys and fragmentation",
                    "Timing templates",
                    "Proxy chains and Tor"
                ],
                "challenge": "Complete a scan without detection",
                "points": 150
            },
            "os_detection": {
                "name": "💻 Operating System Fingerprinting",
                "description": "Learn to identify remote operating systems",
                "duration": "15 minutes",
                "lessons": [
                    "TCP/IP stack fingerprinting",
                    "OS detection flags",
                    "Interpreting OS guesses",
                    "Limitations of OS detection"
                ],
                "challenge": "Detect OS of the target machine",
                "points": 75
            },
            "compliance": {
                "name": "✅ Compliance Scanning",
                "description": "Understand compliance standards",
                "duration": "20 minutes",
                "lessons": [
                    "PCI-DSS requirements",
                    "HIPAA security rules",
                    "GDPR compliance",
                    "ISO 27001 standards"
                ],
                "challenge": "Achieve 80%+ compliance score",
                "points": 125
            },
            "reporting": {
                "name": "📊 Professional Reporting",
                "description": "Create professional security reports",
                "duration": "15 minutes",
                "lessons": [
                    "Report structure",
                    "Executive summaries",
                    "Technical details",
                    "Recommendations"
                ],
                "challenge": "Generate a complete security report",
                "points": 100
            }
        }
        
        return modules.get(module, {})
    
    def get_all_training_modules(self):
        """Get all training modules"""
        modules = [
            "basics",
            "vulnerability", 
            "stealth",
            "os_detection",
            "compliance",
            "reporting"
        ]
        
        result = []
        for module in modules:
            result.append(self.get_training_module(module))
        
        return result
    
    # ========== 4. CHALLENGE TARGETS ==========
    
    def get_challenge_targets(self):
        """Get legal practice targets"""
        return [
            {
                "name": "Scanme",
                "target": "scanme.nmap.org",
                "description": "Official Nmap testing target",
                "difficulty": "Easy",
                "points": 25,
                "hint": "Try scanning common ports (80, 443)"
            },
            {
                "name": "Hack The Box",
                "target": "www.hackthebox.com",
                "description": "Practice penetration testing",
                "difficulty": "Medium",
                "points": 50,
                "hint": "Requires registration"
            },
            {
                "name": "TryHackMe",
                "target": "tryhackme.com",
                "description": "Learn cybersecurity hands-on",
                "difficulty": "Easy",
                "points": 25,
                "hint": "Start with free rooms"
            },
            {
                "name": "OWASP Juice Shop",
                "target": "juice-shop.herokuapp.com",
                "description": "Vulnerable web application",
                "difficulty": "Medium",
                "points": 50,
                "hint": "Try port 80 and 3000"
            },
            {
                "name": "VulnWeb",
                "target": "testphp.vulnweb.com",
                "description": "Vulnerable PHP application",
                "difficulty": "Medium",
                "points": 50,
                "hint": "SQL injection possible"
            },
            {
                "name": "Metasploitable",
                "target": "192.168.79.129",
                "description": "Vulnerable VM (local)",
                "difficulty": "Hard",
                "points": 100,
                "hint": "Many open ports, try full scan"
            }
        ]
    
    def complete_challenge(self, user_id, challenge_name):
        """Mark a challenge as completed"""
        if user_id not in self.training_data:
            self.training_data[user_id] = {}
        
        if 'completed_challenges' not in self.training_data[user_id]:
            self.training_data[user_id]['completed_challenges'] = []
        
        if challenge_name not in self.training_data[user_id]['completed_challenges']:
            self.training_data[user_id]['completed_challenges'].append(challenge_name)
            self.save_data()
            return True
        
        return False
    
    # ========== 5. CERTIFICATION TRACKING ==========
    
    def get_certifications(self):
        """Get available certifications"""
        return [
            {
                "id": "cert_basic",
                "name": "🎓 Security Scanning Fundamentals",
                "description": "Basic certification for security scanning",
                "requirements": [
                    "Complete 10 scans",
                    "Find 5 vulnerabilities",
                    "Complete 'basics' training"
                ],
                "points": 100,
                "icon": "🎓"
            },
            {
                "id": "cert_advanced",
                "name": "⭐ Advanced Security Analyst",
                "description": "Advanced certification for security professionals",
                "requirements": [
                    "Complete 50 scans",
                    "Find 20 vulnerabilities",
                    "Complete all training modules",
                    "Achieve 10 achievements"
                ],
                "points": 500,
                "icon": "⭐"
            },
            {
                "id": "cert_expert",
                "name": "🏆 Certified Security Expert",
                "description": "Expert level certification",
                "requirements": [
                    "Complete 100 scans",
                    "Find 50 vulnerabilities",
                    "Complete all challenges",
                    "Achieve 15 achievements",
                    "Top 10 on leaderboard"
                ],
                "points": 1000,
                "icon": "🏆"
            },
            {
                "id": "cert_compliance",
                "name": "✅ Compliance Specialist",
                "description": "Compliance and standards certification",
                "requirements": [
                    "90%+ compliance score",
                    "Complete compliance training",
                    "Generate 5 compliance reports"
                ],
                "points": 250,
                "icon": "✅"
            },
            {
                "id": "cert_stealth",
                "name": "👻 Stealth Security Expert",
                "description": "Advanced evasion techniques",
                "requirements": [
                    "Complete 10 stealth scans",
                    "Complete stealth training",
                    "Bypass IDS detection"
                ],
                "points": 300,
                "icon": "👻"
            }
        ]
    
    def earn_certification(self, user_id, cert_id):
        """Earn a certification"""
        if user_id not in self.certifications:
            self.certifications[user_id] = []
        
        for cert in self.certifications[user_id]:
            if cert['id'] == cert_id:
                return False
        
        certs = self.get_certifications()
        for cert in certs:
            if cert['id'] == cert_id:
                self.certifications[user_id].append({
                    'id': cert_id,
                    'name': cert['name'],
                    'earned_at': datetime.now().isoformat(),
                    'points': cert['points']
                })
                self.save_data()
                self.update_leaderboard(user_id, cert['points'])
                return True
        
        return False
    
    def get_user_certifications(self, user_id):
        """Get user's earned certifications"""
        if user_id in self.certifications:
            return self.certifications[user_id]
        return []
    
    # ========== FORMAT OUTPUT ==========
    
    def format_achievements_output(self, achievements):
        """Format achievements for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("🏆 ACHIEVEMENTS")
        output.append("="*70)
        
        unlocked = [a for a in achievements if a['unlocked']]
        locked = [a for a in achievements if not a['unlocked']]
        
        output.append(f"\n📊 Unlocked: {len(unlocked)}/{len(achievements)}")
        
        if unlocked:
            output.append("\n✅ UNLOCKED ACHIEVEMENTS:")
            for ach in unlocked:
                output.append(f"   {ach['icon']} {ach['name']} - {ach['points']} pts")
                output.append(f"      {ach['description']}")
        
        if locked:
            output.append("\n🔒 LOCKED ACHIEVEMENTS:")
            for ach in locked[:10]:
                output.append(f"   {ach['icon']} {ach['name']} - {ach['points']} pts")
        
        return "\n".join(output)
    
    def format_leaderboard_output(self, leaderboard, user_rank=None):
        """Format leaderboard for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("👑 LEADERBOARD")
        output.append("="*70)
        
        if not leaderboard:
            output.append("   No entries yet. Complete scans to appear on leaderboard!")
        else:
            output.append("\n🏆 Top Scorers:")
            for i, entry in enumerate(leaderboard[:10]):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                output.append(f"   {medal} {entry['username']} - {entry['points']} pts (🏅 {entry['achievements']} achievements)")
        
        if user_rank:
            output.append(f"\n📊 Your Rank: #{user_rank}")
        
        return "\n".join(output)
    
    def format_training_output(self, modules):
        """Format training modules for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("📚 TRAINING MODULES")
        output.append("="*70)
        
        for module in modules:
            output.append(f"\n📖 {module['name']}")
            output.append(f"   ⏱️ Duration: {module['duration']}")
            output.append(f"   🎯 Points: {module['points']}")
            output.append(f"   📝 Description: {module['description']}")
        
        return "\n".join(output)
    
    def format_challenges_output(self, challenges):
        """Format challenges for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("🎯 PRACTICE CHALLENGES")
        output.append("="*70)
        
        for challenge in challenges:
            difficulty_icon = "🟢" if challenge['difficulty'] == "Easy" else "🟡" if challenge['difficulty'] == "Medium" else "🔴"
            output.append(f"\n{difficulty_icon} {challenge['name']}")
            output.append(f"   Target: {challenge['target']}")
            output.append(f"   Description: {challenge['description']}")
            output.append(f"   💡 Hint: {challenge['hint']}")
            output.append(f"   🎯 Points: {challenge['points']}")
        
        return "\n".join(output)
    
    def format_certifications_output(self, certifications, user_certs):
        """Format certifications for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("🎓 CERTIFICATIONS")
        output.append("="*70)
        
        user_cert_ids = [c['id'] for c in user_certs]
        
        for cert in certifications:
            status = "✅ EARNED" if cert['id'] in user_cert_ids else "🔒 LOCKED"
            output.append(f"\n{cert['icon']} {cert['name']} - {status}")
            output.append(f"   {cert['description']}")
            output.append(f"   📋 Requirements:")
            for req in cert['requirements']:
                output.append(f"      • {req}")
        
        return "\n".join(output)
