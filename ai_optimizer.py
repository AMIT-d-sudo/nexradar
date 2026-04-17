#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Smart Scan Optimization
Network speed के according auto timing adjust करता है
"""

import subprocess
import time
import re

class ScanOptimizer:
    def __init__(self):
        self.network_profile = {
            "latency": 0,
            "packet_loss": 0,
            "bandwidth": "unknown",
            "recommended_timing": "T3",
            "recommended_retries": 2,
            "recommended_rate": 100
        }
        
    def test_network(self, target):
        """Test network conditions to target"""
        try:
            # Ping test
            result = subprocess.run(['ping', '-c', '5', target], 
                                   capture_output=True, text=True, timeout=10)
            
            # Parse ping output
            avg_match = re.search(r'avg = (\d+\.\d+)', result.stdout)
            loss_match = re.search(r'(\d+)% packet loss', result.stdout)
            
            if avg_match:
                self.network_profile["latency"] = float(avg_match.group(1))
            if loss_match:
                self.network_profile["packet_loss"] = int(loss_match.group(1))
                
            # Determine network quality
            if self.network_profile["latency"] < 20 and self.network_profile["packet_loss"] == 0:
                self.network_profile["bandwidth"] = "excellent"
                self.network_profile["recommended_timing"] = "T4"
                self.network_profile["recommended_retries"] = 1
                self.network_profile["recommended_rate"] = 5000
            elif self.network_profile["latency"] < 50 and self.network_profile["packet_loss"] < 5:
                self.network_profile["bandwidth"] = "good"
                self.network_profile["recommended_timing"] = "T4"
                self.network_profile["recommended_retries"] = 2
                self.network_profile["recommended_rate"] = 2000
            elif self.network_profile["latency"] < 150:
                self.network_profile["bandwidth"] = "average"
                self.network_profile["recommended_timing"] = "T3"
                self.network_profile["recommended_retries"] = 2
                self.network_profile["recommended_rate"] = 500
            else:
                self.network_profile["bandwidth"] = "poor"
                self.network_profile["recommended_timing"] = "T2"
                self.network_profile["recommended_retries"] = 3
                self.network_profile["recommended_rate"] = 100
                
        except Exception as e:
            # Default profile if test fails
            self.network_profile = {
                "latency": 50,
                "packet_loss": 0,
                "bandwidth": "unknown",
                "recommended_timing": "T3",
                "recommended_retries": 2,
                "recommended_rate": 500
            }
        
        return self.network_profile
    
    def get_optimization_params(self, scan_type="default"):
        """Get optimized parameters based on network conditions"""
        params = {
            "timing": self.network_profile["recommended_timing"],
            "max_retries": self.network_profile["recommended_retries"],
            "min_rate": self.network_profile["recommended_rate"],
            "host_timeout": self._calculate_timeout(),
            "scan_delay": self._calculate_delay()
        }
        
        # Adjust for different scan types
        if scan_type == "stealth":
            params["timing"] = "T2"
            params["scan_delay"] = "1s"
        elif scan_type == "fast":
            params["timing"] = "T5"
            params["min_rate"] = 10000
        elif scan_type == "comprehensive":
            params["timing"] = "T3"
            params["max_retries"] = 3
            
        return params
    
    def _calculate_timeout(self):
        """Calculate appropriate host timeout"""
        latency = self.network_profile["latency"]
        if latency < 20:
            return "5m"
        elif latency < 50:
            return "10m"
        elif latency < 150:
            return "20m"
        else:
            return "30m"
    
    def _calculate_delay(self):
        """Calculate appropriate scan delay"""
        if self.network_profile["packet_loss"] > 10:
            return "500ms"
        elif self.network_profile["packet_loss"] > 5:
            return "200ms"
        else:
            return "0ms"
    
    def format_output(self, target, params):
        """Format optimization output"""
        output = []
        output.append("\n" + "="*70)
        output.append("⚡ SMART SCAN OPTIMIZATION")
        output.append("="*70)
        
        output.append(f"\n📡 Target: {target}")
        output.append(f"📊 Network Profile:")
        output.append(f"   • Latency: {self.network_profile['latency']}ms")
        output.append(f"   • Packet Loss: {self.network_profile['packet_loss']}%")
        output.append(f"   • Bandwidth: {self.network_profile['bandwidth'].upper()}")
        
        output.append(f"\n🎯 Recommended Parameters:")
        output.append(f"   • Timing Template: -{params['timing']}")
        output.append(f"   • Max Retries: --max-retries {params['max_retries']}")
        output.append(f"   • Min Rate: --min-rate {params['min_rate']}")
        output.append(f"   • Host Timeout: --host-timeout {params['host_timeout']}")
        
        if params['scan_delay'] != '0ms':
            output.append(f"   • Scan Delay: --scan-delay {params['scan_delay']}")
        
        output.append("\n💡 Optimization applied automatically!")
        output.append("="*70)
        
        return "\n".join(output)
