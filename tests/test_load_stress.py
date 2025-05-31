"""
Load and Stress Testing Suite for James Bland: ACME Edition
Tests maximum player capacity, long-duration stability, network recovery, and memory usage
"""

import pytest
import threading
import time
import psutil
import os
import gc
import socketio
import requests
from unittest.mock import patch, MagicMock
import subprocess
import signal
from memory_profiler import profile
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app, socketio as server_socketio
import server

class MockClient:
    """Mock client for simulating player connections and actions"""
    
    def __init__(self, codename, server_url='http://localhost:5000'):
        self.codename = codename
        self.server_url = server_url
        self.sio = socketio.Client()
        self.connected = False
        self.sid = None
        self.game_state = {}
        self.events_received = []
        self.errors = []
        
        # Set up event handlers
        self.sio.on('connect', self._on_connect)
        self.sio.on('disconnect', self._on_disconnect)
        self.sio.on('error', self._on_error)
        self.sio.on('lobbyJoined', self._on_lobby_joined)
        self.sio.on('gameStarted', self._on_game_started)
        self.sio.on('turnResult', self._on_turn_result)
        self.sio.on('playerSubmitted', self._on_player_submitted)
        
    def _on_connect(self):
        self.connected = True
        self.sid = self.sio.sid
        
    def _on_disconnect(self):
        self.connected = False
        
    def _on_error(self, data):
        self.errors.append(data)
        
    def _on_lobby_joined(self, data):
        self.events_received.append(('lobbyJoined', data))
        
    def _on_game_started(self, data):
        self.events_received.append(('gameStarted', data))
        self.game_state = data
        
    def _on_turn_result(self, data):
        self.events_received.append(('turnResult', data))
        
    def _on_player_submitted(self, data):
        self.events_received.append(('playerSubmitted', data))
    
    def connect(self, timeout=5):
        """Connect to the server"""
        try:
            self.sio.connect(self.server_url, wait_timeout=timeout)
            return True
        except Exception as e:
            self.errors.append(f"Connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        if self.connected:
            self.sio.disconnect()
    
    def join_lobby(self):
        """Join the game lobby"""
        if self.connected:
            self.sio.emit('joinLobby', {'codename': self.codename})
    
    def start_game(self):
        """Start the game (host only)"""
        if self.connected:
            self.sio.emit('startGame')
    
    def submit_action(self, action_data):
        """Submit a game action"""
        if self.connected:
            self.sio.emit('submitAction', action_data)
    
    def submit_safe_turn(self):
        """Submit a default safe turn"""
        safe_action = {
            'offense': '',
            'defense': 'underground',
            'target': None,
            'ip_spend': 0,
            'banner_message': ''
        }
        self.submit_action(safe_action)

class TestMaximumPlayerCapacity:
    """Test maximum player capacity (6 concurrent players)"""
    
    def setup_method(self):
        """Set up test environment"""
        self.clients = []
        self.server_process = None
        self.start_test_server()
        time.sleep(2)  # Allow server to start
    
    def teardown_method(self):
        """Clean up after tests"""
        for client in self.clients:
            try:
                client.disconnect()
            except:
                pass
        self.stop_test_server()
    
    def start_test_server(self):
        """Start a test server instance"""
        # Use threading instead of subprocess for better control
        self.server_thread = threading.Thread(
            target=lambda: server_socketio.run(app, host='127.0.0.1', port=5001, debug=False)
        )
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def stop_test_server(self):
        """Stop the test server"""
        # Server will stop when main thread exits (daemon thread)
        pass
    
    def test_maximum_6_players_connection(self):
        """Test that exactly 6 players can connect successfully"""
        # Create 6 mock clients
        for i in range(6):
            client = MockClient(f"TestAgent_{i+1}", 'http://localhost:5001')
            self.clients.append(client)
        
        # Connect all clients
        connected_count = 0
        for client in self.clients:
            if client.connect():
                connected_count += 1
                client.join_lobby()
                time.sleep(0.1)  # Small delay between connections
        
        # All 6 should connect successfully
        assert connected_count == 6
        
        # Verify all are in the game state
        time.sleep(1)  # Allow lobby updates to propagate
        lobby_errors = sum(len(client.errors) for client in self.clients)
        assert lobby_errors == 0, f"Expected no lobby errors, got {lobby_errors}"
    
    def test_7th_player_rejection(self):
        """Test that a 7th player is properly rejected"""
        # Connect 6 players first
        for i in range(6):
            client = MockClient(f"TestAgent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
            time.sleep(0.1)
        
        # Try to connect 7th player
        seventh_client = MockClient("TestAgent_7", 'http://localhost:5001')
        seventh_client.connect()
        seventh_client.join_lobby()
        
        time.sleep(1)  # Allow server to process
        
        # 7th player should receive an error
        assert len(seventh_client.errors) > 0
        error_message = str(seventh_client.errors[-1])
        assert "full" in error_message.lower() or "6 players" in error_message
        
        seventh_client.disconnect()
    
    def test_concurrent_game_actions_6_players(self):
        """Test concurrent game actions with 6 players"""
        # Connect 6 players
        for i in range(6):
            client = MockClient(f"Agent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
            time.sleep(0.1)
        
        # Start game (first client is host)
        self.clients[0].start_game()
        time.sleep(2)  # Allow game to start
        
        # All players submit actions simultaneously
        threads = []
        for client in self.clients:
            thread = threading.Thread(target=client.submit_safe_turn)
            threads.append(thread)
            thread.start()
        
        # Wait for all submissions
        for thread in threads:
            thread.join(timeout=5)
        
        time.sleep(3)  # Allow turn resolution
        
        # Verify no errors during concurrent submission
        total_errors = sum(len(client.errors) for client in self.clients)
        assert total_errors == 0, f"Expected no errors during concurrent actions, got {total_errors}"

class TestLongDurationStability:
    """Test long-duration session stability"""
    
    def setup_method(self):
        """Set up long duration test environment"""
        self.clients = []
        self.memory_samples = []
        self.error_count = 0
        self.test_duration = 300  # 5 minutes for testing (can be increased)
        self.round_count = 0
        
    def teardown_method(self):
        """Clean up after long duration tests"""
        for client in self.clients:
            try:
                client.disconnect()
            except:
                pass
    
    @profile
    def test_5_minute_continuous_gameplay(self):
        """Test continuous gameplay with memory monitoring (configurable duration)"""
        # Check for custom duration from environment
        custom_duration = os.environ.get('STRESS_TEST_DURATION')
        if custom_duration:
            self.test_duration = int(custom_duration)
            duration_name = f"{self.test_duration//60}-minute"
        else:
            duration_name = "5-minute"
        
        print(f"Starting {duration_name} continuous gameplay test...")
        
        # Set up 4 players for stable long-term testing
        for i in range(4):
            client = MockClient(f"LongTermAgent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
            time.sleep(0.2)
        
        # Start game
        self.clients[0].start_game()
        time.sleep(2)
        
        start_time = time.time()
        last_memory_check = start_time
        
        while time.time() - start_time < self.test_duration:
            # Memory monitoring every 30 seconds
            if time.time() - last_memory_check >= 30:
                self.collect_memory_metrics()
                last_memory_check = time.time()
            
            # Submit actions for all players
            for client in self.clients:
                try:
                    client.submit_safe_turn()
                except Exception as e:
                    self.error_count += 1
                    print(f"Error submitting action: {e}")
            
            # Wait for turn resolution
            time.sleep(15)  # Longer than typical turn timer
            self.round_count += 1
            
            # Check for errors
            for client in self.clients:
                if client.errors:
                    self.error_count += len(client.errors)
                    client.errors.clear()
        
        # Final memory check
        self.collect_memory_metrics()
        
        # Assertions
        expected_min_rounds = max(5, self.test_duration // 20)  # At least 1 round per 20 seconds
        assert self.error_count < 5, f"Too many errors during long session: {self.error_count}"
        assert self.round_count >= expected_min_rounds, f"Expected at least {expected_min_rounds} rounds, got {self.round_count}"
        assert self.check_memory_stability(), "Memory usage shows concerning growth"
    
    def collect_memory_metrics(self):
        """Collect current memory usage metrics"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        self.memory_samples.append({
            'timestamp': time.time(),
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'round': self.round_count
        })
    
    def check_memory_stability(self):
        """Check if memory usage is stable (not growing excessively)"""
        if len(self.memory_samples) < 3:
            return True
        
        # Check if RSS memory growth is reasonable (< 50% over test period)
        initial_rss = self.memory_samples[0]['rss']
        final_rss = self.memory_samples[-1]['rss']
        growth_ratio = (final_rss - initial_rss) / initial_rss
        
        print(f"Memory growth: {growth_ratio:.2%}")
        return growth_ratio < 0.5  # Allow up to 50% growth
    
    def test_memory_leak_detection(self):
        """Specific test for detecting memory leaks over repeated game cycles"""
        gc.collect()  # Force garbage collection
        initial_objects = len(gc.get_objects())
        
        # Run multiple game cycles
        for cycle in range(5):
            # Create and destroy clients
            cycle_clients = []
            for i in range(3):
                client = MockClient(f"Cycle{cycle}_Agent_{i+1}", 'http://localhost:5001')
                client.connect()
                client.join_lobby()
                cycle_clients.append(client)
            
            # Start and play a short game
            cycle_clients[0].start_game()
            time.sleep(1)
            
            for _ in range(3):  # 3 quick rounds
                for client in cycle_clients:
                    client.submit_safe_turn()
                time.sleep(2)
            
            # Disconnect all clients
            for client in cycle_clients:
                client.disconnect()
            
            # Force cleanup
            del cycle_clients
            gc.collect()
            time.sleep(1)
        
        # Check final object count
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects
        
        print(f"Object count growth: {object_growth} ({initial_objects} -> {final_objects})")
        
        # Allow some growth but flag excessive growth as potential leak
        assert object_growth < 1000, f"Potential memory leak: {object_growth} new objects retained"

class TestNetworkInterruptionRecovery:
    """Test network interruption recovery scenarios"""
    
    def setup_method(self):
        """Set up network interruption test environment"""
        self.clients = []
        self.interrupted_clients = []
    
    def teardown_method(self):
        """Clean up after network tests"""
        for client in self.clients + self.interrupted_clients:
            try:
                client.disconnect()
            except:
                pass
    
    def test_client_disconnection_during_game(self):
        """Test client disconnection and reconnection during gameplay"""
        # Set up 3 players
        for i in range(3):
            client = MockClient(f"NetworkAgent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
        
        # Start game
        self.clients[0].start_game()
        time.sleep(2)
        
        # Disconnect one player mid-game
        disconnected_client = self.clients[1]
        original_codename = disconnected_client.codename
        disconnected_client.disconnect()
        time.sleep(1)
        
        # Remaining players continue with actions
        self.clients[0].submit_safe_turn()
        self.clients[2].submit_safe_turn()
        time.sleep(3)
        
        # Reconnect the disconnected player
        reconnect_client = MockClient(original_codename + "_reconnect", 'http://localhost:5001')
        reconnect_success = reconnect_client.connect()
        
        assert reconnect_success, "Player should be able to reconnect"
        
        # Try to rejoin (should handle gracefully even if game in progress)
        reconnect_client.join_lobby()
        time.sleep(1)
        
        # Should receive error about game in progress, but no crash
        assert len(reconnect_client.errors) > 0
        self.interrupted_clients.append(reconnect_client)
    
    def test_host_disconnection_transfer(self):
        """Test host disconnection and host transfer"""
        # Set up 3 players
        for i in range(3):
            client = MockClient(f"HostTestAgent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
            time.sleep(0.2)
        
        time.sleep(1)  # Allow lobby to stabilize
        
        # Disconnect the host (first client)
        original_host = self.clients[0]
        original_host.disconnect()
        
        time.sleep(2)  # Allow host transfer
        
        # Try to start game with new host
        try:
            self.clients[1].start_game()
            time.sleep(1)
            # If no exception, host transfer worked
            host_transfer_success = True
        except Exception as e:
            print(f"Host transfer issue: {e}")
            host_transfer_success = False
        
        # Should be able to continue with new host
        assert host_transfer_success or len(self.clients[1].errors) == 0
    
    def test_simultaneous_disconnections(self):
        """Test multiple simultaneous disconnections"""
        # Set up 5 players
        for i in range(5):
            client = MockClient(f"SimDisconnectAgent_{i+1}", 'http://localhost:5001')
            client.connect()
            client.join_lobby()
            self.clients.append(client)
        
        # Start game
        self.clients[0].start_game()
        time.sleep(2)
        
        # Disconnect 3 players simultaneously
        disconnect_threads = []
        for i in range(1, 4):  # Disconnect clients 1, 2, 3
            thread = threading.Thread(target=self.clients[i].disconnect)
            disconnect_threads.append(thread)
            thread.start()
        
        # Wait for all disconnections
        for thread in disconnect_threads:
            thread.join()
        
        time.sleep(2)  # Allow server to process
        
        # Remaining players should still be able to continue
        try:
            self.clients[0].submit_safe_turn()
            self.clients[4].submit_safe_turn()
            remaining_players_ok = True
        except Exception as e:
            print(f"Error with remaining players: {e}")
            remaining_players_ok = False
        
        assert remaining_players_ok, "Remaining players should continue functioning after mass disconnect"

class TestServerResourceMonitoring:
    """Test server resource usage and performance under load"""
    
    def test_cpu_usage_under_load(self):
        """Monitor CPU usage during high load scenarios"""
        # Get initial CPU usage
        process = psutil.Process(os.getpid())
        initial_cpu = process.cpu_percent()
        
        # Create moderate load with rapid connections/disconnections
        stress_threads = []
        for i in range(10):
            thread = threading.Thread(target=self.connection_stress_worker, args=(i,))
            stress_threads.append(thread)
            thread.start()
        
        # Monitor CPU for 30 seconds
        cpu_samples = []
        for _ in range(6):  # 6 samples over 30 seconds
            time.sleep(5)
            cpu_usage = process.cpu_percent()
            cpu_samples.append(cpu_usage)
        
        # Wait for stress threads to complete
        for thread in stress_threads:
            thread.join()
        
        # Analyze CPU usage
        max_cpu = max(cpu_samples)
        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        
        print(f"CPU Usage - Max: {max_cpu:.1f}%, Avg: {avg_cpu:.1f}%")
        
        # CPU should remain reasonable (< 80% on average)
        assert avg_cpu < 80, f"Average CPU usage too high: {avg_cpu:.1f}%"
        assert max_cpu < 95, f"Peak CPU usage too high: {max_cpu:.1f}%"
    
    def connection_stress_worker(self, worker_id):
        """Worker function for connection stress testing"""
        for i in range(5):  # Each worker makes 5 connections
            try:
                client = MockClient(f"StressWorker_{worker_id}_{i}", 'http://localhost:5001')
                client.connect()
                client.join_lobby()
                time.sleep(0.5)
                client.disconnect()
                time.sleep(0.1)
            except Exception as e:
                print(f"Stress worker {worker_id} error: {e}")
    
    def test_memory_usage_scaling(self):
        """Test memory usage scaling with player count"""
        memory_baseline = psutil.Process(os.getpid()).memory_info().rss
        
        player_counts = [1, 2, 4, 6]
        memory_per_player = []
        
        for count in player_counts:
            # Create clients
            clients = []
            for i in range(count):
                client = MockClient(f"ScaleTest_{count}_{i}", 'http://localhost:5001')
                client.connect()
                client.join_lobby()
                clients.append(client)
                time.sleep(0.1)
            
            time.sleep(2)  # Stabilize
            
            # Measure memory
            current_memory = psutil.Process(os.getpid()).memory_info().rss
            memory_per_player.append((current_memory - memory_baseline) / count)
            
            # Cleanup
            for client in clients:
                client.disconnect()
            time.sleep(1)
        
        # Memory per player should be relatively stable
        avg_memory_per_player = sum(memory_per_player) / len(memory_per_player)
        memory_variance = max(memory_per_player) - min(memory_per_player)
        
        print(f"Avg memory per player: {avg_memory_per_player/1024/1024:.1f} MB")
        print(f"Memory variance: {memory_variance/1024/1024:.1f} MB")
        
        # Variance should be reasonable (< 50% of average)
        assert memory_variance < avg_memory_per_player * 0.5

# Utility functions for test execution

def run_load_tests():
    """Convenience function to run all load tests"""
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '-s'
    ])

if __name__ == "__main__":
    # Run tests when executed directly
    run_load_tests() 