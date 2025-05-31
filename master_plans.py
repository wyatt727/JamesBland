#!/usr/bin/env python3
"""
Master Plans System for James Bland: ACME Edition
Handles secret objectives, progress tracking, and completion detection
"""

import random
from typing import Dict, List, Optional, Any

# Master Plan definitions
MASTER_PLANS = [
    {
        'id': 'expose_all',
        'name': 'Expose All Agents',
        'description': 'Use Exposure successfully on every active opponent in a single round',
        'type': 'single_round',
        'reward_type': 'instant_win',
        'reward_value': 'intelligence_supremacy',
        'progress_required': {
            'exposure_successes_single_round': 'all_opponents'
        }
    },
    {
        'id': 'control_all_assets',
        'name': 'Network Dominance',
        'description': 'Control all five Strategic Assets at the start of your turn',
        'type': 'asset_control',
        'reward_type': 'instant_win',
        'reward_value': 'network_control',
        'progress_required': {
            'assets_controlled': 5
        }
    },
    {
        'id': 'anvil_carnage',
        'name': 'Anvil Carnage',
        'description': 'Land successful Assassination using Spring-Loaded Anvil on three different opponents in consecutive rounds',
        'type': 'consecutive_rounds',
        'reward_type': 'special',
        'reward_value': '+3 IP and eliminate one Compromised player',
        'progress_required': {
            'anvil_assassinations': 3,
            'consecutive_rounds': True,
            'different_targets': True
        }
    },
    {
        'id': 'misinformation_master',
        'name': 'Mastermind of Misinformation',
        'description': 'Successfully trick three different opponents with Misinformation in a single round',
        'type': 'single_round',
        'reward_type': 'ip_bonus',
        'reward_value': 4,
        'progress_required': {
            'misinformation_successes_single_round': 3,
            'different_targets': True
        }
    },
    {
        'id': 'saboteur_supreme',
        'name': 'Saboteur Supreme',
        'description': 'Perform successful Sabotage on Strategic Assets three times in a row',
        'type': 'consecutive_rounds',
        'reward_type': 'special',
        'reward_value': 'Asset control lost permanently, +5 IP',
        'progress_required': {
            'asset_sabotages': 3,
            'consecutive_rounds': True
        }
    },
    {
        'id': 'ghost_operative',
        'name': 'Ghost Operative',
        'description': 'Complete 5 rounds without being targeted by any opponent',
        'type': 'survival',
        'reward_type': 'ip_bonus',
        'reward_value': 6,
        'progress_required': {
            'untargeted_rounds': 5,
            'consecutive_rounds': True
        }
    },
    {
        'id': 'alliance_breaker',
        'name': 'Alliance Breaker',
        'description': 'Successfully break 3 different alliances using Alliance Disruption',
        'type': 'cumulative',
        'reward_type': 'ip_bonus',
        'reward_value': 5,
        'progress_required': {
            'alliance_disruptions': 3
        }
    },
    {
        'id': 'intel_collector',
        'name': 'Intel Supremacist',
        'description': 'Collect 10 Intel Cards before any opponent reaches 8',
        'type': 'race',
        'reward_type': 'instant_win',
        'reward_value': 'intelligence_supremacy',
        'progress_required': {
            'intel_cards': 10,
            'before_opponents_reach': 8
        }
    }
]

# Alliance-specific Master Plans (only available in 6-player games)
ALLIANCE_MASTER_PLANS = [
    {
        'id': 'coordinated_elimination',
        'name': 'Coordinated Elimination',
        'description': 'Together with an ally, eliminate all non-allied agents in one round',
        'type': 'alliance_victory',
        'reward_type': 'alliance_win',
        'reward_value': 'final_showdown',
        'progress_required': {
            'alliance_required': True,
            'eliminate_all_others_single_round': True
        }
    },
    {
        'id': 'asset_monopoly',
        'name': 'Asset Monopoly',
        'description': 'Together with an ally, control all 5 Strategic Assets',
        'type': 'alliance_victory',
        'reward_type': 'alliance_win', 
        'reward_value': 'final_showdown',
        'progress_required': {
            'alliance_required': True,
            'combined_assets': 5
        }
    }
]

class MasterPlanManager:
    """Manages Master Plan assignment, progress tracking, and completion detection"""
    
    def __init__(self):
        self.player_plans = {}  # codename -> plan_id
        self.player_progress = {}  # codename -> progress_data
        self.completed_plans = []  # list of completed plan results
        
    def assign_master_plans(self, players: List[str], player_count: int) -> Dict[str, str]:
        """
        Assign Master Plans to all players at game start
        
        Args:
            players: List of player codenames
            player_count: Number of players in game
            
        Returns:
            Dictionary mapping codename to assigned plan_id
        """
        available_plans = MASTER_PLANS.copy()
        
        # Add alliance plans only for 6-player games
        if player_count == 6:
            available_plans.extend(ALLIANCE_MASTER_PLANS)
        
        # Remove alliance plans for 2-player games
        if player_count == 2:
            available_plans = [p for p in available_plans 
                             if 'alliance' not in p.get('progress_required', {})]
        
        # Shuffle and assign unique plans
        random.shuffle(available_plans)
        
        assignments = {}
        for i, codename in enumerate(players):
            if i < len(available_plans):
                plan = available_plans[i]
                assignments[codename] = plan['id']
                self.player_plans[codename] = plan['id']
                self.player_progress[codename] = self._initialize_progress(plan)
            else:
                # Fallback if more players than plans (shouldn't happen with current count)
                fallback_plan = random.choice(MASTER_PLANS)
                assignments[codename] = fallback_plan['id']
                self.player_plans[codename] = fallback_plan['id']
                self.player_progress[codename] = self._initialize_progress(fallback_plan)
        
        return assignments
    
    def _initialize_progress(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize progress tracking data for a Master Plan"""
        progress = {
            'round_started': 1,
            'last_round_active': 0,
            'completed': False
        }
        
        # Initialize type-specific tracking
        if plan['type'] == 'consecutive_rounds':
            progress['consecutive_count'] = 0
            progress['last_success_round'] = 0
            progress['targets_hit'] = set()
            
        elif plan['type'] == 'single_round':
            progress['current_round_successes'] = 0
            progress['targets_this_round'] = set()
            
        elif plan['type'] == 'cumulative':
            progress['total_count'] = 0
            
        elif plan['type'] == 'race':
            progress['current_count'] = 0
            
        elif plan['type'] == 'survival':
            progress['untargeted_streak'] = 0
            
        elif plan['type'] == 'alliance_victory':
            progress['alliance_partner'] = None
            progress['joint_progress'] = {}
            
        return progress
    
    def update_progress(self, codename: str, action_type: str, action_data: Dict[str, Any], 
                       round_number: int, all_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update Master Plan progress based on action results
        
        Args:
            codename: Player who performed the action
            action_type: Type of action performed
            action_data: Details about the action and its results
            round_number: Current round number
            all_players: All player data for context
            
        Returns:
            Completion result if plan was completed, None otherwise
        """
        if codename not in self.player_plans:
            return None
            
        plan_id = self.player_plans[codename]
        plan = self._get_plan_by_id(plan_id)
        progress = self.player_progress[codename]
        
        if progress['completed']:
            return None
        
        # Update based on plan type
        if plan['id'] == 'expose_all':
            return self._update_expose_all(codename, action_type, action_data, round_number, all_players)
        elif plan['id'] == 'control_all_assets':
            return self._update_control_all_assets(codename, action_data)
        elif plan['id'] == 'anvil_carnage':
            return self._update_anvil_carnage(codename, action_type, action_data, round_number)
        elif plan['id'] == 'misinformation_master':
            return self._update_misinformation_master(codename, action_type, action_data, round_number)
        elif plan['id'] == 'saboteur_supreme':
            return self._update_saboteur_supreme(codename, action_type, action_data, round_number)
        elif plan['id'] == 'ghost_operative':
            return self._update_ghost_operative(codename, action_data, round_number)
        elif plan['id'] == 'alliance_breaker':
            return self._update_alliance_breaker(codename, action_type, action_data)
        elif plan['id'] == 'intel_collector':
            return self._update_intel_collector(codename, action_data, all_players)
        # Alliance plans
        elif plan['id'] == 'coordinated_elimination':
            return self._update_coordinated_elimination(codename, action_data, all_players)
        elif plan['id'] == 'asset_monopoly':
            return self._update_asset_monopoly(codename, action_data, all_players)
            
        return None
    
    def _get_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get plan definition by ID"""
        all_plans = MASTER_PLANS + ALLIANCE_MASTER_PLANS
        for plan in all_plans:
            if plan['id'] == plan_id:
                return plan
        return None
    
    def _update_expose_all(self, codename: str, action_type: str, action_data: Dict[str, Any], 
                          round_number: int, all_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Expose All Agents plan"""
        progress = self.player_progress[codename]
        
        # Reset counter at start of new round
        if progress['last_round_active'] != round_number:
            progress['current_round_successes'] = 0
            progress['targets_this_round'] = set()
            progress['last_round_active'] = round_number
        
        # Check if this was a successful exposure
        if action_type == 'exposure_success':
            target = action_data.get('target')
            if target and target not in progress['targets_this_round']:
                progress['current_round_successes'] += 1
                progress['targets_this_round'].add(target)
        
        # Check completion: exposed all active opponents this round
        active_opponents = [p for p in all_players.keys() 
                          if p != codename and all_players[p].get('status') in ['active', 'compromised', 'burned']]
        
        if progress['current_round_successes'] >= len(active_opponents) and len(active_opponents) > 0:
            progress['completed'] = True
            return self._create_completion_result(codename, 'expose_all', {
                'targets_exposed': len(active_opponents),
                'round': round_number
            })
        
        return None
    
    def _update_control_all_assets(self, codename: str, action_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Control All Assets plan"""
        assets_controlled = action_data.get('assets_controlled', 0)
        
        if assets_controlled >= 5:
            progress = self.player_progress[codename]
            progress['completed'] = True
            return self._create_completion_result(codename, 'control_all_assets', {
                'assets_controlled': assets_controlled
            })
        
        return None
    
    def _update_anvil_carnage(self, codename: str, action_type: str, action_data: Dict[str, Any], 
                             round_number: int) -> Optional[Dict[str, Any]]:
        """Update progress for Anvil Carnage plan"""
        progress = self.player_progress[codename]
        
        if action_type == 'assassination_success' and action_data.get('gadget_used') == 'spring_anvil':
            target = action_data.get('target')
            
            # Check if consecutive round
            if progress['last_success_round'] == round_number - 1 or progress['consecutive_count'] == 0:
                if target not in progress['targets_hit']:
                    progress['consecutive_count'] += 1
                    progress['last_success_round'] = round_number
                    progress['targets_hit'].add(target)
                    
                    if progress['consecutive_count'] >= 3:
                        progress['completed'] = True
                        return self._create_completion_result(codename, 'anvil_carnage', {
                            'consecutive_kills': progress['consecutive_count'],
                            'final_round': round_number
                        })
            else:
                # Reset streak if not consecutive
                progress['consecutive_count'] = 1 if target not in progress['targets_hit'] else 0
                progress['targets_hit'] = {target} if target not in progress['targets_hit'] else set()
                progress['last_success_round'] = round_number
        
        return None
    
    def _create_completion_result(self, codename: str, plan_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Create a completion result for a Master Plan"""
        plan = self._get_plan_by_id(plan_id)
        
        result = {
            'codename': codename,
            'plan_id': plan_id,
            'plan_name': plan['name'],
            'reward_type': plan['reward_type'],
            'reward_value': plan['reward_value'],
            'completion_details': details
        }
        
        self.completed_plans.append(result)
        return result
    
    # Additional plan update methods would continue here...
    def _update_misinformation_master(self, codename: str, action_type: str, action_data: Dict[str, Any], 
                                    round_number: int) -> Optional[Dict[str, Any]]:
        """Update progress for Misinformation Master plan"""
        # Implementation for misinformation tracking
        return None
    
    def _update_saboteur_supreme(self, codename: str, action_type: str, action_data: Dict[str, Any], 
                               round_number: int) -> Optional[Dict[str, Any]]:
        """Update progress for Saboteur Supreme plan"""
        # Implementation for sabotage tracking
        return None
    
    def _update_ghost_operative(self, codename: str, action_data: Dict[str, Any], 
                              round_number: int) -> Optional[Dict[str, Any]]:
        """Update progress for Ghost Operative plan"""
        # Implementation for survival tracking
        return None
    
    def _update_alliance_breaker(self, codename: str, action_type: str, 
                               action_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Alliance Breaker plan"""
        # Implementation for alliance disruption tracking
        return None
    
    def _update_intel_collector(self, codename: str, action_data: Dict[str, Any], 
                              all_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Intel Collector plan"""
        # Implementation for intel collection tracking
        return None
    
    def _update_coordinated_elimination(self, codename: str, action_data: Dict[str, Any], 
                                      all_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Coordinated Elimination alliance plan"""
        # Implementation for alliance victory tracking
        return None
    
    def _update_asset_monopoly(self, codename: str, action_data: Dict[str, Any], 
                             all_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update progress for Asset Monopoly alliance plan"""
        # Implementation for alliance asset control tracking
        return None
    
    def get_player_plan_info(self, codename: str) -> Optional[Dict[str, Any]]:
        """Get Master Plan information for a player"""
        if codename not in self.player_plans:
            return None
            
        plan_id = self.player_plans[codename]
        plan = self._get_plan_by_id(plan_id)
        progress = self.player_progress[codename]
        
        return {
            'id': plan_id,
            'name': plan['name'],
            'description': plan['description'],
            'type': plan['type'],
            'progress': progress,
            'completed': progress['completed']
        }

# Global instance
master_plan_manager = MasterPlanManager() 