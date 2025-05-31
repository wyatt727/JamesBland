#!/usr/bin/env python3
"""
Automated Stress Testing Script for James Bland: ACME Edition
Runs comprehensive load and stress tests with detailed reporting
"""

import subprocess
import time
import psutil
import os
import json
import sys
import argparse
from datetime import datetime, timedelta
import threading
import signal

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class StressTestRunner:
    """Orchestrates and monitors stress testing"""
    
    def __init__(self, duration_minutes=10, max_players=6, report_file=None):
        self.duration_minutes = duration_minutes
        self.max_players = max_players
        self.report_file = report_file or f"stress_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.server_process = None
        self.test_results = {
            'start_time': datetime.now().isoformat(),
            'duration_minutes': duration_minutes,
            'max_players': max_players,
            'tests': {},
            'system_metrics': {
                'cpu_usage': [],
                'memory_usage': [],
                'network_connections': []
            },
            'errors': [],
            'summary': {}
        }
        self.monitoring_active = False
        self.monitoring_thread = None
    
    def start_server(self):
        """Start the game server for testing"""
        print("Starting game server...")
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                sys.executable, '-c',
                'import sys; sys.path.insert(0, "."); '
                'from server import app, socketio; '
                'socketio.run(app, host="127.0.0.1", port=5000, debug=False)'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(3)  # Allow server to start
            
            # Verify server is running
            if self.server_process.poll() is None:
                print("✓ Game server started successfully")
                return True
            else:
                print("✗ Failed to start game server")
                return False
                
        except Exception as e:
            print(f"✗ Error starting server: {e}")
            return False
    
    def stop_server(self):
        """Stop the game server"""
        if self.server_process:
            print("Stopping game server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            print("✓ Game server stopped")
    
    def start_system_monitoring(self):
        """Start monitoring system resources"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_system_resources)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        print("✓ System monitoring started")
    
    def stop_system_monitoring(self):
        """Stop monitoring system resources"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        print("✓ System monitoring stopped")
    
    def _monitor_system_resources(self):
        """Monitor system resources in background"""
        start_time = time.time()
        
        while self.monitoring_active:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # Memory usage
                memory = psutil.virtual_memory()
                
                # Network connections (count of established connections)
                connections = len([conn for conn in psutil.net_connections() 
                                 if conn.status == 'ESTABLISHED'])
                
                timestamp = time.time() - start_time
                
                self.test_results['system_metrics']['cpu_usage'].append({
                    'timestamp': timestamp,
                    'value': cpu_percent
                })
                
                self.test_results['system_metrics']['memory_usage'].append({
                    'timestamp': timestamp,
                    'value': memory.percent,
                    'available_mb': memory.available / 1024 / 1024
                })
                
                self.test_results['system_metrics']['network_connections'].append({
                    'timestamp': timestamp,
                    'value': connections
                })
                
            except Exception as e:
                self.test_results['errors'].append(f"Monitoring error: {str(e)}")
            
            time.sleep(5)  # Sample every 5 seconds
    
    def run_capacity_tests(self):
        """Run maximum player capacity tests"""
        print("\n=== Running Maximum Player Capacity Tests ===")
        
        test_name = "maximum_player_capacity"
        self.test_results['tests'][test_name] = {
            'start_time': time.time(),
            'status': 'running',
            'subtests': {}
        }
        
        try:
            # Test 1: Maximum 6 players
            print("Testing maximum 6 player capacity...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestMaximumPlayerCapacity::test_maximum_6_players_connection',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['6_players'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Test 2: 7th player rejection
            print("Testing 7th player rejection...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestMaximumPlayerCapacity::test_7th_player_rejection',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['7th_player_rejection'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Test 3: Concurrent actions
            print("Testing concurrent actions with 6 players...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestMaximumPlayerCapacity::test_concurrent_game_actions_6_players',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['concurrent_actions'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Determine overall status
            all_passed = all(test['returncode'] == 0 for test in 
                           self.test_results['tests'][test_name]['subtests'].values())
            
            self.test_results['tests'][test_name]['status'] = 'passed' if all_passed else 'failed'
            print(f"✓ Capacity tests {'PASSED' if all_passed else 'FAILED'}")
            
        except Exception as e:
            self.test_results['tests'][test_name]['status'] = 'error'
            self.test_results['tests'][test_name]['error'] = str(e)
            print(f"✗ Capacity tests ERROR: {e}")
    
    def run_duration_tests(self):
        """Run long-duration stability tests"""
        print(f"\n=== Running Long-Duration Tests ({self.duration_minutes} minutes) ===")
        
        test_name = "long_duration_stability"
        self.test_results['tests'][test_name] = {
            'start_time': time.time(),
            'status': 'running',
            'subtests': {}
        }
        
        try:
            # Modify test duration for this run
            duration_seconds = self.duration_minutes * 60
            
            # Memory leak detection test
            print("Testing memory leak detection...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestLongDurationStability::test_memory_leak_detection',
                '-v', '--tb=short', '-s'
            ], capture_output=True, text=True, timeout=duration_seconds + 60)
            
            self.test_results['tests'][test_name]['subtests']['memory_leak'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Continuous gameplay test (adjusted for specified duration)
            if self.duration_minutes >= 5:  # Only run if we have enough time
                print(f"Testing {self.duration_minutes}-minute continuous gameplay...")
                
                # Create a custom test with adjusted duration
                test_env = os.environ.copy()
                test_env['STRESS_TEST_DURATION'] = str(duration_seconds)
                
                result = subprocess.run([
                    sys.executable, '-m', 'pytest', 
                    'tests/test_load_stress.py::TestLongDurationStability::test_5_minute_continuous_gameplay',
                    '-v', '--tb=short', '-s'
                ], capture_output=True, text=True, timeout=duration_seconds + 120, env=test_env)
                
                self.test_results['tests'][test_name]['subtests']['continuous_gameplay'] = {
                    'returncode': result.returncode,
                    'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            
            # Determine overall status
            all_passed = all(test['returncode'] == 0 for test in 
                           self.test_results['tests'][test_name]['subtests'].values())
            
            self.test_results['tests'][test_name]['status'] = 'passed' if all_passed else 'failed'
            print(f"✓ Duration tests {'PASSED' if all_passed else 'FAILED'}")
            
        except Exception as e:
            self.test_results['tests'][test_name]['status'] = 'error'
            self.test_results['tests'][test_name]['error'] = str(e)
            print(f"✗ Duration tests ERROR: {e}")
    
    def run_network_tests(self):
        """Run network interruption recovery tests"""
        print("\n=== Running Network Interruption Tests ===")
        
        test_name = "network_interruption_recovery"
        self.test_results['tests'][test_name] = {
            'start_time': time.time(),
            'status': 'running',
            'subtests': {}
        }
        
        try:
            # Test 1: Client disconnection during game
            print("Testing client disconnection recovery...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestNetworkInterruptionRecovery::test_client_disconnection_during_game',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['client_disconnection'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Test 2: Host disconnection transfer
            print("Testing host disconnection transfer...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestNetworkInterruptionRecovery::test_host_disconnection_transfer',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['host_transfer'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Test 3: Simultaneous disconnections
            print("Testing simultaneous disconnections...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestNetworkInterruptionRecovery::test_simultaneous_disconnections',
                '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['simultaneous_disconnections'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Determine overall status
            all_passed = all(test['returncode'] == 0 for test in 
                           self.test_results['tests'][test_name]['subtests'].values())
            
            self.test_results['tests'][test_name]['status'] = 'passed' if all_passed else 'failed'
            print(f"✓ Network tests {'PASSED' if all_passed else 'FAILED'}")
            
        except Exception as e:
            self.test_results['tests'][test_name]['status'] = 'error'
            self.test_results['tests'][test_name]['error'] = str(e)
            print(f"✗ Network tests ERROR: {e}")
    
    def run_resource_tests(self):
        """Run server resource monitoring tests"""
        print("\n=== Running Server Resource Tests ===")
        
        test_name = "server_resource_monitoring"
        self.test_results['tests'][test_name] = {
            'start_time': time.time(),
            'status': 'running',
            'subtests': {}
        }
        
        try:
            # Test 1: CPU usage under load
            print("Testing CPU usage under load...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestServerResourceMonitoring::test_cpu_usage_under_load',
                '-v', '--tb=short', '-s'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['cpu_usage'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Test 2: Memory usage scaling
            print("Testing memory usage scaling...")
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_load_stress.py::TestServerResourceMonitoring::test_memory_usage_scaling',
                '-v', '--tb=short', '-s'
            ], capture_output=True, text=True, timeout=300)
            
            self.test_results['tests'][test_name]['subtests']['memory_scaling'] = {
                'returncode': result.returncode,
                'duration': time.time() - self.test_results['tests'][test_name]['start_time'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Determine overall status
            all_passed = all(test['returncode'] == 0 for test in 
                           self.test_results['tests'][test_name]['subtests'].values())
            
            self.test_results['tests'][test_name]['status'] = 'passed' if all_passed else 'failed'
            print(f"✓ Resource tests {'PASSED' if all_passed else 'FAILED'}")
            
        except Exception as e:
            self.test_results['tests'][test_name]['status'] = 'error'
            self.test_results['tests'][test_name]['error'] = str(e)
            print(f"✗ Resource tests ERROR: {e}")
    
    def generate_summary(self):
        """Generate test summary and statistics"""
        print("\n=== Generating Test Summary ===")
        
        total_tests = len(self.test_results['tests'])
        passed_tests = sum(1 for test in self.test_results['tests'].values() if test['status'] == 'passed')
        failed_tests = sum(1 for test in self.test_results['tests'].values() if test['status'] == 'failed')
        error_tests = sum(1 for test in self.test_results['tests'].values() if test['status'] == 'error')
        
        # System metrics summary
        cpu_usage = self.test_results['system_metrics']['cpu_usage']
        memory_usage = self.test_results['system_metrics']['memory_usage']
        
        cpu_avg = sum(sample['value'] for sample in cpu_usage) / len(cpu_usage) if cpu_usage else 0
        cpu_max = max(sample['value'] for sample in cpu_usage) if cpu_usage else 0
        
        memory_avg = sum(sample['value'] for sample in memory_usage) / len(memory_usage) if memory_usage else 0
        memory_max = max(sample['value'] for sample in memory_usage) if memory_usage else 0
        
        self.test_results['summary'] = {
            'end_time': datetime.now().isoformat(),
            'total_duration_minutes': (time.time() - time.mktime(datetime.fromisoformat(self.test_results['start_time']).timetuple())) / 60,
            'test_results': {
                'total': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'errors': error_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'system_performance': {
                'cpu_usage_avg': cpu_avg,
                'cpu_usage_max': cpu_max,
                'memory_usage_avg': memory_avg,
                'memory_usage_max': memory_max
            },
            'total_errors': len(self.test_results['errors']),
            'recommendations': self.generate_recommendations()
        }
    
    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check system performance
        cpu_usage = self.test_results['system_metrics']['cpu_usage']
        memory_usage = self.test_results['system_metrics']['memory_usage']
        
        if cpu_usage:
            avg_cpu = sum(sample['value'] for sample in cpu_usage) / len(cpu_usage)
            max_cpu = max(sample['value'] for sample in cpu_usage)
            
            if avg_cpu > 70:
                recommendations.append("HIGH: Average CPU usage exceeded 70%. Consider optimizing server performance.")
            if max_cpu > 90:
                recommendations.append("CRITICAL: Peak CPU usage exceeded 90%. Server may struggle under load.")
        
        if memory_usage:
            max_memory = max(sample['value'] for sample in memory_usage)
            if max_memory > 80:
                recommendations.append("HIGH: Memory usage exceeded 80%. Monitor for memory leaks.")
        
        # Check test failures
        failed_tests = [name for name, test in self.test_results['tests'].items() if test['status'] in ['failed', 'error']]
        if failed_tests:
            recommendations.append(f"MEDIUM: The following tests failed: {', '.join(failed_tests)}")
        
        # Check error count
        if len(self.test_results['errors']) > 10:
            recommendations.append("HIGH: Many errors occurred during testing. Review error logs.")
        
        if not recommendations:
            recommendations.append("GOOD: All stress tests passed with good performance metrics.")
        
        return recommendations
    
    def save_report(self):
        """Save test results to JSON file"""
        print(f"\nSaving test report to: {self.report_file}")
        
        try:
            with open(self.report_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"✓ Test report saved successfully")
        except Exception as e:
            print(f"✗ Error saving report: {e}")
    
    def print_summary(self):
        """Print test summary to console"""
        summary = self.test_results['summary']
        
        print("\n" + "="*60)
        print("STRESS TEST SUMMARY")
        print("="*60)
        print(f"Duration: {summary['total_duration_minutes']:.1f} minutes")
        print(f"Tests: {summary['test_results']['total']} total")
        print(f"  ✓ Passed: {summary['test_results']['passed']}")
        print(f"  ✗ Failed: {summary['test_results']['failed']}")
        print(f"  ! Errors: {summary['test_results']['errors']}")
        print(f"Success Rate: {summary['test_results']['success_rate']:.1f}%")
        
        print(f"\nSystem Performance:")
        print(f"  CPU Usage: {summary['system_performance']['cpu_usage_avg']:.1f}% avg, {summary['system_performance']['cpu_usage_max']:.1f}% peak")
        print(f"  Memory Usage: {summary['system_performance']['memory_usage_avg']:.1f}% avg, {summary['system_performance']['memory_usage_max']:.1f}% peak")
        
        print(f"\nRecommendations:")
        for rec in summary['recommendations']:
            print(f"  • {rec}")
        
        print(f"\nDetailed report saved to: {self.report_file}")
        print("="*60)
    
    def run_all_tests(self):
        """Run the complete stress testing suite"""
        print("🚀 Starting James Bland Stress Testing Suite")
        print(f"Duration: {self.duration_minutes} minutes")
        print(f"Max Players: {self.max_players}")
        
        try:
            # Start server
            if not self.start_server():
                return False
            
            # Start monitoring
            self.start_system_monitoring()
            
            # Run all test suites
            self.run_capacity_tests()
            self.run_duration_tests()
            self.run_network_tests()
            self.run_resource_tests()
            
            # Generate summary
            self.generate_summary()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error during testing: {e}")
            self.test_results['errors'].append(f"Fatal error: {str(e)}")
            return False
        finally:
            # Cleanup
            self.stop_system_monitoring()
            self.stop_server()
            self.save_report()
            self.print_summary()

def main():
    """Main entry point for stress testing"""
    parser = argparse.ArgumentParser(description='Run James Bland stress tests')
    parser.add_argument('--duration', type=int, default=10, 
                       help='Test duration in minutes (default: 10)')
    parser.add_argument('--max-players', type=int, default=6,
                       help='Maximum players to test (default: 6)')
    parser.add_argument('--report', type=str,
                       help='Custom report filename')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick tests only (5 minute duration)')
    
    args = parser.parse_args()
    
    if args.quick:
        args.duration = 5
    
    # Create and run stress tester
    runner = StressTestRunner(
        duration_minutes=args.duration,
        max_players=args.max_players,
        report_file=args.report
    )
    
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 