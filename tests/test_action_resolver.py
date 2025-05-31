"""
Test suite for the action resolver
Validates turn resolution, IP management, and victory conditions
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from action_resolver import (
    resolve_turn,
    clamp_ip,
    check_victory_conditions,
    apply_round_end_effects,
    get_sid_by_codename
)

class TestActionResolver:
    
    def setup_method(self):
        """Set up test data before each test"""
        self.users = {
            'sid1': {
                'codename': 'Agent_A',
                'status': 'active',
                'ip': 10,
                'gadgets': ['spring_anvil'],
                'intel': []
            },
            'sid2': {
                'codename': 'Agent_B', 
                'status': 'active',
                'ip': 10,
                'gadgets': ['jetpack_skates'],
                'intel': []
            },
            'sid3': {
                'codename': 'Agent_C',
                'status': 'active',
                'ip': 10,
                'gadgets': [],
                'intel': []
            }
        }
        
        self.assets = {
            'central_server': None,
            'comm_tower': None,
            'data_vault': None,
            'operations_center': None,
            'safe_house_network': None
        }
    
    def test_clamp_ip(self):
        """Test IP clamping functionality"""
        assert clamp_ip(5) == 5
        assert clamp_ip(100) == 50  # max limit
        assert clamp_ip(-20) == -10  # min limit
        assert clamp_ip(25, max_ip=20) == 20
        assert clamp_ip(-15, min_ip=-5) == -5
    
    def test_safe_turn_resolution(self):
        """Test single player safe turn resolution"""
        submitted_actions = {
            'sid1': {
                'offense': '',  # No offense = safe turn
                'defense': 'underground',
                'target': None,
                'ip_spend': 0,
                'banner_message': ''
            }
        }
        
        results = resolve_turn(self.users, submitted_actions, 1)
        
        assert len(results) == 1
        assert results[0]['codename'] == 'Agent_A'
        assert results[0]['action_type'] == 'safe_turn'
        assert results[0]['ip_delta'] == 1
        assert results[0]['new_ip'] == 11
        assert self.users['sid1']['ip'] == 11
    
    def test_assassination_vs_safe_house(self):
        """Test assassination vs safe house interaction"""
        submitted_actions = {
            'sid1': {
                'offense': 'assassination',
                'defense': 'bodyguard_detail',
                'target': 'Agent_B',
                'ip_spend': 0,
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
        
        results = resolve_turn(self.users, submitted_actions, 1)
        
        # Find attacker and defender results
        attacker_result = next(r for r in results if r['codename'] == 'Agent_A' and r['action_type'] == 'attack')
        defender_result = next(r for r in results if r['codename'] == 'Agent_B' and r['action_type'] == 'defense')
        
        # Assassination vs Safe House should fail
        assert attacker_result['success'] == False
        assert attacker_result['ip_delta'] == -1
        assert defender_result['ip_delta'] == 1
        assert self.users['sid1']['status'] == 'exposed'  # Attacker exposed
        assert self.users['sid2']['status'] == 'active'   # Defender unchanged
    
    def test_multiple_attackers_same_target(self):
        """Test multiple players attacking the same target"""
        # Agent A and Agent C both attack Agent B
        submitted_actions = {
            'sid1': {
                'offense': 'assassination',
                'defense': 'mobile_operations',
                'target': 'Agent_B',
                'ip_spend': 3,  # Higher IP spend
                'banner_message': ''
            },
            'sid2': {
                'offense': '',
                'defense': 'safe_house',
                'target': None,
                'ip_spend': 0,
                'banner_message': ''
            },
            'sid3': {
                'offense': 'surveillance',
                'defense': 'underground',
                'target': 'Agent_B',
                'ip_spend': 1,  # Lower IP spend
                'banner_message': ''
            }
        }
        
        results = resolve_turn(self.users, submitted_actions, 1)
        
        # Agent A should attack first (higher IP spend)
        attack_results = [r for r in results if r['action_type'] == 'attack']
        attack_results.sort(key=lambda x: x['codename'])
        
        assert len(attack_results) == 2
        # Both attacks should process, but Agent A's should be resolved first due to higher IP spend
    
    def test_cannot_attack_captured_player(self):
        """Test that captured/eliminated players cannot be attacked"""
        self.users['sid2']['status'] = 'captured'
        
        submitted_actions = {
            'sid1': {
                'offense': 'assassination',
                'defense': 'safe_house',
                'target': 'Agent_B',
                'ip_spend': 0,
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
        
        results = resolve_turn(self.users, submitted_actions, 1)
        
        # Should have a failed attack result
        failed_attack = next(r for r in results if r['action_type'] == 'failed_attack')
        assert failed_attack['codename'] == 'Agent_A'
        assert 'captured' in failed_attack['description']
    
    def test_victory_last_spy_standing(self):
        """Test Last Spy Standing victory condition"""
        # Set two players to eliminated status
        self.users['sid2']['status'] = 'eliminated'
        self.users['sid3']['status'] = 'captured'
        
        victory = check_victory_conditions(self.users, self.assets)
        
        assert victory is not None
        assert victory['condition'] == 'Last Spy Standing'
        assert victory['winners'] == ['Agent_A']
    
    def test_victory_network_control(self):
        """Test Network Control victory condition"""
        # Give Agent A control of 3 assets
        self.assets['central_server'] = 'Agent_A'
        self.assets['comm_tower'] = 'Agent_A'
        self.assets['data_vault'] = 'Agent_A'
        
        victory = check_victory_conditions(self.users, self.assets)
        
        assert victory is not None
        assert victory['condition'] == 'Network Control'
        assert victory['winners'] == ['Agent_A']
    
    def test_victory_intelligence_supremacy(self):
        """Test Intelligence Supremacy victory condition"""
        # Give Agent A lots of intel (simplified test)
        self.users['sid1']['intel'] = [
            'intel1', 'intel2', 'intel3', 'intel4', 'intel5', 'intel6'
        ]
        
        victory = check_victory_conditions(self.users, self.assets)
        
        assert victory is not None
        assert victory['condition'] == 'Intelligence Supremacy'
        assert victory['winners'] == ['Agent_A']
    
    def test_no_victory_conditions_met(self):
        """Test when no victory conditions are met"""
        victory = check_victory_conditions(self.users, self.assets)
        assert victory is None
    
    def test_get_sid_by_codename(self):
        """Test SID lookup by codename"""
        assert get_sid_by_codename(self.users, 'Agent_A') == 'sid1'
        assert get_sid_by_codename(self.users, 'Agent_B') == 'sid2'
        assert get_sid_by_codename(self.users, 'NonExistent') is None
    
    def test_round_end_effects_asset_yields(self):
        """Test asset yields at end of round"""
        # Give Agent A control of an asset
        self.assets['central_server'] = 'Agent_A'
        
        original_ip = self.users['sid1']['ip']
        apply_round_end_effects(self.users, self.assets)
        
        # Should gain 2 IP from asset yield, but lose 1 IP from gadget upkeep (net +1)
        expected_ip = original_ip + 2 - 1  # Asset yield minus gadget upkeep
        assert self.users['sid1']['ip'] == expected_ip
    
    def test_round_end_effects_gadget_upkeep(self):
        """Test gadget upkeep costs"""
        # Agent A has 1 gadget, should cost 1 IP
        original_ip = self.users['sid1']['ip']
        apply_round_end_effects(self.users, self.assets)
        
        assert self.users['sid1']['ip'] == original_ip - 1
        assert len(self.users['sid1']['gadgets']) == 1  # Gadget kept
    
    def test_gadget_removal_insufficient_ip(self):
        """Test gadget removal when unable to pay upkeep"""
        # Set low IP and multiple gadgets
        self.users['sid1']['ip'] = 1
        self.users['sid1']['gadgets'] = ['gadget1', 'gadget2', 'gadget3']
        
        apply_round_end_effects(self.users, self.assets)
        
        # Should only keep 1 gadget (equal to available IP)
        assert self.users['sid1']['ip'] == 0
        assert len(self.users['sid1']['gadgets']) == 1

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 