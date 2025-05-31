#!/usr/bin/env python3
"""
Test Master Plans System
Tests for Master Plan assignment, progress tracking, and completion detection
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from master_plans import MasterPlanManager, MASTER_PLANS, ALLIANCE_MASTER_PLANS

class TestMasterPlanManager:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = MasterPlanManager()
        self.test_players = ['Agent_A', 'Agent_B', 'Agent_C', 'Agent_D']
        
    def test_assign_master_plans_4_players(self):
        """Test Master Plan assignment for 4 players"""
        assignments = self.manager.assign_master_plans(self.test_players, 4)
        
        # Should assign plans to all players
        assert len(assignments) == 4
        
        # All players should have different plans
        assigned_plans = list(assignments.values())
        assert len(set(assigned_plans)) == 4  # All unique
        
        # All assignments should be valid plan IDs
        all_plan_ids = [p['id'] for p in MASTER_PLANS + ALLIANCE_MASTER_PLANS]
        for plan_id in assigned_plans:
            assert plan_id in all_plan_ids
            
    def test_assign_master_plans_2_players(self):
        """Test Master Plan assignment for 2 players (no alliance plans)"""
        two_players = ['Agent_A', 'Agent_B']
        assignments = self.manager.assign_master_plans(two_players, 2)
        
        # Should assign plans to both players
        assert len(assignments) == 2
        
        # Should not assign alliance plans in 2-player games
        alliance_plan_ids = [p['id'] for p in ALLIANCE_MASTER_PLANS]
        for plan_id in assignments.values():
            assert plan_id not in alliance_plan_ids
            
    def test_assign_master_plans_6_players(self):
        """Test Master Plan assignment for 6 players (includes alliance plans)"""
        six_players = ['Agent_A', 'Agent_B', 'Agent_C', 'Agent_D', 'Agent_E', 'Agent_F']
        assignments = self.manager.assign_master_plans(six_players, 6)
        
        # Should assign plans to all players
        assert len(assignments) == 6
        
        # Should include alliance plans as options
        all_plan_ids = [p['id'] for p in MASTER_PLANS + ALLIANCE_MASTER_PLANS]
        for plan_id in assignments.values():
            assert plan_id in all_plan_ids
            
    def test_expose_all_plan_completion(self):
        """Test Expose All Agents Master Plan completion"""
        # Assign expose_all plan to Agent_A
        self.manager.player_plans['Agent_A'] = 'expose_all'
        self.manager.player_progress['Agent_A'] = self.manager._initialize_progress(
            {'id': 'expose_all', 'type': 'single_round'}
        )
        
        # Mock all players data
        all_players = {
            'Agent_A': {'status': 'active'},
            'Agent_B': {'status': 'active'},
            'Agent_C': {'status': 'compromised'},
            'Agent_D': {'status': 'captured'}  # Shouldn't count as target
        }
        
        # First successful exposure
        result1 = self.manager.update_progress(
            'Agent_A', 'exposure_success', 
            {'target': 'Agent_B'}, 1, all_players
        )
        assert result1 is None  # Not complete yet
        
        # Second successful exposure (same round)
        result2 = self.manager.update_progress(
            'Agent_A', 'exposure_success',
            {'target': 'Agent_C'}, 1, all_players
        )
        
        # Should complete the plan (exposed all 2 active opponents)
        assert result2 is not None
        assert result2['plan_id'] == 'expose_all'
        assert result2['reward_type'] == 'instant_win'
        
    def test_anvil_carnage_plan_progression(self):
        """Test Anvil Carnage Master Plan consecutive progression"""
        # Assign anvil_carnage plan to Agent_A
        self.manager.player_plans['Agent_A'] = 'anvil_carnage'
        self.manager.player_progress['Agent_A'] = self.manager._initialize_progress(
            {'id': 'anvil_carnage', 'type': 'consecutive_rounds'}
        )
        
        # Round 1: First anvil assassination
        result1 = self.manager.update_progress(
            'Agent_A', 'assassination_success',
            {'target': 'Agent_B', 'gadget_used': 'spring_anvil'}, 1, {}
        )
        assert result1 is None  # Not complete yet
        assert self.manager.player_progress['Agent_A']['consecutive_count'] == 1
        
        # Round 2: Second anvil assassination (consecutive, different target)
        result2 = self.manager.update_progress(
            'Agent_A', 'assassination_success',
            {'target': 'Agent_C', 'gadget_used': 'spring_anvil'}, 2, {}
        )
        assert result2 is None  # Not complete yet
        assert self.manager.player_progress['Agent_A']['consecutive_count'] == 2
        
        # Round 3: Third anvil assassination (consecutive, different target)
        result3 = self.manager.update_progress(
            'Agent_A', 'assassination_success',
            {'target': 'Agent_D', 'gadget_used': 'spring_anvil'}, 3, {}
        )
        
        # Should complete the plan
        assert result3 is not None
        assert result3['plan_id'] == 'anvil_carnage'
        assert result3['reward_type'] == 'special'
        
    def test_anvil_carnage_streak_broken(self):
        """Test Anvil Carnage streak is broken by non-consecutive rounds"""
        # Assign anvil_carnage plan to Agent_A
        self.manager.player_plans['Agent_A'] = 'anvil_carnage'
        self.manager.player_progress['Agent_A'] = self.manager._initialize_progress(
            {'id': 'anvil_carnage', 'type': 'consecutive_rounds'}
        )
        
        # Round 1: First anvil assassination
        self.manager.update_progress(
            'Agent_A', 'assassination_success',
            {'target': 'Agent_B', 'gadget_used': 'spring_anvil'}, 1, {}
        )
        assert self.manager.player_progress['Agent_A']['consecutive_count'] == 1
        
        # Round 3: Second anvil assassination (NOT consecutive - skipped round 2)
        self.manager.update_progress(
            'Agent_A', 'assassination_success',
            {'target': 'Agent_C', 'gadget_used': 'spring_anvil'}, 3, {}
        )
        
        # Should reset streak
        assert self.manager.player_progress['Agent_A']['consecutive_count'] == 1
        
    def test_control_all_assets_plan(self):
        """Test Control All Assets Master Plan completion"""
        # Assign control_all_assets plan to Agent_A
        self.manager.player_plans['Agent_A'] = 'control_all_assets'
        self.manager.player_progress['Agent_A'] = self.manager._initialize_progress(
            {'id': 'control_all_assets', 'type': 'asset_control'}
        )
        
        # Update with 4 assets controlled (not enough)
        result1 = self.manager.update_progress(
            'Agent_A', 'asset_control',
            {'assets_controlled': 4}, 1, {}
        )
        assert result1 is None  # Not complete yet
        
        # Update with 5 assets controlled (complete)
        result2 = self.manager.update_progress(
            'Agent_A', 'asset_control',
            {'assets_controlled': 5}, 1, {}
        )
        
        # Should complete the plan
        assert result2 is not None
        assert result2['plan_id'] == 'control_all_assets'
        assert result2['reward_type'] == 'instant_win'
        
    def test_get_player_plan_info(self):
        """Test getting player plan information"""
        # Assign plan and initialize progress
        self.manager.player_plans['Agent_A'] = 'expose_all'
        self.manager.player_progress['Agent_A'] = self.manager._initialize_progress(
            {'id': 'expose_all', 'type': 'single_round'}
        )
        
        # Get plan info
        plan_info = self.manager.get_player_plan_info('Agent_A')
        
        assert plan_info is not None
        assert plan_info['id'] == 'expose_all'
        assert plan_info['name'] == 'Expose All Agents'
        assert 'description' in plan_info
        assert 'progress' in plan_info
        assert plan_info['completed'] == False
        
    def test_get_player_plan_info_nonexistent(self):
        """Test getting plan info for player without plan"""
        plan_info = self.manager.get_player_plan_info('Nonexistent_Agent')
        assert plan_info is None
        
    def test_plan_already_completed(self):
        """Test that completed plans don't get updated further"""
        # Assign and complete a plan
        self.manager.player_plans['Agent_A'] = 'expose_all'
        progress = self.manager._initialize_progress(
            {'id': 'expose_all', 'type': 'single_round'}
        )
        progress['completed'] = True
        self.manager.player_progress['Agent_A'] = progress
        
        # Try to update progress
        result = self.manager.update_progress(
            'Agent_A', 'exposure_success',
            {'target': 'Agent_B'}, 1, {}
        )
        
        # Should return None since plan is already completed
        assert result is None
        
    def test_plan_definitions_valid(self):
        """Test that all plan definitions have required fields"""
        all_plans = MASTER_PLANS + ALLIANCE_MASTER_PLANS
        
        required_fields = ['id', 'name', 'description', 'type', 'reward_type', 'reward_value']
        
        for plan in all_plans:
            for field in required_fields:
                assert field in plan, f"Plan {plan.get('id', 'unknown')} missing required field: {field}"
            
            # Validate reward types
            assert plan['reward_type'] in ['instant_win', 'ip_bonus', 'special', 'alliance_win']
            
            # Validate plan types
            assert plan['type'] in ['single_round', 'consecutive_rounds', 'cumulative', 
                                  'race', 'survival', 'asset_control', 'alliance_victory']

if __name__ == '__main__':
    pytest.main([__file__]) 