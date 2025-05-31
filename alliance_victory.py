#!/usr/bin/env python3
"""
Alliance Victory System for James Bland: ACME Edition
Handles alliance formation, shared objectives, and Final Showdown mechanics
"""

import random
import time
from typing import Dict, List, Optional, Any, Tuple

class Alliance:
    """Represents an alliance between two players"""
    
    def __init__(self, player1: str, player2: str, alliance_type: str, duration: int = 2):
        self.player1 = player1
        self.player2 = player2
        self.alliance_type = alliance_type  # 'non_aggression' or 'coordinated_operation'
        self.duration = duration  # rounds remaining
        self.created_round = 0
        self.shared_objectives = []
        self.betrayed = False
        
    def get_members(self) -> List[str]:
        """Get list of alliance members"""
        return [self.player1, self.player2]
    
    def is_member(self, codename: str) -> bool:
        """Check if player is a member of this alliance"""
        return codename in [self.player1, self.player2]
    
    def get_partner(self, codename: str) -> Optional[str]:
        """Get the partner of a given player in this alliance"""
        if codename == self.player1:
            return self.player2
        elif codename == self.player2:
            return self.player1
        return None
    
    def is_expired(self) -> bool:
        """Check if alliance has expired"""
        return self.duration <= 0
    
    def decrement_duration(self):
        """Reduce alliance duration by 1 round"""
        self.duration = max(0, self.duration - 1)

class AllianceManager:
    """Manages all alliances and alliance victory conditions"""
    
    def __init__(self):
        self.alliances = {}  # alliance_id -> Alliance
        self.player_alliances = {}  # codename -> list of alliance_ids
        self.alliance_counter = 0
        self.final_showdown_active = False
        self.showdown_participants = []
        self.showdown_actions = {}
        
    def create_alliance(self, player1: str, player2: str, alliance_type: str, 
                       round_number: int) -> str:
        """
        Create a new alliance between two players
        
        Args:
            player1: First player codename
            player2: Second player codename 
            alliance_type: Type of alliance ('non_aggression' or 'coordinated_operation')
            round_number: Current round number
            
        Returns:
            Alliance ID string
        """
        alliance_id = f"alliance_{self.alliance_counter}"
        self.alliance_counter += 1
        
        duration = 2 if alliance_type == 'non_aggression' else 1
        alliance = Alliance(player1, player2, alliance_type, duration)
        alliance.created_round = round_number
        
        self.alliances[alliance_id] = alliance
        
        # Track alliances for each player
        if player1 not in self.player_alliances:
            self.player_alliances[player1] = []
        if player2 not in self.player_alliances:
            self.player_alliances[player2] = []
            
        self.player_alliances[player1].append(alliance_id)
        self.player_alliances[player2].append(alliance_id)
        
        return alliance_id
    
    def break_alliance(self, alliance_id: str, betrayer: Optional[str] = None) -> Dict[str, Any]:
        """
        Break an alliance, optionally due to betrayal
        
        Args:
            alliance_id: ID of alliance to break
            betrayer: Codename of player who betrayed (if applicable)
            
        Returns:
            Dictionary with break result details
        """
        if alliance_id not in self.alliances:
            return {'success': False, 'reason': 'Alliance not found'}
        
        alliance = self.alliances[alliance_id]
        
        # Handle betrayal penalties
        penalty_info = {}
        if betrayer and alliance.is_member(betrayer):
            alliance.betrayed = True
            penalty_info = {
                'betrayer': betrayer,
                'penalty_applied': True,
                'ip_loss': 2,
                'status_change': 'compromised',
                'alliance_cooldown': 3  # rounds
            }
        
        # Remove alliance from player tracking
        for player in alliance.get_members():
            if player in self.player_alliances:
                self.player_alliances[player] = [
                    aid for aid in self.player_alliances[player] if aid != alliance_id
                ]
        
        # Remove alliance
        del self.alliances[alliance_id]
        
        return {
            'success': True,
            'broken_alliance': {
                'members': alliance.get_members(),
                'type': alliance.alliance_type
            },
            'betrayal_info': penalty_info
        }
    
    def process_round_end(self) -> List[str]:
        """
        Process alliance duration decrements and expirations
        
        Returns:
            List of expired alliance IDs
        """
        expired_alliances = []
        
        for alliance_id, alliance in list(self.alliances.items()):
            alliance.decrement_duration()
            
            if alliance.is_expired():
                self.break_alliance(alliance_id)
                expired_alliances.append(alliance_id)
        
        return expired_alliances
    
    def check_alliance_victory(self, users: Dict[str, Any], assets: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Check if any alliance has achieved victory conditions
        
        Args:
            users: All player data
            assets: Strategic asset control data
            
        Returns:
            Victory result if alliance victory achieved, None otherwise
        """
        for alliance_id, alliance in self.alliances.items():
            if alliance.alliance_type == 'coordinated_operation':
                # Check coordinated elimination
                elimination_victory = self._check_coordinated_elimination(alliance, users)
                if elimination_victory:
                    return elimination_victory
                
                # Check asset monopoly
                asset_victory = self._check_asset_monopoly(alliance, assets)
                if asset_victory:
                    return asset_victory
        
        return None
    
    def _check_coordinated_elimination(self, alliance: Alliance, users: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if alliance achieved coordinated elimination victory"""
        members = alliance.get_members()
        
        # Count active non-allied players
        active_opponents = []
        for codename, user_data in users.items():
            if (codename not in members and 
                user_data.get('status') in ['active', 'compromised', 'burned']):
                active_opponents.append(codename)
        
        # Victory if all opponents are eliminated/captured
        if len(active_opponents) == 0:
            return {
                'type': 'alliance_victory',
                'condition': 'Coordinated Elimination',
                'winners': members,
                'trigger_final_showdown': True,
                'description': f"{' and '.join(members)} eliminated all opposition and must face each other!"
            }
        
        return None
    
    def _check_asset_monopoly(self, alliance: Alliance, assets: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if alliance achieved asset monopoly victory"""
        members = alliance.get_members()
        
        # Count assets controlled by alliance members
        controlled_assets = 0
        for asset, controller in assets.items():
            if controller in members:
                controlled_assets += 1
        
        # Victory if alliance controls all 5 assets
        if controlled_assets >= 5:
            return {
                'type': 'alliance_victory',
                'condition': 'Asset Monopoly',
                'winners': members,
                'trigger_final_showdown': True,
                'description': f"{' and '.join(members)} control all strategic assets and must determine the ultimate victor!"
            }
        
        return None
    
    def start_final_showdown(self, participants: List[str]) -> Dict[str, Any]:
        """
        Initiate Final Showdown between alliance partners
        
        Args:
            participants: List of alliance member codenames
            
        Returns:
            Showdown initialization data
        """
        if len(participants) != 2:
            raise ValueError("Final Showdown requires exactly 2 participants")
        
        self.final_showdown_active = True
        self.showdown_participants = participants.copy()
        self.showdown_actions = {}
        
        return {
            'active': True,
            'participants': participants,
            'phase': 'action_selection',
            'time_limit': 30,  # seconds for action selection
            'available_actions': ['assassination', 'sabotage'],
            'ip_bonus': 3,  # Each participant gets +3 IP
            'rules': 'No defenses allowed - higher roll wins, IP breaks ties'
        }
    
    def submit_showdown_action(self, codename: str, action: str) -> bool:
        """
        Submit Final Showdown action for a participant
        
        Args:
            codename: Player codename
            action: Action chosen ('assassination' or 'sabotage')
            
        Returns:
            True if submission successful, False otherwise
        """
        if not self.final_showdown_active:
            return False
        
        if codename not in self.showdown_participants:
            return False
        
        if action not in ['assassination', 'sabotage']:
            return False
        
        self.showdown_actions[codename] = {
            'action': action,
            'timestamp': time.time()
        }
        
        return True
    
    def resolve_final_showdown(self, users: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve Final Showdown and determine winner
        
        Args:
            users: Player data for participants
            
        Returns:
            Showdown resolution results
        """
        if not self.final_showdown_active or len(self.showdown_actions) != 2:
            raise ValueError("Cannot resolve showdown - invalid state")
        
        participants = self.showdown_participants
        
        # Auto-submit if missing actions
        for participant in participants:
            if participant not in self.showdown_actions:
                self.showdown_actions[participant] = {
                    'action': 'assassination',  # Default action
                    'timestamp': time.time()
                }
        
        # Roll dice for each participant
        results = {}
        for codename in participants:
            action_data = self.showdown_actions[codename]
            action = action_data['action']
            
            # Base roll (1-10)
            roll = random.randint(1, 10)
            
            # Assassination gets slight bonus
            if action == 'assassination':
                roll += 1
            
            results[codename] = {
                'action': action,
                'roll': roll,
                'final_score': roll,
                'ip': users[codename].get('ip', 0)
            }
        
        # Determine winner
        participant1, participant2 = participants
        result1 = results[participant1]
        result2 = results[participant2]
        
        if result1['final_score'] > result2['final_score']:
            winner = participant1
            runner_up = participant2
        elif result2['final_score'] > result1['final_score']:
            winner = participant2
            runner_up = participant1
        else:
            # Tie - use IP as tiebreaker
            if result1['ip'] > result2['ip']:
                winner = participant1
                runner_up = participant2
            elif result2['ip'] > result1['ip']:
                winner = participant2
                runner_up = participant1
            else:
                # Still tied - random
                winner = random.choice(participants)
                runner_up = participant2 if winner == participant1 else participant1
        
        # Clean up
        self.final_showdown_active = False
        self.showdown_participants = []
        self.showdown_actions = {}
        
        return {
            'winner': winner,
            'runner_up': runner_up,
            'results': results,
            'description': f"{winner} emerges victorious in the Final Showdown! {runner_up} is the runner-up.",
            'winner_action': results[winner]['action'],
            'winner_roll': results[winner]['roll'],
            'final_rankings': [winner, runner_up]
        }
    
    def get_player_alliances(self, codename: str) -> List[Dict[str, Any]]:
        """Get all alliances for a specific player"""
        if codename not in self.player_alliances:
            return []
        
        alliances = []
        for alliance_id in self.player_alliances[codename]:
            if alliance_id in self.alliances:
                alliance = self.alliances[alliance_id]
                alliances.append({
                    'id': alliance_id,
                    'partner': alliance.get_partner(codename),
                    'type': alliance.alliance_type,
                    'duration': alliance.duration,
                    'created_round': alliance.created_round
                })
        
        return alliances
    
    def can_form_alliance(self, player1: str, player2: str) -> Tuple[bool, str]:
        """
        Check if two players can form an alliance
        
        Args:
            player1: First player codename
            player2: Second player codename
            
        Returns:
            Tuple of (can_form, reason)
        """
        # Check if already allied
        for alliance in self.alliances.values():
            if alliance.is_member(player1) and alliance.is_member(player2):
                return False, "Players are already allied"
        
        # Check maximum alliances per player (limit to 1 active alliance)
        if player1 in self.player_alliances and len(self.player_alliances[player1]) > 0:
            return False, f"{player1} is already in an alliance"
        
        if player2 in self.player_alliances and len(self.player_alliances[player2]) > 0:
            return False, f"{player2} is already in an alliance"
        
        return True, "Alliance can be formed"
    
    def get_alliance_summary(self) -> Dict[str, Any]:
        """Get summary of all active alliances"""
        summary = {
            'total_alliances': len(self.alliances),
            'alliances': [],
            'final_showdown': {
                'active': self.final_showdown_active,
                'participants': self.showdown_participants if self.final_showdown_active else []
            }
        }
        
        for alliance_id, alliance in self.alliances.items():
            summary['alliances'].append({
                'id': alliance_id,
                'members': alliance.get_members(),
                'type': alliance.alliance_type,
                'duration': alliance.duration,
                'created_round': alliance.created_round
            })
        
        return summary

# Global instance
alliance_manager = AllianceManager() 