Below is a fully revised, code-free development checklist for building **James Bland: ACME Edition** as a **mobile-first**, **LAN-only** (WLAN) HTML5/JavaScript + Python Flask-SocketIO application. Because you don’t have any assets yet, this guide begins by specifying exactly what assets you need and where to place or create them. Follow each item in order—by the end, you’ll have a complete to-do list describing every file, folder, and content requirement without showing any actual code.

---

## 1. Project Root & Top-Level Files

### 1.1 Create the Project Folder

* **Name**: `JamesBland/`
* **Purpose**: This will be the root of everything—source code, assets, documentation, tests, and helper scripts.

### 1.2 Inside the Root, Add:

1. **README.md**

   * **Purpose**: Provide a high-level overview of the game, instructions to build and run, and a plain-English explanation of the folder structure.
   * **Contents** (fill in details as you build; outline in plain language):

     1. **Brief Description**

        > “James Bland: ACME Edition is a 2–6 player, mobile-first espionage game that runs over your home Wi-Fi network. Each player uses a browser on their phone, tablet, or laptop to join a local Python server. Gameplay revolves around selecting cartoonish ACME-style traps each turn, balancing offense and defense, and gathering Intelligence Points (IP).”

     2. **Prerequisites**

        * Python 3.7+ (no extra game engines).
        * A modern browser (Chrome, Safari, Firefox) on each device.
        * All devices connected to the same Wi-Fi network.

     3. **Installation Steps** (in prose):

        1. “Clone or download this repository.”
        2. “Create and activate a Python virtual environment.”
        3. “Install dependencies from `requirements.txt`.”
        4. “Run the Python server script: `python server.py`.”
        5. “On each device, open a browser and navigate to `http://<HOST_IP>:5000` (replace `<HOST_IP>` with your server’s LAN address).”

     4. **Folder Structure Overview**

        * `docs/` – Design docs (game rules, protocols, art guide, network topology).
        * `assets/` – Raw images, audio, and fonts (before optimization).
        * `static/` – All files served by Flask (optimized assets, CSS, JS).
        * `templates/` – HTML templates (only `index.html` for this single-page app).
        * `tests/` – Pytest files to verify core logic.
        * `scripts/` – Helper scripts (asset copying, deck generation).
        * `server.py` – The main Flask + Flask-SocketIO server.
        * `requirements.txt` – Python dependencies.
        * `.gitignore` – Files and folders to ignore in Git.

     5. **How to Play Summary**

        > “Players join a lobby, pick a codename, and wait until at least 2 players are ready. Each round, everyone has \~90 seconds to select one offense, one defense, optionally set IP to spend, and (if chosen) type a brief biplane banner message. All choices reveal simultaneously, the server resolves all pairings, updates IP/status/intel, and then players adapt before the next round. Victory can come from elimination, gathering complete dossiers, controlling strategic assets, or fulfilling a secret Master Plan.”

     6. **License & Contributing Notes**

        * Mention your chosen license (e.g., MIT or “All Rights Reserved”).
        * “This project is primarily for personal/family use; feel free to fork and adjust, but please credit the original authors.”

2. **LICENSE**

   * **Purpose**: Declare licensing terms.
   * **Contents**: If you choose the MIT License, include the standard MIT text. If you prefer to reserve all rights, state that clearly.

---

## 2. Documentation Folder (`docs/`)

Create a folder named `docs/` at the project root. Inside `docs/`, create these four Markdown files. They will capture design details, network protocols, art direction, and topology diagrams. Fill them in as you develop the game.

```
/docs/
├── game_design.md
├── protocol_spec.md
├── art_style_guide.md
└── network_topology.md
```

### 2.1 `game_design.md`

* **Purpose**: Fully document game rules, mechanics, flow, and examples in plain English, so anyone can understand exactly how James Bland: ACME Edition works.

* **Structure & Required Content**:

  1. **Introduction & Core Concept**

     * Explain that James Bland: ACME Edition transforms a solo “presidential protection” idea into a competitive 2–6 player espionage game over LAN.
     * Emphasize the ACME-style cartoon traps (pianos, anvils, springs, custard pies) and the slapstick tone.

  2. **Overall Turn Structure**

     * **Planning Phase (90 sec)**

       1. Players choose one **Offensive Operation** (optionally targeting another player).
       2. Players choose one **Defensive Measure** to protect themselves.
       3. Players decide how many **Intelligence Points (IP)** to commit (0 up to their current IP).
       4. If they selected “Information Warfare (Biplane Banner),” they also type a short message (max 50 characters) to be flown overhead.
       5. Each client sends these choices to the server (via WebSocket).
     * **Resolution Phase**

       * As soon as all active players have submitted (or the 90 sec timer runs out), the server reveals everyone’s offense, defense, and (if used) banner messages.
       * If any player paid for a **Biplane Banner**, the server triggers a banner animation on all clients, then prompts each attacker who targeted that banner-caster to **“Believe”** the message or **“Ignore”** it (10 sec timer).
       * After banner decisions are collected (or timeouts), the server resolves every offense vs. defense pairing simultaneously according to the **Interaction Matrix** (detailed below).
       * Results include IP changes, status changes (Compromised, Burned, Captured, Eliminated), gadgets lost or gained, and intel revelations.
     * **Adaptation Phase**

       * The server updates each player’s in-memory state: new IP totals, new statuses, newly gained Intel Cards, and updated gadget inventories.
       * Players may spend IP on new gadgets, recharge existing ones, bribe NPCs, or form/break alliances (as long as they have the IP).
       * The server checks all victory conditions (Last Spy Standing, Intelligence Supremacy, Network Control, Mission Completion, Alliance Victory). If someone has won, the game ends. Otherwise, the server resets submissions and increments the round counter, and a new Planning Phase begins.

  3. **Offensive Operation Categories**
     For each offense, include:

     * **Name** (e.g., “Assassination”)
     * **Base Success Rate** (in prose, e.g., “Roll a d10; success on 6+ before modifiers.”)
     * **Cost in IP** (if any)
     * **Possible Targets** (which statuses you can legally target: Active, Compromised, Burned; you cannot target Captured or Eliminated)
     * **On Success Effects** (e.g., “Target becomes Compromised; attacker gains +3 IP; if defender did not have Bodyguard Detail, trigger cartoon piano-drop.”)
     * **On Failure Effects** (e.g., “Attacker loses 1 IP; attacker’s identity becomes Exposed (everyone’s dossier tags you as Exposed).”)

     List all offenses in separate subsections:

     1. **Assassination**

     2. **Sabotage**

     3. **Exposure** (reveals target’s codename or vulnerabilities)

     4. **Surveillance**

     5. **Infiltration**

     6. **Asset Theft**

     7. **Misinformation**

     8. **Network Attack**

     9. **Resource Denial**

     10. **Alliance Disruption**

     11. **False Flag**

     > **Note**: In a two-player duel, omit “Alliance Disruption” and “Alliance-related” offenses, since no alliances can form.

  4. **Defensive Measure Categories**
     For each defense, describe:

     * **Name** (e.g., “Safe House”)
     * **Cost in IP** (if any)
     * **Which Offenses It Counters** (e.g., “Blocks Assassination and Sabotage attempts.”)
     * **On Successful Block Effects** (e.g., “Defender gains +1 IP; attacker’s gadget is destroyed; attacker becomes Exposed.”)
     * **Secondary Notes** (e.g., “If you use Safe House, you cannot attack this turn.”)

     List all defenses similarly:

     1. **Safe House**

     2. **Bodyguard Detail**

     3. **Mobile Operations**

     4. **Underground**

     5. **Sweep & Clear** (counters Surveillance and Infiltration)

     6. **False Identity**

     7. **Counter-Surveillance**

     8. **Disinformation**

     9. **Preemptive Strike**

     10. **Alliance Building** (temporary pact)

     11. **Honeypot Operations**

     12. **Information Warfare (Biplane Banner)**

     > **Note**: In a 2-player duel, “Alliance Building” and “Alliance-related” defenses should not appear in the dropdown.

  5. **Interaction Matrix Overview**

     * Explain that every possible `(Offense, Defense)` pair is defined in a lookup table (JSON or Python dict). Each pairing maps to an **outcome object** describing:
       • Whether the offense succeeds or fails
       • IP changes for attacker and defender (positive or negative)
       • Status changes (e.g., “Defender → Compromised,” “Attacker → Exposed”)
       • Exactly which bits of intel the attacker or defender gains (e.g., “Reveal defender’s next chosen defense,” “Reveal attacker’s codename”)

     * Provide a small **excerpt** as an example (two or three pairings). For instance:

       ```
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
         },
         ...
       }
       ```

     * Note that “default” covers any defense not explicitly listed under that offense.

  6. **Resource Management & Equipment**

     * **Intelligence Points (IP)**:

       1. **How IP Is Earned**

          * **Successful Offense** (see above for each offense’s rewards).
          * **Successful Defense** (e.g., blocking an attack yields +1 IP, intercepting a bug yields +2 IP).
          * **Witness Bonus**: If you neither attacked nor were attacked, you gain +1 IP for a Safe Turn.
          * **Prediction Bonus**: If you correctly guess another player’s offense and defense that round (revealed at end), you gain +2 IP.
          * **Asset Control**: Each Strategic Asset you hold yields +1 IP (or +2/ +3 IP for higher-value assets) per round.
       2. **How IP Is Spent**

          * **Purchasing Gadgets** (cost varies by gadget).
          * **Spending on offense or defense** (some actions require IP to activate).
          * **Forming Alliances** (cost per partner per round).
          * **Bribing NPCs** (e.g., ACME Guard Dog or ACME Mailman).
          * **Gadget Upkeep & Recharge** (certain gadgets need 1 IP each round to stay active).
          * **Maintaining False Identity** (2 IP if someone tries to expose you).
          * **Underground Maintenance** (1 IP per round to remain underground).
          * **Biplane Banner Broadcast** (always costs 2 IP).
       3. **IP Floor & Ceiling**

          * Document if IP can go negative (you may allow down to –10 before auto-elimination) or if there is a hard minimum (e.g., cannot spend if you have 0).

     * **Gadgets** (“special cards” you can purchase; list 10–12 total). For each gadget:

       1. **Name** (e.g., “Spring-Loaded Anvil”)
       2. **Cost** (in IP)
       3. **Effect** (in plain language, including on-use success modifiers or one-time triggers)
       4. **Cooldown/Recharge** (if applicable)

       Example gadgets:

       1. **Spring-Loaded Anvil**

          * **Cost**: 2 IP
          * **Effect**: +1 success modifier when performing Sabotage; if Sabotage fails, you lose 2 IP and become Compromised.
       2. **Jetpack Roller Skates**

          * **Cost**: 3 IP
          * **Effect**: Grants +2 defense bonus against Assassination and Capture; however, you generate –1 IP per round spent on skates (you’re too busy skating).
       3. **Robo-Duck Patrol**

          * **Cost**: 2 IP
          * **Effect**: Automatically blocks one Assassination or Infiltration each round. If it blocks, you gain +1 IP and reveal the attacker’s identity.
       4. **Bug Detector**

          * **Cost**: 2 IP
          * **Effect**: Counters one Infiltration or Surveillance per round. If it succeeds, you gain +1 IP and see the attacker’s identity.
       5. **Silenced Weapons**

          * **Cost**: 1 IP per use
          * **Effect**: Lowers detection chance on Assassination by 25% (effectively +1 success modifier).
       6. **Mobile Fortress (Advanced)**

          * **Cost**: 5 IP
          * **Prerequisite**: Must already own “Robo-Duck Patrol” and “Portable Safe House.”
          * **Effect**: One-turn invincibility: all attacks automatically fail. You generate no IP that turn.
       7. **Time-Bomb Beetle**

          * **Cost**: 3 IP
          * **Effect**: On a successful Infiltration (if target has no Counter-Intel), you plant a time bomb. At the start of the next Resolution Phase, if target is still Active or Compromised, they become Compromised (–2 IP).
       8. **Anvil Drone**

          * **Cost**: 4 IP
          * **Prerequisite**: Own “Jetpack Roller Skates.”
          * **Effect**: One-time long-range Assassination with +2 success modifier; 25% chance to misfire, dropping an anvil on a random adjacent agent.
       9. **Honeypot Forklift**

          * **Cost**: 3 IP
          * **Effect**: Used only when you selected “Honeypot Operations.” If someone attempts Sabotage or Asset Theft against you and enters the designated zone, they become Stuck (lose their next action) and you draw 2 Intel Cards. If no one triggers it, you must discard one gadget due to wasted setup.
       10. **Mirror Drone Squadron**

       * **Cost**: 2 IP (usable every other round)
       * **Effect**: If targeted by Surveillance, attacker loses spent IP, their drone is destroyed, and you draw 1 Intel Card revealing attacker’s details.

       11. *(Add 1–2 more as needed to reach around a dozen total.)*

     * **Statuses & Transitions** (explain how players move between these states):

       1. **Active**

          * Full offense/defense options, IP generation ×1.
       2. **Compromised**

          * Triggered by a successful Assassination or heavy Sabotage.
          * IP generation at ×0.8 (rounded down).
          * Cannot use “False Identity” or “Honeypot Operations.”
          * To recover: spend 2 IP to “Bribe ACME Rumor Mill” during Adaptation Phase (return to Active).
       3. **Burned**

          * Triggered by repeated Compromises or failing a Capture.
          * IP generation at ×0.5 (rounded down).
          * Only allowed defenses: Mobile Operations or Sweep & Clear; cannot purchase new gadgets or broadcast banners.
          * To recover: spend 3 IP to “Bribe ACME Rumor Mill” during Adaptation Phase (return to Active).
       4. **Captured**

          * Triggered by a successful Capture offense.
          * Skips the next Planning Phase (no offense/defense choices).
          * IP generation = 0 while captured.
          * Upon capture, you become a **Ghost Agent**: you draw 1 Intel Card each round.
          * You may spend 2 Intel Cards to “Bribe ACME Jailbreak” and escape immediately—upon escape, you return as Burned.
       5. **Eliminated**

          * Occurs if you are Captured twice without escaping, or if your IP drops below –10 while Burned.
          * Removed from normal play.
          * You remain as a **Ghost Agent** (semi-transparent view). Each round, you draw 1 Intel Card.
          * You can spend 2 Intel Cards to “Haunt” a living agent: they lose 1 IP that round. You cannot win but can influence the endgame.

     * **Strategic Assets** (neutral board tokens that players can capture for passive IP):

       1. **ACME Bank**

          * **Control Cost**: 2 IP
          * **Yield**: +1 IP per round as long as you hold it.
       2. **ACME Armory**

          * **Control Cost**: 3 IP
          * **Yield**: +2 IP per round.
       3. **ACME Black Market**

          * **Control Cost**: 2 IP
          * **Yield**: +1 IP per round.
       4. **ACME Broadcast Station**

          * **Control Cost**: 2 IP
          * **Yield**: +2 IP per round.
       5. **ACME Underground Tunnel Hub**

          * **Control Cost**: 4 IP

          * **Yield**: +3 IP per round.

       > When you perform a “Network Attack” or “Alliance Building” that succeeds against a controller, you replace their Influence Token on that asset with your own.

     * **Alliances & Betrayal**:

       1. **Non-Aggression Pact**

          * **Cost**: 2 IP per partner, lasts 2 rounds.
          * **Effect**: Neither agent can target the other for 2 rounds. Any Intel Cards one draws are automatically shared (the partner receives a copy).
          * **Betrayal Penalty**: If one insidiously attacks their ally during the pact, they become Compromised (–2 IP) and cannot form new alliances for 3 rounds.
       2. **Coordinated Operation**

          * **Cost**: 3 IP per partner, must select the same target in Planning Phase.
          * **Effect**: If both succeed in hitting the agreed target, they split the stolen IP (rounded down) equally.
          * **Failure Penalty**: If either fails, both lose their spent IP.

  7. **Master Plans (Secret Objectives)**

     * At game start, each player draws one hidden Master Plan from a shuffled deck. These are long-term goals that usually require multiple steps.
     * Provide 5–10 sample Master Plans. For each:

       1. **Name** (e.g., “Expose All Agents”)
       2. **Description** (in plain English)
       3. **Reward IP** (if any) or **Instant Win Condition**
       4. **Conditions to Fulfill** (exact requirement)

       Examples:

       1. **Expose All**

          * “Use ‘Exposure’ successfully on every Active opponent in a single round.”
          * **Reward**: +5 IP (and immediate Intelligence Supremacy if you reveal all opponents).
       2. **Control All Assets**

          * “Hold all five Strategic Assets at the start of your turn.”
          * **Effect**: Immediate Network Control victory.
       3. **Anvil Carnage**

          * “Land a successful Assassination using a ‘Spring-Loaded Anvil’ on three different opponents in consecutive rounds.”
          * **Reward**: +3 IP and immediate elimination of any one Compromised player of your choice.
       4. **Mastermind of Misinformation**

          * “Successfully trick three different opponents with ‘Misinformation’ in a single round (they waste IP defending against false intel).”
          * **Reward**: +4 IP.
       5. **Saboteur Supreme**

          * “Perform successful ‘Sabotage’ on a Strategic Asset three times in a row.”
          * **Reward**: The target loses control of that asset permanently (remains unowned for one round), plus +5 IP.

  8. **Victory Conditions & Endgame**

     * **Last Spy Standing**: You are the only player whose status is not Captured or Eliminated.

     * **Intelligence Supremacy**: You collect a **Full Dossier** on every other Active agent (three distinct Intel Cards per opponent: codename, safe-house location, and preferred gadget).

     * **Network Control**: You control **three** of the five Strategic Assets simultaneously at the start of a round.

     * **Mission Completion (Master Plan)**: You fulfill your secret Master Plan’s conditions.

     * **Alliance Victory**: If two allied players fulfill a shared Master Plan objective together, they achieve a joint victory. Immediately after that, the server triggers a **Final Showdown**: both get +3 IP, then simultaneously choose between Assassination or Sabotage (no defenses). The one with the higher roll (or, on a tie, higher current IP) takes 1st place; the other is runner-up.

     * **Endgame Tension**:

       > As players get Compromised or Eliminated, the board narrows. A player nearing victory (controlling assets or nearly completing a Master Plan) becomes everyone’s target. Alliances form and collapse in desperation. Limited IP and few remaining valid targets force high-stakes gambits, ensuring every playthrough ends in slapstick chaos (piano crashes, anvil drops, custard pies).

  9. **Mode Variants**

     * **2-Player (1v1) Mode**

       1. **Starting IP**: Each begins with 7 IP instead of 5, plus two random starting gadgets (e.g., “Spring-Loaded Anvil” & “Jetpack Roller Skates”).
       2. **Timer**: Planning Phase timer reduced to 60 seconds.
       3. **Offense/Defense Listings**: Remove any offense or defense requiring alliances (e.g., “Alliance Disruption,” “Alliance Building”). Biplane Banner remains available.
       4. **Victory**: Only “Last Spy Standing” and “Intelligence Supremacy” apply; “Network Control” and “Alliance Victory” are unavailable.

     * **6-Player Mode**

       1. **Starting IP**: Each begins with 5 IP.
       2. **Timer**: Use full 90 seconds.
       3. **All Offenses & Defenses Active**: All 11 offenses and 12 defenses appear in the dropdowns.
       4. **Victory**: All five conditions apply. Alliances become strategic necessities.

  10. **Sample Round Transcript**
      Provide a step-by-step example in plain English (no code) of a 4-player turn:

      **Players**: AgentA (Active, 6 IP), AgentB (Compromised, 3 IP), AgentC (Active, 5 IP), AgentD (Burned, 2 IP).

      1. **Planning Phase (90 sec)**

         * AgentA chooses: Offense = “Assassination vs. AgentB,” Defense = “Bodyguard Detail,” IP to spend = 2.
         * AgentB chooses: Offense = “Surveillance vs. AgentC,” Defense = “Counter-Surveillance,” IP = 1.
         * AgentC chooses: Offense = “Sabotage vs. AgentD,” Defense = “Safe House,” IP = 0.
         * AgentD chooses: Offense = “Exposure vs. AgentA,” Defense = “Underground,” IP = 1.
         * None selected Biplane Banner, so no banner message is entered.
         * All players click “Confirm Choices” at \~60 sec remaining.

      2. **Execution Phase**

         * All offensive/defensive choices reveal simultaneously.
         * No banners to resolve this round.

      3. **Resolution Phase** (using Interaction Matrix):

         * **AgentA’s Assassination vs. AgentB’s Counter-Surveillance**

           * Counter-Surveillance automatically blocks Surveillance/Infiltration, but in this case, it blocks “Exposure” or “Surveillance”; for Assassination, treat as a generic “active defense with +1,” so the assassination fails.
           * Outcome: AgentA loses 1 IP (→ 5 IP), becomes Exposed. AgentB gains +1 IP (→ 4 IP). AgentB sees AgentA’s gadget and new status.
         * **AgentB’s Surveillance vs. AgentC’s Safe House**

           * Safe House defends against low-level espionage. Surveillance fails.
           * Outcome: AgentB loses 1 IP (→ 3 IP). AgentC gains +1 IP (→ 6 IP). AgentC’s dossier records “AgentB attempted Surveillance.”
         * **AgentC’s Sabotage vs. AgentD’s Underground**

           * Underground makes AgentD untargetable by Sabotage.
           * Outcome: Sabotage fails automatically. AgentC loses 0 IP (spent none), but does not gain any IP. AgentD remains safe and unchanged.
         * **AgentD’s Exposure vs. AgentA’s Bodyguard Detail**

           * Bodyguard Detail blocks one Exposure. The attempt fails.
           * Outcome: AgentD loses 1 IP (→ 1 IP). AgentA gains +1 IP (from blocked Exposure) (→ 6 IP). AgentA’s dossier records “AgentD tried to expose you.”

      4. **Cascading & Adaptation**

         * **IP Adjustments**:

           * AgentA: 6 IP (after losing 1, then gaining 1)
           * AgentB: 3 IP (after failing Surveillance)
           * AgentC: 6 IP (after safe-house block)
           * AgentD: 1 IP (after failing Exposure)
         * **Status Updates**:

           * AgentA: Becomes **Compromised** (yellow) because of the failed assassination.
           * AgentB: Remains **Active**.
           * AgentC: Remains **Active**.
           * AgentD: Remains **Burned** (no change).
         * **Intel Gains**:

           * AgentB saw AgentA’s gadget.
           * AgentC knows AgentB tried to surveil them.
           * AgentA knows AgentD attempted an Exposure.
         * **Safe Turn & Prediction Bonuses**:

           * No one had a “safe turn” (everyone tried an offense).
           * If any player correctly predicted two opponents’ offense+defense, they get +2 IP now. (Document this if it happened.)
         * **Gadget Upkeep**: Any agents who own gadgets requiring recharge (e.g., Mirror Drones, Robo-Duck) must spend 1 IP to keep them active. Document which gadgets were recharged or deactivated.
         * **Asset Control**: If anyone held a Strategic Asset, they gain its IP yield.
         * **Alliance Adjustments**: If any two were in a Non-Aggression Pact, decrement its remaining rounds; if it expired, break the pact now.
         * **Victory Check**:

           * No one is eliminated.
           * No full dossiers completed.
           * No one controls ≥3 assets.
           * No Master Plan fulfilled.
           * No alliance joint objective met.
         * **Prepare for Round 2**: Server increments `current_round` to 2 and clears submissions. New Planning Phase begins.

      5. **Next Round Considerations**

         * AgentA (Compromised, 6 IP) might spend 2 IP to “Bribe ACME Rumor Mill” to return to Active.
         * AgentB (Active, 3 IP) might plan offensive combos or gather Intel.
         * AgentC (Active, 6 IP) could attempt Asset Theft to grab a Strategic Asset.
         * AgentD (Burned, 1 IP) is low on IP, so likely “Underground” again or attempt “Misinformation” for 1 IP to generate free IP.

### 2.2 `protocol_spec.md`

* **Purpose**: Precisely document how all real-time messages flow over WebSocket events between the clients and the server. This ensures frontend and backend remain in sync as you implement.

* **Structure & Required Content**:

  1. **Overview**

     * Explain that the server is a Flask + Flask-SocketIO application listening on port 5000.
     * Each client device (phone, tablet, laptop) opens a WebSocket connection to `http://<HOST_IP>:5000`.
     * All real-time messages (lobby join, action submissions, turn results, reconnections) use this WebSocket; no HTTP polling.

  2. **Event Definitions**

     * **Client → Server**

       1. **`joinLobby`**

          * Payload:

            ```json
            { "codename": "<string>" }
            ```
          * Purpose: Register a new player. The server assigns them initial IP, gadgets, and “active” status.
       2. **`startGame`** (host only)

          * Payload: *none*
          * Purpose: Host signals that all players in lobby are ready and game should begin.
       3. **`submitAction`**

          * Payload:

            ```json
            {
              "offenseId": "<string or empty>",
              "defenseId": "<string>",
              "targetCodename": "<string or empty>",
              "ipToSpend": <integer>
            }
            ```
          * Purpose: Client sends their selected offense, defense, target (if any), and IP to spend this turn.
       4. **`requestGameState`**

          * Payload: *none*
          * Purpose: If a client reconnects mid-game, server responds with a snapshot of the current round and full state so they can catch up.

     * **Server → Client**

       1. **`lobbyJoined`**

          * Payload:

            ```json
            {
              "yourCodename": "<string>",
              "allPlayers": [
                { "codename": "<string>", "status": "<string>", "ip": <integer> }, …
              ],
              "roundTimer": <integer>,      // e.g., 90
              "maxPlayers": <integer>      // always 6
            }
            ```
          * Purpose: Confirm to the newly joined client their assigned codename (or echoed), and send the current lobby roster with each player’s status and IP.

       2. **`lobbyUpdate`**

          * Payload:

            ```json
            {
              "allPlayers": [
                { "codename": "<string>", "status": "<string>", "ip": <integer> }, …
              ]
            }
            ```
          * Purpose: Broadcast to everyone in the lobby whenever anyone joins or leaves, updating the displayed player list.

       3. **`gameStarted`**

          * Payload:

            ```json
            {
              "gameConfig": {
                "initialIP": 5,
                "roundTimer": 90,
                "maxPlayers": 6
              },
              "currentPlayers": [
                {
                  "codename": "<string>",
                  "status": "<string>",
                  "ip": <integer>,
                  "gadgets": ["<gadgetId>", …],
                  "intel": []
                }, …
              ]
            }
            ```
          * Purpose: Signal all clients to switch from the lobby view to the planning UI. Contains initial IP, timer, and each player’s starting state.

       4. **`playerSubmitted`**

          * Payload:

            ```json
            { "codename": "<string>" }
            ```
          * Purpose: Notify all clients that this player has locked in their offense & defense. UI will display a checkmark next to their name.

       5. **`turnResult`**

          * Payload:

            ```json
            {
              "round": <integer>,
              "results": [
                {
                  "codename": "<string>",
                  "ipDelta": <integer>,
                  "newIP": <integer>,
                  "newStatus": "<string>",
                  "intelGained": ["<desc>", …]
                }, …
              ]
            }
            ```
          * Purpose: Provide every client with the outcome of the just-completed round. Clients update their HUDs, play SFX/animations, and show the resolution log.

       6. **`gameStateSnapshot`**

          * Payload:

            ```json
            {
              "round": <integer>,
              "players": [
                {
                  "codename": "<string>",
                  "status": "<string>",
                  "ip": <integer>,
                  "gadgets": ["<gadgetId>", …],
                  "intel": ["<string>", …]
                }, …
              ]
            }
            ```
          * Purpose: Provide a newly reconnected client with the full current game state (round number, each player’s status, IP, gadget inventory, collected intel), so the client can rebuild its UI mid-game.

       7. **`gameOver`**

          * Payload:

            ```json
            {
              "winners": ["<codename1>", …],
              "condition": "<string>"  // e.g., "Last Spy Standing", "Network Control"
            }
            ```
          * Purpose: Notify all clients that the game ended, list the winner(s), and specify which victory condition was met. Clients will display a Victory screen, stop timers, and play the fanfare.

  3. **Sequence Flows**

     * **Lobby Join Flow**:

       1. Client opens WebSocket to server.
       2. Client emits `joinLobby` with chosen codename (or empty to allow server to auto-assign).
       3. Server registers the player, sends back `lobbyJoined`.
       4. Server broadcasts `lobbyUpdate` to everyone in the lobby.

     * **Game Start Flow**:

       1. Host clicks “Start Game” → client emits `startGame`.
       2. Server checks there are ≥2 players, initializes round data (`round = 1`, clear submissions).
       3. Server emits `gameStarted` to all clients.

     * **Single Round Flow**:

       1. Server broadcasts “Begin Planning Phase” implicitly by clients seeing `gameStarted` or next-round start.
       2. Each client shows Planning UI with countdown (`roundTimer`).
       3. Each client picks offense/defense/target/IP (and banner message if defense = “Information Warfare”), then emits `submitAction`.
       4. Upon receiving each `submitAction`, server emits `playerSubmitted` to all.
       5. As soon as all active players have submitted (or when timer hits 0), server resolves the turn.
       6. Server emits `turnResult` to all. Clients update HUD, show animations, then display a “Continue” button.
       7. When all clients have clicked “Continue” (or after a short delay), server increments `round` and starts next Planning Phase (clients display Planning UI anew).

     * **Reconnect Flow**:

       1. A client loses WebSocket mid-round (e.g., phone sleeps).
       2. Client reconnects, server’s `connect` event triggers.
       3. Client emits `requestGameState`.
       4. Server responds with `gameStateSnapshot`. Client rebuilds HUD, Planning UI (if Planning Phase), or shows appropriate resolution/wait view.

  4. **Error Handling**

     * If a client sends invalid JSON or unknown fields, server logs a warning and ignores the message.
     * If a player fails to submit before the Planning timer expires, server auto-submits defaults:

       * `offenseId = ""` (no offense),
       * `defenseId = "underground"`,
       * `targetCodename = ""`,
       * `ipToSpend = 0`.
     * If the host disconnects, server emits a special `hostDisconnected` event to all clients; clients display “Host disconnected—please restart.”
     * If a client disconnects before submitting, server treats them as if they auto-submitted defaults; it does not block other players.

  5. **Versioning**

     * Every message payload **may** include an optional `"protocolVersion": 1` field. If server or client sees a mismatch, they display a message prompting users to update and halt further processing.

### 2.3 `art_style_guide.md`

* **Purpose**: Document exactly how all visual elements should look—color palette, fonts, iconography, and animation guidelines—so artists and front-end developers can produce assets that match the intended “ACME cartoon” aesthetic.

* **Structure & Required Content**:

  1. **Overall Aesthetic**

     * Emphasize the **ACME cartoons** vibe: bright primary colors (red, yellow, blue), thick black outlines, exaggerated forms, minimal shading.
     * All artwork should feel playful, over-the-top, and like a living cartoon.

  2. **Color Palette**

     * **Primary Colors**:

       1. **Red** (`#E53935`): For action highlights (e.g., “Confirm” buttons, critical warnings).
       2. **Yellow** (`#FFEB3B`): For caution/hover highlights and gadget icons.
       3. **Blue** (`#1E88E5`): For neutral UI backgrounds and Safe House icons.
     * **Secondary Colors**:

       * **Black** (`#000000`): Thick outlines around every shape.
       * **White** (`#FFFFFF`): Text on colored backgrounds and highlights.
       * **Light Gray** (`#F2F2F2`): Panel backgrounds and dropdown backgrounds.

  3. **Fonts**

     * **Display Font**: `acme_cartoon.ttf` (or a similarly free, cartoonish font).

       * Used for headings, button labels, gadget names.
       * All uppercase, thick letterforms; a slight “wobble” effect in CSS can be optional for hover states.
     * **Monospace Font**: `monospace_console.ttf` (or a system monospace fallback).

       * Used for in-game chat or resolution log text, where clarity is critical at small sizes.
       * Regular weight, high legibility on mobile screens.

  4. **UI Components**

     * **Buttons**:

       * Minimum tap area: 44×44 px.
       * Rounded corners (radius \~8 px).
       * Thick black outline (2 px).
       * Flat fill in primary color (e.g., red for “Confirm,” yellow for “Settings”).
       * Button text: uppercase, white, with a thin black outline for legibility.
     * **Panels** (Planning, Resolution, HUD):

       * Background: solid light gray (`#F2F2F2`) or white (`#FFFFFF`) with a thin black border (1–2 px).
       * Rounded corners (\~8 px).
       * Slight drop shadow (e.g., CSS `box-shadow: 0 2px 4px rgba(0,0,0,0.2)`) for layering effect.
     * **Dropdowns & Inputs**:

       * Use native `<select>` elements styled to match the ACME aesthetic: background white, black border, 8 px padding.
       * Options appear in a scrollable overlay with each option’s background highlighting to yellow on hover or tap.

  5. **Icons & Board Tiles**

     * **Tile Size**: 128×128 px, RGBA (transparent background).
     * **Board Tile Icons**:

       1. **Safe House Icon**: Light pastel blue fortress with cartoon springs underneath (white coils), thick black outline.
       2. **Anvil Crate Icon**: Wooden crate (browns) with a silver anvil popping out, thick black outline.
       3. **Spy Marker**: Black silhouette of a spy wearing a fedora, with large white googly eyes and a small collar, thick black outline.
     * **Gadget Icons** (128×128 px, transparent background):

       1. **Spring-Loaded Anvil**: Silver anvil on a big coiled yellow spring, ready to launch; thick black lines.
       2. **Jetpack Roller Skates**: Bright red roller skates with miniature rocket thrusters and stylized orange flame; black outline.
       3. **Robo-Duck**: Cartoon yellow duck wearing a small metal helmet, black outline, flapping wings.
       4. **Bug Detector**: Handheld radar device with a blinking red light, gray metallic body, black outline.
       5. **Mirror Drone Squadron**: Tiny silver drones with mirrored panels, each \~32×32 px, grouped in a 2×2 formation; black outlines.
       6. (Add 4–6 more gadget icons, each with consistent style: thick black outlines, bright fill colors, minimal shading.)
     * **Status Icons** (32×32 px each):

       1. **Active**: Green circle (`#43A047`) with black outline.
       2. **Compromised**: Yellow/amber circle (`#FBC02D`).
       3. **Burned**: Orange circle (`#F57C00`).
       4. **Captured**: Red circle (`#E53935`).
       5. **Eliminated**: Black circle (`#000000`).

  6. **Animations** (CSS keyframes or frame-by-frame GIF)

     * **Piano Drop**:

       * A multi-frame GIF or CSS keyframes: a cartoon grand piano falling onto a spring platform, producing a “WHOMP” explosion of feathers.
       * Dimensions \~64×64 px when displayed.
       * Duration \~1 sec, \~12 frames at 12 fps.
     * **Anvil Bounce**:

       * Multi-frame GIF: an anvil sitting on a compressed spring, then bouncing upward.
       * Dimensions \~64×64 px.
       * Duration \~0.8 sec, \~10 frames.
     * **Custard Pie Splash**:

       * 8–10 frame GIF of a custard pie hitting a target’s face, spreading pie filling.
       * Dimensions \~64×64 px, \~8 frames.
     * **Explosion**:

       * Quick 10-frame GIF: “BOOM!” with smoke puffs.
       * Dimensions \~64×64 px, \~12 fps.
     * Provide guidelines for artists: “Create assets at 2× scale (128×128 px for icons, 128×128 px for animations) so they downscale nicely to 64×64 px in the UI.”

  7. **HUD Layout**

     * A horizontal bar at the very top of the screen (height \~10% of viewport), dark gray background (`#333333`).
     * For each player (up to 6), display a mini-panel containing:

       1. **Avatar Circle**: a colored pastel circle (unique color per player) with black outline.
       2. **Codename Label**: white text in `acme_cartoon.ttf`, size \~1rem.
       3. **IP Count**: a small “brain” icon (32×32 px) with the current IP number next to it (0.8rem text).
       4. **Status Dot**: small circle (32×32 px) using the status colors defined above.
       5. **Gadget Icons**: up to three small (32×32 px) gadget icons arranged horizontally under the codename.
     * If there are more players than fit on one line, the HUD is horizontally scrollable (`overflow-x: auto; white-space: nowrap;`).
     * Ensure each mini-panel’s width is at least 80 px to accommodate all elements.

  8. **Touch & Mobile Considerations**

     * **Tap Targets**: Minimum 44×44 px for any button or dropdown.
     * **Font Sizes**:

       * Main text: \~1 rem (≈16 px) or larger.
       * Headings and button labels: \~1.2 rem or 1.5 rem.
       * HUD codename/IP: 0.9 rem, bold.
     * **Margins/Padding**: At least 8 px of vertical/horizontal spacing between elements to avoid accidental taps.
     * On narrow screens (portrait), the Planning UI stacks vertically in this order: Offense dropdown → Defense dropdown → Target dropdown → IP slider → Confirm button.
     * Use CSS media queries if needed (e.g., `@media (max-width: 480px) { … }`) to adjust spacing or font sizes.

  9. **Export & File Formats**

     * **PNG (24-bit)** for all icons and UI elements (use transparency where needed).
     * **MP3** for audio (SFX and music loops), compressed to keep file sizes small.
     * **TTF** or **WOFF** for fonts (include both TTF and WOFF in `static/fonts/` for best browser compatibility).
     * **GIF (optional)** for any frame-by-frame animations, but prefer CSS keyframes if possible to reduce file size and CPU overhead.

### 2.4 `network_topology.md`

* **Purpose**: Diagram and explain how all devices connect over LAN to play the game. This ensures players know how to find the host and how reconnects are handled.

* **Structure & Required Content**:

  1. **Assumptions**

     * All players’ devices (phones, tablets, laptops) are on the same Wi-Fi subnet (e.g., `192.168.1.x/24`).
     * The user running the Python server knows their own LAN IP (e.g., `192.168.1.42`).
     * No Internet is required beyond the LAN.

  2. **Manual Join Flow**

     * **On the host machine**: Run `python server.py`. The server listens on `0.0.0.0:5000` and prints something like:

       > “Server listening on 0.0.0.0:5000 (LAN IP: 192.168.1.42).”
     * **On each client device**:

       1. Open a browser.
       2. Navigate to `http://192.168.1.42:5000`.
     * Include a simple ASCII or drawn diagram:

       ```
       +--------------+
       | Host PC      |
       |  (192.168.1.42) 
       |  python server |
       +--------------+
            /   |   \
           /    |    \
       ```

     +----+  +----+  +----+
     |Phone|  |Tablet| |Laptop|
     +----+  +----+  +----+

     ```
     - Show that all client devices open a browser to the same LAN IP and port.

     ```

  3. **WebSocket Topology**

     * The server is the **single central authority**. There is **no** peer-to-peer.
     * Each client opens a WebSocket connection to the server.
     * All real-time messages (`joinLobby`, `submitAction`, etc.) travel over this single WebSocket channel.
     * If a client loses the connection, the server auto-submits defaults on their behalf; if they reconnect within the planning window, they catch up via `gameStateSnapshot`.

  4. **Failure Modes & Recovery**

     * **Client Disconnect**:

       * Happens if phone goes to sleep or Wi-Fi drops.
       * Upon reconnection, client automatically emits `requestGameState`.
       * Server replies with `gameStateSnapshot`, allowing the client to rebuild HUD and UI for the current Phase (Planning or Resolution).
       * If a client fails to reconnect before the Planning timer expires, the server auto-submits: offense = `""`, defense = `"underground"`, `targetCodename = ""`, `ipToSpend = 0`.
     * **Server/Host Disconnect**:

       * When the host machine running `server.py` shuts down or crashes, all clients lose WebSocket connection.
       * Clients detect this and display “Host disconnected—please restart the game.”
       * No automatic host failover is implemented in this version; a new host must restart the game manually.

  5. **(Optional) Future Automatic Discovery Sketch**

     * If you later want to implement automatic host discovery, you could:

       1. Have the host broadcast a UDP “GameAvailable” message on port 9999 every few seconds.
       2. Each client listens on UDP port 9999 for those broadcasts and populates a “Join Game” dropdown with any discovered hosts (showing host IP and current player count).
       3. For now, document that clients must manually enter the host IP in their browser.

---

## 3. Asset Preparation (`assets/`)

Because you have no images, audio, or fonts yet, this section explains **exactly what you need** and **how to produce or source** them. Once all assets are ready, you will copy them into `static/` so Flask can serve them.

```
/assets/
├── audio/
│   ├── sfx/
│   │   ├── anvil_drop.mp3
│   │   ├── piano_launch.mp3
│   │   └── explosion_sizzle.mp3
│   └── music/
│       ├── suspense_loop.mp3
│       └── victory_fanfare.mp3
├── images/
│   ├── UI/
│   │   ├── button_play.png
│   │   ├── button_settings.png
│   │   └── panel_background.png
│   ├── board_tiles/
│   │   ├── safe_house_icon.png
│   │   ├── anvil_crate.png
│   │   └── spy_marker_default.png
│   └── gadgets/
│       ├── spring_anvil.png
│       ├── jetpack_skates.png
│       ├── robo_duck.png
│       └── bug_detector.png
└── fonts/
    ├── acme_cartoon.ttf
    └── monospace_console.ttf
```

### 3.1 Audio SFX (`assets/audio/sfx/`)

* **Create or Source** the following short MP3 clips (all ≤300 KB) under a free license or record your own:

  1. **`anvil_drop.mp3`**

     * Description: A short (≤1 sec) cartoon anvil “thud” sound.
     * Specs: 44.1 kHz sample rate, mono or stereo, ≤200 KB.

  2. **`piano_launch.mp3`**

     * Description: A 1–1.5 sec cartoon “whoosh” plus a descending piano gliss.
     * Specs: 44.1 kHz, ≤300 KB.

  3. **`explosion_sizzle.mp3`**

     * Description: A quick, comedic “boom” with cartoonish reverb.

     * Specs: \~1 sec, 44.1 kHz, ≤250 KB.

  > **Sourcing Tips**: If you cannot record your own, search for public domain or Creative Commons cartoon SFX (e.g., freesound.org).

### 3.2 Music Loops (`assets/audio/music/`)

* **Create or Source** two simple, loopable MP3 tracks:

  1. **`suspense_loop.mp3`**

     * Description: A 30–60 sec, low-tempo, cartoon suspense loop to play during the Planning Phase.
     * Specs: Mono or stereo, ≤1 MB, must loop seamlessly.

  2. **`victory_fanfare.mp3`**

     * Description: A short (10–15 sec) triumphant melody with xylophone or brass.

     * Specs: 44.1 kHz, ≤500 KB.

  > **Sourcing Tips**: Look for public-domain or Creative Commons cartoon-style background loops; confirm they loop cleanly.

### 3.3 Images – UI (`assets/images/UI/`)

* **Design or Source** these UI PNG files (24-bit PNG with transparency if needed):

  1. **`button_play.png`**

     * Dimensions: 256×64 px.
     * Style: Rounded corners (\~8 px radius), thick black outline (\~2 px), red fill (`#E53935`), white uppercase text “PLAY” in a cartoon font, small black outline around the letters.

  2. **`button_settings.png`**

     * Dimensions: 256×64 px.
     * Style: Rounded corners, thick black outline, yellow fill (`#FFEB3B`), a simple black gear icon on the left, white uppercase text “SETTINGS” with black outline.

  3. **`panel_background.png`**

     * Dimensions: 1024×768 px (tileable).
     * Style: Light gray (`#F2F2F2`) grid pattern with faint blueprint lines (thin white or light blue lines), evoking a schematic. Should tile seamlessly.

### 3.4 Images – Board Tiles (`assets/images/board_tiles/`)

* **Create or Source** these 128×128 px PNG icons:

  1. **`safe_house_icon.png`**

     * Pastel blue fortress building perched on cartoon springs (white coils), thick black outline.
     * Simple front-on 2D view.

  2. **`anvil_crate.png`**

     * Wooden crate (brown hues) with a large silver anvil sticking out, thick black outline.
     * Transparent background.

  3. **`spy_marker_default.png`**

     * Black silhouette of a spy in a fedora with big white googly eyes, minimal detail (hat, collar, eyes).
     * Transparent background (but final display size is 64×64 px in the UI).

### 3.5 Images – Gadgets (`assets/images/gadgets/`)

* **Create or Source** these 128×128 px PNG gadget icons:

  1. **`spring_anvil.png`**

     * A silver anvil mounted on a big coiled yellow spring, ready to pop, with thick black outline.

  2. **`jetpack_skates.png`**

     * Bright red roller skates outfitted with tiny rocket thrusters emitting cartoon orange/yellow flames, black outline.

  3. **`robo_duck.png`**

     * A cartoon yellow duck wearing a small metal helmet, big googly eyes, thick black outline.

  4. **`bug_detector.png`**

     * A handheld radar device: gray/black box with a blinking red LED and a small antenna, thick black outline.

  > **Optional**: If you add more gadgets later, create similar 128×128 px PNG icons in this folder.

### 3.6 Fonts (`assets/fonts/`)

* **Obtain** or create the following TrueType or OpenType fonts:

  1. **`acme_cartoon.ttf`**

     * A bold, quirky cartoon display font for headings, button labels, and gadget names.
     * If you can’t find “Acme,” any free “cartoonish” TTF will suffice.

  2. **`monospace_console.ttf`**

     * A classic monospaced font for “console” or “log” text.
     * High legibility on small screens, used for in-game resolution logs or chat.

> **Once all assets are created/sourced** here, you will copy them into the `static/` folder so Flask can serve them. Section 4 below explains exactly how and where they go.

---

## 4. Static Files for the Web App (`static/`)

Flask automatically serves everything in the `static/` directory. After you prepare your assets in `assets/`, copy them into `static/` using the structure below. These are the files your HTML/CSS/JS will reference at runtime.

```
/static/
├── audio/
│   ├── sfx/
│   │   ├── anvil_drop.mp3
│   │   ├── piano_launch.mp3
│   │   └── explosion_sizzle.mp3
│   └── music/
│       ├── suspense_loop.mp3
│       └── victory_fanfare.mp3
├── css/
│   └── style.css
├── fonts/
│   ├── acme_cartoon.ttf
│   └── monospace_console.ttf
├── images/
│   ├── UI/
│   │   ├── button_play.png
│   │   ├── button_settings.png
│   │   └── panel_background.png
│   ├── board_tiles/
│   │   ├── safe_house_icon.png
│   │   ├── anvil_crate.png
│   │   └── spy_marker_default.png
│   └── gadgets/
│       ├── spring_anvil.png
│       ├── jetpack_skates.png
│       ├── robo_duck.png
│       └── bug_detector.png
└── js/
    └── app.js
```

### 4.1 Audio

* **Copy** all MP3 files from `assets/audio/sfx/` into `static/audio/sfx/`.
* **Copy** all MP3 files from `assets/audio/music/` into `static/audio/music/`.

### 4.2 Fonts

* **Copy** `acme_cartoon.ttf` and `monospace_console.ttf` into `static/fonts/`.
* In your CSS (`static/css/style.css`), you will reference these fonts via `@font-face { … src: url('/static/fonts/acme_cartoon.ttf'); }` and similarly for monospace.

### 4.3 Images

* **UI Images**:

  * Copy `button_play.png`, `button_settings.png`, and `panel_background.png` into `static/images/UI/`.
* **Board Tiles**:

  * Copy `safe_house_icon.png`, `anvil_crate.png`, and `spy_marker_default.png` into `static/images/board_tiles/`.
* **Gadgets**:

  * Copy `spring_anvil.png`, `jetpack_skates.png`, `robo_duck.png`, and `bug_detector.png` into `static/images/gadgets/`.

### 4.4 CSS (`static/css/style.css`)

* **Create** `style.css` to define all mobile-first styles (no code shown here, but outline the responsibilities below):

  1. **Layout**

     * Use a mobile-first flex or grid layout.
     * The HUD bar must be a horizontally scrollable flex container (`display: flex; overflow-x: auto; white-space: nowrap;`).
     * Planning & Resolution panels should stack vertically on narrow screens.

  2. **HUD Styling**

     * `.hud-player` class for each mini-panel with `display: inline-block; width: 80px; margin: 0 4px; text-align: center;`.
     * Status dot classes:

       * `.status-active { background: #43A047; }`
       * `.status-compromised { background: #FBC02D; }`
       * `.status-burned { background: #F57C00; }`
       * `.status-captured { background: #E53935; }`
       * `.status-eliminated { background: #000000; }`
     * IP count styling: small “brain” icon followed by a 0.8rem number in white font.

  3. **Planning & Resolution Panels**

     * `.planning-panel`, `.resolution-panel` classes with `background: #F2F2F2; border: 2px solid #000; border-radius: 8px; padding: 8px; margin: 8px;`.
     * Inputs and dropdowns: `width: 100%; font-size: 1rem; padding: 8px; margin-bottom: 8px; border: 2px solid #000; border-radius: 8px;`.
     * Buttons: `.btn { display: block; width: 100%; padding: 12px; font-size: 1.2rem; color: #FFF; text-transform: uppercase; border: 2px solid #000; border-radius: 8px; background-color: #E53935; }`.
     * For a “disabled” button: `.btn:disabled { background-color: #B0BEC5; color: #ECEFF1; }`.

  4. **Font Imports**

     * `@font-face { font-family: 'AcmeCartoon'; src: url('/static/fonts/acme_cartoon.ttf') format('truetype'); }`
     * `@font-face { font-family: 'MonoConsole'; src: url('/static/fonts/monospace_console.ttf') format('truetype'); }`
     * Apply `font-family: 'AcmeCartoon', sans-serif;` to headings and buttons, `font-family: 'MonoConsole', monospace;` to logs and chat.

  5. **Media Queries**

     * Example:

       ```css
       @media (max-width: 480px) {
         .planning-panel select,
         .planning-panel input,
         .planning-panel .btn {
           font-size: 1.1rem;
           padding: 10px;
         }
       }
       ```

  > **Reminder**: Do not show actual CSS code here—just document what selectors and styles you must implement.

### 4.5 JavaScript (`static/js/app.js`)

* **Create** `app.js` to implement all client-side logic in plain JavaScript (no frameworks). Responsibilities:

  1. **WebSocket Connection**

     * On load, open a `new io('<SERVER_URL>')` (Socket.IO) connection.
     * Handle `connect`, `disconnect`, and reconnection logic.

  2. **Lobby Logic**

     * When the user clicks **“Join Lobby”**, read `#input-codename` value, then emit `joinLobby` with `{ codename }`.
     * Listen for `lobbyJoined` and fill in lobby UI: show your codename confirmation, list all players (codename, status, IP).
     * Listen for `lobbyUpdate` to keep the player list in sync whenever someone joins/leaves.
     * Once ≥2 players are in the lobby (and you are in it), enable the **“Start Game”** button on the host’s screen.

  3. **Game Logic**

     * On “Start Game” (host clicks), emit `startGame`.
     * Listen for `gameStarted` to switch the UI from the lobby overlay to the game overlay: hide `#overlay-lobby`, show `#overlay-game`.
     * Populate HUD (`#hud`) with each player’s mini-panel: codename, IP, status dot, and initial gadget icons.
     * Populate Planning UI dropdowns:

       * `#select-offense` with all offense options (11 total for 6 players; hide alliance options if only 2 players).
       * `#select-defense` with all defense options (12 total; hide alliance options if only 2 players).
       * `#select-target` with a dynamic list of other players’ codenames (exclude yourself, exclude Captured/Eliminated).
       * `#input-ip` numeric input (`min="0"`, `max="<your current IP>"`, default `0`).
       * If the player selects “Information Warfare” (the biplane banner defense), show an extra text input `#input-banner` (max length 25 chars) and automatically set `ipToSpend = 2`.

  4. **Planning Phase Timer**

     * Read `roundTimer` (usually 90) from `gameStarted`.
     * Start a countdown (`#timerDisplay`) and display a progress bar or shrinking bar beneath the Planning UI.
     * When timer > 0, clients may change offense/defense/target/IP.
     * Once the player clicks **“Confirm Choices”**, gather those four values plus banner text (if applicable), disable all inputs, update `#planning-status` to “Action Submitted,” and emit `submitAction`.
     * Listen for `playerSubmitted` to show a checkmark next to that codename in the HUD.

  5. **Biplane Banner Logic**

     * If you selected “Information Warfare” (biplane banner), your `submitAction` payload also includes `{ "bannerMessage": "<your 25-char text>" }`.
     * When the server resolves the turn, if any player paid for a banner, the server will broadcast a special “ShowBanner” event (you can define a custom event) containing `{ broadcaster: "<codename>", bannerText: "<string>" }`.
     * On receiving “ShowBanner,” play a short CSS animation or canvas draw of a plane flying across the top of the viewport, dragging `bannerText`. Play a “propeller” audio loop via HTML5 Audio (from `static/audio/sfx/`).
     * Then, for each player whose locked offense targeted the banner-caster, show a modal with two buttons: “Believe Banner” or “Ignore Banner,” and a 10 sec countdown.

       * If they click “Believe Banner” within 10 sec: their offense’s target is rerouted per the banner text (the server marks it as “trusted reroute”).
       * If they click “Ignore Banner” (or time out): their offense target remains the original banner-caster, but if the banner was genuine, they incur a –1 penalty on any die roll (server-side).
       * After all affected players respond (or 10 sec elapses), emit a custom event “BannerDecision” back to the server with `{ codename: "<self>", decision: "believe" | "ignore" }`.
       * The server collects all BannerDecision events, then proceeds with offense/defense resolution.

  6. **Turn Resolution**

     * Listen for `turnResult`. When received:

       1. Hide Planning UI, show `#resolution` panel.
       2. Clear `#resolution-content`.
       3. For each entry in `results` (one per player), append a line of text to `#resolution-content` in this format:

          > “\[Codename] → IP Δ: +X (now Y), Status: <newStatus>. Intel: <comma-separated intel items>.”
       4. For each result that includes specific SFX triggers (e.g., “piano hit,” “anvil bounce,” “explosion”), play the corresponding MP3 from `static/audio/sfx/`. For example, if a successful Assassination landed, play `piano_launch.mp3`.
       5. After a short delay (e.g., 1 second), show `#btn-continue` (“Continue to Next Round”).

  7. **Continue to Next Round**

     * When the user taps `#btn-continue`, hide `#resolution` and `#btn-continue`, reset Planning UI fields (offense dropdown sets to default empty, defense empty, target empty, IP = 0, banner input hidden), clear any status messages.
     * Emit a client-side “ready” event or simply wait for the server’s next Planning Phase start (which is automatic, since server already incremented `round` and cleared submissions). Clients will start the next 90 sec timer on receiving the next “planning started” implicit message (you may broadcast a custom event if needed, e.g., `planningPhaseStart`).

  8. **Reconnect Handling**

     * If `socket.on('disconnect')` fires unexpectedly (Wi-Fi drop), show a small overlay: “Reconnecting…” and attempt `socket.connect()` automatically.
     * On `socket.on('connect')`, emit `requestGameState`.
     * Upon receiving `gameStateSnapshot`, rebuild HUD (codename, IP, status, gadget icons), restore any unanswered Planning or Resolution UI depending on the current round. If in Planning Phase and the timer is still running, restart the countdown with the remaining time (server includes `remainingTime` in the snapshot).
     * If the client does not reconnect before timer 0, server will have auto-submitted defaults for them.

  9. **Victory Handling**

     * Listen for `gameOver`. When received:

       1. Hide Planning UI and Resolution UI.
       2. Display a full-screen modal: “Winner(s): \[comma-separated codenames] by \[condition].”
       3. Play `victory_fanfare.mp3`.
       4. Optionally offer a “Return to Lobby” or “Restart” button (which simply reloads the page).

  10. **Asset Preloading (Optional but Recommended)**

      * On initial page load (or when in Lobby), create JavaScript `Audio` objects for each SFX and music:

        ```js
        const sfxAnvil = new Audio('/static/audio/sfx/anvil_drop.mp3');
        const sfxPiano = new Audio('/static/audio/sfx/piano_launch.mp3');
        const sfxExplosion = new Audio('/static/audio/sfx/explosion_sizzle.mp3');
        const bgMusic = new Audio('/static/audio/music/suspense_loop.mp3');
        bgMusic.loop = true;
        ```
      * Call `sfxAnvil.load()`, etc., so browsers cache them.

  11. **Mobile-First Considerations**

      * Use only `click` event listeners (avoid hover or right-click).
      * Ensure every interactive element (buttons, dropdowns) is ≥44×44 px.
      * Use `window.setTimeout` or `requestAnimationFrame` judiciously to keep UI responsive on slower devices.
      * On iOS/Android, ensure audio playback is triggered by a user interaction (e.g., playing `bgMusic` only when “Start Game” is tapped).

> **Reminder**: Do not show actual JavaScript code here—only document in plain language what `app.js` must accomplish.

---

## 5. HTML Template (`templates/index.html`)

Flask will render this single HTML page. You still need to create it, but in this checklist we describe exactly **what elements** it must include and **where**, without showing actual code.

```
/templates/
└── index.html
```

### 5.1 `index.html`

* **Purpose**: Serve as a single-page HTML that contains both the Lobby UI and the Game UI (hidden by default). It also loads your CSS and JS.

* **Required Structure (in prose)**:

  1. **`<head>` Section**

     * Include `<meta name="viewport" content="width=device-width, initial-scale=1.0">` for mobile responsiveness.
     * Link to `/static/css/style.css`.
     * Include the Socket.IO client library from a CDN (e.g., `<script src="https://cdn.socket.io/4.5.1/socket.io.min.js"></script>`).
     * Include `<script defer src="/static/js/app.js"></script>`.
     * Set a `<title>James Bland: ACME Edition</title>`.

  2. **`<body>` Section**

     * **Lobby Overlay** (`<div id="overlay-lobby">`)

       1. Heading: `<h1>James Bland: ACME Edition</h1>`.
       2. Codename Input: `<input type="text" id="input-codename" placeholder="Your Codename" maxlength="16">`.
       3. Join Button: `<button id="btn-join">Join Lobby</button>`.
       4. Lobby Status: `<div id="lobby-status"></div>` (for messages like “Joined as AgentX”).
       5. Player List: `<div id="player-list-lobby"></div>` (scrollable, listing codename, status, IP for each joined player).
       6. Start Game Button: `<button id="btn-start" disabled>Start Game</button>` (enabled once ≥2 players are in lobby).
       7. (Optional) A small instructions link or “?” icon that shows a help overlay.
     * **Game Overlay** (`<div id="overlay-game" class="hidden">`)

       1. **HUD** (`<div id="hud"></div>`)

          * Will contain up to 6 mini-panels with class `.hud-player`. Each mini-panel includes:

            * Avatar circle (colored `<div class="avatar-circle">`),
            * `<div class="codename-label">AgentX</div>`,
            * a small brain icon + `<span class="ip-count">5</span>`,
            * `<div class="status-dot status-active"></div>`,
            * `<div class="gadget-icons"></div>` with up to three `<img>` tags for gadget icons.
       2. **Board Placeholder** (`<div id="board">Board (Placeholder)</div>`)

          * A flex container or simple `<div>` labeled “Board (Mockup)” where tile graphics will be displayed later.
       3. **Planning Panel** (`<div id="planning" class="planning-panel">`)

          * Round Number: “Round : <span id="roundNumber">0</span>.”
          * Offense Dropdown: `<select id="select-offense"><option value="">Select Offense</option>…</select>`.
          * Defense Dropdown: `<select id="select-defense"><option value="">Select Defense</option>…</select>`.
          * Target Dropdown: `<select id="select-target"><option value="">Select Target</option>…</select>`.
          * IP Numeric Input: `<input type="number" id="input-ip" min="0" value="0">`.
          * (Initially hidden) Banner Text Input: `<input type="text" id="input-banner" maxlength="25" placeholder="Banner Message" class="hidden">`.
          * Confirm Button: `<button id="btn-confirm" disabled>Confirm Choices</button>`.
          * Timer Display: `<div id="planning-timer">Time: <span id="timerDisplay">90</span>s</div>`.
          * Planning Status: `<div id="planning-status"></div>` (for messages like “Action Submitted” or “Hurry up!”).
       4. **Resolution Panel** (`<div id="resolution" class="resolution-panel hidden">`)

          * Heading: `<h2>Resolution</h2>`.
          * Scrollable Content: `<div id="resolution-content"></div>` (each line appended as text).
          * Continue Button: `<button id="btn-continue" class="hidden">Continue to Next Round</button>`.

* **No External Libraries** (other than Socket.IO). All structure is vanilla HTML with IDs and classes that match what your CSS/JS expects.

---

## 6. Backend Code & Structure (No Code Shown)

You will implement a **single Python script** named `server.py` at the project root. Instead of showing code, here is an **outline of what it must do**—step by step in plain English.

```
/server.py
```

### 6.1 High-Level Responsibilities

1. **Initialize Flask + Flask-SocketIO**

   * Create a Flask application instance.
   * Initialize Socket.IO on top of Flask with `async_mode='eventlet'` (or similar), and allow CORS from local LAN (e.g., use `cors_allowed_origins="*"` because all clients are local).

2. **Maintain In-Memory Game State**

   * A dictionary `users` mapping each connected client’s Socket.IO session ID (`sid`) → a player object containing:

     * `codename` (string)
     * `status` (string; initial = `"active"`)
     * `ip` (integer; initial = 5)
     * `gadgets` (list of strings; initial = two basic gadget IDs, e.g., `["springAnvil", "jetpackSkates"]`)
     * `intel` (list of strings; initially empty)
   * A dictionary `connections` mapping the lobby room name (e.g., `"main"`) → a set of `sid` for players currently in the lobby/game.
   * A dictionary `current_turn` keyed by room name (always `"main"` for this version) storing:

     * `round` (integer; initial = 1)
     * `submissions`: a map from codename → submission object, where each submission includes:
       • `offenseId` (string)
       • `defenseId` (string)
       • `targetCodename` (string or empty)
       • `ipToSpend` (integer)
       • `bannerMessage` (string or empty)
   * A dictionary `assets` capturing Strategic Asset control: mapping each asset name → the codename of the current controller or `null` if unowned.

3. **Define the Interaction Matrix**

   * In Python (or load from a JSON file), create a nested dictionary mapping each offense ID (string) → each defense ID (string) → an outcome object containing:

     * `offenseSucceeds` (bool)
     * `ipChangeOffender` (int)
     * `ipChangeDefender` (int)
     * `newStatusOffender` (string)
     * `newStatusDefender` (string)
     * `intelOffender` (list of strings)
     * `intelDefender` (list of strings)

   * Include a `"default"` subkey under each offense to handle defenses that aren’t explicitly listed.

   * Example excerpt (do not embed code, just store this as a Python dict or JSON file):

     ```
     interaction_matrix = {
       "assassination": {
         "safeHouse": { … },
         "bodyguardDetail": { … },
         "mobileOperations": { … },
         "default": { … }
       },
       "surveillance": {
         "counterSurveillance": { … },
         "sweepAndClear": { … },
         "default": { … }
       },
       … (all offenses) …
     }
     ```

4. **WebSocket Event Handlers**

   * **`connect`**: When a new WebSocket connection arrives, do nothing yet; wait for `joinLobby`.

   * **`disconnect`**: When a client disconnects:

     1. If they are in the lobby: remove them from `connections["main"]`, remove their `users[sid]`, and broadcast an updated player list via `lobbyUpdate`.
     2. If the game already started: mark them as “disconnected.” If they have not submitted in this turn, auto-submit defaults (`offenseId=""`, `defenseId="underground"`, `targetCodename=""`, `ipToSpend=0`, `bannerMessage=""`) on their behalf. Broadcast `playerSubmitted` for that codename so other players know.

   * **`joinLobby`** (client → server)

     * Payload: `{ "codename": "<string>" }`.
     * Server must:

       1. Check if `codename` is unique among current lobbies. If empty or taken, generate a unique codename (e.g., “Agent123”).
       2. Create a new entry in `users[sid]` with:

          * `codename`,
          * `status = "active"`,
          * `ip = 5`,
          * `gadgets = ["springAnvil", "jetpackSkates"]`,
          * `intel = []`.
       3. Add `sid` to `connections["main"]`.
       4. Emit to that `sid` a `lobbyJoined` event with:

          * `yourCodename` (string),
          * `allPlayers`: an array of `{ codename, status, ip }` for everyone currently in the lobby,
          * `roundTimer` (integer, 90),
          * `maxPlayers` (integer, 6).
       5. Broadcast `lobbyUpdate` to all other sids in `connections["main"]`, with the updated `allPlayers` list.

   * **`startGame`** (client → server, host only)

     * No payload.
     * Server must check:

       1. That the caller’s `sid` is the same as the first player who joined the lobby (designated host).
       2. That the lobby has ≥2 players.
     * If valid:

       1. Initialize `current_turn["main"] = { "round": 1, "submissions": {} }`.
       2. Initialize `assets` so that all five Strategic Assets are unowned (`null`).
       3. Emit `gameStarted` to all sids in `connections["main"]`, with:

          * `gameConfig = { "initialIP": 5, "roundTimer": 90, "maxPlayers": 6 }`,
          * `currentPlayers`: an array of each player’s full state (`{ codename, status, ip, gadgets, intel }`).

   * **`submitAction`** (client → server)

     * Payload:

       ```json
       {
         "offenseId": "<string or empty>",
         "defenseId": "<string>",
         "targetCodename": "<string or empty>",
         "ipToSpend": <integer>,
         "bannerMessage": "<string or empty>"
       }
       ```
     * Server must:

       1. Verify that the player’s status is not “captured” or “eliminated.” If it is, ignore (they cannot submit).
       2. Clamp `ipToSpend` to the player’s current IP (cannot spend more than they have).
       3. Deduct `ipToSpend` immediately from their `users[sid]["ip"]`.
       4. Store in `current_turn["main"]["submissions"][codename] = { offenseId, defenseId, targetCodename, ipToSpend, bannerMessage }`.
       5. Emit `playerSubmitted` to all sids in `connections["main"]` with `{ codename }`.
       6. Check if all **active** players (status not in \["captured", "eliminated"]) appear in `submissions`.

          * If yes, immediately call the **Turn Resolution** routine.
          * If not, do nothing; wait for remaining players or for the Planning timer to expire.

   * **`requestGameState`** (client → server)

     * No payload.
     * Server must:

       1. Look up `sid` in `users`. If they exist, compile a snapshot:

          ```json
          {
            "round": current_turn["main"]["round"],
            "players": [
              {
                "codename": "<string>",
                "status": "<string>",
                "ip": <integer>,
                "gadgets": ["<string>", …],
                "intel": ["<string>", …]
              },
              …
            ]
          }
          ```
       2. Emit `gameStateSnapshot` back to that `sid`.

5. **Turn Resolution Logic (Internal)**

   * This runs once per round, either when all active players have submitted or when the timer hits 0 (server enforces default submissions). Steps:

     1. **Timer Expiry Handling**

        * If the Planning timer hit 0 and some active players have not submitted, auto-submit defaults for each missing player:

          * `offenseId = ""` (Safe Turn),
          * `defenseId = "underground"`,
          * `targetCodename = ""`,
          * `ipToSpend = 0`,
          * `bannerMessage = ""`.
        * Add each of these to `current_turn["main"]["submissions"]`.

     2. **Banner Phase**

        * Check if **any** submission has `defenseId = "informationWarfare"`. For each such broadcaster:

          * Emit a custom event (e.g., `"showBanner"`) containing `{ broadcasterCodename, bannerMessage }` to all clients.
          * Wait to collect a `"bannerDecision"` event from each player who targeted the broadcaster that round.
          * Each affected player’s decision is `{ codename, decision: "believe"|"ignore" }`.
          * After collecting all decisions (or 10 sec timeout), adjust each affected player’s `targetCodename` in their submission:

            * If “believe” and banner was genuine (i.e., the broadcaster intended a reroute), set `targetCodename` to the location indicated by the banner (the server may parse that banner string into a valid target or threat zone).
            * If “ignore” and banner was genuine, mark that player’s submission with a “–1 penalty” flag.
            * If “believe” but banner was a bluff (broadcaster had no real intent for the fake location), mark their offense as “wasted” (no effect on anyone, and broadcaster gains +1 IP).
            * If “ignore” but banner was a bluff, do nothing to their submission.

     3. **Apply Offense-Defense Pairings**

        * For each submission s where `offenseId != ""`:

          1. Identify `offender = users[sidOfOffender]` and `target = users[sidOfTargetCodename]`.
          2. Let `defenseId = submissionOfTarget["defenseId"]`. If the target was not an active player or had no submission (e.g., double elimination), treat as `defenseId = "default"`.
          3. Look up `(offenseId, defenseId)` in `interaction_matrix`. If that defense is missing, use `interaction_matrix[offenseId]["default"]`.
          4. Let `outcome = interaction_matrix[offenseId][defenseId]` (the outcome object).
          5. If the offender’s submission had a “–1 penalty” flag from banner logic, reduce `outcome.offenseSucceeds` probability by 10% or simply override to failure if your design says so.
          6. Apply the outcome:

             * `offender["ip"] += outcome.ipChangeOffender`
             * `target["ip"]  += outcome.ipChangeDefender`
             * `offender["status"] = outcome.newStatusOffender`
             * `target["status"]   = outcome.newStatusDefender`
             * Append each string in `outcome.intelOffender` to `offender["intel"]`.
             * Append each string in `outcome.intelDefender` to `target["intel"]`.
        * For each submission where `offenseId == ""` (Safe Turn):

          * Award that player `+1 IP` (their `ip` increases by 1).
        * **Note**: If multiple players attacked the same target, process them in a deterministic order (e.g., descending by current IP, then lexicographically by codename). Update IP/status in that order so subsequent pairings see the updated IPs (document this rule in `game_design.md`).

     4. **Process Strategic Asset Captures**

        * If any offense was “Network Attack” or “Alliance Operation” successfully targeting a Strategic Asset’s current controller, update `assets[assetName] = offenderCodename` and award appropriate IP yields.

     5. **Compile `turnResult` Payload**

        * Construct:

          ```json
          {
            "round": <current_round>,
            "results": [
              {
                "codename": "<string>",
                "ipDelta": <integer>,        // net IP change this turn
                "newIP": <integer>,          // updated IP
                "newStatus": "<string>",     // updated status
                "intelGained": ["<string>", …]
              }, …
            ]
          }
          ```
        * Emit `turnResult` to all sids in `connections["main"]`.

     6. **Post-Resolution Updates**

        * Increment `current_turn["main"]["round"]` by 1.
        * Clear `current_turn["main"]["submissions"] = {}`.
        * Deduct gadget upkeep IP (if any gadgets require recharging, those players automatically spend 1 IP; if they lack enough IP, that gadget deactivates and is removed from their `gadgets` list).
        * Award any passive IP from Strategic Assets: for each asset controlled by a codename, add that asset’s IP yield to that player’s `ip`.
        * Process any alliance expiry: decrement each active Non-Aggression Pact’s remaining rounds by 1; if it reaches 0, break the pact.
        * Any captured players who have skipped one turn now become Burned (their status changes from “captured” to “burned”).

     7. **Check Victory Conditions**

        * **Last Spy Standing**: Count players whose status is not in \[`"captured"`, `"eliminated"`]. If exactly 1 remains, they are declared winner.
        * **Intelligence Supremacy**: For any player, if they have collected at least 3 Intel Cards about every other Active agent (Identity, Safe House, Preferred Gadget), declare them winner.
        * **Network Control**: If any player controls ≥3 Strategic Assets at the start of the turn, declare them winner.
        * **Mission Completion**: If any player’s Master Plan conditions are satisfied now, declare them winner.
        * **Alliance Victory**: If two allied players share an active “Alliance Victory” objective and have both met its requirements, declare them joint winners and immediately trigger a Final Showdown:

          1. Both allied players `ip += 3`.
          2. Both choose one of {Assassination, Sabotage} with no defense.
          3. Server resolves both attacks; compare success roll (or net IP if both succeed) to rank 1st vs. 2nd.
        * If any condition is met, emit `gameOver` with `{ "winners": [ ... ], "condition": "<string>" }` and halt further rounds.

6. **Run the Server**

   * In the `if __name__ == '__main__':` block, start the Flask-SocketIO server on `host='0.0.0.0', port=5000`, with `debug=False`. This ensures that any device on the LAN can connect to `http://<host_ip>:5000`.

> **Reminder**: Do not include actual Python code here—just describe in plain language what `server.py` must implement.

---

## 7. Testing Folder (`tests/`)

Use **pytest** to verify your core resolution logic. Create a `tests/` folder with the following four test files. In each, write plain-language descriptions (no code) of what must be covered.

```
/tests/
├── test_interaction_matrix.py
├── test_action_resolver.py
├── test_game_loop.py
└── test_utils.py   (optional)
```

### 7.1 `test_interaction_matrix.py`

* **Purpose**: Verify that every `(offenseId, defenseId)` pairing in your Interaction Matrix yields the correct outcome object.

* **What to Test (in plain language)**:

  1. **Known Pairings**

     * For each offense (e.g., `"assassination"`) and each defense that you explicitly listed (e.g., `"safeHouse"`, `"bodyguardDetail"`, `"mobileOperations"`), confirm that looking up `interaction_matrix[offenseId][defenseId]` returns an outcome matching your documented effects:

       * Correct `offenseSucceeds` boolean.
       * Correct `ipChangeOffender` and `ipChangeDefender`.
       * Correct `newStatusOffender` and `newStatusDefender`.
       * Correct intel lists (`intelOffender`, `intelDefender`).

  2. **Default Fallback**

     * Pick an offense (e.g., `"assassination"`) and a made-up defense string (e.g., `"nonexistentDefense"`). Confirm that the matrix lookup returns `interaction_matrix[offenseId]["default"]`.

  3. **Missing Offense**

     * If the offense key is not in `interaction_matrix` at all (e.g., `"invalidOffense"`), confirm that your helper returns a generic “failure” outcome: attacker loses IP, becomes Exposed, defender gains IP, no intel gained.

* **How to Structure Tests (pseudocode)**:

  1. Manually create a dummy `offsender` and `defender` object in memory (codename, status, IP, gadgets, intel lists empty).
  2. Call a function like `lookup_outcome(offenseId, defenseId, offender, defender)`.
  3. Assert that the returned outcome matches expectations for that pairing.

### 7.2 `test_action_resolver.py`

* **Purpose**: Verify that a full turn resolution handles multiple submissions simultaneously and updates IP/status correctly.

* **What to Test**:

  1. **Single-Player Safe Turn**

     * If only one player is in the game and they submit `offenseId=""`, `defenseId="underground"`, confirm they gain +1 IP (resulting IP = initial +1).

  2. **Two-Player Assassination vs. Safe House**

     * Player A submits `offenseId="assassination", target="PlayerB", ipToSpend=0` and Player B submits `offenseId=""`, `defenseId="safeHouse", ipToSpend=0`.
     * Confirm the outcome: A loses 1 IP and becomes Exposed; B gains 1 IP and remains Active.

  3. **Three Players Attacking One Target**

     * Players A and B both submit offenses targeting Player C; Player C submits defense `safeHouse`.
     * Determine the resolution order (highest IP first). Confirm that each attacker’s outcome is applied in sequence, updating IP/status in a deterministic order.
     * Check final IP and status for A, B, and C.

  4. **Failed Infiltration vs. Sweep & Clear**

     * Player A submits `offenseId="infiltration", target="PlayerB"`, Player B submits `defenseId="sweepAndClear", ipToSpend=0`.
     * Confirm attacker loses 1 IP and becomes Exposed; defender gains +2 IP and draws an Intel Card (i.e., `intelDefender = ["attackerId"]`).

* **How to Structure**:

  * Initialize a minimal in-memory state for 2–3 dummy players.
  * Call your function that resolves a list of submissions (pass in a dict mapping codename → submission).
  * Assert that after resolution, each player’s IP and status match expected values.

### 7.3 `test_game_loop.py`

* **Purpose**: Validate end-to-end game loop behavior for basic scenarios across multiple rounds.

* **What to Test**:

  1. **IP Economy Over Multiple Rounds**

     * Simulate a 2-player game where both choose Safe Turn (`offenseId=""`, `defenseId="underground"`) for 3 consecutive rounds.
     * Confirm that each player’s IP increases by exactly 1 each round (cumulative +3).

  2. **Compromise Chain**

     * Player A attempts an assassination and fails (due to, say, Player B’s `bodyguardDetail`), so Player A becomes Compromised.
     * In the next round, confirm Player A’s status is “compromised,” so they cannot choose `defenseId="falseIdentity"`. If they attempt to, your code should reject it or clamp to a valid choice.

  3. **Victory Condition – Last Spy Standing**

     * Simulate 3 players:

       1. Round 1: Player A successfully captures Player B (B becomes Captured).
       2. Round 2: Player A successfully captures Player C.
     * Confirm that after Round 2 resolution, server declares Player A winner by “Last Spy Standing” and emits `gameOver` accordingly.

  4. **Victory Condition – Network Control**

     * Simulate Player A capturing Strategic Assets one by one (e.g., “ACME Bank,” “ACME Armory,” “ACME Black Market” in consecutive rounds).
     * Confirm that at the moment Player A controls the third asset, server immediately emits `gameOver` with `condition = "Network Control"` and `winners = ["PlayerA"]`.

* **How to Structure**:

  * In each test, initialize an in-memory state with the needed number of dummy players.
  * Manually simulate calling the turn resolution function (or your helper that advances the game by one round) with specified submissions.
  * After each simulation step, assert that the state (IP, status, asset control, etc.) is as expected.
  * When verifying victory, confirm that your code would have emitted `gameOver` with the correct payload.

### 7.4 `test_utils.py` (Optional)

* **Purpose**: If you create any utility functions (e.g., random probability helpers, time formatting, IP clamping), write tests to verify them.

* **What to Test**:

  1. **Random Weighted Choice**

     * If you have a helper that returns a random choice from a weighted set (e.g., `{A:0.1, B:0.9}`), run it 10 000 times and confirm B is selected roughly 90% of the time (±5%).

  2. **IP Clamping**

     * If you have a helper to clamp IP between –10 and a max (e.g., 20), test edge inputs:

       * Input = 25 → clamped to 20.
       * Input = –15 → clamped to –10.
       * Input = 5 → remains 5.

> **Running Tests**:
> After setting up everything, run `pytest tests/` from the project root. All tests should pass before you release.

---

## 8. Scripts Folder (`scripts/`)

This folder holds helper scripts to process assets and generate any data-driven files (e.g., Intel card deck). You will write plain-language descriptions of each script’s purpose and behavior—no code.

```
/scripts/
├── build_assets.sh
└── generate_intel_deck.py
```

### 8.1 `build_assets.sh`

* **Purpose**: Optimize and copy all raw assets from `assets/` into `static/` so the web server can serve them.

* **Tasks (in order)**:

  1. **Optimize PNGs (optional)**

     * If tools like `optipng` or `pngquant` are installed, run them on every PNG under `assets/images/` to reduce file size without losing visual fidelity.
     * If those tools are unavailable, skip this step gracefully.

  2. **Copy Audio**

     * Ensure `static/audio/sfx/` and `static/audio/music/` directories exist; create them if they don’t.
     * Copy every file from `assets/audio/sfx/*.mp3` to `static/audio/sfx/`.
     * Copy every file from `assets/audio/music/*.mp3` to `static/audio/music/`.

  3. **Copy Fonts**

     * Ensure `static/fonts/` exists; create it if needed.
     * Copy every file from `assets/fonts/*.ttf` (and any `.woff` if present) to `static/fonts/`.

  4. **Copy Images**

     * Ensure `static/images/UI/`, `static/images/board_tiles/`, and `static/images/gadgets/` directories exist; create them if needed.
     * Copy each file from `assets/images/UI/*.png` → `static/images/UI/`.
     * Copy each file from `assets/images/board_tiles/*.png` → `static/images/board_tiles/`.
     * Copy each file from `assets/images/gadgets/*.png` → `static/images/gadgets/`.

  5. **Confirm Completion**

     * Print a message: “Assets successfully built and copied to static/.”

* **How to Execute**:

  1. From the project root, run:

     ```bash
     cd scripts
     ./build_assets.sh
     ```
  2. Ensure you gave execute permissions: `chmod +x build_assets.sh`.

### 8.2 `generate_intel_deck.py`

* **Purpose**: Create a shuffled deck of Intel cards and write the result to a JSON file in `static/data/`. Optionally generate a printable PDF for offline use.

* **Tasks**:

  1. **Load Intel Card Definitions**

     * Attempt to read `assets/data/intel_definitions.json`. If it does not exist, create a minimal default list in memory consisting of objects like:

       ```json
       {
         "id": "revealNextDefense",
         "type": "reveal",
         "uses": 1,
         "description": "Reveal your chosen defense before planning phase ends.",
         "copies": 10
       }
       ```
     * Each definition must include:

       * `id` (string)
       * `type` (e.g., `"reveal"`, `"force"`)
       * `uses` (integer: how many times this card can be used)
       * `description` (string)
       * `copies` (integer: how many identical cards to include)

  2. **Build Deck**

     * For each definition, replicate it `copies` times (default to 10 if `copies` not specified).
     * Shuffle the combined list randomly (use a true random shuffle).

  3. **Write JSON**

     * Create `static/data/` directory if it doesn’t exist.
     * Write the shuffled array to `static/data/intel_deck.json`. Each element in the array should be an object:

       ```json
       {
         "id": "<string>",
         "type": "<string>",
         "usesLeft": <integer>,
         "description": "<string>"
       }
       ```

  4. **(Optional) Generate PDF**

     * If you want a printable deck for tabletop play, use a Python PDF library (like ReportLab) to generate a PDF with one card per page. Each page should show:

       * Large `id` at top (font \~24 pt using `AcmeCartoon`).
       * Below, the `description` text in a readable font (\~14 pt).
       * A small icon if available (for example, an Intel card placeholder).
     * Save this as `static/data/intel_deck.pdf`.
     * If you cannot generate a PDF now, skip this step.

* **How to Execute**:

  1. From the project root, run:

     ```bash
     cd scripts
     python3 generate_intel_deck.py
     ```
  2. Confirm that `static/data/intel_deck.json` exists (and `intel_deck.pdf` if you opted for it).

---

## 10. Testing (pytest) Without Showing Code

In each Python test file, outline what the tests must cover:

### 10.1 `tests/test_interaction_matrix.py`

* **Goal**: Ensure every offense/defense pairing yields the correct outcome.

* **Test Cases**:

  1. **Assassination vs. Safe House**: Assert offense fails, attacker loses 1 IP, defender gains 1 IP, attacker becomes Exposed, defender stays Active, no intel for attacker, defender sees attacker’s ID.
  2. **Assassination vs. Mobile Operations**: Assert offense succeeds, attacker gains 2 IP, defender loses 2 IP, defender becomes Compromised, no intel for defender, attacker sees “target compromised.”
  3. **Surveillance vs. Counter-Surveillance**: Assert offense fails, attacker loses 1 IP, defender gains 2 IP, defender sees attacker’s identity.
  4. **Any Offense vs. Unlisted Defense** (fallback/default): Confirm that the “default” outcome is returned (e.g., generic failure or success as documented).

### 10.2 `tests/test_action_resolver.py`

* **Goal**: Confirm full turn resolution processes multiple simultaneous submissions correctly.

* **Test Cases**:

  1. **Single Player Safe Turn**: One player with no offense gains +1 IP.
  2. **Head-to-Head Assassination vs. Safe House**: Player A attacks Player B (who chose Safe House); confirm Player A loses 1 IP and becomes Exposed; Player B gains 1 IP and remains Active.
  3. **Three Attackers on One Target**: Players A, B, and C all choose offenses targeting D (who chooses Safe House). Suppose their IPs are A=6, B=5, C=4. Confirm resolution order and final IP/status for each.
  4. **Failed Infiltration vs. Sweep & Clear**: Player A’s Infiltration against B’s Sweep & Clear fails, A loses 1 IP and becomes Exposed, B gains 1 IP and draws intel.

### 10.3 `tests/test_game_loop.py`

* **Goal**: Validate multi-round loop logic (IP economy, status transitions, victory).

* **Test Cases**:

  1. **IP Accrual Over Safe Turns**: Two players both choose no offense vs. “underground” defense for 3 rounds; confirm each receives +1 IP per round.
  2. **Compromise Chain**: Player A fails an assassination, becomes Compromised; next round, confirm they cannot select `defenseId="falseIdentity"`.
  3. **Victory – Last Spy Standing**: Simulate 3 players until only one is not Captured/Eliminated; confirm the server emits `gameOver` with that winner and “Last Spy Standing.”
  4. **Victory – Network Control**: Simulate Player A capturing three Strategic Assets; confirm immediate `gameOver` with `["PlayerA"]` and `"Network Control"`.

### 10.4 `tests/test_utils.py` (Optional)

* **Purpose**: If you wrote any helper functions, test them here (e.g., random weighting, IP clamping, timer formatting).

* **Test Cases**:

  1. **Random Weighted Choice**: Over many iterations, confirm selection distribution roughly matches weights.
  2. **IP Clamping**: For input = 25 and max=20, output is 20; for input = –15 and min=–10, output is –10; for input = 5, output is 5.

> **Running Tests**:
> After writing tests, run from the project root:
>
> ```
> pytest tests/
> ```

---

## 11. Scripts (`scripts/`)

This folder holds helper scripts to automate building assets and generating data files. Write plain-language descriptions of each script’s purpose and behavior—no code.

```
/scripts/
├── build_assets.sh
└── generate_intel_deck.py
```

### 11.1 `build_assets.sh`

* **Purpose**: Optimize and copy raw assets from `assets/` into `static/` so Flask can serve them.

* **Steps**:

  1. **Optimize PNGs** (optional):

     * If `optipng` or `pngquant` is installed, run it on each PNG under `assets/images/` to reduce file size. Otherwise, skip.
  2. **Copy Audio**:

     * Create `static/audio/sfx/` and `static/audio/music/` if they don’t exist.
     * Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`.
     * Copy `assets/audio/music/*.mp3` → `static/audio/music/`.
  3. **Copy Fonts**:

     * Create `static/fonts/` if it doesn’t exist.
     * Copy `assets/fonts/*.ttf` → `static/fonts/`.
  4. **Copy Images**:

     * Create `static/images/UI/`, `static/images/board_tiles/`, `static/images/gadgets/` if needed.
     * Copy `assets/images/UI/*.png` → `static/images/UI/`.
     * Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`.
     * Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`.
  5. **Completion Message**:

     * Print “Assets copied to static/ successfully.”

* **How to Run**:

  1. From the project root, run:

     ```
     cd scripts
     ./build_assets.sh
     ```
  2. Ensure execute permissions: `chmod +x build_assets.sh`.

### 11.2 `generate_intel_deck.py`

* **Purpose**: Build and shuffle an Intel card deck, then save it as JSON (and optionally as PDF).

* **Steps**:

  1. **Load Intel Definitions**:

     * Attempt to read `assets/data/intel_definitions.json`. If it doesn’t exist, define a minimal default set in memory (e.g., “revealNextDefense,” “revealIPCount,” “forceReplay”). Each definition has:

       * `id`, `type`, `uses`, `description`, and optional `copies` (default 10).
  2. **Build & Shuffle Deck**:

     * For each definition, replicate it `copies` times (or 10 if unspecified).
     * Shuffle the combined list randomly.
  3. **Save JSON**:

     * Ensure `static/data/` exists.
     * Write the shuffled array as `static/data/intel_deck.json`, with each object containing:

       ```json
       {
         "id": "<string>",
         "type": "<string>",
         "usesLeft": <integer>,
         "description": "<string>"
       }
       ```
  4. **(Optional) Generate PDF**:

     * If desired, use a PDF library (e.g., ReportLab) to put each card on its own PDF page:

       * Large title (card ID) in `AcmeCartoon` font.
       * Description text below in `MonoConsole` or a plain serif font.
       * Save as `static/data/intel_deck.pdf`.
     * If you can’t or don’t want to generate a PDF, skip this step gracefully.

* **How to Run**:

  1. From the project root, run:

     ```
     cd scripts
     python3 generate_intel_deck.py
     ```
  2. Confirm that `static/data/intel_deck.json` (and optionally `intel_deck.pdf`) appear.

---

## 12. Flask Template (`templates/index.html`) & Static References

Reiterating key IDs and classes that your CSS and JS depend on:

1. **Top-Level Overlays**

   * `#overlay-lobby`
   * `#overlay-game`

2. **Lobby Elements**

   * `#input-codename`
   * `#btn-join`
   * `#lobby-status`
   * `#player-list-lobby`
   * `#btn-start`

3. **Game Elements**

   * `#hud`
   * `#board`
   * Planning UI:

     * `#roundNumber`
     * `#select-offense`
     * `#select-defense`
     * `#select-target`
     * `#input-ip`
     * `#input-banner`
     * `#btn-confirm`
     * `#timerDisplay`
     * `#planning-status`
   * Resolution UI:

     * `#resolution`
     * `#resolution-content`
     * `#btn-continue`

4. **Mobile-Friendly Markers**

   * Use CSS class `.hidden` to hide elements (`display: none`).
   * HUD mini-panels have class `hud-player`.
   * Status dots inside each mini-panel use classes like `status-active`, `status-compromised`, etc.
   * Buttons use class `btn`.
   * Dropdowns and numeric input use distinct IDs for JS to `getElementById(...)`.

---

## 13. Requirements (`requirements.txt`)

Create a `requirements.txt` in the project root with exactly:

```
Flask==2.2.5
Flask-SocketIO==5.3.4
eventlet==0.33.0
```

> These versions have been tested to work together. You may add additional packages (e.g., a PDF library for intel deck generation), but keep core dependencies minimal.

---

## 14. Putting It All Together & Final Checks

Below is a concise, step-by-step checklist. As you create files and folders (without writing code), check them off and ensure each item’s content requirements are met.

### 14.1 Project Initialization

* [ ] Create the project root folder `JamesBland/`.
* [ ] Add `README.md` with:

  * Project description, prerequisites, installation & run instructions.
  * Folder structure overview.
  * How to play summary.
  * License and contributing notes.
* [ ] Add `LICENSE` (MIT text or “All Rights Reserved”).

### 14.2 Documentation (`docs/`)

* [ ] Create `docs/game_design.md` with:

  1. Introduction & core concept.
  2. Turn structure: Planning, Resolution, Adaptation.
  3. Detailed offense list (11 items), each with name, base success, cost, targets, on-success + on-failure effects.
  4. Detailed defense list (12 items), each with name, cost, offenses countered, on-block effects, notes.
  5. Interaction Matrix overview and example excerpt.
  6. Resource management: IP economy, gadgets (10–12 examples), statuses & transitions, strategic assets, alliances & betrayal.
  7. Master Plans (5–10 examples), each with name, description, reward or instant win, conditions.
  8. Victory conditions (5 types) and endgame tension.
  9. Mode variants (2-player vs. 6-player) and how to adjust.
  10. Sample round transcript (4-player example).

* [ ] Create `docs/protocol_spec.md` with:

  1. Overview of Flask-SocketIO on port 5000.
  2. Client→Server events: `joinLobby`, `startGame`, `submitAction`, `requestGameState` (payload fields).
  3. Server→Client events: `lobbyJoined`, `lobbyUpdate`, `gameStarted`, `playerSubmitted`, `turnResult`, `gameStateSnapshot`, `gameOver` (payload fields).
  4. Sequence flows (Lobby Join, Game Start, Single Round, Reconnect).
  5. Error handling rules (invalid JSON, default submissions, host disconnect).
  6. Versioning notes (optional `"protocolVersion"` field).
  7. Sketch of future automatic discovery (UDP broadcast).

* [ ] Create `docs/art_style_guide.md` with:

  1. Overall ACME cartoon aesthetic (colors, outlines, exaggeration).
  2. Color palette: primary (red, yellow, blue) and secondary (black, white, light gray).
  3. Fonts: `acme_cartoon.ttf` for display, `monospace_console.ttf` for logs.
  4. UI component styles (buttons, panels, dropdowns, tap sizes).
  5. Icon guidelines: board tiles (Safe House, Anvil Crate, Spy Marker), gadget icons (Spring Anvil, Jetpack Skates, Robo Duck, Bug Detector, Mirror Drone), status dots.
  6. Animation guidelines: Piano Drop, Anvil Bounce, Custard Pie, Explosion (dimensions, frame rate).
  7. HUD layout: top bar with scrollable mini-panels, status dot classes, gadget icon placements.
  8. Mobile/touch considerations (tap targets ≥44 px, font sizes, stacking).
  9. File formats: PNG for images, MP3 for audio, TTF/WOFF for fonts.

* [ ] Create `docs/network_topology.md` with:

  1. LAN assumptions (same subnet, host IP known).
  2. Manual join flow (host runs server, clients open `http://<host_ip>:5000`).
  3. WebSocket topology (server central authority; messages over single channel).
  4. Failure modes & recovery (client disconnect auto-submit defaults, host disconnect stops game).
  5. Optional UDP discovery sketch (for future).

### 14.3 Asset Definitions (`assets/`)

* [ ] Create `assets/audio/sfx/` and obtain:

  * `anvil_drop.mp3` (≤200 KB cartoon anvil thud).
  * `piano_launch.mp3` (≤300 KB cartoon piano whoosh + gliss).
  * `explosion_sizzle.mp3` (≤250 KB cartoon explosion).

* [ ] Create `assets/audio/music/` and obtain:

  * `suspense_loop.mp3` (30–60 sec loop, ≤1 MB).
  * `victory_fanfare.mp3` (10–15 sec fanfare, ≤500 KB).

* [ ] Create `assets/images/UI/` and design:

  * `button_play.png` (256×64 px, red, white “PLAY,” black outline).
  * `button_settings.png` (256×64 px, yellow, black gear + “SETTINGS,” black outline).
  * `panel_background.png` (1024×768 px, light gray blueprint grid, tileable).

* [ ] Create `assets/images/board_tiles/` and design:

  * `safe_house_icon.png` (128×128 px pastel blue fortress on springs).
  * `anvil_crate.png` (128×128 px wooden crate + silver anvil).
  * `spy_marker_default.png` (64×64 px black fedora silhouette with googly eyes).

* [ ] Create `assets/images/gadgets/` and design:

  * `spring_anvil.png` (128×128 px silver anvil on yellow spring).
  * `jetpack_skates.png` (128×128 px red roller skates with rocket flames).
  * `robo_duck.png` (128×128 px yellow duck with helmet).
  * `bug_detector.png` (128×128 px handheld radar device).

* [ ] Create `assets/fonts/` and obtain:

  * `acme_cartoon.ttf` (cartoon display font).
  * `monospace_console.ttf` (monospaced console font).

### 14.4 Static Files (`static/`)

1. **Audio**

   * [ ] Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`.
   * [ ] Copy `assets/audio/music/*.mp3` → `static/audio/music/`.

2. **Fonts**

   * [ ] Copy `assets/fonts/acme_cartoon.ttf` and `monospace_console.ttf` → `static/fonts/`.

3. **Images**

   * [ ] Copy `assets/images/UI/*.png` → `static/images/UI/`.
   * [ ] Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`.
   * [ ] Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`.

4. **CSS**

   * [ ] Create `static/css/style.css` with all mobile-first styles (HUD, planning panel, resolution panel, fonts, colors, responsive behaviors).

5. **JavaScript**

   * [ ] Create `static/js/app.js` implementing all client logic in plain JS (WebSocket handling, lobby flow, planning/resolution UI, timers, audio, banner logic, reconnect, victory handling).

### 14.5 HTML Template (`templates/index.html`)

* [ ] Create `templates/index.html` containing:

  1. **`<meta viewport>`** tag.
  2. **Link** to `/static/css/style.css`.
  3. **Include** Socket.IO client library from a CDN.
  4. **`<script defer>`** linking to `/static/js/app.js`.
  5. **Lobby Overlay** IDs: `overlay-lobby`, `input-codename`, `btn-join`, `lobby-status`, `player-list-lobby`, `btn-start`.
  6. **Game Overlay** (hidden by default) IDs: `overlay-game`, `hud`, `board`, and inside:

     * Planning UI: `roundNumber`, `select-offense`, `select-defense`, `select-target`, `input-ip`, `input-banner`, `btn-confirm`, `timerDisplay`, `planning-status`.
     * Resolution UI: `resolution`, `resolution-content`, `btn-continue`.

### 14.6 Backend Script (`server.py`)

* [ ] Create `server.py` which must:

  1. **Initialize** Flask + Flask-SocketIO (with `async_mode="eventlet"`, CORS allowed).
  2. **Maintain** in-memory state:

     * `users` (mapping `sid` → `{ codename, status, ip, gadgets, intel }`).
     * `connections["main"]` (set of sids in the lobby/game).
     * `current_turn["main"] = { "round": int, "submissions": { codename → submission } }`.
     * `assets` (mapping assetName → codename or `null`).
  3. **Define** the **Interaction Matrix** (nested dict) for every offense vs. defense, plus a “default” fallback.
  4. **Handle** WebSocket events:

     * `connect` & `disconnect` (clean up `users` and `connections`, auto-submit defaults on disconnect).
     * `joinLobby` (create new player, assign IP/gadgets/status, emit `lobbyJoined`, broadcast `lobbyUpdate`).
     * `startGame` (host only; initialize `current_turn`, `assets`, emit `gameStarted`).
     * `submitAction` (record submission, deduct IP, emit `playerSubmitted`, check if all active players have submitted—if yes, call **Turn Resolution**).
     * `requestGameState` (emit `gameStateSnapshot` with full current state to reconnecting client).
  5. **Turn Resolution Logic (internal)**:

     1. Handle Planning timer expiry (auto-submit defaults).
     2. Banner Phase: emit “showBanner” if any “informationWarfare,” collect “bannerDecision,” adjust targets/penalties.
     3. For each submission with `offenseId != ""`: look up `(offenseId, defenseId)` in the Interaction Matrix (or fallback to “default”), apply IP/status/intel changes.
     4. For each submission with no offense: treat as Safe Turn → award +1 IP.
     5. Process Strategic Asset captures (update `assets` and yield IP).
     6. Build and emit `turnResult`.
     7. Increment `round`, clear `submissions`, apply gadget upkeep, award asset yields, expire alliances, process captured players.
     8. Check victory conditions—if any met, emit `gameOver` and stop.
  6. **Run** the server on `0.0.0.0:5000` (so LAN devices can connect).

### 14.7 Requirements (`requirements.txt`)

* [ ] Create `requirements.txt` with exactly:

  ```
  Flask==2.2.5
  Flask-SocketIO==5.3.4
  eventlet==0.33.0
  ```

### 14.8 Tests (`tests/`)

* [ ] `tests/test_interaction_matrix.py`: Verify every offense/defense pairing outcome, plus default fallback.
* [ ] `tests/test_action_resolver.py`: Test single safe turn, head-to-head assassination vs. safe house, multi-attacker scenario, failed infiltration vs. sweep & clear.
* [ ] `tests/test_game_loop.py`: Test multi-round IP accumulation, status transitions (Compromised → cannot use False Identity), and victory detection (Last Spy Standing, Network Control).
* [ ] (Optional) `tests/test_utils.py`: Test any utility functions (random weighting, IP clamping, time formatting).

> **Run tests** with `pytest tests/` once `server.py` and all core logic are in place.

### 14.9 Scripts (`scripts/`)

* [ ] `scripts/build_assets.sh`: Optimize PNGs (if possible) and copy audio, images, and fonts from `assets/` → `static/`. Print a confirmation message at the end.
* [ ] `scripts/generate_intel_deck.py`: Read `assets/data/intel_definitions.json` (or create defaults), build and shuffle a deck, write `static/data/intel_deck.json`, and optionally generate `static/data/intel_deck.pdf`.

### 14.10 `.gitignore`

* [ ] Create a `.gitignore` in the project root with entries:

  ```
  # Python
  venv/
  __pycache__/
  *.pyc

  # Flask logs or DB files
  *.log

  # Node (if any)
  node_modules/

  # OS & Editor
  .DS_Store
  Thumbs.db
  .vscode/
  .idea/

  # Static data (optional)
  static/data/*.json
  static/data/*.pdf
  ```

---

## 15. 2-Player vs 6-Player Adjustments

When you implement and test, keep these in mind. You do not need separate code branches—just adjust a few parameters at runtime based on the number of players in the lobby.

1. **Minimum/Maximum Players**

   * The lobby allows 2–6 players.
   * Show “(2–6 players)” in the lobby UI.
   * In a 2-player game, disable alliance-related offenses/defenses.

2. **Timer Adjustments**

   * **2-Player Mode**: Reduce Planning timer to 60 seconds (customer preference). Document this in `game_design.md` as a recommended variant.
   * **6-Player Mode**: Use full 90 seconds to give everyone time to think.

3. **Offense/Defense Availability**

   * If `connections["main"]` length = 2, omit:

     * Offenses: “Alliance Disruption,” “False Flag” (which requires a third target), “Network Attack” (since no third target’s assets).
     * Defenses: “Alliance Building,” “Honeypot Operations” (less effective in 2-player since no third party to lure).
   * In 6-player mode, enable all 11 offense and 12 defense options.

4. **Starting Gadgets**

   * **2-Player Mode**: Give each player two starting gadgets (e.g., `["springAnvil", "jetpackSkates"]`), so the duel is more dynamic. Document as a house rule.
   * **6-Player Mode**: Each starts with two random basic gadgets chosen from `["springAnvil", "jetpackSkates", "roboDuck", "bugDetector"]`.

5. **Victory Conditions**

   * **2-Player Mode**: Only “Last Spy Standing” and “Intelligence Supremacy” are possible. Omit “Network Control” (not enough assets), “Alliance Victory” (no alliances), and “Mission Completion” only if the drawn Master Plans include solo objectives.
   * **6-Player Mode**: All five victory paths apply. Alliances play a key role.

---

## 16. Mobile-First Design Checklist

Because the target devices are phones and tablets on the same Wi-Fi, ensure:

1. **Responsive UI**

   * Use relative units (`%`, `rem`) for widths so elements adjust to any viewport.
   * Buttons and inputs fill \~80% of the screen width with adequate padding (≥0.5 rem).
   * HUD is a flex container with `overflow-x: auto` and no wrapping.

2. **Touch-Friendly Elements**

   * All clickable items (buttons, `<select>`, IP slider) are ≥44×44 px.
   * Avoid hover states; rely exclusively on taps.

3. **Font Size & Legibility**

   * Main text: \~1 rem (16 px).
   * Headings/buttons: 1.2 rem or 1.5 rem.
   * HUD codename and IP: 0.9 rem bold.

4. **Autoplay Restrictions**

   * On mobile, audio does *not* play until a user interaction.
   * For example, call `bgMusic.play()` only when “Start Game” is tapped.

5. **Performance**

   * Keep audio files small (SFX ≤300 KB, loops ≤1 MB).
   * Keep icon PNGs small (≤100 KB).
   * Prefer CSS keyframe animations over heavy GIFs; if using GIFs, keep them ≤50 KB, ≤15 frames.

6. **Orientation**

   * Test both portrait and landscape.
   * In portrait, Planning UI stacks; HUD scrolls horizontally if it doesn’t fit.
   * In landscape, HUD might shrink to a smaller vertical bar on one side (if you prefer), or remain at top.

7. **Touch Events**

   * Use only `click` events.
   * If you need tooltips over gadget icons, use a “long-press” detection or a tap that toggles a small info box, because hover does not exist on touch screens.

---

## 17. Playtester Checklist & Final Validation

Before declaring the project “complete,” perform playtests with these checkpoints:

1. **Lobby Flow**

   * At least 2 devices connect to `http://<host_ip>:5000`.
   * Each enters a unique codename and clicks “Join Lobby.”
   * The lobby list updates on all devices, showing codename, status “active,” and IP = 5.
   * When ≥2 are in the lobby, “Start Game” button on the host’s device becomes enabled.
   * Host clicks “Start Game → All devices switch to game screen.

2. **Gameplay Flow**

   * **Round 1**:

     * HUD displays each player’s codename, IP = 5, status = Active (green), and two starting gadget icons.
     * Planning Phase: countdown timer begins at 90 sec.
     * `#select-offense` lists 11 offense options (all except alliance-only if 2 players).
     * `#select-defense` lists 12 defense options (same caveat for alliances).
     * `#select-target` lists valid targets (exclude self and any Captured/Eliminated).
     * `#input-ip` numeric field clamps between 0 and current IP.
     * If a player selects “Information Warfare,” an input box `#input-banner` appears and `#input-ip` automatically sets to 2 and is disabled from manual change.
     * Click “Confirm Choices” disables all inputs and shows “Action Submitted.”
     * `playerSubmitted` fires from server, and UI shows checkmark next to that player on the HUD.
     * Once all players have submitted, the server immediately resolves (no need to wait the full 90 sec).

   * **Resolution Phase**:

     * Clients hide Planning UI and show `#resolution`.
     * `#resolution-content` displays lines like “AgentX → IP Δ: +2, new IP = 7, Status = Active, Intel Gained: \[‘targetDefense’].”
     * If an assassination landed, `piano_launch.mp3` plays. If an anvil bounced, `anvil_drop.mp3` plays.
     * After \~1 sec delay, `#btn-continue` appears.

   * **Continue**:

     * Tapping `#btn-continue` hides `#resolution`, resets Planning UI for the next round. Server emits next planning start automatically.

3. **Biplane Banner Tests**

   * Player picks “Information Warfare” as defense, types a banner message, and pays 2 IP.
   * When resolution begins, a small plane flies across the top on all clients, dragging that banner.
   * Any player who targeted the bannerer sees a prompt: “Believe Banner” vs. “Ignore Banner” with a 10 sec countdown.
   * If they tap “Believe” and the banner was genuine, their target is rerouted. If they “Ignore” and the banner was genuine, they suffer a –1 penalty. If they “Believe” but the banner was a bluff, their action is wasted and broadcaster gains +1 IP. Confirm all logic works as documented.

4. **State Updates**

   * After `turnResult`, the HUD updates IP and status circle colors correctly.
   * If a player becomes Compromised or Burned, their status dot changes.
   * If a player is Captured or Eliminated, their mini-panel gray out or show a special icon.
   * Intel Cards are delivered: when you gain an Intel Card (e.g., successful Infiltration), a dialog appears: “You drew: \[CardName].” The card is appended to your local `user.intel`.

5. **Victory Scenarios**

   * **Network Control**: Simulate a player capturing 3 assets; confirm `gameOver` with “Network Control.”
   * **Master Plan**: Simulate a player fulfilling a Master Plan (e.g., exposing all opponents at once); confirm `gameOver` with “Mission Completion.”
   * **Last Spy Standing**: In a 2-player match, let one eliminate the other; confirm “Last Spy Standing.”
   * **Intelligence Supremacy**: Simulate a player collecting full dossiers on all others; confirm “Intelligence Supremacy.”
   * **Alliance Victory**: In a 6-player free-for-all, have two allies fulfill a joint objective; confirm joint winners, then trigger Final Showdown. Confirm that both get +3 IP and can choose Assassination or Sabotage, and final ranking is correct.

6. **Reconnect Handling**

   * During Planning Phase, turn off Wi-Fi on one device to force a disconnect.
   * Wait a few seconds, then re-enable Wi-Fi. The client should reconnect, emit `requestGameState`, and receive `gameStateSnapshot`.
   * The UI should rebuild (HUD, Planning UI, and timer with remaining time).
   * If the device fails to reconnect before timer 0, confirm its turn defaulted to (`offenseId=""`, `defenseId="underground"`, `ipToSpend=0`).

7. **Edge Cases**

   * If a player never clicks “Confirm,” server auto-submits defaults at timer 0. Confirm expected behavior.
   * If multiple players target the same defender, confirm correct resolution order (highest IP first) and that each attacker’s outcome is applied sequentially.
   * If an offense/defense is missing from the matrix, confirm the “default” outcome is used.
   * If a player tries to spend more IP than they have (client-side), the JS clamps `#input-ip` to their current IP. On server-side, it also clamps to avoid negative IP.

8. **Mobile Testing**

   * Test on iOS Safari and Android Chrome.
   * Confirm dropdowns open native pickers, buttons are large enough, and no text or UI elements are clipped.
   * Test in both portrait and landscape: HUD scrolls horizontally if too many players, Planning UI stacks or reflows properly.

9. **Code-Free Artifact Check**

   * Verify that no code snippets appear in your `docs/` files. Everything in `/docs/` is plain English describing design, protocols, art direction, and topology.
   * Confirm that all assets listed in Section 3 exist in `assets/` and have been copied to `static/` via `build_assets.sh`.

---

## 18. Summary of Key Files & Their Contents

Below is a **plain-English list** of every file/folder you should end up with and **exactly what each contains**. Use this as a final checklist.

````
JamesBland/
├── README.md
│   └─ Overview, build/run instructions, folder structure, how to play, license.
├── LICENSE
│   └─ MIT text (or “All Rights Reserved”).
├── docs/
│   ├── game_design.md
│   │   └─ Full game rules:  
│   │       • Introduction & concept.  
│   │       • Turn phases (Planning, Resolution, Adaptation).  
│   │       • Offensive operations (11) with costs, success/failure effects.  
│   │       • Defensive measures (12) with costs, counters, effects.  
│   │       • Interaction Matrix overview + example excerpt.  
│   │       • Resource management: IP economy, gadget list (10–12), statuses & transitions, strategic assets, alliances & betrayal.  
│   │       • Master Plans (5–10 examples).  
│   │       • Victory conditions (5 types) and endgame drama.  
│   │       • Mode variants (2-player vs. 6-player).  
│   │       • Sample 4-player round transcript.  
│   ├── protocol_spec.md
│   │   └─ WebSocket events & payloads:  
│   │       • Client→Server: `joinLobby`, `startGame`, `submitAction`, `requestGameState`.  
│   │       • Server→Client: `lobbyJoined`, `lobbyUpdate`, `gameStarted`, `playerSubmitted`, `turnResult`, `gameStateSnapshot`, `gameOver`.  
│   │       • Sequence flows (Lobby Join, Game Start, Round, Reconnect).  
│   │       • Error handling and versioning notes.  
│   │       • Optional UDP discovery sketch.  
│   ├── art_style_guide.md
│   │   └─ ACME cartoon aesthetic:  
│   │       • Color palette (primary, secondary).  
│   │       • Fonts (`acme_cartoon.ttf`, `monospace_console.ttf`).  
│   │       • UI component styles (buttons, panels, dropdowns, sizes).  
│   │       • Icon guidelines (board tiles, gadget icons, status dots).  
│   │       • Animation specs (Piano Drop, Anvil Bounce, Custard Pie, Explosion).  
│   │       • HUD layout and classes.  
│   │       • Mobile/touch considerations.  
│   │       • File format recommendations (PNG, MP3, TTF/WOFF).  
│   └── network_topology.md
│       └─ LAN assumptions; manual join flow; WebSocket topology; failure modes (client/host disconnect); optional UDP discovery ideas.
├── assets/
│   ├── audio/
│   │   ├── sfx/
│   │   │   ├── anvil_drop.mp3       (cartoon anvil “thud” ≤200 KB)
│   │   │   ├── piano_launch.mp3     (cartoon piano whoosh + gliss ≤300 KB)
│   │   │   └── explosion_sizzle.mp3 (cartoon explosion “boom” ≤250 KB)
│   │   └── music/
│   │       ├── suspense_loop.mp3   (30–60 sec loop, ≤1 MB)
│   │       └── victory_fanfare.mp3 (10–15 sec fanfare, ≤500 KB)
│   ├── images/
│   │   ├── UI/
│   │   │   ├── button_play.png        (256×64 px, red, white “PLAY”)
│   │   │   ├── button_settings.png    (256×64 px, yellow, gear + “SETTINGS”)
│   │   │   └── panel_background.png   (1024×768 px, light gray blueprint grid)
│   │   ├── board_tiles/
│   │   │   ├── safe_house_icon.png    (128×128 px, pastel blue fortress on springs)
│   │   │   ├── anvil_crate.png        (128×128 px, wooden crate with anvil)
│   │   │   └── spy_marker_default.png (64×64 px, spy silhouette with googly eyes)
│   │   └── gadgets/
│   │       ├── spring_anvil.png    (128×128 px, silver anvil on yellow spring)
│   │       ├── jetpack_skates.png  (128×128 px, red roller skates with rockets)
│   │       ├── robo_duck.png       (128×128 px, yellow duck with helmet)
│   │       └── bug_detector.png    (128×128 px, handheld radar device)
│   └── fonts/
│       ├── acme_cartoon.ttf       (cartoon display font for headings/buttons)
│       └── monospace_console.ttf  (monospace font for logs/chat)
├── server.py
│   └─ Flask + Flask-SocketIO app:
│       • In-memory state (`users`, `connections`, `current_turn`, `assets`).  
│       • Interaction Matrix nested dict for offense vs. defense outcomes (with “default” fallback).  
│       • WebSocket event handlers:  
│         – `connect`, `disconnect` (clean up, auto-submit defaults).  
│         – `joinLobby` (register player, send `lobbyJoined`, broadcast `lobbyUpdate`).  
│         – `startGame` (host only; initialize first round, send `gameStarted`).  
│         – `submitAction` (record submission, deduct IP, send `playerSubmitted`, run resolution when all in).  
│         – `requestGameState` (send `gameStateSnapshot` to reconnecting client).  
│       • Internal **Turn Resolution**:  
│         – Handle banner phase (“showBanner”, collect “bannerDecision”).  
│         – For each offense vs. defense, look up outcome and apply IP/status/intel changes.  
│         – Safe Turn defaults award +1 IP.  
│         – Process asset captures, gadget upkeep, alliance expiry, captured→burned transitions.  
│         – Emit `turnResult`.  
│         – Increment round, clear submissions, check victory conditions, emit `gameOver` if needed.  
│       • Runs server on `0.0.0.0:5000` using eventlet.  
├── requirements.txt
│   └─  
│      Flask==2.2.5  
│      Flask-SocketIO==5.3.4  
│      eventlet==0.33.0
├── templates/
│   └── index.html
│       └─ Single dynamic HTML page with:  
│           • `<meta name="viewport">`.  
│           • Link to `/static/css/style.css`.  
│           • `<script src="https://cdn.socket.io/..."></script>`.  
│           • `<script defer src="/static/js/app.js"></script>`.  
│           • Lobby UI (`#overlay-lobby`, `#input-codename`, `#btn-join`, `#lobby-status`, `#player-list-lobby`, `#btn-start`).  
│           • Game UI (`#overlay-game`) with HUD (`#hud`), board placeholder (`#board`), Planning UI (`#roundNumber`, `#select-offense`, `#select-defense`, `#select-target`, `#input-ip`, `#input-banner`, `#btn-confirm`, `#timerDisplay`, `#planning-status`), Resolution UI (`#resolution`, `#resolution-content`, `#btn-continue`).  
├── static/
│   ├── audio/
│   │   ├── sfx/
│   │   │   ├── anvil_drop.mp3
│   │   │   ├── piano_launch.mp3
│   │   │   └── explosion_sizzle.mp3
│   │   └── music/
│   │       ├── suspense_loop.mp3
│   │       └── victory_fanfare.mp3
│   ├── css/
│   │   └── style.css
│   ├── fonts/
│   │   ├── acme_cartoon.ttf
│   │   └── monospace_console.ttf
│   ├── images/
│   │   ├── UI/
│   │   │   ├── button_play.png
│   │   │   ├── button_settings.png
│   │   │   └── panel_background.png
│   │   ├── board_tiles/
│   │   │   ├── safe_house_icon.png
│   │   │   ├── anvil_crate.png
│   │   │   └── spy_marker_default.png
│   │   └── gadgets/
│   │       ├── spring_anvil.png
│   │       ├── jetpack_skates.png
│   │       ├── robo_duck.png
│   │       └── bug_detector.png
│   └── js/
│       └── app.js
├── tests/
│   ├── test_interaction_matrix.py
│   │   └─ Tests every offense/defense pairing outcome plus default fallback.  
│   ├── test_action_resolver.py
│   │   └─ Tests full turn resolution: safe turn, head-to-head, multi-attacker.  
│   ├── test_game_loop.py
│   │   └─ Tests multi-round IP economy, status transitions, victory condition triggers.  
│   └── test_utils.py (optional)
│       └─ Tests any helper utility functions (random weighting, IP clamping).  
├── scripts/
│   ├── build_assets.sh
│   │   └─ Optimize PNGs (if possible) and copy all assets from `assets/` → `static/`; print “Done.”  
│   └── generate_intel_deck.py
│       └─ Read `assets/data/intel_definitions.json` (or create minimal defaults), build & shuffle deck, write `static/data/intel_deck.json`; optionally generate `intel_deck.pdf`.  
└── .gitignore
    └─ Ignores: `venv/`, `__pycache__/`, `*.pyc`, `*.log`, `node_modules/`, `.DS_Store`, `Thumbs.db`, `.vscode/`, `.idea/`, `static/data/*.json`, `static/data/*.pdf`.

---

## 19. Development Flow Summary

1. **Write Documentation First**: Populate all `docs/` files so your design, protocols, art style, and topology are crystal-clear.  
2. **Create/Source Assets**: Produce or source each audio, image, and font asset under `assets/`.  
3. **Copy Assets**: Run `scripts/build_assets.sh` (or manually) to populate `static/` with optimized assets.  
4. **Draft `templates/index.html`**: Create the HTML structure with correct IDs & classes.  
5. **Write `static/css/style.css`**: Implement mobile-first CSS for HUD, panels, buttons, fonts, responsiveness.  
6. **Write `static/js/app.js`**: Implement client logic (WebSockets, lobby, planning, resolution, banner, reconnect, victory).  
7. **Implement `server.py`**: Build the backend: in-memory state, Interaction Matrix, WebSocket event handlers, turn resolution, victory checks.  
8. **Install Dependencies**: Run `pip install -r requirements.txt`.  
9. **Write Unit Tests**: Populate `tests/` with pytest files (no code shown here, just plain-English test plans).  
10. **Run Playtests**: Use actual mobile devices on your LAN to validate the full flow (lobby, gameplay, banner logic, resolution, reconnect, victory).  
11. **Iterate & Polish**: Tweak IP costs, success rates, artwork, audio, and CSS based on feedback.  
12. **Finalize**: Ensure `.gitignore` is correct, documentation is up to date, and tag a “v1.0” release.

Following this **complete checklist** will result in:

- A **clear folder structure** with every file described in plain English.  
- No embedded code in documentation—only descriptions of where code belongs and what it does.  
- A mobile-first, browser-based game running on any device connected to your home Wi-Fi, with no need for Unity, Godot, or Flutter.  
- All assets (images, audio, fonts) sourced or created and placed into the correct folders.  
- Detailed documentation covering game design, network protocols, art direction, and topology.  
- Unit tests (pytest) ensuring game logic is correct before you release.  
- Helper scripts to automate asset copying and Intel deck generation.

When ready, run the server with:
```bash
python server.py
````
