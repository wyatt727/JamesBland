"""
James Bland: ACME Edition - Interaction Matrix
Defines all offense vs defense pairings and their outcomes
"""

# Offense types
OFFENSES = [
    'assassination', 'sabotage', 'exposure', 'surveillance', 'infiltration',
    'asset_theft', 'misinformation', 'network_attack', 'resource_denial',
    'alliance_disruption', 'false_flag'
]

# Defense types
DEFENSES = [
    'safe_house', 'bodyguard_detail', 'mobile_operations', 'underground',
    'sweep_clear', 'false_identity', 'counter_surveillance', 'disinformation',
    'preemptive_strike', 'alliance_building', 'honeypot_operations', 'information_warfare'
]

# Status types
STATUSES = ['active', 'compromised', 'burned', 'captured', 'eliminated']

# Interaction Matrix: offense -> defense -> outcome
INTERACTION_MATRIX = {
    'assassination': {
        'safe_house': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +1,
            'status_change_attacker': 'exposed',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_codename'],
            'audio_effect': 'anvil_drop',
            'description': 'Anvil trap springs! Assassin bonked on head, identity revealed.'
        },
        'bodyguard_detail': {
            'offense_succeeds': False,
            'ip_change_attacker': -2,
            'ip_change_defender': +2,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_next_offense'],
            'audio_effect': 'piano_launch',
            'description': 'Bodyguards launch piano at assassin! Attack thwarted.'
        },
        'mobile_operations': {
            'offense_succeeds': False,
            'ip_change_attacker': 0,
            'ip_change_defender': +1,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Target was mobile - assassination attempt missed!'
        },
        'underground': {
            'offense_succeeds': True,
            'ip_change_attacker': +2,
            'ip_change_defender': -1,
            'status_change_attacker': None,
            'status_change_defender': 'compromised',
            'intel_gained_attacker': ['defender_gadgets'],
            'intel_gained_defender': None,
            'audio_effect': 'explosion_sizzle',
            'description': 'Underground hideout bombed! Target compromised.'
        },
        'sweep_clear': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +1,
            'status_change_attacker': 'exposed',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_location'],
            'audio_effect': 'anvil_drop',
            'description': 'Sweep detected the assassin! Identity exposed.'
        },
        'false_identity': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': 'compromised',
            'intel_gained_attacker': None,
            'intel_gained_defender': None,
            'audio_effect': 'piano_launch',
            'description': 'Wrong target! But still caused damage to operations.'
        },
        'counter_surveillance': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +2,
            'status_change_attacker': 'exposed',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_allies'],
            'audio_effect': 'explosion_sizzle',
            'description': 'Counter-surveillance caught the assassin red-handed!'
        },
        'disinformation': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': -1,
            'status_change_attacker': None,
            'status_change_defender': 'compromised',
            'intel_gained_attacker': ['defender_next_defense'],
            'intel_gained_defender': None,
            'audio_effect': 'piano_launch',
            'description': 'Disinformation led assassin to target, but gave away defender plans.'
        },
        'preemptive_strike': {
            'offense_succeeds': False,
            'ip_change_attacker': -2,
            'ip_change_defender': +3,
            'status_change_attacker': 'compromised',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_master_plan_hint'],
            'audio_effect': 'explosion_sizzle',
            'description': 'Preemptive strike neutralized the assassin first!'
        },
        'alliance_building': {
            'offense_succeeds': True,
            'ip_change_attacker': +2,
            'ip_change_defender': -1,
            'status_change_attacker': None,
            'status_change_defender': 'compromised',
            'intel_gained_attacker': ['defender_allies'],
            'intel_gained_defender': None,
            'audio_effect': 'anvil_drop',
            'description': 'Alliance meeting disrupted by assassination!'
        },
        'honeypot_operations': {
            'offense_succeeds': False,
            'ip_change_attacker': -3,
            'ip_change_defender': +2,
            'status_change_attacker': 'burned',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_full_dossier'],
            'audio_effect': 'explosion_sizzle',
            'description': 'Honeypot trap! Assassin walked into elaborate setup and got burned!'
        },
        'information_warfare': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': 'compromised',
            'intel_gained_attacker': None,
            'intel_gained_defender': None,
            'audio_effect': 'piano_launch',
            'description': 'Biplane banner distracted security - assassination succeeded!'
        }
    },
    
    'surveillance': {
        'safe_house': {
            'offense_succeeds': False,
            'ip_change_attacker': 0,
            'ip_change_defender': +1,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Safe house too secure for surveillance.'
        },
        'bodyguard_detail': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +1,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_codename'],
            'audio_effect': 'anvil_drop',
            'description': 'Bodyguards spotted the surveillance team!'
        },
        'mobile_operations': {
            'offense_succeeds': False,
            'ip_change_attacker': 0,
            'ip_change_defender': +1,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Target kept moving - surveillance lost the trail.'
        },
        'underground': {
            'offense_succeeds': True,
            'ip_change_attacker': +2,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': ['defender_location', 'defender_next_defense'],
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Underground hideout surveilled successfully!'
        },
        'sweep_clear': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +2,
            'status_change_attacker': 'exposed',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_equipment'],
            'audio_effect': 'anvil_drop',
            'description': 'Sweep and clear found the surveillance equipment!'
        },
        'false_identity': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': ['defender_fake_intel'],
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Surveillance successful, but gathered false information!'
        },
        'counter_surveillance': {
            'offense_succeeds': False,
            'ip_change_attacker': -2,
            'ip_change_defender': +3,
            'status_change_attacker': 'exposed',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_full_equipment'],
            'audio_effect': 'explosion_sizzle',
            'description': 'Counter-surveillance turned the tables completely!'
        },
        'disinformation': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': ['defender_false_plans'],
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Surveillance gathered disinformation successfully.'
        },
        'preemptive_strike': {
            'offense_succeeds': False,
            'ip_change_attacker': -1,
            'ip_change_defender': +1,
            'status_change_attacker': 'compromised',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_surveillance_target'],
            'audio_effect': 'piano_launch',
            'description': 'Preemptive strike disrupted surveillance operation!'
        },
        'alliance_building': {
            'offense_succeeds': True,
            'ip_change_attacker': +2,
            'ip_change_defender': -1,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': ['defender_allies', 'defender_alliance_plans'],
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Alliance meeting successfully surveilled!'
        },
        'honeypot_operations': {
            'offense_succeeds': False,
            'ip_change_attacker': -2,
            'ip_change_defender': +2,
            'status_change_attacker': 'burned',
            'status_change_defender': None,
            'intel_gained_attacker': None,
            'intel_gained_defender': ['attacker_surveillance_methods'],
            'audio_effect': 'explosion_sizzle',
            'description': 'Surveillance team fell for the honeypot!'
        },
        'information_warfare': {
            'offense_succeeds': True,
            'ip_change_attacker': +1,
            'ip_change_defender': 0,
            'status_change_attacker': None,
            'status_change_defender': None,
            'intel_gained_attacker': ['defender_next_defense'],
            'intel_gained_defender': None,
            'audio_effect': None,
            'description': 'Biplane banner provided cover for surveillance!'
        }
    }
    # TODO: Add remaining offense types (sabotage, exposure, infiltration, etc.)
}

def get_interaction_outcome(offense, defense, attacker_ip_spend=0, defender_ip_spend=0):
    """
    Get the outcome of an offense vs defense interaction
    
    Args:
        offense: The attacking action
        defense: The defending action
        attacker_ip_spend: IP spent by attacker
        defender_ip_spend: IP spent by defender
    
    Returns:
        dict: Outcome with all effects
    """
    # Get base outcome from matrix
    if offense not in INTERACTION_MATRIX:
        # Default outcome for unspecified offenses
        return get_default_outcome(offense, defense)
    
    if defense not in INTERACTION_MATRIX[offense]:
        # Default outcome for unspecified defense
        return get_default_outcome(offense, defense)
    
    outcome = INTERACTION_MATRIX[offense][defense].copy()
    
    # Apply IP spending modifiers
    if attacker_ip_spend > 0:
        outcome['ip_change_attacker'] += attacker_ip_spend
        outcome['description'] += f" (Attacker spent {attacker_ip_spend} IP)"
    
    if defender_ip_spend > 0:
        outcome['ip_change_defender'] += defender_ip_spend
        outcome['description'] += f" (Defender spent {defender_ip_spend} IP)"
    
    return outcome

def get_default_outcome(offense, defense):
    """Get a default outcome for unspecified offense/defense pairings"""
    return {
        'offense_succeeds': False,
        'ip_change_attacker': 0,
        'ip_change_defender': +1,
        'status_change_attacker': None,
        'status_change_defender': None,
        'intel_gained_attacker': None,
        'intel_gained_defender': None,
        'audio_effect': None,
        'description': f'{offense.title()} vs {defense.title()}: Defense holds.'
    }

def get_available_offenses(player_count=6):
    """Get list of available offenses based on player count"""
    offenses = OFFENSES.copy()
    
    # Remove alliance-related offenses in 2-player games
    if player_count == 2:
        offenses = [o for o in offenses if 'alliance' not in o]
    
    return offenses

def get_available_defenses(player_count=6):
    """Get list of available defenses based on player count"""
    defenses = DEFENSES.copy()
    
    # Remove alliance-related defenses in 2-player games
    if player_count == 2:
        defenses = [d for d in defenses if 'alliance' not in d]
    
    return defenses 