#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Enhancements Module
Parallel scanning, Distributed scanning, Scan scheduling
Resource monitoring, Resume capability
"""

import subprocess
import threading
import time
import os
import psutil
import json
from datetime import datetime, timedelta
from queue import Queue
import multiprocessing

class PerformanceEnhancer:
    def __init__(self):
        self.scan_queue = Queue()
        self.active_scans = []
        self.scan_results = {}
        self.scheduled_jobs = []
        self.resume_data = {}
        self.scan_log = []
        
    # ========== 1. PARALLEL SCANNING ==========
    
    def parallel_scan(self, targets, ports="1-1000", scan_type="-sS", max_workers=5):
        """Scan multiple targets simultaneously"""
        results = {}
        threads = []
        
        def scan_target(target):
            """Scan a single target"""
            cmd = f"nmap {scan_type} -p {ports} {target}"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                results[target] = {
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode,
                    'timestamp': datetime.now().isoformat()
                }
            except subprocess.TimeoutExpired:
                results[target] = {'error': 'Timeout', 'timestamp': datetime.now().isoformat()}
            except Exception as e:
                results[target] = {'error': str(e), 'timestamp': datetime.now().isoformat()}
        
        # Start threads for each target
        for target in targets:
            if len(threads) >= max_workers:
                # Wait for some threads to complete
                for t in threads:
                    t.join(timeout=1)
                threads = [t for t in threads if t.is_alive()]
            
            thread = threading.Thread(target=scan_target, args=(target,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        return results
    
    def get_parallel_scan_status(self):
        """Get status of parallel scans"""
        status = {
            'active_scans': len([t for t in self.active_scans if t.is_alive()]),
            'completed_scans': len(self.scan_results),
            'total_scans': len(self.active_scans) + len(self.scan_results)
        }
        return status
    
    # ========== 2. DISTRIBUTED SCANNING ==========
    
    def distributed_scan(self, targets, workers_config):
        """Scan using multiple machines"""
        results = {}
        
        for worker_name, worker_config in workers_config.items():
            print(f"[*] Using worker: {worker_name}")
            
            # For local workers
            if worker_config['type'] == 'local':
                for target in targets:
                    cmd = f"nmap -sS -p 1-1000 {target}"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    results[f"{worker_name}_{target}"] = {
                        'worker': worker_name,
                        'target': target,
                        'output': result.stdout,
                        'error': result.stderr
                    }
            
            # For remote workers (SSH)
            elif worker_config['type'] == 'remote':
                try:
                    ssh_cmd = f"ssh {worker_config['user']}@{worker_config['host']} 'nmap -sS -p 1-1000 {targets[0]}'"
                    result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
                    results[f"{worker_name}_{targets[0]}"] = {
                        'worker': worker_name,
                        'target': targets[0],
                        'output': result.stdout,
                        'error': result.stderr
                    }
                except Exception as e:
                    results[f"{worker_name}_error"] = {'error': str(e)}
        
        return results
    
    def add_worker(self, name, config):
        """Add a worker for distributed scanning"""
        worker = {
            'name': name,
            'type': config.get('type', 'local'),
            'host': config.get('host', 'localhost'),
            'user': config.get('user', ''),
            'status': 'available'
        }
        return worker
    
    # ========== 3. SCAN SCHEDULING ==========
    
    def schedule_scan(self, target, scan_config, schedule_time):
        """Schedule a scan for later execution"""
        job = {
            'id': len(self.scheduled_jobs) + 1,
            'target': target,
            'config': scan_config,
            'schedule_time': schedule_time,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat()
        }
        self.scheduled_jobs.append(job)
        return job
    
    def run_scheduled_scans(self):
        """Run all scheduled scans that are due"""
        now = datetime.now()
        results = []
        
        for job in self.scheduled_jobs:
            if job['status'] == 'scheduled':
                job_time = datetime.fromisoformat(job['schedule_time'])
                if job_time <= now:
                    # Run the scan
                    cmd = f"nmap {job['config'].get('options', '-sS')} -p {job['config'].get('ports', '1-1000')} {job['target']}"
                    try:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                        job['status'] = 'completed'
                        job['result'] = result.stdout
                        job['completed_at'] = datetime.now().isoformat()
                        results.append(job)
                    except Exception as e:
                        job['status'] = 'failed'
                        job['error'] = str(e)
        
        return results
    
    def list_scheduled_jobs(self):
        """List all scheduled jobs"""
        return self.scheduled_jobs
    
    def cancel_scheduled_job(self, job_id):
        """Cancel a scheduled job"""
        for job in self.scheduled_jobs:
            if job['id'] == job_id:
                job['status'] = 'cancelled'
                return True
        return False
    
    def cron_expression_to_time(self, cron_expr):
        """Convert cron expression to next run time"""
        # Simple implementation - can be extended
        parts = cron_expr.split()
        if len(parts) == 5:
            minute, hour, day, month, weekday = parts
            
            now = datetime.now()
            next_time = now.replace(minute=int(minute) if minute != '*' else now.minute,
                                    hour=int(hour) if hour != '*' else now.hour,
                                    second=0, microsecond=0)
            
            if next_time <= now:
                next_time += timedelta(hours=1)
            
            return next_time.isoformat()
        
        return None
    
    # ========== 4. RESOURCE MONITORING ==========
    
    def get_resource_usage(self):
        """Get current CPU and memory usage"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used': psutil.virtual_memory().used,
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_threads': threading.active_count(),
            'timestamp': datetime.now().isoformat()
        }
    
    def monitor_resources(self, interval=5, duration=None):
        """Monitor system resources over time"""
        monitoring_data = []
        start_time = datetime.now()
        
        while True:
            data = self.get_resource_usage()
            monitoring_data.append(data)
            
            if duration and (datetime.now() - start_time).seconds >= duration:
                break
            
            time.sleep(interval)
        
        return monitoring_data
    
    def optimize_scan_settings(self, resource_usage):
        """Optimize scan settings based on resource usage"""
        recommendations = []
        
        if resource_usage['cpu_percent'] > 80:
            recommendations.append("High CPU usage detected. Consider reducing parallel scans.")
            recommendations.append("Use --max-retries 1 to reduce load")
            recommendations.append("Use -T3 instead of -T4/T5")
        
        if resource_usage['memory_percent'] > 85:
            recommendations.append("High memory usage detected.")
            recommendations.append("Reduce number of parallel scans")
            recommendations.append("Close other applications")
        
        if resource_usage['disk_usage'] > 90:
            recommendations.append("Low disk space. Clean up old scan results.")
        
        return recommendations
    
    # ========== 5. RESUME CAPABILITY ==========
    
    def save_scan_state(self, scan_id, scan_data):
        """Save scan state for later resume"""
        state_file = f"scan_state_{scan_id}.json"
        state_data = {
            'scan_id': scan_id,
            'data': scan_data,
            'saved_at': datetime.now().isoformat(),
            'completed_ports': scan_data.get('completed_ports', []),
            'pending_ports': scan_data.get('pending_ports', [])
        }
        
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=4)
        
        return state_file
    
    def load_scan_state(self, scan_id):
        """Load previously saved scan state"""
        state_file = f"scan_state_{scan_id}.json"
        
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def resume_scan(self, scan_id):
        """Resume an interrupted scan"""
        state = self.load_scan_state(scan_id)
        
        if not state:
            return {'error': 'No saved state found for this scan ID'}
        
        # Resume from where it left off
        pending_ports = state.get('pending_ports', [])
        
        if not pending_ports:
            return {'message': 'Scan already completed', 'data': state.get('data')}
        
        # Continue scan on pending ports
        target = state['data'].get('target')
        ports = ','.join(map(str, pending_ports))
        
        cmd = f"nmap -sS -p {ports} {target}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        return {
            'scan_id': scan_id,
            'resumed_from': state['saved_at'],
            'completed_ports': state['completed_ports'],
            'new_results': result.stdout,
            'status': 'completed'
        }
    
    def auto_save_scan(self, scan_id, target, current_port, total_ports):
        """Auto-save scan progress"""
        scan_data = {
            'target': target,
            'current_port': current_port,
            'total_ports': total_ports,
            'progress': (current_port / total_ports) * 100,
            'completed_ports': list(range(1, current_port + 1)),
            'pending_ports': list(range(current_port + 1, total_ports + 1))
        }
        
        self.save_scan_state(scan_id, scan_data)
        return scan_data
    
    # ========== UTILITY FUNCTIONS ==========
    
    def format_parallel_output(self, results):
        """Format parallel scan output"""
        output = []
        output.append("\n" + "="*70)
        output.append("⚡ PARALLEL SCAN RESULTS")
        output.append("="*70)
        
        for target, data in results.items():
            output.append(f"\n📡 Target: {target}")
            if 'error' in data:
                output.append(f"   ❌ Error: {data['error']}")
            else:
                if data['stdout']:
                    lines = data['stdout'].split('\n')
                    for line in lines[:20]:
                        if 'open' in line:
                            output.append(f"   {line}")
        
        return "\n".join(output)
    
    def format_resource_output(self, resource_data):
        """Format resource monitoring output"""
        output = []
        output.append("\n" + "="*70)
        output.append("📊 SYSTEM RESOURCE MONITORING")
        output.append("="*70)
        
        latest = resource_data[-1] if resource_data else {}
        
        output.append(f"\n🖥️ CPU Usage: {latest.get('cpu_percent', 0)}%")
        output.append(f"💾 Memory Usage: {latest.get('memory_percent', 0)}%")
        output.append(f"📀 Disk Usage: {latest.get('disk_usage', 0)}%")
        output.append(f"🔧 Active Threads: {latest.get('active_threads', 0)}")
        
        # Create progress bar for CPU
        cpu = latest.get('cpu_percent', 0)
        bar_length = 50
        filled = int(bar_length * cpu / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        output.append(f"\n📊 CPU Load: [{bar}] {cpu}%")
        
        # Create progress bar for Memory
        mem = latest.get('memory_percent', 0)
        filled = int(bar_length * mem / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        output.append(f"📊 Memory: [{bar}] {mem}%")
        
        return "\n".join(output)
    
    def format_schedule_output(self, jobs):
        """Format scheduled jobs output"""
        output = []
        output.append("\n" + "="*70)
        output.append("⏰ SCHEDULED SCANS")
        output.append("="*70)
        
        if not jobs:
            output.append("\n   No scheduled scans")
        else:
            for job in jobs:
                output.append(f"\n📋 Job ID: {job['id']}")
                output.append(f"   🎯 Target: {job['target']}")
                output.append(f"   ⏰ Scheduled: {job['schedule_time']}")
                output.append(f"   📊 Status: {job['status']}")
        
        return "\n".join(output)
