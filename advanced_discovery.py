#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Discovery Module - OPTIMIZED FOR SPEED
DNS caching, faster lookups
"""

import subprocess
import re
import dns.resolver
from functools import lru_cache
from datetime import datetime

class AdvancedDiscovery:
    def __init__(self):
        self.cache = {}
        
    # ========== DNS CACHING ==========
    
    @lru_cache(maxsize=200)
    def _dns_lookup(self, domain, record_type='A'):
        """Cached DNS lookup - FAST"""
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [str(rdata) for rdata in answers]
        except:
            return []
    
    # ========== PASSIVE RECONNAISSANCE (FAST) ==========
    
    def passive_recon(self, target):
        """Fast passive reconnaissance with caching"""
        
        # Check cache
        cache_key = f"recon_{target}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        results = []
        target = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Fast DNS lookups
        a_records = self._dns_lookup(target, 'A')
        for ip in a_records:
            results.append({'type': 'DNS_A', 'value': ip})
        
        mx_records = self._dns_lookup(target, 'MX')
        for mx in mx_records[:5]:  # Limit for speed
            results.append({'type': 'DNS_MX', 'value': mx})
        
        ns_records = self._dns_lookup(target, 'NS')
        for ns in ns_records[:5]:
            results.append({'type': 'DNS_NS', 'value': ns})
        
        txt_records = self._dns_lookup(target, 'TXT')
        for txt in txt_records[:3]:
            results.append({'type': 'DNS_TXT', 'value': txt[:100]})
        
        # Cache results
        self.cache[cache_key] = results
        return results
    
    # ========== EMAIL ENUMERATION (FAST) ==========
    
    def enumerate_emails(self, domain):
        """Fast email enumeration"""
        
        cache_key = f"emails_{domain}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        common_usernames = [
            'admin', 'info', 'support', 'sales', 'contact', 'webmaster',
            'postmaster', 'hostmaster', 'abuse', 'security', 'noc'
        ]
        
        emails = []
        for username in common_usernames:
            emails.append({
                'email': f"{username}@{domain}",
                'source': 'common_pattern',
                'confidence': 'LOW'
            })
        
        self.cache[cache_key] = emails
        return emails
    
    # ========== TECHNOLOGY FINGERPRINTING (FAST) ==========
    
    def fingerprint_technology(self, target):
        """Fast technology fingerprinting"""
        
        cache_key = f"tech_{target}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        technologies = []
        target = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Fast HTTP request
        try:
            import requests
            url = f"http://{target}"
            response = requests.get(url, timeout=5, headers={'User-Agent': 'T-8 Scanner'})
            
            server = response.headers.get('Server', '')
            if server:
                technologies.append({
                    'technology': 'Web Server',
                    'name': server,
                    'confidence': 'HIGH'
                })
            
            # Fast content checks
            if 'wordpress' in response.text.lower():
                technologies.append({'technology': 'CMS', 'name': 'WordPress', 'confidence': 'HIGH'})
            if 'jquery' in response.text.lower():
                technologies.append({'technology': 'JavaScript', 'name': 'jQuery', 'confidence': 'MEDIUM'})
                
        except:
            pass
        
        self.cache[cache_key] = technologies
        return technologies
    
    # ========== CLOUD DISCOVERY (FAST) ==========
    
    def discover_all_cloud_assets(self, domain):
        """Fast cloud discovery"""
        
        cache_key = f"cloud_{domain}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        assets = []
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Fast checks
        aws_urls = [
            f"https://{domain}.s3.amazonaws.com",
            f"https://{domain}.cloudfront.net"
        ]
        
        for url in aws_urls:
            try:
                import requests
                response = requests.head(url, timeout=3)
                if response.status_code != 404:
                    assets.append({
                        'cloud': 'AWS',
                        'type': 'S3 Bucket' if 's3' in url else 'CloudFront',
                        'url': url,
                        'status': 'found'
                    })
            except:
                pass
        
        self.cache[cache_key] = assets
        return assets
    
    # ========== OSINT INTEGRATION (PLACEHOLDER) ==========
    
    def shodan_lookup(self, target):
        return [{'source': 'Shodan', 'status': 'API key required'}]
    
    def censys_lookup(self, target):
        return [{'source': 'Censys', 'status': 'API key required'}]
    
    def virustotal_lookup(self, target):
        return [{'source': 'VirusTotal', 'status': 'API key required'}]
    
    # ========== FORMAT OUTPUT ==========
    
    def format_output(self, data_type, data):
        """Fast formatted output"""
        output = []
        output.append("\n" + "="*70)
        output.append(f"🔍 {data_type.upper()} (FAST)")
        output.append("="*70)
        
        if not data:
            output.append("   No data found")
        else:
            for item in data[:20]:  # Limit for speed
                if isinstance(item, dict):
                    for key, value in list(item.items())[:3]:
                        output.append(f"   • {key}: {value}")
                else:
                    output.append(f"   • {item}")
        
        return "\n".join(output)
