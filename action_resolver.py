"""
James Bland: ACME Edition - Action Resolver
Handles turn resolution, applying interaction matrix outcomes, and game state updates
"""

import random
from interaction_matrix import get_interaction_outcome, STATUSES

def clamp_ip(ip_value, min_ip=-10, max_ip=50):
    """Clamp IP value to valid range"""
    return max(min_ip, min(max_ip, ip_value))

def resolve_turn(users, submitted_actions, round_number, assets=None):
    """
    Resolve a complete turn of actions
    
    Args:
        users: Dictionary of user data {sid: {codename, status, ip, gadgets, intel, ...}}
        submitted_actions: Dictionary of submitted actions {sid: action_data}
        round_number: Current round number
        assets: Dictionary of strategic asset control (optional)
    
    Returns:
        list: Turn results for each player
    """
    results = []
    if assets is None:
        assets = {}
    
    # Convert SID-based actions to codename-based for easier processing
    actions_by_codename = {}
    sid_to_codename = {}
    
    for sid, user in users.items():
        sid_to_codename[sid] = user['codename']
        # Only process submitted actions, don't auto-submit for everyone
        if sid in submitted_actions:
            actions_by_codename[user['codename']] = submitted_actions[sid]
    
    # Phase 1: Handle Banner Phase (Information Warfare)
    banner_effects = handle_banner_phase(users, actions_by_codename, results)
    
    # Phase 2: Process safe turns first (no offense)
    for codename, action in actions_by_codename.items():
        if not action.get('offense') or action['offense'] == '':
            # Safe turn - award +1 IP
            user_sid = get_sid_by_codename(users, codename)
            if user_sid:
                users[user_sid]['ip'] = clamp_ip(users[user_sid]['ip'] + 1)
                results.append({
                    'codename': codename,
                    'action_type': 'safe_turn',
                    'ip_delta': 1,
                    'new_ip': users[user_sid]['ip'],
                    'new_status': users[user_sid]['status'],
                    'intel_gained': [],
                    'description': 'Safe turn - gained 1 IP'
                })
    
    # Phase 3: Group offensive actions by target
    offensive_actions = {}
    for codename, action in actions_by_codename.items():
        if action.get('offense') and action['offense'] != '':
            target = action.get('target')
            if target and target in [u['codename'] for u in users.values()]:
                if target not in offensive_actions:
                    offensive_actions[target] = []
                offensive_actions[target].append((codename, action))
    
    # Phase 4: Process offensive actions by target
    for target_codename, attackers in offensive_actions.items():
        # Sort attackers by IP spent (descending), then by codename (alphabetical)
        attackers.sort(key=lambda x: (-x[1].get('ip_spend', 0), x[0]))
        
        target_sid = get_sid_by_codename(users, target_codename)
        target_action = actions_by_codename.get(target_codename, {})
        target_defense = target_action.get('defense', 'safe_house')
        
        if not target_sid:
            continue
            
        # Check if target can be attacked
        target_status = users[target_sid]['status']
        if target_status in ['captured', 'eliminated']:
            # Target cannot be attacked
            for attacker_codename, _ in attackers:
                results.append({
                    'codename': attacker_codename,
                    'action_type': 'failed_attack',
                    'ip_delta': 0,
                    'new_ip': users[get_sid_by_codename(users, attacker_codename)]['ip'],
                    'new_status': users[get_sid_by_codename(users, attacker_codename)]['status'],
                    'intel_gained': [],
                    'description': f'Cannot attack {target_codename} - {target_status}'
                })
            continue
        
        # Process each attack on this target
        for attacker_codename, attack_action in attackers:
            attacker_sid = get_sid_by_codename(users, attacker_codename)
            if not attacker_sid:
                continue
            
            # Check if attacker can attack
            attacker_status = users[attacker_sid]['status']
            if attacker_status in ['captured', 'eliminated']:
                continue
            
            # Apply banner effects if any
            banner_penalty = banner_effects.get(attacker_codename, 0)
            
            # Get the interaction outcome
            offense = attack_action['offense']
            defense = target_defense
            attacker_ip_spend = attack_action.get('ip_spend', 0)
            
            outcome = get_interaction_outcome(offense, defense, attacker_ip_spend, 0)
            
            # Apply banner penalty to success rate
            if banner_penalty < 0 and outcome['offense_succeeds']:
                # 50% chance to fail due to banner distraction
                if random.random() < 0.5:
                    outcome = get_interaction_outcome(offense, 'default', 0, 0)
                    outcome['description'] += " (Distracted by banner!)"
            
            # Apply IP changes
            old_attacker_ip = users[attacker_sid]['ip']
            old_target_ip = users[target_sid]['ip']
            
            users[attacker_sid]['ip'] = clamp_ip(old_attacker_ip + outcome['ip_change_attacker'])
            users[target_sid]['ip'] = clamp_ip(old_target_ip + outcome['ip_change_defender'])
            
            # Apply status changes
            if outcome['status_change_attacker']:
                users[attacker_sid]['status'] = outcome['status_change_attacker']
            
            if outcome['status_change_defender']:
                users[target_sid]['status'] = outcome['status_change_defender']
            
            # Apply intel gains
            attacker_intel = []
            if outcome['intel_gained_attacker']:
                users[attacker_sid]['intel'].extend(outcome['intel_gained_attacker'])
                attacker_intel = outcome['intel_gained_attacker']
            
            target_intel = []
            if outcome['intel_gained_defender']:
                users[target_sid]['intel'].extend(outcome['intel_gained_defender'])
                target_intel = outcome['intel_gained_defender']
            
            # Handle strategic asset captures
            if offense == 'network_attack' and outcome['offense_succeeds']:
                asset_captured = capture_strategic_asset(users, attacker_sid, assets, results)
                if asset_captured:
                    outcome['description'] += f" Captured {asset_captured}!"
            
            # Record results
            results.append({
                'codename': attacker_codename,
                'action_type': 'attack',
                'target': target_codename,
                'offense': offense,
                'defense': defense,
                'success': outcome['offense_succeeds'],
                'ip_delta': outcome['ip_change_attacker'],
                'new_ip': users[attacker_sid]['ip'],
                'new_status': users[attacker_sid]['status'],
                'intel_gained': attacker_intel,
                'audio_effect': outcome.get('audio_effect'),
                'description': outcome['description']
            })
            
            # If this is the first attack on target, also record target result
            if attackers.index((attacker_codename, attack_action)) == 0:
                results.append({
                    'codename': target_codename,
                    'action_type': 'defense',
                    'attacker': attacker_codename,
                    'offense': offense,
                    'defense': defense,
                    'success': not outcome['offense_succeeds'],
                    'ip_delta': outcome['ip_change_defender'],
                    'new_ip': users[target_sid]['ip'],
                    'new_status': users[target_sid]['status'],
                    'intel_gained': target_intel,
                    'description': f"Defended against {offense} with {defense}"
                })
    
    return results

def handle_banner_phase(users, actions_by_codename, results):
    """
    Handle information warfare banner phase
    
    Returns:
        dict: Banner effects by codename (penalties/bonuses)
    """
    banner_effects = {}
    
    # Find all information warfare defenses
    for codename, action in actions_by_codename.items():
        if action.get('defense') == 'information_warfare':
            banner_message = action.get('banner_message', 'ACME RULES!')
            
            # Find all players who targeted this broadcaster
            affected_players = []
            for other_codename, other_action in actions_by_codename.items():
                if other_action.get('target') == codename and other_action.get('offense'):
                    affected_players.append(other_codename)
            
            # Apply banner effects
            for affected in affected_players:
                # In a full implementation, would wait for player responses
                # For now, apply random effect based on banner message
                if 'ACME' in banner_message.upper():
                    banner_effects[affected] = -1  # Penalty for distraction
                else:
                    banner_effects[affected] = 0   # No effect
            
            if affected_players:
                results.append({
                    'codename': codename,
                    'action_type': 'banner',
                    'ip_delta': 0,
                    'new_ip': users[get_sid_by_codename(users, codename)]['ip'],
                    'new_status': users[get_sid_by_codename(users, codename)]['status'],
                    'intel_gained': [],
                    'description': f'Banner displayed: "{banner_message}" - affected {len(affected_players)} attackers'
                })
    
    return banner_effects

def capture_strategic_asset(users, attacker_sid, assets, results):
    """
    Handle strategic asset capture for network attacks
    
    Returns:
        str or None: Name of captured asset, or None if none available
    """
    available_assets = [name for name, controller in assets.items() if controller is None]
    
    if available_assets:
        # Capture a random available asset
        captured_asset = random.choice(available_assets)
        attacker_codename = users[attacker_sid]['codename']
        assets[captured_asset] = attacker_codename
        
        # Award bonus IP for capture
        users[attacker_sid]['ip'] = clamp_ip(users[attacker_sid]['ip'] + 3)
        
        return captured_asset
    
    return None

def get_sid_by_codename(users, codename):
    """Get session ID by codename"""
    for sid, user in users.items():
        if user['codename'] == codename:
            return sid
    return None

def check_victory_conditions(users, assets):
    """
    Check all victory conditions and return winner(s) if any
    
    Args:
        users: Dictionary of user data
        assets: Dictionary of strategic asset control
    
    Returns:
        dict or None: Victory result with winners and condition, or None if no victory
    """
    active_players = []
    for user in users.values():
        if user['status'] not in ['captured', 'eliminated']:
            active_players.append(user)
    
    # Last Spy Standing
    if len(active_players) <= 1:
        if len(active_players) == 1:
            return {
                'winners': [active_players[0]['codename']],
                'condition': 'Last Spy Standing',
                'description': f"{active_players[0]['codename']} is the last spy standing!"
            }
        else:
            return {
                'winners': [],
                'condition': 'Mutual Elimination',
                'description': 'All spies have been eliminated - no winner!'
            }
    
    # Network Control (3+ strategic assets)
    asset_control = {}
    for asset, controller in assets.items():
        if controller:
            if controller not in asset_control:
                asset_control[controller] = 0
            asset_control[controller] += 1
    
    for codename, count in asset_control.items():
        if count >= 3:
            return {
                'winners': [codename],
                'condition': 'Network Control',
                'description': f"{codename} controls {count} strategic assets and wins by Network Control!"
            }
    
    # Intelligence Supremacy (3+ intel cards about every other active player)
    for user in active_players:
        other_active = [p for p in active_players if p['codename'] != user['codename']]
        if len(other_active) > 0:
            # Check if this player has intel about all other active players
            # This is a simplified version - in full game would check specific intel types
            if len(user.get('intel', [])) >= len(other_active) * 3:
                return {
                    'winners': [user['codename']],
                    'condition': 'Intelligence Supremacy',
                    'description': f"{user['codename']} has gathered comprehensive intelligence and wins by Intelligence Supremacy!"
                }
    
    # Master Plan and Alliance Victory conditions are checked separately in server.py
    
    return None

def apply_round_end_effects(users, assets):
    """
    Apply end-of-round effects like asset yields, gadget upkeep, etc.
    
    Args:
        users: Dictionary of user data
        assets: Dictionary of strategic asset control
    """
    # Award asset yields (2 IP per controlled asset)
    for asset, controller in assets.items():
        if controller:
            controller_sid = get_sid_by_codename(users, controller)
            if controller_sid and users[controller_sid]['status'] not in ['captured', 'eliminated']:
                users[controller_sid]['ip'] = clamp_ip(users[controller_sid]['ip'] + 2)
    
    # Apply gadget upkeep (1 IP per gadget) - DEDUCT costs
    for user in users.values():
        gadgets = user.get('gadgets', [])
        if gadgets:
            upkeep_cost = len(gadgets)
            if user['ip'] >= upkeep_cost:
                user['ip'] = clamp_ip(user['ip'] - upkeep_cost)  # Subtract upkeep
            else:
                # Remove gadgets if can't pay upkeep (keep as many as possible)
                affordable_gadgets = user['ip']  # Can afford this many gadgets
                user['gadgets'] = gadgets[:affordable_gadgets]
                user['ip'] = 0  # Spent all IP on upkeep
    
    # Handle status transitions
    for user in users.values():
        # Convert captured players who have been captured for a full round to burned
        if user['status'] == 'captured':
            # Track rounds captured (simplified - use random chance for now)
            if random.random() < 0.4:  # 40% chance per round
                user['status'] = 'burned'
        
        # Burned players have a chance to become compromised
        elif user['status'] == 'burned':
            if random.random() < 0.3:  # 30% chance per round
                user['status'] = 'compromised'
        
        # Compromised players can recover to active with high IP
        elif user['status'] == 'compromised':
            if user['ip'] >= 15:  # High IP threshold
                user['status'] = 'active'
    
    # Decrement alliance timers (simplified - would track Non-Aggression Pacts)
    for user in users.values():
        alliances = user.get('alliances', [])
        # Remove expired alliances (simplified)
        user['alliances'] = [a for a in alliances if random.random() > 0.1]  # 10% chance to expire
    
    # Award bonus IP for surviving players (encourages longer games)
    active_count = len([u for u in users.values() if u['status'] not in ['captured', 'eliminated']])
    if active_count <= 2:  # Late game bonus - changed from 3 to 2
        for user in users.values():
            if user['status'] not in ['captured', 'eliminated']:
                user['ip'] = clamp_ip(user['ip'] + 1) 