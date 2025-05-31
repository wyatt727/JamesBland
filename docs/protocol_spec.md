# James Bland: ACME Edition - Protocol Specification

## 1. Overview

James Bland: ACME Edition uses a Flask + Flask-SocketIO server application listening on port 5000 (configurable). Each client device (phone, tablet, laptop) opens a WebSocket connection to `http://<HOST_IP>:5000`. All real-time communication (lobby management, action submissions, turn results, reconnections) flows through WebSocket events with no HTTP polling dependency.

The protocol is designed for mobile-first gameplay with minimal latency and clear error handling for network interruptions common in local wireless environments.

## 2. Event Definitions

### 2.1 Client → Server Events

#### `joinLobby`
**Purpose**: Register a new player and enter the game lobby

**Payload**:
```json
{
  "codename": "<string>",
  "protocolVersion": 1
}
```

**Parameters**:
- `codename`: Player's chosen display name (3-15 characters, alphanumeric + spaces)
- `protocolVersion`: Protocol compatibility check (optional)

**Response**: Server emits `lobbyJoined` and `lobbyUpdate` events

#### `readyToggle`
**Purpose**: Toggle player's ready state in lobby

**Payload**:
```json
{
  "ready": <boolean>
}
```

**Response**: Server emits `lobbyUpdate` to all clients

#### `startGame`
**Purpose**: Host initiates game start (host-only event)

**Payload**: `{}` (empty object)

**Prerequisites**: At least 2 players, all players ready

**Response**: Server emits `gameStarted` to all clients

#### `submitAction`
**Purpose**: Submit player's turn choices during Planning Phase

**Payload**:
```json
{
  "offenseId": "<string|null>",
  "defenseId": "<string>", 
  "targetCodename": "<string|null>",
  "ipToSpend": <integer>,
  "bannerMessage": "<string|null>",
  "gadgetPurchases": ["<gadgetId>", ...],
  "gadgetRecharges": ["<gadgetId>", ...]
}
```

**Parameters**:
- `offenseId`: Selected offensive operation ID, null for "Safe Turn"
- `defenseId`: Selected defensive measure ID (required)
- `targetCodename`: Target player for offense (null if no target required)
- `ipToSpend`: IP allocated to enhance actions (0-current IP)
- `bannerMessage`: Text for Biplane Banner (max 50 chars, only if defense = "informationWarfare")
- `gadgetPurchases`: Array of gadget IDs to purchase this turn
- `gadgetRecharges`: Array of owned gadget IDs to recharge

**Response**: Server emits `playerSubmitted` to all clients

#### `bannerChoice`
**Purpose**: Player's response to a Biplane Banner during Resolution Phase

**Payload**:
```json
{
  "bannerCaster": "<string>",
  "choice": "<string>"
}
```

**Parameters**:
- `bannerCaster`: Codename of player who cast the banner
- `choice`: Either "believe" or "ignore"

**Response**: Server processes choice and continues turn resolution

#### `requestGameState`
**Purpose**: Request current game state (for reconnection)

**Payload**: `{}` (empty object)

**Response**: Server emits `gameStateSnapshot`

#### `endTurnAcknowledgment`
**Purpose**: Acknowledge receipt of turn results and readiness for next turn

**Payload**: `{}` (empty object)

**Response**: Server tracks acknowledgments, starts next turn when all received

### 2.2 Server → Client Events

#### `lobbyJoined`
**Purpose**: Confirm successful lobby entry and provide initial state

**Payload**:
```json
{
  "yourCodename": "<string>",
  "isHost": <boolean>,
  "allPlayers": [
    {
      "codename": "<string>",
      "ready": <boolean>,
      "connected": <boolean>
    }, ...
  ],
  "gameConfig": {
    "roundTimer": 90,
    "maxPlayers": 6,
    "minPlayers": 2
  }
}
```

#### `lobbyUpdate`
**Purpose**: Broadcast lobby state changes to all players

**Payload**:
```json
{
  "allPlayers": [
    {
      "codename": "<string>", 
      "ready": <boolean>,
      "connected": <boolean>
    }, ...
  ],
  "canStart": <boolean>
}
```

#### `gameStarted`
**Purpose**: Signal transition from lobby to game and provide initial game state

**Payload**:
```json
{
  "gameConfig": {
    "initialIP": 5,
    "roundTimer": 90,
    "maxRounds": 20
  },
  "currentPlayers": [
    {
      "codename": "<string>",
      "status": "active",
      "ip": <integer>,
      "gadgets": ["<gadgetId>", ...],
      "intel": [],
      "masterPlan": "<planId>"
    }, ...
  ],
  "strategicAssets": [
    {
      "id": "<assetId>",
      "name": "<string>",
      "controller": "<codename|null>",
      "yield": <integer>
    }, ...
  ],
  "round": 1
}
```

#### `planningPhaseStart`
**Purpose**: Begin new Planning Phase with countdown timer

**Payload**:
```json
{
  "round": <integer>,
  "timeLimit": <integer>,
  "availableActions": {
    "offenses": ["<offenseId>", ...],
    "defenses": ["<defenseId>", ...]
  },
  "playersAlive": ["<codename>", ...]
}
```

#### `playerSubmitted`
**Purpose**: Notify all players when someone submits their turn

**Payload**:
```json
{
  "codename": "<string>",
  "submittedAt": <timestamp>
}
```

#### `planningPhaseEnd`
**Purpose**: Signal end of Planning Phase, begin Resolution

**Payload**:
```json
{
  "submittedPlayers": ["<codename>", ...],
  "defaultedPlayers": ["<codename>", ...]
}
```

#### `bannerDisplay`
**Purpose**: Show biplane banner animation and collect responses

**Payload**:
```json
{
  "bannerMessage": "<string>",
  "casterCodename": "<string>", 
  "affectedPlayers": ["<codename>", ...],
  "responseTimeLimit": 10
}
```

**Note**: Only sent to players who originally targeted the banner caster

#### `turnResult`
**Purpose**: Provide complete turn resolution results

**Payload**:
```json
{
  "round": <integer>,
  "resolutions": [
    {
      "attacker": "<codename>",
      "defender": "<codename>", 
      "offense": "<offenseId>",
      "defense": "<defenseId>",
      "success": <boolean>,
      "description": "<string>",
      "effects": {
        "attackerIpDelta": <integer>,
        "defenderIpDelta": <integer>,
        "attackerStatusChange": "<status|null>",
        "defenderStatusChange": "<status|null>",
        "intelGained": {
          "attacker": ["<intelType>", ...],
          "defender": ["<intelType>", ...]
        },
        "gadgetsAffected": {
          "attacker": ["<gadgetId>", ...],
          "defender": ["<gadgetId>", ...]
        }
      }
    }, ...
  ],
  "newGameState": {
    "players": [
      {
        "codename": "<string>",
        "status": "<string>",
        "ip": <integer>,
        "gadgets": ["<gadgetId>", ...],
        "intel": ["<intelType>", ...]
      }, ...
    ],
    "strategicAssets": [
      {
        "id": "<assetId>",
        "controller": "<codename|null>"
      }, ...
    ]
  }
}
```

#### `gameStateSnapshot`
**Purpose**: Provide complete current game state for reconnecting clients

**Payload**:
```json
{
  "round": <integer>,
  "phase": "<string>",
  "timeRemaining": <integer|null>,
  "players": [
    {
      "codename": "<string>",
      "status": "<string>",
      "ip": <integer>,
      "gadgets": ["<gadgetId>", ...],
      "intel": ["<intelType>", ...],
      "submitted": <boolean>
    }, ...
  ],
  "strategicAssets": [
    {
      "id": "<assetId>",
      "name": "<string>",
      "controller": "<codename|null>",
      "yield": <integer>
    }, ...
  ],
  "yourData": {
    "codename": "<string>",
    "masterPlan": "<planId>",
    "privateIntel": ["<intelType>", ...]
  }
}
```

#### `gameOver`
**Purpose**: Signal game end and declare winners

**Payload**:
```json
{
  "winners": ["<codename>", ...],
  "condition": "<string>",
  "description": "<string>",
  "finalStats": {
    "totalRounds": <integer>,
    "playerStats": [
      {
        "codename": "<string>",
        "finalIP": <integer>,
        "finalStatus": "<string>",
        "successfulActions": <integer>,
        "assetsControlled": <integer>
      }, ...
    ]
  }
}
```

#### `error`
**Purpose**: Communicate errors to clients

**Payload**:
```json
{
  "type": "<errorType>",
  "message": "<string>",
  "code": "<errorCode>",
  "details": <object|null>
}
```

**Error Types**:
- `validation`: Invalid input data
- `game_state`: Action not valid in current game state  
- `permission`: Action not permitted for this player
- `network`: Connection or protocol error
- `server`: Internal server error

## 3. Sequence Flows

### 3.1 Lobby Join Flow

1. **Client connects** to WebSocket endpoint
2. **Client emits** `joinLobby` with desired codename
3. **Server validates** codename (unique, valid format)
4. **Server registers** player in lobby
5. **Server emits** `lobbyJoined` to joining client
6. **Server broadcasts** `lobbyUpdate` to all lobby clients

### 3.2 Game Start Flow

1. **Host clicks** "Start Game" button
2. **Client emits** `startGame`
3. **Server validates** minimum players (≥2) and all ready
4. **Server initializes** game state (IP, gadgets, Master Plans, assets)
5. **Server emits** `gameStarted` to all clients
6. **Server immediately emits** `planningPhaseStart` for Round 1

### 3.3 Single Round Flow

#### Planning Phase
1. **Server emits** `planningPhaseStart` with timer and available actions
2. **Clients display** Planning UI with countdown
3. **Each client** selects offense/defense/target/IP/gadgets
4. **Each client emits** `submitAction` with choices
5. **Server emits** `playerSubmitted` on each submission
6. **Timer expires** or all active players submit
7. **Server emits** `planningPhaseEnd`

#### Resolution Phase
1. **Server processes** all banner effects first
2. **If banners exist**: Server emits `bannerDisplay` to affected players
3. **Server waits** for `bannerChoice` responses (10 sec timeout)
4. **Server resolves** all offense vs. defense pairings
5. **Server applies** cascading effects (status changes, IP updates, intel)
6. **Server emits** `turnResult` with complete resolution

#### Adaptation Phase
1. **Clients process** turn results and update UI
2. **Server checks** victory conditions
3. **If game continues**: increment round, emit `planningPhaseStart`
4. **If game ends**: emit `gameOver`

### 3.4 Reconnection Flow

1. **Client reconnects** after disconnection
2. **Server detects** reconnection in `connect` handler
3. **Client emits** `requestGameState`
4. **Server emits** `gameStateSnapshot` with current state
5. **Client rebuilds** UI based on current phase and state

### 3.5 Banner Resolution Flow

1. **Banner caster** selects "Information Warfare" defense with message
2. **Attackers** target the banner caster during planning
3. **Resolution begins**: Server emits `bannerDisplay` to affected attackers only
4. **Affected players** see modal with "Believe Banner" / "Ignore Banner" buttons
5. **Players respond** via `bannerChoice` event (10 second timeout)
6. **Server redirects** attacks based on banner content and player choices
7. **Normal resolution** proceeds with redirected/unredirected attacks

## 4. Error Handling

### 4.1 Input Validation
- **Invalid JSON**: Server logs warning, ignores message
- **Missing required fields**: Server emits `error` event with validation details
- **Out-of-range values**: Server emits `error` event, uses default values where possible

### 4.2 Timeout Handling
- **Planning Phase timeout**: Auto-submit defaults for non-submitted players
  - `offenseId`: null (Safe Turn)
  - `defenseId`: "underground"
  - `targetCodename`: null
  - `ipToSpend`: 0
- **Banner response timeout**: Default to "ignore"
- **Reconnection timeout**: Remove player from game after 5 minutes

### 4.3 Host Disconnection
- **Server detects** host disconnection
- **Server promotes** next connected player to host
- **Server emits** `hostChanged` event to all clients
- **If no players remain**: Server resets lobby state

### 4.4 Network Interruption
- **Client disconnection**: Server marks player as disconnected, continues game
- **Client reconnection**: Use reconnection flow to restore state
- **Partial connectivity**: Server waits for stable connection before critical operations

## 5. Protocol Versioning

### 5.1 Version Compatibility
- **Current version**: 1
- **Version field**: Optional `protocolVersion` in all client messages
- **Mismatch handling**: Server emits `error` with upgrade instructions

### 5.2 Future Versions
- **Backward compatibility**: Server supports previous version for transition period
- **Breaking changes**: Increment major version, require client updates
- **Feature additions**: Increment minor version, graceful degradation

## 6. Security Considerations

### 6.1 Input Sanitization
- **Codenames**: Alphanumeric + spaces only, 3-15 characters
- **Banner messages**: Plain text only, 50 character limit, HTML escaped
- **IP spending**: Cannot exceed current IP, minimum 0

### 6.2 Game State Integrity
- **Action validation**: Server validates all actions against current game state
- **Duplicate submissions**: Only first valid submission accepted per player per turn
- **Spectator prevention**: Eliminated players can only perform ghost actions

### 6.3 Rate Limiting
- **Message frequency**: Maximum 10 messages per second per client
- **Reconnection attempts**: Maximum 5 attempts per minute
- **Spam protection**: Automatic temporary bans for excessive invalid messages

## 7. Performance Considerations

### 7.1 Message Optimization
- **Minimal payloads**: Only include necessary data in each message
- **Delta updates**: Send only changed data where possible
- **Compression**: WebSocket compression enabled for larger messages

### 7.2 Scalability
- **Single game server**: Designed for 2-6 players maximum
- **Memory usage**: Game state held in server memory, no database required
- **CPU usage**: Minimize computation during time-critical resolution phase

### 7.3 Mobile Optimization
- **Battery conservation**: Reduce message frequency when possible
- **Bandwidth efficiency**: Use compact JSON structures
- **Offline handling**: Graceful degradation when network unavailable 