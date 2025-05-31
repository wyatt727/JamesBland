#!/usr/bin/env python3
"""
James Bland: ACME Edition - Main Server
Flask + Flask-SocketIO server for LAN-only multiplayer espionage game
"""

import eventlet
eventlet.monkey_patch()

import json
import random
import socket
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

# Import game logic modules
from interaction_matrix import get_available_offenses, get_available_defenses
from action_resolver import resolve_turn, check_victory_conditions, apply_round_end_effects
from master_plans import master_plan_manager
from alliance_victory import alliance_manager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'james_bland_acme_secret_key_2024'

# Configure CORS for LAN access
CORS(app, origins=['http://192.168.*.*:*', 'http://10.*.*.*:*', 'http://172.16.*.*:*'])

# Initialize SocketIO with eventlet
socketio = SocketIO(app, 
                   cors_allowed_origins=['http://192.168.*.*:*', 'http://10.*.*.*:*', 'http://172.16.*.*:*'],
                   async_mode='eventlet',
                   logger=True,
                   engineio_logger=True)

# Global game state
users = {}              # sid -> {codename, status, ip, gadgets, intel, etc}
connections = {}        # sid -> connection info
lobby_state = {
    'players': [],      # list of {sid, codename, ready}
    'host_sid': None,
    'game_started': False
}
game_state = {
    'round_number': 0,
    'phase': 'lobby',   # 'lobby', 'planning', 'banner', 'resolution', 'game_over'
    'timer_start': None,
    'timer_duration': 90,  # seconds
    'submitted_actions': {},  # sid -> action data
    'banner_responses': {},   # sid -> banner choice data
    'assets': {},        # strategic assets control
    'turn_results': []   # latest turn results
}

def get_lan_ip():
    """Get the LAN IP address of this server"""
    try:
        # Connect to a dummy address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

# WebSocket Event Handlers

@socketio.on('connect')
def handle_connect():
    """Handle new client connection"""
    from flask import request
    print(f"Client {request.sid} connected")
    connections[request.sid] = {
        'connected_at': time.time(),
        'ip_address': request.environ.get('REMOTE_ADDR')
    }

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection with cleanup"""
    from flask import request
    sid = request.sid
    print(f"Client {sid} disconnected")
    
    # Remove from connections
    if sid in connections:
        del connections[sid]
    
    # Handle lobby disconnection
    if not game_state['game_started']:
        # Remove from lobby
        lobby_state['players'] = [p for p in lobby_state['players'] if p['sid'] != sid]
        
        # Transfer host if needed
        if lobby_state['host_sid'] == sid and lobby_state['players']:
            lobby_state['host_sid'] = lobby_state['players'][0]['sid']
            emit('hostTransferred', {'newHost': lobby_state['host_sid']}, broadcast=True)
        
        emit('lobbyUpdate', {
            'players': lobby_state['players'],
            'host': lobby_state['host_sid']
        }, broadcast=True)
    
    # Handle in-game disconnection
    else:
        if sid in users:
            # Auto-submit default actions if player was active
            if users[sid].get('status') in ['active', 'compromised', 'burned']:
                auto_submit_defaults(sid)
            
            # Mark as disconnected but keep in game
            users[sid]['disconnected'] = True

@socketio.on('joinLobby')
def handle_join_lobby(data):
    """Handle player joining the lobby"""
    from flask import request
    sid = request.sid
    codename = data.get('codename', '').strip()
    
    # Validate codename
    if not codename or len(codename) > 16:
        emit('error', {'message': 'Codename must be 1-16 characters'})
        return
    
    # Check if codename is already taken
    if any(p['codename'].lower() == codename.lower() for p in lobby_state['players']):
        emit('error', {'message': 'Codename already taken'})
        return
    
    # Check if game already started
    if game_state['game_started']:
        emit('error', {'message': 'Game already in progress'})
        return
    
    # Check player limit
    if len(lobby_state['players']) >= 6:
        emit('error', {'message': 'Lobby is full (6 players max)'})
        return
    
    # Add player to lobby
    player_data = {
        'sid': sid,
        'codename': codename,
        'ready': False
    }
    lobby_state['players'].append(player_data)
    
    # Set first player as host
    if not lobby_state['host_sid']:
        lobby_state['host_sid'] = sid
    
    # Initialize user data
    users[sid] = {
        'codename': codename,
        'status': 'active',
        'ip': 10,  # Starting IP
        'gadgets': [],
        'intel': [],
        'master_plan': None,
        'alliances': [],
        'disconnected': False
    }
    
    emit('lobbyJoined', {
        'success': True,
        'codename': codename,
        'isHost': sid == lobby_state['host_sid']
    })
    
    # Broadcast lobby update
    emit('lobbyUpdate', {
        'players': lobby_state['players'],
        'host': lobby_state['host_sid']
    }, broadcast=True)

@socketio.on('startGame')
def handle_start_game():
    """Handle game start request (host only)"""
    from flask import request
    sid = request.sid
    
    # Validate host
    if sid != lobby_state['host_sid']:
        emit('error', {'message': 'Only the host can start the game'})
        return
    
    # Validate minimum players
    if len(lobby_state['players']) < 2:
        emit('error', {'message': 'Need at least 2 players to start'})
        return
    
    # Initialize game
    initialize_game()
    
    emit('gameStarted', {
        'players': [{'codename': users[p['sid']]['codename'], 'sid': p['sid']} 
                   for p in lobby_state['players']],
        'roundNumber': game_state['round_number']
    }, broadcast=True)

def initialize_game():
    """Initialize game state for all players"""
    game_state['game_started'] = True
    game_state['phase'] = 'planning'
    game_state['round_number'] = 1
    game_state['timer_start'] = time.time()
    game_state['submitted_actions'] = {}
    game_state['banner_responses'] = {}
    
    # Initialize strategic assets
    game_state['assets'] = {
        'central_server': None,
        'comm_tower': None, 
        'data_vault': None,
        'operations_center': None,
        'safe_house_network': None
    }
    
    # Assign Master Plans to all players
    player_codenames = [users[p['sid']]['codename'] for p in lobby_state['players']]
    player_count = len(player_codenames)
    
    master_plan_assignments = master_plan_manager.assign_master_plans(player_codenames, player_count)
    
    # Update user data with Master Plan assignments
    for player_data in lobby_state['players']:
        codename = users[player_data['sid']]['codename']
        if codename in master_plan_assignments:
            users[player_data['sid']]['master_plan'] = master_plan_assignments[codename]
    
    print(f"Game started with {len(lobby_state['players'])} players")
    print(f"Master Plans assigned: {master_plan_assignments}")

@socketio.on('submitAction')
def handle_submit_action(data):
    """Handle player action submission during planning phase"""
    from flask import request
    sid = request.sid
    
    # Validate game state
    if game_state['phase'] != 'planning':
        emit('error', {'message': 'Not in planning phase'})
        return
    
    # Validate player
    if sid not in users or users[sid].get('status') not in ['active', 'compromised', 'burned']:
        emit('error', {'message': 'Cannot submit action in current status'})
        return
    
    # Validate and store action
    action = {
        'offense': data.get('offense'),
        'defense': data.get('defense'), 
        'target': data.get('target'),
        'ip_spend': max(0, min(data.get('ip_spend', 0), users[sid]['ip'])),
        'banner_message': data.get('banner_message', '').strip()[:50] if data.get('banner_message') else ''
    }
    
    game_state['submitted_actions'][sid] = action
    
    emit('actionSubmitted', {'success': True})
    
    # Broadcast submission status (without revealing actions)
    submitted_count = len(game_state['submitted_actions'])
    total_active = len([u for u in users.values() 
                       if u.get('status') in ['active', 'compromised', 'burned']])
    
    emit('playerSubmitted', {
        'submitted': submitted_count,
        'total': total_active
    }, broadcast=True)
    
    # Check if all players submitted
    if submitted_count >= total_active:
        start_resolution_phase()

def auto_submit_defaults(sid):
    """Auto-submit default actions for disconnected/timed-out players"""
    if sid not in game_state['submitted_actions']:
        game_state['submitted_actions'][sid] = {
            'offense': 'surveillance',  # Safe default
            'defense': 'safe_house',    # Defensive default
            'target': None,
            'ip_spend': 0,
            'banner_message': ''
        }

def start_resolution_phase():
    """Start the resolution phase after all actions submitted"""
    game_state['phase'] = 'resolution'
    
    # Auto-submit defaults for any missing players
    active_players = [sid for sid, user in users.items() 
                     if user.get('status') in ['active', 'compromised', 'burned']]
    
    for sid in active_players:
        if sid not in game_state['submitted_actions']:
            auto_submit_defaults(sid)
    
    # Resolve the turn using action resolver
    try:
        turn_results = resolve_turn(users, game_state['submitted_actions'], 
                                  game_state['round_number'], game_state['assets'])
        game_state['turn_results'] = turn_results
        
        # Update Master Plan progress based on turn results
        for result in turn_results:
            if result['action_type'] in ['assassination_success', 'exposure_success', 'sabotage_success']:
                codename = result['codename']
                master_plan_completion = master_plan_manager.update_progress(
                    codename, 
                    result['action_type'], 
                    result, 
                    game_state['round_number'],
                    {users[p['sid']]['codename']: users[p['sid']] for p in lobby_state['players']}
                )
                
                # Handle Master Plan completion
                if master_plan_completion:
                    if master_plan_completion['reward_type'] == 'instant_win':
                        # Immediate victory
                        game_state['phase'] = 'game_over'
                        emit('gameOver', {
                            'winners': [master_plan_completion['codename']],
                            'condition': 'Mission Completion',
                            'description': f"{master_plan_completion['codename']} completed {master_plan_completion['plan_name']}!",
                            'masterPlan': master_plan_completion,
                            'finalResults': turn_results,
                            'assets': game_state['assets']
                        }, broadcast=True)
                        return
                    elif master_plan_completion['reward_type'] == 'ip_bonus':
                        # Award IP bonus
                        for p in lobby_state['players']:
                            if users[p['sid']]['codename'] == codename:
                                users[p['sid']]['ip'] += master_plan_completion['reward_value']
                                break
        
        # Apply round end effects
        apply_round_end_effects(users, game_state['assets'])
        
        # Process alliance round end effects
        expired_alliances = alliance_manager.process_round_end()
        
        # Check victory conditions
        victory = check_victory_conditions(users, game_state['assets'])
        
        # Check alliance victory conditions
        if not victory:
            alliance_victory = alliance_manager.check_alliance_victory(users, game_state['assets'])
            if alliance_victory and alliance_victory.get('trigger_final_showdown'):
                # Start Final Showdown
                participants = alliance_victory['winners']
                showdown_data = alliance_manager.start_final_showdown(participants)
                
                # Award +3 IP to each participant
                for participant in participants:
                    for p in lobby_state['players']:
                        if users[p['sid']]['codename'] == participant:
                            users[p['sid']]['ip'] += 3
                            break
                
                # Notify clients of Final Showdown
                emit('finalShowdownStarted', {
                    'alliance_victory': alliance_victory,
                    'showdown': showdown_data
                }, broadcast=True)
                
                game_state['phase'] = 'final_showdown'
                return
        
        if victory:
            # Game over!
            game_state['phase'] = 'game_over'
            emit('gameOver', {
                'winners': victory['winners'],
                'condition': victory['condition'],
                'description': victory['description'],
                'finalResults': turn_results,
                'assets': game_state['assets']
            }, broadcast=True)
            return
        
        # Broadcast turn results
        emit('turnResult', {
            'round': game_state['round_number'],
            'results': turn_results,
            'players': get_player_summaries(),
            'assets': game_state['assets'],
            'expired_alliances': expired_alliances
        }, broadcast=True)
        
        # Advance to next round after a delay
        advance_to_next_round()
        
    except Exception as e:
        print(f"Error resolving turn: {e}")
        emit('error', {'message': 'Turn resolution failed'}, broadcast=True)
        advance_to_next_round()

def get_player_summaries():
    """Get summary data for all players"""
    summaries = []
    for sid, user in users.items():
        summaries.append({
            'codename': user['codename'],
            'status': user['status'],
            'ip': user['ip'],
            'gadgets': user['gadgets'],
            'intel_count': len(user.get('intel', [])),
            'disconnected': user.get('disconnected', False)
        })
    return summaries

def advance_to_next_round():
    """Advance to the next planning round"""
    game_state['round_number'] += 1
    game_state['phase'] = 'planning'
    game_state['timer_start'] = time.time()
    game_state['submitted_actions'] = {}
    game_state['banner_responses'] = {}
    
    emit('nextRound', {
        'roundNumber': game_state['round_number']
    }, broadcast=True)

@socketio.on('requestGameState')  
def handle_request_game_state():
    """Handle reconnection game state request"""
    from flask import request
    sid = request.sid
    
    if sid in users:
        users[sid]['disconnected'] = False
        
        emit('gameStateSnapshot', {
            'gameStarted': game_state['game_started'],
            'phase': game_state['phase'], 
            'roundNumber': game_state['round_number'],
            'players': [{'codename': users[p['sid']]['codename'], 
                        'sid': p['sid'],
                        'status': users[p['sid']]['status'],
                        'ip': users[p['sid']]['ip']} 
                       for p in lobby_state['players'] if p['sid'] in users],
            'userState': users[sid]
        })

@socketio.on('getGameOptions')
def handle_get_game_options():
    """Send available offenses and defenses based on player count"""
    from flask import request
    player_count = len(lobby_state['players'])
    
    emit('gameOptions', {
        'offenses': get_available_offenses(player_count),
        'defenses': get_available_defenses(player_count),
        'targets': [p['codename'] for p in lobby_state['players'] 
                   if p['sid'] != request.sid]
    })

@socketio.on('bannerChoice')
def handle_banner_choice(data):
    """Handle banner choice during information warfare"""
    from flask import request
    sid = request.sid
    choice = data.get('choice')  # 'believe' or 'ignore'
    banner_caster = data.get('caster')
    
    if sid not in users:
        return
    
    game_state['banner_responses'][sid] = {
        'choice': choice,
        'caster': banner_caster,
        'timestamp': time.time()
    }
    
    # Check if all banner responses collected
    # This is a simplified version - full implementation would track who needs to respond
    emit('bannerResponseRecorded', {'success': True})

@socketio.on('submitShowdownAction')
def handle_submit_showdown_action(data):
    """Handle Final Showdown action submission"""
    from flask import request
    sid = request.sid
    
    # Validate game state
    if game_state['phase'] != 'final_showdown':
        emit('error', {'message': 'Not in Final Showdown phase'})
        return
    
    # Validate player
    if sid not in users:
        emit('error', {'message': 'Player not found'})
        return
    
    codename = users[sid]['codename']
    action = data.get('action')
    
    # Submit action to alliance manager
    success = alliance_manager.submit_showdown_action(codename, action)
    
    if success:
        emit('showdownActionSubmitted', {'success': True})
        
        # Check if both participants have submitted
        if len(alliance_manager.showdown_actions) >= 2:
            # Resolve Final Showdown
            try:
                showdown_result = alliance_manager.resolve_final_showdown(users)
                
                # Game over with Final Showdown results
                game_state['phase'] = 'game_over'
                emit('gameOver', {
                    'winners': [showdown_result['winner']],
                    'condition': 'Alliance Victory - Final Showdown',
                    'description': showdown_result['description'],
                    'finalShowdown': showdown_result,
                    'finalRankings': showdown_result['final_rankings']
                }, broadcast=True)
                
            except Exception as e:
                print(f"Error resolving Final Showdown: {e}")
                emit('error', {'message': 'Final Showdown resolution failed'}, broadcast=True)
    else:
        emit('error', {'message': 'Failed to submit showdown action'})

@socketio.on('getMasterPlan')
def handle_get_master_plan():
    """Send player's Master Plan information"""
    from flask import request
    sid = request.sid
    
    if sid in users:
        codename = users[sid]['codename']
        plan_info = master_plan_manager.get_player_plan_info(codename)
        
        if plan_info:
            emit('masterPlanInfo', plan_info)
        else:
            emit('error', {'message': 'Master Plan not found'})

@socketio.on('getAlliances')
def handle_get_alliances():
    """Send alliance information to client"""
    from flask import request
    sid = request.sid
    
    if sid in users:
        codename = users[sid]['codename']
        player_alliances = alliance_manager.get_player_alliances(codename)
        alliance_summary = alliance_manager.get_alliance_summary()
        
        emit('allianceInfo', {
            'playerAlliances': player_alliances,
            'allAlliances': alliance_summary
        })

@socketio.on('createAlliance')
def handle_create_alliance(data):
    """Handle alliance creation request"""
    from flask import request
    sid = request.sid
    
    if sid not in users:
        emit('error', {'message': 'Player not found'})
        return
    
    initiator = users[sid]['codename']
    target = data.get('target')
    alliance_type = data.get('type', 'non_aggression')
    
    # Validate target
    target_found = False
    for p in lobby_state['players']:
        if users[p['sid']]['codename'] == target:
            target_found = True
            break
    
    if not target_found:
        emit('error', {'message': 'Target player not found'})
        return
    
    # Check if alliance can be formed
    can_form, reason = alliance_manager.can_form_alliance(initiator, target)
    
    if not can_form:
        emit('error', {'message': reason})
        return
    
    # Create alliance
    alliance_id = alliance_manager.create_alliance(
        initiator, target, alliance_type, game_state['round_number']
    )
    
    # Broadcast alliance creation
    emit('allianceCreated', {
        'allianceId': alliance_id,
        'members': [initiator, target],
        'type': alliance_type,
        'round': game_state['round_number']
    }, broadcast=True)

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    print(f"James Bland: ACME Edition Server")
    print(f"Server listening on 0.0.0.0:5000 (LAN IP: {lan_ip})")
    print(f"Players should connect to: http://{lan_ip}:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user") 