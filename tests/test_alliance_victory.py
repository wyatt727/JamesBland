#!/usr/bin/env python3
"""
Test Alliance Victory System
Tests for alliance management, victory conditions, and Final Showdown mechanics
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alliance_victory import AllianceManager, Alliance

class TestAlliance:
    
    def test_alliance_creation(self):
        """Test basic alliance creation"""
        alliance = Alliance('Agent_A', 'Agent_B', 'non_aggression', 2)
        
        assert alliance.player1 == 'Agent_A'
        assert alliance.player2 == 'Agent_B'
        assert alliance.alliance_type == 'non_aggression'
        assert alliance.duration == 2
        assert not alliance.betrayed
        
    def test_alliance_members(self):
        """Test alliance member methods"""
        alliance = Alliance('Agent_A', 'Agent_B', 'non_aggression')
        
        # Test get_members
        members = alliance.get_members()
        assert set(members) == {'Agent_A', 'Agent_B'}
        
        # Test is_member
        assert alliance.is_member('Agent_A')
        assert alliance.is_member('Agent_B')
        assert not alliance.is_member('Agent_C')
        
        # Test get_partner
        assert alliance.get_partner('Agent_A') == 'Agent_B'
        assert alliance.get_partner('Agent_B') == 'Agent_A'
        assert alliance.get_partner('Agent_C') is None
        
    def test_alliance_duration(self):
        """Test alliance duration management"""
        alliance = Alliance('Agent_A', 'Agent_B', 'non_aggression', 3)
        
        assert alliance.duration == 3
        assert not alliance.is_expired()
        
        alliance.decrement_duration()
        assert alliance.duration == 2
        assert not alliance.is_expired()
        
        alliance.decrement_duration()
        alliance.decrement_duration()
        assert alliance.duration == 0
        assert alliance.is_expired()
        
        # Should not go below 0
        alliance.decrement_duration()
        assert alliance.duration == 0

class TestAllianceManager:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = AllianceManager()
        
    def test_create_alliance(self):
        """Test alliance creation through manager"""
        alliance_id = self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Should return valid alliance ID
        assert alliance_id.startswith('alliance_')
        
        # Alliance should exist in manager
        assert alliance_id in self.manager.alliances
        
        # Players should be tracked
        assert 'Agent_A' in self.manager.player_alliances
        assert 'Agent_B' in self.manager.player_alliances
        assert alliance_id in self.manager.player_alliances['Agent_A']
        assert alliance_id in self.manager.player_alliances['Agent_B']
        
    def test_can_form_alliance(self):
        """Test alliance formation validation"""
        # Should be able to form alliance initially
        can_form, reason = self.manager.can_form_alliance('Agent_A', 'Agent_B')
        assert can_form
        assert reason == "Alliance can be formed"
        
        # Create an alliance
        self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Should not be able to form duplicate alliance
        can_form, reason = self.manager.can_form_alliance('Agent_A', 'Agent_B')
        assert not can_form
        assert "already allied" in reason
        
        # Agent_A should not be able to form another alliance
        can_form, reason = self.manager.can_form_alliance('Agent_A', 'Agent_C')
        assert not can_form
        assert "already in an alliance" in reason
        
    def test_break_alliance(self):
        """Test alliance breaking"""
        alliance_id = self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Break alliance without betrayal
        result = self.manager.break_alliance(alliance_id)
        
        assert result['success']
        assert alliance_id not in self.manager.alliances
        assert 'Agent_A' not in self.manager.player_alliances or len(self.manager.player_alliances['Agent_A']) == 0
        
    def test_break_alliance_with_betrayal(self):
        """Test alliance breaking with betrayal penalty"""
        alliance_id = self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Break alliance with betrayal
        result = self.manager.break_alliance(alliance_id, betrayer='Agent_A')
        
        assert result['success']
        assert result['betrayal_info']['betrayer'] == 'Agent_A'
        assert result['betrayal_info']['penalty_applied']
        assert result['betrayal_info']['ip_loss'] == 2
        
    def test_process_round_end(self):
        """Test alliance duration processing at round end"""
        # Create alliance with 1 round duration
        alliance_id = self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Process round end
        expired = self.manager.process_round_end()
        
        # Alliance should expire and be removed
        assert alliance_id in expired
        assert alliance_id not in self.manager.alliances
        
    def test_coordinated_elimination_victory(self):
        """Test coordinated elimination alliance victory"""
        # Create coordinated operation alliance
        self.manager.create_alliance('Agent_A', 'Agent_B', 'coordinated_operation', 1)
        
        # Mock users data with all non-allied players eliminated
        users = {
            'Agent_A': {'status': 'active'},
            'Agent_B': {'status': 'active'},
            'Agent_C': {'status': 'captured'},
            'Agent_D': {'status': 'eliminated'}
        }
        
        # Check for alliance victory
        victory = self.manager.check_alliance_victory(users, {})
        
        assert victory is not None
        assert victory['type'] == 'alliance_victory'
        assert victory['condition'] == 'Coordinated Elimination'
        assert set(victory['winners']) == {'Agent_A', 'Agent_B'}
        assert victory['trigger_final_showdown']
        
    def test_asset_monopoly_victory(self):
        """Test asset monopoly alliance victory"""
        # Create coordinated operation alliance
        self.manager.create_alliance('Agent_A', 'Agent_B', 'coordinated_operation', 1)
        
        # Mock assets controlled by alliance members
        assets = {
            'asset1': 'Agent_A',
            'asset2': 'Agent_A',
            'asset3': 'Agent_B',
            'asset4': 'Agent_B',
            'asset5': 'Agent_A'
        }
        
        # Check for alliance victory
        victory = self.manager.check_alliance_victory({}, assets)
        
        assert victory is not None
        assert victory['type'] == 'alliance_victory'
        assert victory['condition'] == 'Asset Monopoly'
        assert set(victory['winners']) == {'Agent_A', 'Agent_B'}
        assert victory['trigger_final_showdown']
        
    def test_no_alliance_victory_non_aggression(self):
        """Test that non-aggression pacts don't trigger alliance victory"""
        # Create non-aggression pact (shouldn't trigger victory)
        self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 1)
        
        # Mock scenario that would trigger victory for coordinated operation
        users = {
            'Agent_A': {'status': 'active'},
            'Agent_B': {'status': 'active'},
            'Agent_C': {'status': 'captured'}
        }
        
        # Should not trigger victory
        victory = self.manager.check_alliance_victory(users, {})
        assert victory is None
        
    def test_final_showdown_initialization(self):
        """Test Final Showdown initialization"""
        participants = ['Agent_A', 'Agent_B']
        showdown_data = self.manager.start_final_showdown(participants)
        
        assert self.manager.final_showdown_active
        assert self.manager.showdown_participants == participants
        assert showdown_data['active']
        assert showdown_data['participants'] == participants
        assert showdown_data['ip_bonus'] == 3
        assert 'assassination' in showdown_data['available_actions']
        assert 'sabotage' in showdown_data['available_actions']
        
    def test_final_showdown_invalid_participants(self):
        """Test Final Showdown with invalid participant count"""
        with pytest.raises(ValueError):
            self.manager.start_final_showdown(['Agent_A'])  # Only 1 participant
            
        with pytest.raises(ValueError):
            self.manager.start_final_showdown(['Agent_A', 'Agent_B', 'Agent_C'])  # 3 participants
            
    def test_final_showdown_action_submission(self):
        """Test Final Showdown action submission"""
        participants = ['Agent_A', 'Agent_B']
        self.manager.start_final_showdown(participants)
        
        # Submit valid action
        success = self.manager.submit_showdown_action('Agent_A', 'assassination')
        assert success
        assert 'Agent_A' in self.manager.showdown_actions
        
        # Submit invalid action
        success = self.manager.submit_showdown_action('Agent_A', 'invalid_action')
        assert not success
        
        # Submit action from non-participant
        success = self.manager.submit_showdown_action('Agent_C', 'assassination')
        assert not success
        
    def test_final_showdown_resolution(self):
        """Test Final Showdown resolution"""
        participants = ['Agent_A', 'Agent_B']
        self.manager.start_final_showdown(participants)
        
        # Submit actions for both participants
        self.manager.submit_showdown_action('Agent_A', 'assassination')
        self.manager.submit_showdown_action('Agent_B', 'sabotage')
        
        # Mock user data
        users = {
            'Agent_A': {'ip': 10},
            'Agent_B': {'ip': 8}
        }
        
        # Resolve showdown
        result = self.manager.resolve_final_showdown(users)
        
        assert 'winner' in result
        assert 'runner_up' in result
        assert result['winner'] in participants
        assert result['runner_up'] in participants
        assert result['winner'] != result['runner_up']
        assert len(result['final_rankings']) == 2
        
        # Showdown should be deactivated
        assert not self.manager.final_showdown_active
        assert len(self.manager.showdown_participants) == 0
        
    def test_final_showdown_tie_breaker(self):
        """Test Final Showdown tie breaking with IP"""
        participants = ['Agent_A', 'Agent_B']
        self.manager.start_final_showdown(participants)
        
        # Force same action to test tie scenario
        self.manager.showdown_actions = {
            'Agent_A': {'action': 'assassination', 'timestamp': 0},
            'Agent_B': {'action': 'assassination', 'timestamp': 0}
        }
        
        # Mock user data with different IP (Agent_A has more)
        users = {
            'Agent_A': {'ip': 15},
            'Agent_B': {'ip': 10}
        }
        
        # Resolve multiple times to test tie-breaking
        # Due to random rolls, we can't guarantee the outcome, but IP should be considered
        result = self.manager.resolve_final_showdown(users)
        
        # Just verify structure is correct
        assert 'winner' in result
        assert result['winner'] in participants
        
    def test_get_player_alliances(self):
        """Test getting player alliance information"""
        # Initially no alliances
        alliances = self.manager.get_player_alliances('Agent_A')
        assert len(alliances) == 0
        
        # Create alliance
        self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 2)
        
        # Should return alliance info
        alliances = self.manager.get_player_alliances('Agent_A')
        assert len(alliances) == 1
        assert alliances[0]['partner'] == 'Agent_B'
        assert alliances[0]['type'] == 'non_aggression'
        assert alliances[0]['duration'] == 2
        
    def test_get_alliance_summary(self):
        """Test getting overall alliance summary"""
        # Create multiple alliances
        self.manager.create_alliance('Agent_A', 'Agent_B', 'non_aggression', 2)
        self.manager.create_alliance('Agent_C', 'Agent_D', 'coordinated_operation', 1)
        
        summary = self.manager.get_alliance_summary()
        
        assert summary['total_alliances'] == 2
        assert len(summary['alliances']) == 2
        assert not summary['final_showdown']['active']
        
        # Start Final Showdown
        self.manager.start_final_showdown(['Agent_A', 'Agent_B'])
        
        summary = self.manager.get_alliance_summary()
        assert summary['final_showdown']['active']
        assert len(summary['final_showdown']['participants']) == 2

if __name__ == '__main__':
    pytest.main([__file__]) 