"""
Test suite for the interaction matrix
Validates all offense vs defense pairings and outcomes
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interaction_matrix import (
    get_interaction_outcome, 
    get_default_outcome,
    get_available_offenses,
    get_available_defenses,
    OFFENSES,
    DEFENSES,
    INTERACTION_MATRIX
)

class TestInteractionMatrix:
    
    def test_assassination_vs_safe_house(self):
        """Test specific assassination vs safe house interaction"""
        outcome = get_interaction_outcome('assassination', 'safe_house')
        
        assert outcome['offense_succeeds'] == False
        assert outcome['ip_change_attacker'] == -1
        assert outcome['ip_change_defender'] == 1
        assert outcome['status_change_attacker'] == 'exposed'
        assert outcome['status_change_defender'] is None
        assert 'attacker_codename' in outcome['intel_gained_defender']
        assert outcome['audio_effect'] == 'anvil_drop'
        assert 'Anvil trap springs' in outcome['description']
    
    def test_surveillance_vs_underground(self):
        """Test surveillance vs underground interaction"""
        outcome = get_interaction_outcome('surveillance', 'underground')
        
        assert outcome['offense_succeeds'] == True
        assert outcome['ip_change_attacker'] == 2
        assert outcome['ip_change_defender'] == 0
        assert 'defender_location' in outcome['intel_gained_attacker']
        assert 'defender_next_defense' in outcome['intel_gained_attacker']
    
    def test_ip_spending_modifiers(self):
        """Test that IP spending affects outcomes correctly"""
        base_outcome = get_interaction_outcome('assassination', 'safe_house')
        modified_outcome = get_interaction_outcome('assassination', 'safe_house', 
                                                 attacker_ip_spend=3, defender_ip_spend=2)
        
        # Base IP changes plus spending
        assert modified_outcome['ip_change_attacker'] == base_outcome['ip_change_attacker'] + 3
        assert modified_outcome['ip_change_defender'] == base_outcome['ip_change_defender'] + 2
        
        # Description should include spending info
        assert '3 IP' in modified_outcome['description']
        assert '2 IP' in modified_outcome['description']
    
    def test_default_outcome_for_unknown_pairing(self):
        """Test default outcome when pairing not in matrix"""
        outcome = get_interaction_outcome('unknown_offense', 'unknown_defense')
        
        assert outcome['offense_succeeds'] == False
        assert outcome['ip_change_attacker'] == 0
        assert outcome['ip_change_defender'] == 1
        assert outcome['status_change_attacker'] is None
        assert outcome['status_change_defender'] is None
        assert 'Defense holds' in outcome['description']
    
    def test_available_offenses_full_game(self):
        """Test that all offenses are available in 6-player game"""
        offenses = get_available_offenses(6)
        assert len(offenses) == len(OFFENSES)
        assert 'alliance_disruption' in offenses
    
    def test_available_offenses_two_player(self):
        """Test that alliance offenses removed in 2-player game"""
        offenses = get_available_offenses(2)
        assert 'alliance_disruption' not in offenses
        assert len(offenses) < len(OFFENSES)
    
    def test_available_defenses_full_game(self):
        """Test that all defenses are available in 6-player game"""
        defenses = get_available_defenses(6)
        assert len(defenses) == len(DEFENSES)
        assert 'alliance_building' in defenses
    
    def test_available_defenses_two_player(self):
        """Test that alliance defenses removed in 2-player game"""
        defenses = get_available_defenses(2)
        assert 'alliance_building' not in defenses
        assert len(defenses) < len(DEFENSES)
    
    def test_all_defined_assassination_pairings(self):
        """Test that all assassination pairings are defined"""
        assassination_outcomes = INTERACTION_MATRIX['assassination']
        
        for defense in DEFENSES:
            assert defense in assassination_outcomes, f"Missing pairing: assassination vs {defense}"
            outcome = assassination_outcomes[defense]
            
            # Validate outcome structure
            required_keys = [
                'offense_succeeds', 'ip_change_attacker', 'ip_change_defender',
                'status_change_attacker', 'status_change_defender',
                'intel_gained_attacker', 'intel_gained_defender',
                'audio_effect', 'description'
            ]
            
            for key in required_keys:
                assert key in outcome, f"Missing key {key} in assassination vs {defense}"
    
    def test_all_defined_surveillance_pairings(self):
        """Test that all surveillance pairings are defined"""
        surveillance_outcomes = INTERACTION_MATRIX['surveillance']
        
        for defense in DEFENSES:
            assert defense in surveillance_outcomes, f"Missing pairing: surveillance vs {defense}"
            outcome = surveillance_outcomes[defense]
            
            # Basic structure validation
            assert isinstance(outcome['offense_succeeds'], bool)
            assert isinstance(outcome['ip_change_attacker'], int)
            assert isinstance(outcome['ip_change_defender'], int)
            assert isinstance(outcome['description'], str)
    
    def test_outcome_consistency(self):
        """Test that outcomes are logically consistent"""
        for offense in INTERACTION_MATRIX:
            for defense in INTERACTION_MATRIX[offense]:
                outcome = INTERACTION_MATRIX[offense][defense]
                
                # If offense succeeds, attacker should generally gain IP
                if outcome['offense_succeeds']:
                    assert outcome['ip_change_attacker'] >= 0, \
                        f"Successful {offense} vs {defense} should not penalize attacker"
                
                # If offense fails, defender should generally gain IP
                else:
                    assert outcome['ip_change_defender'] >= 0, \
                        f"Failed {offense} vs {defense} should not penalize defender"
    
    def test_status_transitions_valid(self):
        """Test that status changes are valid transitions"""
        valid_statuses = ['active', 'compromised', 'burned', 'captured', 'eliminated', 'exposed', None]
        
        for offense in INTERACTION_MATRIX:
            for defense in INTERACTION_MATRIX[offense]:
                outcome = INTERACTION_MATRIX[offense][defense]
                
                assert outcome['status_change_attacker'] in valid_statuses, \
                    f"Invalid attacker status change in {offense} vs {defense}"
                assert outcome['status_change_defender'] in valid_statuses, \
                    f"Invalid defender status change in {offense} vs {defense}"

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 