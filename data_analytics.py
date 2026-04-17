#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Analytics Module
Trend analysis, Risk scoring, Compliance checking
SLA monitoring, Predictive analysis
"""

import json
import os
import math
from datetime import datetime, timedelta
from collections import Counter

class DataAnalytics:
    def __init__(self):
        self.data_dir = "analytics_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self.scan_history = []
        self.load_history()
    
    def load_history(self):
        """Load scan history from file"""
        history_file = f"{self.data_dir}/scan_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.scan_history = json.load(f)
            except:
                self.scan_history = []
    
    def save_history(self):
        """Save scan history to file"""
        history_file = f"{self.data_dir}/scan_history.json"
        with open(history_file, 'w') as f:
            json.dump(self.scan_history, f, indent=4)
    
    def add_scan_record(self, target, risk_score, open_ports, critical_count, high_count):
        """Add a scan record to history"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'target': target,
            'risk_score': risk_score,
            'open_ports': open_ports,
            'critical_count': critical_count,
            'high_count': high_count,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        self.scan_history.append(record)
        self.save_history()
        return record
    
    # ========== 1. TREND ANALYSIS ==========
    
    def get_trend_analysis(self, days=30):
        """Get security trend over time"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_scans = [s for s in self.scan_history 
                       if datetime.fromisoformat(s['timestamp']) > cutoff]
        
        if not recent_scans:
            return {'error': 'No scan history available'}
        
        # Sort by date
        recent_scans.sort(key=lambda x: x['timestamp'])
        
        # Calculate trends
        risk_scores = [s['risk_score'] for s in recent_scans]
        critical_counts = [s['critical_count'] for s in recent_scans]
        high_counts = [s['high_count'] for s in recent_scans]
        
        # Calculate trend direction
        if len(risk_scores) >= 2:
            risk_trend = risk_scores[-1] - risk_scores[0]
            critical_trend = critical_counts[-1] - critical_counts[0]
            high_trend = high_counts[-1] - high_counts[0]
        else:
            risk_trend = 0
            critical_trend = 0
            high_trend = 0
        
        # Calculate averages
        avg_risk = sum(risk_scores) / len(risk_scores)
        avg_critical = sum(critical_counts) / len(critical_counts)
        avg_high = sum(high_counts) / len(high_counts)
        
        # Determine trend status
        if risk_trend < -10:
            risk_status = "✅ IMPROVING"
        elif risk_trend < 0:
            risk_status = "🟢 SLIGHTLY IMPROVING"
        elif risk_trend < 10:
            risk_status = "🟡 STABLE"
        elif risk_trend < 20:
            risk_status = "🟠 DETERIORATING"
        else:
            risk_status = "🔴 CRITICAL DECLINE"
        
        return {
            'total_scans': len(recent_scans),
            'period': f'Last {days} days',
            'risk_trend': risk_trend,
            'risk_trend_percent': round((risk_trend / max(risk_scores[0], 1)) * 100, 1) if risk_scores[0] > 0 else 0,
            'risk_status': risk_status,
            'avg_risk_score': round(avg_risk, 1),
            'avg_critical': round(avg_critical, 1),
            'avg_high': round(avg_high, 1),
            'current_risk': risk_scores[-1] if risk_scores else 0,
            'best_risk': min(risk_scores),
            'worst_risk': max(risk_scores),
            'critical_trend': critical_trend,
            'high_trend': high_trend,
            'dates': [s['date'] for s in recent_scans],
            'risk_scores': risk_scores,
            'critical_counts': critical_counts,
            'high_counts': high_counts
        }
    
    # ========== 2. RISK SCORING ==========
    
    def calculate_risk_score(self, open_ports, services, vulnerabilities):
        """Calculate automated risk score"""
        base_score = 0
        
        # Critical ports (high risk)
        critical_ports = [445, 3389, 23, 21, 512, 513, 514, 1524, 6667]
        for port in open_ports:
            if port in critical_ports:
                base_score += 15
        
        # Service based scoring
        high_risk_services = ['telnet', 'ftp', 'smb', 'netbios', 'vnc', 'x11']
        for service in services:
            if service.lower() in high_risk_services:
                base_score += 10
        
        # Vulnerability based scoring
        if vulnerabilities:
            for vuln in vulnerabilities:
                cvss = vuln.get('cvss', 0)
                if cvss >= 9:
                    base_score += 20
                elif cvss >= 7:
                    base_score += 10
                elif cvss >= 5:
                    base_score += 5
        
        # Calculate final score (0-100)
        risk_score = min(100, base_score)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "CRITICAL"
            color = "🔴"
        elif risk_score >= 50:
            risk_level = "HIGH"
            color = "🟠"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            color = "🟡"
        else:
            risk_level = "LOW"
            color = "🟢"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'color': color,
            'recommendation': self._get_recommendation(risk_score)
        }
    
    def _get_recommendation(self, risk_score):
        """Get recommendation based on risk score"""
        if risk_score >= 70:
            return "IMMEDIATE ACTION REQUIRED - Patch critical vulnerabilities"
        elif risk_score >= 50:
            return "High risk - Address vulnerabilities within 7 days"
        elif risk_score >= 30:
            return "Medium risk - Plan remediation within 30 days"
        else:
            return "Low risk - Continue monitoring"
    
    # ========== 3. COMPLIANCE CHECKING ==========
    
    def check_compliance(self, scan_data):
        """Check compliance with standards"""
        results = {
            'pci_dss': self._check_pci_dss(scan_data),
            'hipaa': self._check_hipaa(scan_data),
            'gdpr': self._check_gdpr(scan_data),
            'iso27001': self._check_iso27001(scan_data)
        }
        
        # Calculate overall compliance score
        passed = sum(1 for r in results.values() if r.get('compliant', False))
        total = len(results)
        overall_score = (passed / total) * 100 if total > 0 else 0
        
        return {
            'standards': results,
            'overall_score': overall_score,
            'overall_status': 'COMPLIANT' if overall_score >= 80 else 'NON-COMPLIANT'
        }
    
    def _check_pci_dss(self, scan_data):
        """PCI-DSS compliance check"""
        issues = []
        open_ports = scan_data.get('open_ports', [])
        
        # Check for prohibited ports
        prohibited_ports = [23, 21, 513, 514, 512]
        for port in prohibited_ports:
            if port in open_ports:
                issues.append(f"Prohibited port {port} open (Telnet/FTP/r-services)")
        
        # Check for weak encryption
        services = scan_data.get('services', [])
        if 'telnet' in services:
            issues.append("Telnet uses unencrypted communication")
        
        compliant = len(issues) == 0
        
        return {
            'compliant': compliant,
            'issues': issues,
            'score': 100 - (len(issues) * 20) if not compliant else 100
        }
    
    def _check_hipaa(self, scan_data):
        """HIPAA compliance check"""
        issues = []
        open_ports = scan_data.get('open_ports', [])
        
        # Check for unencrypted services
        unencrypted_services = [21, 23, 80, 139, 445]
        for port in unencrypted_services:
            if port in open_ports:
                issues.append(f"Unencrypted service on port {port}")
        
        # Check for remote access
        remote_ports = [22, 3389, 5900]
        remote_found = [p for p in remote_ports if p in open_ports]
        if remote_found:
            issues.append(f"Remote access ports open: {remote_found}")
        
        compliant = len(issues) <= 2
        
        return {
            'compliant': compliant,
            'issues': issues,
            'score': max(0, 100 - (len(issues) * 15))
        }
    
    def _check_gdpr(self, scan_data):
        """GDPR compliance check"""
        issues = []
        
        # Check for data exposure risks
        sensitive_ports = [3306, 5432, 27017, 1433]
        open_ports = scan_data.get('open_ports', [])
        
        for port in sensitive_ports:
            if port in open_ports:
                issues.append(f"Database port {port} exposed")
        
        compliant = len(issues) == 0
        
        return {
            'compliant': compliant,
            'issues': issues,
            'score': 100 - (len(issues) * 25)
        }
    
    def _check_iso27001(self, scan_data):
        """ISO 27001 compliance check"""
        issues = []
        open_ports = scan_data.get('open_ports', [])
        
        # Check for unnecessary services
        unnecessary_ports = [23, 21, 513, 514, 512, 6667]
        for port in unnecessary_ports:
            if port in open_ports:
                issues.append(f"Unnecessary service on port {port}")
        
        compliant = len(issues) <= 1
        
        return {
            'compliant': compliant,
            'issues': issues,
            'score': max(0, 100 - (len(issues) * 20))
        }
    
    # ========== 4. SLA MONITORING ==========
    
    def check_sla(self, target, uptime_history):
        """Check SLA compliance"""
        if not uptime_history:
            return {'error': 'No uptime data available'}
        
        total_checks = len(uptime_history)
        up_checks = sum(1 for u in uptime_history if u.get('status') == 'up')
        uptime_percentage = (up_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # SLA tiers
        if uptime_percentage >= 99.99:
            sla_level = "PLATINUM (99.99%)"
            compliant = True
        elif uptime_percentage >= 99.9:
            sla_level = "GOLD (99.9%)"
            compliant = True
        elif uptime_percentage >= 99:
            sla_level = "SILVER (99%)"
            compliant = True
        elif uptime_percentage >= 95:
            sla_level = "BRONZE (95%)"
            compliant = False
        else:
            sla_level = "BELOW STANDARD"
            compliant = False
        
        # Calculate downtime
        downtime_count = total_checks - up_checks
        avg_downtime = downtime_count * 5  # Assuming 5 min intervals
        
        return {
            'target': target,
            'uptime_percentage': round(uptime_percentage, 3),
            'sla_level': sla_level,
            'compliant': compliant,
            'total_checks': total_checks,
            'up_checks': up_checks,
            'downtime_events': downtime_count,
            'estimated_downtime_minutes': avg_downtime,
            'recommendation': self._get_sla_recommendation(uptime_percentage)
        }
    
    def _get_sla_recommendation(self, uptime):
        """Get SLA recommendation"""
        if uptime >= 99.99:
            return "Excellent uptime - Maintain current infrastructure"
        elif uptime >= 99.9:
            return "Good uptime - Monitor for potential issues"
        elif uptime >= 99:
            return "Adequate uptime - Consider infrastructure improvements"
        else:
            return "Poor uptime - Immediate infrastructure review required"
    
    # ========== 5. PREDICTIVE ANALYSIS ==========
    
    def predict_risk_trend(self, days_ahead=7):
        """Predict future risk trends"""
        if len(self.scan_history) < 3:
            return {'error': 'Need at least 3 scans for prediction'}
        
        recent_scans = self.scan_history[-10:]  # Last 10 scans
        risk_scores = [s['risk_score'] for s in recent_scans]
        
        # Simple linear regression for prediction
        n = len(risk_scores)
        if n < 2:
            return {'error': 'Insufficient data'}
        
        x = list(range(n))
        y = risk_scores
        
        # Calculate trend line
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = mean_y - slope * mean_x
        
        # Predict future values
        predictions = []
        for i in range(1, days_ahead + 1):
            pred_x = n + i - 1
            pred_y = slope * pred_x + intercept
            predictions.append({
                'day': i,
                'predicted_risk': round(max(0, min(100, pred_y)), 1)
            })
        
        # Calculate confidence based on data consistency
        residuals = [y[i] - (slope * x[i] + intercept) for i in range(n)]
        variance = sum(r**2 for r in residuals) / n if n > 0 else 0
        confidence = max(50, min(95, 100 - (variance * 2)))
        
        # Determine alert level
        last_risk = risk_scores[-1] if risk_scores else 0
        predicted_risk = predictions[-1]['predicted_risk'] if predictions else last_risk
        risk_change = predicted_risk - last_risk
        
        if risk_change > 20:
            alert = "🔴 CRITICAL ALERT - Risk expected to increase significantly"
        elif risk_change > 10:
            alert = "🟠 HIGH ALERT - Risk trend upward"
        elif risk_change > 5:
            alert = "🟡 MEDIUM ALERT - Slight risk increase expected"
        elif risk_change < -10:
            alert = "🟢 POSITIVE - Risk expected to decrease"
        else:
            alert = "ℹ️ STABLE - No major risk changes expected"
        
        return {
            'predictions': predictions,
            'current_risk': last_risk,
            'predicted_risk_7d': predictions[-1]['predicted_risk'] if predictions else last_risk,
            'risk_change': round(risk_change, 1),
            'confidence': round(confidence, 1),
            'alert': alert,
            'trend': 'increasing' if slope > 0 else 'decreasing',
            'slope': round(slope, 2)
        }
    
    def predict_breach_probability(self, scan_data):
        """Predict potential breach probability"""
        risk_score = scan_data.get('risk_score', 0)
        open_ports = scan_data.get('open_ports', [])
        critical_count = scan_data.get('critical_count', 0)
        
        # Calculate breach probability based on multiple factors
        probability = 0
        
        # Factor 1: Risk score (40% weight)
        probability += (risk_score / 100) * 40
        
        # Factor 2: Critical vulnerabilities (30% weight)
        probability += min(1, critical_count / 5) * 30
        
        # Factor 3: High-risk open ports (20% weight)
        high_risk_ports = [445, 3389, 23, 21, 139]
        high_risk_count = sum(1 for p in open_ports if p in high_risk_ports)
        probability += min(1, high_risk_count / 3) * 20
        
        # Factor 4: Historical trend (10% weight)
        if len(self.scan_history) > 1:
            last_risk = self.scan_history[-1].get('risk_score', risk_score)
            if risk_score > last_risk:
                probability += 10
        
        probability = min(100, probability)
        
        # Determine risk level
        if probability >= 70:
            level = "CRITICAL"
            color = "🔴"
            action = "IMMEDIATE PATCHING REQUIRED"
        elif probability >= 50:
            level = "HIGH"
            color = "🟠"
            action = "Schedule urgent security review"
        elif probability >= 30:
            level = "MEDIUM"
            color = "🟡"
            action = "Monitor and plan remediation"
        else:
            level = "LOW"
            color = "🟢"
            action = "Continue regular monitoring"
        
        return {
            'probability': round(probability, 1),
            'level': level,
            'color': color,
            'action': action,
            'factors': {
                'risk_score_contribution': round((risk_score / 100) * 40, 1),
                'critical_vulns_contribution': round(min(1, critical_count / 5) * 30, 1),
                'open_ports_contribution': round(min(1, high_risk_count / 3) * 20, 1)
            }
        }
    
    # ========== FORMAT OUTPUT ==========
    
    def format_trend_output(self, trend_data):
        """Format trend analysis output"""
        output = []
        output.append("\n" + "="*70)
        output.append("📈 TREND ANALYSIS")
        output.append("="*70)
        
        if 'error' in trend_data:
            output.append(f"   {trend_data['error']}")
            return "\n".join(output)
        
        output.append(f"\n📊 Period: {trend_data['period']}")
        output.append(f"📡 Total Scans: {trend_data['total_scans']}")
        output.append(f"\n📉 RISK TREND:")
        output.append(f"   Current Risk: {trend_data['current_risk']}/100")
        output.append(f"   Average Risk: {trend_data['avg_risk_score']}/100")
        output.append(f"   Best Risk: {trend_data['best_risk']}/100")
        output.append(f"   Worst Risk: {trend_data['worst_risk']}/100")
        output.append(f"   Trend: {trend_data['risk_trend']:+.1f} points ({trend_data['risk_trend_percent']:+.1f}%)")
        output.append(f"   Status: {trend_data['risk_status']}")
        
        output.append(f"\n🔄 VULNERABILITY TRENDS:")
        output.append(f"   Critical: {trend_data['critical_trend']:+.1f} change")
        output.append(f"   High: {trend_data['high_trend']:+.1f} change")
        
        return "\n".join(output)
    
    def format_compliance_output(self, compliance_data):
        """Format compliance output"""
        output = []
        output.append("\n" + "="*70)
        output.append("✅ COMPLIANCE CHECK")
        output.append("="*70)
        
        output.append(f"\n📊 Overall Compliance Score: {compliance_data['overall_score']:.1f}%")
        output.append(f"📋 Overall Status: {compliance_data['overall_status']}")
        
        for std, data in compliance_data['standards'].items():
            status = "✅ PASS" if data['compliant'] else "❌ FAIL"
            output.append(f"\n{std.upper()}: {status} ({data['score']}%)")
            if data['issues']:
                for issue in data['issues']:
                    output.append(f"   • {issue}")
        
        return "\n".join(output)
    
    def format_sla_output(self, sla_data):
        """Format SLA output"""
        output = []
        output.append("\n" + "="*70)
        output.append("⏱️ SLA MONITORING")
        output.append("="*70)
        
        if 'error' in sla_data:
            output.append(f"   {sla_data['error']}")
            return "\n".join(output)
        
        output.append(f"\n📡 Target: {sla_data['target']}")
        output.append(f"📊 Uptime: {sla_data['uptime_percentage']}%")
        output.append(f"🏆 SLA Level: {sla_data['sla_level']}")
        
        status = "✅ COMPLIANT" if sla_data['compliant'] else "❌ NON-COMPLIANT"
        output.append(f"📋 Status: {status}")
        
        output.append(f"\n📈 Statistics:")
        output.append(f"   Total Checks: {sla_data['total_checks']}")
        output.append(f"   Successful: {sla_data['up_checks']}")
        output.append(f"   Downtime Events: {sla_data['downtime_events']}")
        output.append(f"   Est. Downtime: {sla_data['estimated_downtime_minutes']} minutes")
        
        output.append(f"\n💡 Recommendation: {sla_data['recommendation']}")
        
        return "\n".join(output)
    
    def format_prediction_output(self, prediction_data):
        """Format prediction output"""
        output = []
        output.append("\n" + "="*70)
        output.append("🔮 PREDICTIVE ANALYSIS")
        output.append("="*70)
        
        if 'error' in prediction_data:
            output.append(f"   {prediction_data['error']}")
            return "\n".join(output)
        
        output.append(f"\n📊 Current Risk: {prediction_data['current_risk']}/100")
        output.append(f"🎯 Predicted Risk (7 days): {prediction_data['predicted_risk_7d']}/100")
        output.append(f"📈 Risk Change: {prediction_data['risk_change']:+.1f} points")
        output.append(f"🎯 Confidence: {prediction_data['confidence']}%")
        output.append(f"\n⚠️ Alert: {prediction_data['alert']}")
        
        output.append(f"\n📅 Day-by-Day Predictions:")
        for pred in prediction_data['predictions'][:7]:
            output.append(f"   Day {pred['day']}: {pred['predicted_risk']}/100")
        
        return "\n".join(output)
    
    def format_breach_output(self, breach_data):
        """Format breach probability output"""
        output = []
        output.append("\n" + "="*70)
        output.append("💀 BREACH PROBABILITY ANALYSIS")
        output.append("="*70)
        
        output.append(f"\n{breach_data['color']} Probability: {breach_data['probability']}%")
        output.append(f"📊 Risk Level: {breach_data['level']}")
        output.append(f"🎯 Recommended Action: {breach_data['action']}")
        
        output.append(f"\n📊 Probability Factors:")
        for factor, value in breach_data['factors'].items():
            output.append(f"   • {factor.replace('_', ' ').title()}: {value}%")
        
        return "\n".join(output)
    
    def format_risk_output(self, risk_data):
        """Format risk scoring output"""
        output = []
        output.append("\n" + "="*70)
        output.append("🎯 RISK ASSESSMENT")
        output.append("="*70)
        
        output.append(f"\n{risk_data['color']} Risk Score: {risk_data['score']}/100")
        output.append(f"📊 Risk Level: {risk_data['level']}")
        output.append(f"💡 Recommendation: {risk_data['recommendation']}")
        
        return "\n".join(output)
