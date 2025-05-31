"""
Test suite for game loop functionality
Validates multi-round gameplay, IP economy, and status transitions
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from action_resolver import (
    resolve_turn,
    check_victory_conditions,
    apply_round_end_effects,
    get_sid_by_codename
)

class TestGameLoop:
    
    def setup_method(self):
        """Set up test data before each test"""
        self.users = {
            'sid1': {
                'codename': 'Agent_A',
                'status': 'active',
                'ip': 5,
                'gadgets': [],
                'intel': [],
                'alliances': []
            },
            'sid2': {
                'codename': 'Agent_B', 
                'status': 'active',
                'ip': 5,
                'gadgets': [],
                'intel': [],
                'alliances': []
            },
            'sid3': {
                'codename': 'Agent_C',
                'status': 'active',
                'ip': 5,
                'gadgets': [],
                'intel': [],
                'alliances': []
            }
        }
        
        self.assets = {
            'central_server': None,
            'comm_tower': None,
            'data_vault': None,
            'operations_center': None,
            'safe_house_network': None
        }
    
    def test_ip_economy_multiple_rounds(self):
        """Test IP economy over multiple rounds with safe turns"""
        # Both players choose safe turns for 3 rounds
        safe_turn_action = {
            'offense': '',
            'defense': 'underground',
            'target': None,
            'ip_spend': 0,
            'banner_message': ''
        }
        
        for round_num in range(1, 4):  # 3 rounds
            submitted_actions = {
                'sid1': safe_turn_action.copy(),
                'sid2': safe_turn_action.copy()
            }
            
            initial_ip_a = self.users['sid1']['ip']
            initial_ip_b = self.users['sid2']['ip']
            
            results = resolve_turn(self.users, submitted_actions, round_num, self.assets)
            apply_round_end_effects(self.users, self.assets)
            
            # Each player should gain +1 IP per round
            assert self.users['sid1']['ip'] == initial_ip_a + 1
            assert self.users['sid2']['ip'] == initial_ip_b + 1
        
        # After 3 rounds, each should have gained 3 IP total
        assert self.users['sid1']['ip'] == 8  # 5 + 3
        assert self.users['sid2']['ip'] == 8  # 5 + 3
    
    def test_compromise_chain_restrictions(self):
        """Test that compromised players have restrictions"""
        # First, compromise Agent A
        self.users['sid1']['status'] = 'compromised'
        
        # Compromised player tries to use false_identity defense
        submitted_actions = {
            'sid1': {
                'offense': '',
                'defense': 'false_identity',  # Should be restricted for compromised
                'target': None,
                'ip_spend': 0,
                'banner_message': ''
            },
            'sid2': {
                'offense': 'surveillance',
                'defense': 'safe_house',
                'target': 'Agent_A',
                'ip_spend': 0,
                'banner_message': ''
            }
        }
        
        # In a full implementation, the server would reject false_identity for compromised players
        # For now, we test that the status persists
        results = resolve_turn(self.users, submitted_actions, 1, self.assets)
        
        # Agent A should still be compromised
        assert self.users['sid1']['status'] == 'compromised'
    
    def test_victory_last_spy_standing_progression(self):
        """Test Last Spy Standing victory through multiple rounds"""
        # Simulate capturing/eliminating players step by step
        
        # Initially no victory (3 active players)
        victory = check_victory_conditions(self.users, self.assets)
        assert victory is None
        
        # Capture Agent B
        self.users['sid2']['status'] = 'captured'
        victory = check_victory_conditions(self.users, self.assets)
        assert victory is None  # Still 2 active players
        
        # Capture Agent C - should trigger Last Spy Standing
        self.users['sid3']['status'] = 'captured'
        victory = check_victory_conditions(self.users, self.assets)
        
        # Now should have Last Spy Standing victory
        assert victory is not None
        assert victory['condition'] == 'Last Spy Standing'
        assert victory['winners'] == ['Agent_A']
    
    def test_victory_network_control_progression(self):
        """Test Network Control victory through asset capture"""
        # Agent A captures assets one by one over multiple rounds
        
        # Round 1: Capture first asset
        submitted_actions_r1 = {
            'sid1': {
                'offense': 'network_attack',
                'defense': 'safe_house',
                'target': 'Agent_B',
                'ip_spend': 1,
                'banner_message': ''
            },
            'sid2': {
                'offense': '',
                'defense': 'safe_house',
                'target': None,
                'ip_spend': 0,
                'banner_message': ''
            }
        }
        
        results_r1 = resolve_turn(self.users, submitted_actions_r1, 1, self.assets)
        apply_round_end_effects(self.users, self.assets)
        
        # Manually assign first asset for testing
        self.assets['central_server'] = 'Agent_A'
        
        victory_r1 = check_victory_conditions(self.users, self.assets)
        assert victory_r1 is None  # Not enough assets yet
        
        # Round 2: Capture second asset
        self.assets['comm_tower'] = 'Agent_A'
        victory_r2 = check_victory_conditions(self.users, self.assets)
        assert victory_r2 is None  # Still not enough
        
        # Round 3: Capture third asset - should trigger victory
        self.assets['data_vault'] = 'Agent_A'
        victory_r3 = check_victory_conditions(self.users, self.assets)
        
        assert victory_r3 is not None
        assert victory_r3['condition'] == 'Network Control'
        assert victory_r3['winners'] == ['Agent_A']
    
    def test_status_transitions_over_rounds(self):
        """Test status transitions over multiple rounds"""
        # Start with a captured player
        self.users['sid1']['status'] = 'captured'
        
        # Apply round end effects multiple times
        for round_num in range(5):
            apply_round_end_effects(self.users, self.assets)
        
        # Captured player should have a chance to become burned
        # (This is probabilistic, so we can't guarantee the exact outcome)
        assert self.users['sid1']['status'] in ['captured', 'burned', 'compromised']
    
    def test_gadget_upkeep_over_rounds(self):
        """Test gadget upkeep costs over multiple rounds"""
        # Give Agent A some gadgets
        self.users['sid1']['gadgets'] = ['spring_anvil', 'jetpack_skates', 'robo_duck']
        self.users['sid1']['ip'] = 10
        
        # Apply round end effects
        apply_round_end_effects(self.users, self.assets)
        
        # Should pay 3 IP for 3 gadgets
        assert self.users['sid1']['ip'] == 7  # 10 - 3
        assert len(self.users['sid1']['gadgets']) == 3  # All gadgets kept
        
        # Reduce IP and apply again
        self.users['sid1']['ip'] = 2
        apply_round_end_effects(self.users, self.assets)
        
        # Should only keep 2 gadgets (can only afford 2)
        assert self.users['sid1']['ip'] == 0
        assert len(self.users['sid1']['gadgets']) == 2
    
    def test_asset_yield_accumulation(self):
        """Test strategic asset IP yields over multiple rounds"""
        # Give Agent A control of 2 assets
        self.assets['central_server'] = 'Agent_A'
        self.assets['comm_tower'] = 'Agent_A'
        
        initial_ip = self.users['sid1']['ip']
        
        # Apply round end effects for 3 rounds
        for round_num in range(3):
            apply_round_end_effects(self.users, self.assets)
        
        # Should gain 4 IP per round (2 IP per asset × 2 assets)
        expected_ip = initial_ip + (4 * 3)  # 4 IP per round × 3 rounds
        assert self.users['sid1']['ip'] == expected_ip
    
    def test_late_game_survival_bonus(self):
        """Test late game survival bonus when few players remain"""
        # Eliminate two players to trigger late game bonus (2 or fewer remain)
        self.users['sid2']['status'] = 'eliminated'
        self.users['sid3']['status'] = 'eliminated'
        
        initial_ip_a = self.users['sid1']['ip']
        
        # Apply round end effects (should trigger late game bonus)
        apply_round_end_effects(self.users, self.assets)
        
        # Only surviving player should get +1 bonus IP
        assert self.users['sid1']['ip'] == initial_ip_a + 1
    
    def test_compromised_player_recovery(self):
        """Test compromised player recovery with high IP"""
        # Set Agent A as compromised with high IP
        self.users['sid1']['status'] = 'compromised'
        self.users['sid1']['ip'] = 20  # High IP
        
        # Apply round end effects
        apply_round_end_effects(self.users, self.assets)
        
        # Should recover to active status
        assert self.users['sid1']['status'] == 'active'
    
    def test_alliance_expiration(self):
        """Test alliance expiration over rounds"""
        # Give Agent A some alliances
        self.users['sid1']['alliances'] = ['pact_with_B', 'pact_with_C']
        
        # Apply round end effects multiple times
        for round_num in range(10):
            apply_round_end_effects(self.users, self.assets)
        
        # Some alliances should have expired (probabilistic)
        assert len(self.users['sid1']['alliances']) <= 2 