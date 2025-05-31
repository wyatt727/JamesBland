# James Bland: ACME Edition - Game Design Document

## 1. Introduction & Core Concept

James Bland: ACME Edition transforms is a competitive 2–6 player espionage game over local area network (LAN). The game embraces ACME-style cartoon traps including exploding pianos, spring-loaded anvils, jet-powered roller skates, and custard pie launchers. The tone is deliberately slapstick and over-the-top, drawing inspiration from classic cartoon spy scenarios.

Players take on the roles of competing secret agents, each equipped with an arsenal of cartoonish gadgets and schemes. The game combines strategic planning with psychological warfare, as players must anticipate their opponents' moves while deploying their own offensive and defensive measures.

## 2. Overall Turn Structure

### Planning Phase (90 seconds)

During this phase, all players simultaneously and secretly make their choices for the round:

1. **Choose One Offensive Operation**: Players select from a list of available offensive actions, potentially targeting another specific player
2. **Choose One Defensive Measure**: Players select a defensive action to protect themselves from incoming attacks
3. **Allocate Intelligence Points (IP)**: Players decide how many IP to spend on enhancing their actions or purchasing equipment
4. **Banner Message Entry** (if applicable): If a player selected "Information Warfare (Biplane Banner)" as their defense, they type a message (max 50 characters) to be displayed during resolution
5. **Submit Choices**: Each client sends their complete action package to the server via WebSocket

### Resolution Phase

Once all players have submitted their choices or the 90-second timer expires:

1. **Reveal Phase**: All offensive and defensive choices are revealed simultaneously to all players
2. **Banner Resolution** (if applicable): 
   - If any player used a Biplane Banner, an animation shows a small plane flying across the screen dragging the banner message
   - Each player who originally targeted the banner-caster receives a prompt: "Believe Banner" or "Ignore Banner" (10-second timer)
   - Player choices determine whether their attacks are redirected based on the banner's content
3. **Combat Resolution**: The server resolves each offense vs. defense pairing using the Interaction Matrix
4. **Cascading Effects**: Status changes, IP adjustments, gadget losses/gains, and intel revelations are applied

### Adaptation Phase

After combat resolution:

1. **State Updates**: Player IP totals, statuses, gadget inventories, and intel collections are updated
2. **Equipment Management**: Players may spend remaining IP on new gadgets, recharging existing ones, or bribing NPCs
3. **Alliance Negotiations**: Players can form, extend, or break alliances (with associated costs)
4. **Victory Check**: The server checks all victory conditions; if none are met, a new Planning Phase begins

## 3. Offensive Operation Categories

### 3.1 Assassination
- **Base Success Rate**: Roll d10; success on 6+ before modifiers
- **Cost**: 0 IP
- **Valid Targets**: Active, Compromised, Burned (not Captured or Eliminated)
- **On Success**: Target becomes Compromised; attacker gains +3 IP; triggers cartoon piano-drop animation
- **On Failure**: Attacker loses 1 IP; attacker's identity becomes Exposed (revealed to all players)

### 3.2 Sabotage
- **Base Success Rate**: Roll d10; success on 5+ before modifiers
- **Cost**: 0 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Target's next-round IP generation halved; attacker gains +2 IP
- **On Failure**: If defender has Counter-Surveillance active, attacker loses 1 IP

### 3.3 Exposure
- **Base Success Rate**: Roll d10; success on 6+ before modifiers
- **Cost**: 1 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Target's codename revealed for 2 rounds; attacker draws 1 Intel Card and gains +2 IP
- **On Failure**: Attacker's cover is blown; everyone's dossier gets an "Exposed" marker for the attacker; attacker loses 1 IP

### 3.4 Surveillance
- **Base Success Rate**: Roll d10; success on 5+ before modifiers
- **Cost**: 1-2 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Reveal target's chosen defense; if pre-guess matched, +2 IP; draw 1 Intel Card
- **On Failure**: Spent IP is lost; defender draws 1 Intel Card

### 3.5 Infiltration
- **Base Success Rate**: Roll d10; success on 6+ before modifiers
- **Cost**: 1 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Add permanent "Bugged" token to target; draw 1 Secret Intel Card; +1 IP
- **On Failure**: Defender confiscates one random Intel Card; attacker loses 1 IP

### 3.6 Asset Theft
- **Base Success Rate**: Roll d10; success on 5+ before modifiers
- **Cost**: 1 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Steal half of target's unspent IP (rounded down) plus one random gadget; attacker gains +1 IP
- **On Failure**: Spent IP is lost; defender draws 1 Intel Card

### 3.7 Misinformation
- **Base Success Rate**: No roll; target may spend 1 IP on "Disinformation Counter"
- **Cost**: 1 IP
- **Valid Targets**: Active, Compromised, Burned
- **If Unblocked**: Attacker gains +2 IP next round when defender wastes resources
- **If Blocked**: Attacker loses 1 IP; defender draws 1 Intel Card

### 3.8 Network Attack
- **Base Success Rate**: Roll d10; success on 5+ before modifiers
- **Cost**: 2 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Remove one Alliance Token from target; attacker gains +1 IP per link removed
- **On Failure**: Attacker loses 2 IP; defender draws 1 Intel Card

### 3.9 Resource Denial
- **Base Success Rate**: Roll d10; success on 6+ before modifiers
- **Cost**: 2 IP
- **Valid Targets**: Active, Compromised, Burned
- **On Success**: Target loses IP gains from Safe Turns or Witness Bonuses next round; attacker gains +1 IP
- **On Failure**: Attacker loses 2 IP; defender draws 1 Intel Card

### 3.10 Alliance Disruption
- **Base Success Rate**: Roll d10; success on 4-6
- **Cost**: 2 IP
- **Prerequisites**: Two other players must share an active Alliance Token
- **On Success (4-6)**: Breaks their alliance; both allied players lose 1 IP and discard shared intel; attacker gains +1 IP
- **On Failure (1-3)**: Attacker loses 2 IP; both allied defenders draw 1 Intel Card

### 3.11 False Flag
- **Base Success Rate**: Conditional on target's defense
- **Cost**: 2 IP
- **Mechanic**: Choose two players, X (to frame) and Y (actual target)
- **If Y lacks Counter-Intel**: Y believes X attacked; X becomes Exposed and loses 1 IP; attacker gains +2 IP
- **If Y has Counter-Intel**: Attacker loses 2 IP; defender draws 1 Intel Card

### 3.12 Safe Turn (No Operation)
- **Cost**: 0 IP
- **Effect**: Automatically gains +1 IP; no offense declared; can still choose defense and spend IP on gadgets

## 4. Defensive Measure Categories

### 4.1 Physical Security

#### Safe House (Fortress of Trampolines)
- **Cost**: 0 IP (repair costs 1 IP if breached)
- **Counters**: Assassination, Sabotage
- **Effect**: On successful block, attacker discards attacking gadget and loses 1 IP; defender loses 1 IP for repairs

#### Bodyguard Detail (Robo-Duck Patrol)
- **Cost**: 2 IP per round + 1 "Duck Ammo" gadget per block
- **Counters**: Assassination, Infiltration
- **Effect**: Automatically counters one attack; on block, defender draws 1 Intel Card

#### Mobile Operations (Jet-Powered Roller Skates)
- **Cost**: 0 IP (foregoes Safe Turn bonus)
- **Effect**: Attacks against you incur -2 penalty; attacker must guess position first; no IP from Safe Turn

#### Underground (Secret Tunnel Network)
- **Cost**: 1 IP
- **Effect**: Untargetable by direct offenses unless attacker spends 3 IP on Network Attack; grants "Tunnel Map" token

### 4.2 Counter-Intelligence

#### Sweep & Clear (Bug-Sweeping Robot Vacuum)
- **Cost**: 0 IP
- **Counters**: Surveillance, Infiltration
- **Effect**: Automatically counters one attempt; on success, defender draws 1 Intel Card showing attacker's identity

#### False Identity (Switchable Mask Rack)
- **Cost**: 2 IP if Exposure is attempted; otherwise free
- **Effect**: Any Exposure attempt fails; attacker is exposed instead

#### Counter-Surveillance (Mirror Drone Squadron)
- **Cost**: 2 IP (usable every other round)
- **Counters**: Surveillance
- **Effect**: Attacker loses spent IP and Surveillance gadget is destroyed; defender draws 1 Intel Card

#### Disinformation (ACME Fake News Broadcaster)
- **Cost**: 1 IP
- **Effect**: Broadcast false rumor; next round attacks have 50% misfire chance

### 4.3 Active Defense

#### Preemptive Strike (ACME Bat-Torpedo Launch)
- **Cost**: 3 IP
- **Effect**: Before standard matchups, choose suspected attacker; if correct and successful, they lose 2 IP and reveal gadget

#### Alliance Building (Mutual Booby Trap Setup)
- **Cost**: 2 IP per partner
- **Effect**: For 2 rounds, partners cannot target each other; share Intel Cards; betrayal penalties apply

#### Honeypot Operations (Cartoon Bear Trap Suite)
- **Cost**: 3 IP; must discard one gadget if unused
- **Effect**: Place visible lure; opponents entering zone become Stuck and you draw 2 Intel Cards

#### Information Warfare (Biplane Banner Broadcast)
- **Cost**: 2 IP
- **Effect**: See Banner Resolution mechanics in Resolution Phase

## 5. Interaction Matrix Overview

Every possible (Offense, Defense) pair is defined in a lookup table. Each pairing maps to an outcome object describing:
- Whether the offense succeeds or fails
- IP changes for attacker and defender (positive or negative)
- Status changes (e.g., "Defender → Compromised," "Attacker → Exposed")
- Intel revelations gained by either party

### Example Interaction Matrix Entries

```json
{
  "assassination": {
    "safeHouse": {
      "offenseSucceeds": false,
      "ipChangeOffender": -1,
      "ipChangeDefender": +1,
      "newStatusOffender": "exposed",
      "newStatusDefender": "active",
      "intelOffender": [],
      "intelDefender": ["attackerIdentity"]
    },
    "bodyguardDetail": {
      "offenseSucceeds": false,
      "ipChangeOffender": -1,
      "ipChangeDefender": +1,
      "newStatusOffender": "exposed",
      "newStatusDefender": "active",
      "intelOffender": [],
      "intelDefender": ["attackerGadget"]
    },
    "mobileOperations": {
      "offenseSucceeds": true,
      "ipChangeOffender": +2,
      "ipChangeDefender": -2,
      "newStatusOffender": "active",
      "newStatusDefender": "compromised",
      "intelOffender": ["defenderCompromised"],
      "intelDefender": []
    },
    "default": {
      "offenseSucceeds": true,
      "ipChangeOffender": +3,
      "ipChangeDefender": -3,
      "newStatusOffender": "active",
      "newStatusDefender": "compromised",
      "intelOffender": ["defenderStatus"],
      "intelDefender": []
    }
  }
}
```

## 6. Resource Management & Equipment

### 6.1 Intelligence Points (IP)

#### How IP Is Earned
- **Successful Operations**: Assassination (+3), Sabotage/Exposure/Capture (+2 each)
- **Defensive Success**: Neutralizing an attack (+1), Counter-intel intercept (+2)
- **Witness Bonuses**: Safe Turn (+1), Prediction Bonus (+2 for correctly guessing two opponents' actions)
- **Asset Control**: +1 IP per round per Strategic Asset held

#### How IP Is Spent
- **Gadget Purchases & Recharges**: 1-5 IP each
- **Alliance Funding**: Non-Aggression Pact (2 IP per partner), Coordinated Operation (3 IP per partner)
- **NPC Bribes**: 1-2 IP for ACME Guard Dog, ACME Mailman
- **Defensive Costs**: False Identity (2 IP), Underground (1 IP), Biplane Banner (2 IP)
- **Gadget Upkeep**: 1 IP per active gadget requiring recharge

#### IP Limits
- **Floor**: IP can go to -10; below -10 while Burned triggers elimination
- **Ceiling**: No maximum limit
- **Negative Spending**: Cannot spend IP you don't have (minimum 0 for purchases)

### 6.2 Gadgets

#### Surveillance Gear

**Listening Devices** (1 IP, one-time)
- Effect: Next Surveillance attempt succeeds automatically unless target has Sweep & Clear

**Camera Networks** (3 IP)
- Effect: Takes one full Planning Phase to assemble; following round reveals one opponent's chosen defense

**Communication Intercepts** (2 IP, one-time)
- Effect: When any two players form alliance, automatically steal and reveal that intel

#### Combat Equipment

**Silenced Weapons** (2 IP)
- Effect: +1 success modifier on Assassination rolls; treats ties as attacker wins vs. Safe House

**Explosives Box** (3 IP)
- Effect: One-time Sabotage with +2 success modifier; 50% misfire chance (attacker → Compromised, -2 IP)

**Body Armor** (2 IP)
- Effect: +1 defense roll modifier when targeted by direct attacks; cannot combine with Underground

#### Counter-Intelligence Tools

**Bug Detectors** (2 IP)
- Effect: Automatically nullify one Infiltration or Surveillance per round; defender draws 1 Intel Card

**Signal Jammers** (3 IP)
- Effect: Blocks one remote-wired gadget per round; if triggered, attacker's gadget destroyed

**Fake Documents Kit** (2 IP)
- Effect: If targeted by Exposure, treat as failure; attacker loses 1 IP, you remain hidden

#### Advanced Gadgets

**ACME Mobile Fortress** (5 IP)
- Prerequisites: Own both Robo-Duck Patrol and Portable Safe House Kit
- Effect: One-turn invincibility; all attacks automatically fail; no IP generation that round

**ACME Time-Bomb Beetle** (3 IP)
- Effect: On successful Infiltration vs. non-Counter-Intel defense, target starts next round as Compromised (-2 IP)

**ACME Anvil Drone** (4 IP)
- Prerequisite: Own Jetpack Roller Skates
- Effect: One-time long-range Assassination with +2 success modifier; 25% misfire chance

**Jetpack Roller Skates** (3 IP)
- Effect: +1 initiative when using Mobile Operations; act first among ties

### 6.3 Status System

#### Active (Green)
- Full offensive/defensive options
- 100% IP generation
- UI: Green avatar border, no penalty badges

#### Compromised (Yellow)
- Triggered by: Lost direct attack, severe sabotage, gadget misfire
- IP generation: 80% of normal
- Restrictions: Cannot select False Identity or Honeypot Operations
- Recovery: Spend 2 IP to "Bribe ACME Rumor Mill" → return to Active

#### Burned (Orange)
- Triggered by: Repeated Compromises, failed Capture escape
- IP generation: 50% of normal
- Restrictions: Only Mobile Operations or Sweep & Clear defenses; no new gadget purchases or banner broadcasts
- Recovery: Spend 3 IP to "Bribe ACME Rumor Mill" → return to Active

#### Captured (Red)
- Triggered by: Successful Capture offense
- Effect: Skip next Planning Phase; no offense/defense choices; IP generation = 0
- Ghost Status: Draw 1 Intel Card per round
- Escape: Spend 2 Intel Cards to "Bribe ACME Jailbreak" → return as Burned

#### Eliminated (Black)
- Triggered by: Captured twice without escape, or IP below -10 while Burned
- Effect: Removed from normal play; switch to Ghost Mode
- Ghost Powers: Draw 1 Intel Card per round; spend 2 Intel Cards to "Haunt" (force living agent to lose 1 IP)
- Endgame: Cannot win but can influence outcome

### 6.4 Strategic Assets

**ACME Bank**
- Control Cost: 2 IP
- Yield: +1 IP per round

**ACME Armory**  
- Control Cost: 3 IP
- Yield: +2 IP per round

**ACME Black Market**
- Control Cost: 2 IP  
- Yield: +1 IP per round

**ACME Broadcast Station**
- Control Cost: 2 IP
- Yield: +2 IP per round

**ACME Underground Tunnel Hub**
- Control Cost: 4 IP
- Yield: +3 IP per round

Asset control is gained through successful Network Attacks or Alliance Building against current controllers.

### 6.5 Alliances & Betrayal

#### Non-Aggression Pact
- **Cost**: 2 IP per partner, lasts 2 rounds
- **Effect**: Partners cannot target each other; shared Intel Cards (copies distributed)
- **Betrayal Penalty**: Attacker → Compromised (-2 IP), cannot form new alliances for 3 rounds

#### Coordinated Operation
- **Cost**: 3 IP per partner
- **Effect**: Must select same target; if both succeed, split stolen IP equally
- **Failure**: If either fails, both lose spent IP

## 7. Master Plans (Secret Objectives)

Each player receives one hidden Master Plan at game start. These provide alternative victory paths and long-term strategic goals.

### Sample Master Plans

#### Expose All
- **Objective**: Use 'Exposure' successfully on every Active opponent in a single round
- **Reward**: +5 IP and immediate Intelligence Supremacy if all opponents revealed

#### Control All Assets
- **Objective**: Hold all five Strategic Assets at the start of your turn
- **Effect**: Immediate Network Control victory

#### Anvil Carnage
- **Objective**: Land successful Assassination using 'Spring-Loaded Anvil' on three different opponents in consecutive rounds
- **Reward**: +3 IP and immediate elimination of any one Compromised player of choice

#### Mastermind of Misinformation
- **Objective**: Successfully trick three different opponents with 'Misinformation' in a single round
- **Reward**: +4 IP

#### Saboteur Supreme
- **Objective**: Perform successful 'Sabotage' on a Strategic Asset three times in a row
- **Reward**: Target loses control permanently (asset remains unowned for one round), +5 IP

## 8. Victory Conditions & Endgame

### Victory Conditions

1. **Last Spy Standing**: Only player whose status is not Captured or Eliminated
2. **Intelligence Supremacy**: Collect Full Dossier on every other Active agent (three distinct Intel Cards per opponent: codename, safe-house location, preferred gadget)
3. **Network Control**: Control three of five Strategic Assets simultaneously at round start
4. **Mission Completion**: Fulfill secret Master Plan conditions
5. **Alliance Victory**: Two allied players fulfill shared Master Plan objective → triggers Final Showdown

### Final Showdown (Alliance Victory)
When allied players achieve joint victory:
1. Both players receive +3 IP immediately
2. Both simultaneously choose between Assassination or Sabotage (no defenses allowed)
3. Higher roll (or higher current IP on tie) takes 1st place; other gets runner-up

### Endgame Tension
As players become Compromised or Eliminated, the board narrows. Players nearing victory become primary targets. Limited IP and fewer valid targets force high-stakes decisions, ensuring chaotic slapstick endings with piano crashes, anvil drops, and custard pie mayhem.

## 9. Mode Variants

### 2-Player (1v1) Mode
- **Starting IP**: 7 IP each instead of 5, plus two random starting gadgets
- **Timer**: 60 seconds Planning Phase instead of 90
- **Available Actions**: Remove alliance-dependent offenses/defenses
- **Victory Conditions**: Only "Last Spy Standing" and "Intelligence Supremacy"

### 6-Player Mode
- **Starting IP**: 5 IP each
- **Timer**: Full 90 seconds Planning Phase
- **Available Actions**: All 11 offenses and 12 defenses active
- **Victory Conditions**: All five conditions apply; alliances become strategic necessities

## 10. Sample Round Transcript

**Setup**: 4 players - AgentA (Active, 6 IP), AgentB (Compromised, 3 IP), AgentC (Active, 5 IP), AgentD (Burned, 2 IP)

### Planning Phase (90 seconds)
- **AgentA**: Offense = Assassination vs. AgentB, Defense = Bodyguard Detail, IP = 2
- **AgentB**: Offense = Surveillance vs. AgentC, Defense = Counter-Surveillance, IP = 1  
- **AgentC**: Offense = Sabotage vs. AgentD, Defense = Safe House, IP = 0
- **AgentD**: Offense = Exposure vs. AgentA, Defense = Underground, IP = 1
- All players confirm choices at ~60 seconds remaining

### Execution Phase
- All choices revealed simultaneously
- No banners this round

### Resolution Phase (using Interaction Matrix)

**AgentA's Assassination vs. AgentB's Counter-Surveillance**
- Counter-Surveillance doesn't specifically counter Assassination; treated as active defense with +1 modifier
- Assassination fails; AgentA loses 1 IP (→ 5 IP), becomes Exposed; AgentB gains +1 IP (→ 4 IP)

**AgentB's Surveillance vs. AgentC's Safe House** 
- Safe House blocks low-level espionage; Surveillance fails
- AgentB loses 1 IP (→ 3 IP); AgentC gains +1 IP (→ 6 IP)

**AgentC's Sabotage vs. AgentD's Underground**
- Underground makes AgentD untargetable by Sabotage
- Sabotage fails automatically; AgentC loses 0 IP (spent none), gains no IP

**AgentD's Exposure vs. AgentA's Bodyguard Detail**
- Bodyguard Detail blocks one Exposure attempt
- AgentD loses 1 IP (→ 1 IP); AgentA gains +1 IP (→ 6 IP)

### Adaptation Phase
**Final IP Totals**: AgentA: 6 IP (Compromised), AgentB: 3 IP (Active), AgentC: 6 IP (Active), AgentD: 1 IP (Burned)

**Status Updates**: AgentA becomes Compromised (yellow border)

**Intel Gains**: AgentB saw AgentA's gadget; AgentC knows AgentB attempted surveillance; AgentA knows AgentD tried exposure

**Victory Check**: No conditions met; prepare for Round 2 