* [x] **Project Root Setup**

  * [x] Create folder `JamesBland/`
  * [x] Inside `JamesBland/`, create:

    * [x] `README.md`
    * [x] `LICENSE`
    * [x] Folder `docs/`
    * [x] Folder `assets/`
    * [x] Folder `static/`
    * [x] Folder `templates/`
    * [x] File `server.py`
    * [x] File `requirements.txt`
    * [x] Folder `tests/`
    * [x] Folder `scripts/`
    * [x] File `.gitignore`

* [x] **Documentation (`docs/`)**

  * [x] Create `docs/game_design.md`

    * [x] Introduction & Core Concept
    * [x] Turn Structure: Planning → Resolution → Adaptation
    * [x] Detailed list of **11 Offenses**, each with:

      * [x] Name, Base Success, Cost in IP, Legal Targets
      * [x] On-Success Effects
      * [x] On-Failure Effects
    * [x] Detailed list of **12 Defenses**, each with:

      * [x] Name, Cost in IP, Offenses Countered
      * [x] On-Block Effects and Secondary Notes
    * [x] Interaction Matrix Overview + Example Excerpt
    * [x] Resource Management & Equipment:

      * [x] IP Economy (how IP is earned and spent, floor/ceiling rules)
      * [x] Gadget List (10–12 gadgets with Name, Cost, Effect, Cooldown)
      * [x] Statuses & Transitions (Active, Compromised, Burned, Captured, Eliminated)
      * [x] Strategic Assets (names, control cost, yield)
      * [x] Alliances & Betrayal mechanics (Non-Aggression Pact, Coordinated Operation)
    * [x] Master Plans (5–10 examples: Name, Description, Reward/Win, Conditions)
    * [x] Victory Conditions & Endgame (5 types, detailed descriptions)
    * [x] Mode Variants (2-Player vs. 6-Player rules adjustments)
    * [x] Sample Round Transcript (4-player example)
  * [x] Create `docs/protocol_spec.md`

    * [x] Overview of Flask + Flask-SocketIO setup (port 5000, CORS)
    * [x] Event Definitions:

      * [x] **Client → Server**: `joinLobby`, `startGame`, `submitAction`, `requestGameState`
      * [x] **Server → Client**: `lobbyJoined`, `lobbyUpdate`, `gameStarted`, `playerSubmitted`, `turnResult`, `gameStateSnapshot`, `gameOver`
    * [x] Sequence Flows:

      * [x] Lobby Join Flow
      * [x] Game Start Flow
      * [x] Single Round Flow
      * [x] Reconnect Flow
    * [x] Error Handling Rules (invalid JSON, default submissions, host disconnect)
    * [x] Versioning Notes (optional `"protocolVersion"` field)
    * [x] Optional Future Automatic Discovery Sketch (UDP broadcast)
  * [x] Create `docs/art_style_guide.md`

    * [x] Overall ACME Cartoon Aesthetic description
    * [x] Color Palette (Primary: Red #E53935, Yellow #FFEB3B, Blue #1E88E5; Secondary: Black, White, Light Gray)
    * [x] Fonts:

      * [x] `acme_cartoon.ttf` for headings/buttons
      * [x] `monospace_console.ttf` for logs/chat
    * [x] UI Components:

      * [x] Buttons (size, corners, outlines, text)
      * [x] Panels (background, borders, shadows)
      * [x] Dropdowns & Inputs (styles, padding)
    * [x] Icons & Board Tiles:

      * [x] Tile Size: 128×128 px, transparent background, thick black outlines
      * [x] Board Tile Icons: Safe House, Anvil Crate, Spy Marker
      * [x] Gadget Icons: Spring-Loaded Anvil, Jetpack Skates, Robo-Duck, Bug Detector, Mirror Drone Squadron, plus 4–6 more
      * [x] Status Icons: Active (green), Compromised (yellow), Burned (orange), Captured (red), Eliminated (black) (32×32 px)
    * [x] Animations:

      * [x] Piano Drop (64×64 px GIF or CSS keyframes, \~1 sec, 12 fps)
      * [x] Anvil Bounce (64×64 px, \~0.8 sec, 10 fps)
      * [x] Custard Pie Splash (64×64 px, 8–10 frames)
      * [x] Explosion (64×64 px, 10 frames at 12 fps)
      * [x] "2× scale" guideline: Create assets at 128×128 and scale down to 64×64
    * [x] HUD Layout:

      * [x] Top bar (\~10% viewport height, dark gray #333333)
      * [x] Mini-panel for each player: Avatar Circle, Codename, IP Count (brain icon + number), Status Dot, Gadget Icons (up to 3)
      * [x] Horizontal scroll if >6 players (`overflow-x: auto; white-space: nowrap;`)
      * [x] Mini-panel width ≥80 px
    * [x] Touch & Mobile Considerations:

      * [x] Tap Targets ≥44×44 px
      * [x] Font Sizes: Main \~1 rem, Headings/Buttons \~1.2–1.5 rem, HUD Codename/IP \~0.9 rem bold
      * [x] Spacing: ≥8 px margins/padding between elements
      * [x] Portrait stacking: Offense → Defense → Target → IP Slider → Confirm
      * [x] Use media queries (`@media (max-width: 480px) { … }`)
    * [x] Export & File Formats:

      * [x] PNG 24-bit for icons/UI (transparency)
      * [x] MP3 for audio (SFX ≤300 KB; loops ≤1 MB)
      * [x] TTF and WOFF for fonts
      * [x] GIF optional for animations but prefer CSS keyframes
  * [x] Create `docs/network_topology.md`

    * [x] LAN Assumptions (same subnet `192.168.1.x/24`, host IP known)
    * [x] Manual Join Flow:

      * [x] Host runs `python server.py` → "Server listening on 0.0.0.0:5000 (LAN IP: 192.168.1.42)"
      * [x] Clients open browser to `http://192.168.1.42:5000`
      * [x] ASCII/diagram showing Host PC and three devices (Phone, Tablet, Laptop) connecting
    * [x] WebSocket Topology:

      * [x] Single central server; no P2P
      * [x] Each client opens one WebSocket to server
      * [x] All real-time events use that WebSocket
      * [x] On disconnect, server auto-submits defaults; on reconnect, server sends `gameStateSnapshot`
    * [x] Failure Modes & Recovery:

      * [x] Client Disconnect: auto-submit defaults if not reconnected before timer expires; reconnect triggers `requestGameState` → `gameStateSnapshot`
      * [x] Server/Host Disconnect: clients show "Host disconnected—please restart"
      * [x] No automatic host failover in v1
    * [x] (Optional) Future Automatic Discovery Sketch: UDP broadcast "GameAvailable" on port 9999, clients listen and populate "Join Game" dropdown

* [x] **Asset Preparation (`assets/`)**

  * [x] **Audio SFX** (`assets/audio/sfx/`)

    * [x] Obtain or record `anvil_drop.mp3` (≤200 KB, cartoon anvil thud)
    * [x] Obtain or record `piano_launch.mp3` (≤300 KB, whoosh + descending piano gliss)
    * [x] Obtain or record `explosion_sizzle.mp3` (≤250 KB, comedic boom)
  * [x] **Music Loops** (`assets/audio/music/`)

    * [x] Obtain or create `suspense_loop.mp3` (30–60 sec loop, ≤1 MB)
    * [x] Obtain or create `victory_fanfare.mp3` (10–15 sec fanfare, ≤500 KB)
  * [x] **Images – UI** (`assets/images/UI/`)

    * [x] Design `button_play.png` (256×64 px, red fill #E53935, white "PLAY" uppercase text with black outline, rounded corners 8 px, thick black border)
    * [x] Design `button_settings.png` (256×64 px, yellow fill #FFEB3B, black gear icon left, white "SETTINGS" uppercase text with black outline, rounded corners 8 px)
    * [x] Design `panel_background.png` (1024×768 px tileable, light gray #F2F2F2 blueprint grid with thin white/light-blue lines)
  * [x] **Images – Board Tiles** (`assets/images/board_tiles/`)

    * [x] Design `safe_house_icon.png` (128×128 px, pastel blue fortress on cartoon white springs, thick black outline)
    * [x] Design `anvil_crate.png` (128×128 px, brown wooden crate with silver anvil popping out, thick black outline)
    * [x] Design `spy_marker_default.png` (64×64 px, black fedora silhouette with large white googly eyes, thick black outline)
  * [x] **Images – Gadgets** (`assets/images/gadgets/`)

    * [x] Design `spring_anvil.png` (128×128 px, silver anvil on big coiled yellow spring, thick black outline)
    * [x] Design `jetpack_skates.png` (128×128 px, bright red roller skates with small rocket thrusters and stylized orange flame, thick black outline)
    * [x] Design `robo_duck.png` (128×128 px, cartoon yellow duck wearing a small metal helmet, big googly eyes, thick black outline)
    * [x] Design `bug_detector.png` (128×128 px, handheld radar device with blinking red LED, gray metallic body, thick black outline)
    * [ ] (Optional) Add 1–2 more gadget icons as needed
  * [x] **Fonts** (`assets/fonts/`)

    * [x] Obtain or create `acme_cartoon.ttf` (bold quirky cartoon display font)
    * [x] Obtain or create `monospace_console.ttf` (classic monospaced font for logs/chat)

* [x] **Static Files (`static/`)**

  * [x] **Audio**

    * [x] Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`
    * [x] Copy `assets/audio/music/*.mp3` → `static/audio/music/`
  * [x] **Fonts**

    * [x] Copy `assets/fonts/acme_cartoon.ttf` → `static/fonts/`
    * [x] Copy `assets/fonts/monospace_console.ttf` → `static/fonts/`
  * [x] **Images**

    * [x] Copy `assets/images/UI/*.png` → `static/images/UI/`
    * [x] Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`
    * [x] Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`
  * [x] **CSS**

    * [x] Create `static/css/style.css` with:

      * [x] Mobile-first flex/grid layout
      * [x] HUD styling (scrollable flex, mini-panels with `.hud-player`, status dot classes)
      * [x] Planning & Resolution panels (`.planning-panel`, `.resolution-panel` styles)
      * [x] Inputs/dropdowns/buttons styles (font sizes, padding, borders, radius)
      * [x] Font imports (`@font-face` for AcmeCartoon and MonoConsole)
      * [x] Media queries for screens ≤480 px
  * [x] **JavaScript**

    * [x] Create `static/js/app.js` to implement client-side logic in plain JS:

      * [x] WebSocket connection (`io('<SERVER_URL>')`, handle `connect`/`disconnect`)
      * [x] Lobby logic (`joinLobby`, `lobbyJoined`, `lobbyUpdate`, enable "Start Game" when ≥2 players)
      * [x] Game logic:

        * [x] Handle `gameStarted` → build HUD (`#hud`) and Planning UI (`#select-offense`, `#select-defense`, `#select-target`, `#input-ip`, `#input-banner`, `#btn-confirm`, `#timerDisplay`, `#planning-status`)
        * [x] Start Planning Phase timer (90 sec or 60 sec for 2-player)
        * [x] On "Confirm Choices" → disable inputs, show "Action Submitted," emit `submitAction`
        * [x] Listen for `playerSubmitted` → show checkmark in HUD
      * [x] Biplane Banner logic:

        * [x] If defense = "informationWarfare," show `#input-banner`, set `ipToSpend = 2`
        * [x] Listen for custom `"showBanner"` event → play banner animation, prompt "Believe" or "Ignore" for affected players
        * [x] Emit `"bannerDecision"`
      * [x] Turn Resolution:

        * [x] Listen for `turnResult` → hide Planning UI, show `#resolution`, append lines to `#resolution-content`, play SFX (`anvil_drop.mp3`, `piano_launch.mp3`, `explosion_sizzle.mp3`), show `#btn-continue` after \~1 sec
      * [x] On `#btn-continue` click → hide `#resolution`, reset Planning UI fields, wait for next round
      * [x] Reconnect handling:

        * [x] On `disconnect`, show "Reconnecting…" overlay
        * [x] On `connect`, emit `requestGameState`
        * [x] On `gameStateSnapshot`, rebuild HUD and UI, restart timer if applicable
      * [x] Victory handling:

        * [x] Listen for `gameOver` → hide all UIs, show full-screen "Winner(s): … by …" modal, play `victory_fanfare.mp3`, offer "Return to Lobby" or "Restart"
      * [x] Asset preloading (optional): load `Audio` objects and call `.load()`
      * [x] Mobile-first: use only `click` events, ensure all interactive elements ≥44×44 px, audio playback triggered by user

* [x] **HTML Template (`templates/index.html`)**

  * [x] `<head>`

    * [x] `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
    * [x] `<link rel="stylesheet" href="/static/css/style.css">`
    * [x] `<script src="https://cdn.socket.io/4.5.1/socket.io.min.js"></script>`
    * [x] `<script defer src="/static/js/app.js"></script>`
    * [x] `<title>James Bland: ACME Edition</title>`
  * [x] `<body>`

    * [x] **Lobby Overlay** (`<div id="overlay-lobby">`)

      * [x] `<h1>James Bland: ACME Edition</h1>`
      * [x] `<input type="text" id="input-codename" placeholder="Your Codename" maxlength="16">`
      * [x] `<button id="btn-join">Join Lobby</button>`
      * [x] `<div id="lobby-status"></div>`
      * [x] `<div id="player-list-lobby"></div>`
      * [x] `<button id="btn-start" disabled>Start Game</button>`
      * [x] Optional help icon or instructions link
    * [x] **Game Overlay** (`<div id="overlay-game" class="hidden">`)

      * [x] **HUD** (`<div id="hud"></div>`) containing up to 6 mini-panels with class `hud-player`, each with:

        * [x] Avatar circle (`<div class="avatar-circle"></div>`)
        * [x] Codename label (`<div class="codename-label">AgentX</div>`)
        * [x] Brain icon + `<span class="ip-count">5</span>`
        * [x] Status dot (`<div class="status-dot status-active"></div>`)
        * [x] Gadget icons container (`<div class="gadget-icons"></div>`)
      * [x] **Board Placeholder** (`<div id="board">Board (Placeholder)</div>`)
      * [x] **Planning Panel** (`<div id="planning" class="planning-panel">`)

        * [x] "Round: <span id="roundNumber">0</span>"
        * [x] Offense dropdown: `<select id="select-offense"><option value="">Select Offense</option>…</select>`
        * [x] Defense dropdown: `<select id="select-defense"><option value="">Select Defense</option>…</select>`
        * [x] Target dropdown: `<select id="select-target"><option value="">Select Target</option>…</select>`
        * [x] IP numeric input: `<input type="number" id="input-ip" min="0" value="0">`
        * [x] Banner text input (hidden initially): `<input type="text" id="input-banner" maxlength="25" placeholder="Banner Message" class="hidden">`
        * [x] Confirm button: `<button id="btn-confirm" disabled>Confirm Choices</button>`
        * [x] Timer display: `<div id="planning-timer">Time: <span id="timerDisplay">90</span>s</div>`
        * [x] Planning status: `<div id="planning-status"></div>`
      * [x] **Resolution Panel** (`<div id="resolution" class="resolution-panel hidden">`)

        * [x] `<h2>Resolution</h2>`
        * [x] `<div id="resolution-content"></div>`
        * [x] `<button id="btn-continue" class="hidden">Continue to Next Round</button>`

* [x] **Backend Script (`server.py`)**

  * [x] Initialize Flask + Flask-SocketIO (`async_mode="eventlet"`, `cors_allowed_origins="*"`)
  * [x] Maintain in-memory state:

    * [x] Dictionary `users`: `sid → { codename, status, ip, gadgets, intel }`
    * [x] Dictionary `connections["main"]`: set of `sid` in lobby/game
    * [x] Dictionary `current_turn["main"]`: `{ round: int, submissions: { codename → submission } }`
    * [x] Dictionary `assets`: `{ assetName → codename or null }`
  * [x] Define Interaction Matrix as nested dict:

    * [x] Each `offenseId` → `defenseId` → outcome object with:

      * [x] `offenseSucceeds` (bool)
      * [x] `ipChangeOffender` (int)
      * [x] `ipChangeDefender` (int)
      * [x] `newStatusOffender` (string)
      * [x] `newStatusDefender` (string)
      * [x] `intelOffender` (list of strings)
      * [x] `intelDefender` (list of strings)
    * [x] Include `"default"` fallback under each offense
  * [x] WebSocket event handlers:

    * [x] **`connect`**: do nothing immediately
    * [x] **`disconnect`**:

      * [x] If in lobby: remove `sid` from `connections["main"]` and `users`, broadcast `lobbyUpdate`
      * [x] If game started:

        * [x] Mark player as "disconnected"
        * [x] If no submission for this round: auto-submit defaults (`offenseId=""`, `defenseId="underground"`, `targetCodename=""`, `ipToSpend=0`, `bannerMessage=""`), broadcast `playerSubmitted`
    * [x] **`joinLobby`** (payload `{ codename }`):

      * [x] Ensure codename is unique (generate one if empty or taken)
      * [x] Create `users[sid] = { codename, status="active", ip=5, gadgets=["springAnvil","jetpackSkates"], intel=[] }`
      * [x] Add `sid` to `connections["main"]`
      * [x] Emit to `sid`: `lobbyJoined` with `{ yourCodename, allPlayers:[ {codename,status,ip}… ], roundTimer:90, maxPlayers:6 }`
      * [x] Broadcast `lobbyUpdate` with updated `{ allPlayers }`
    * [x] **`startGame`** (host only):

      * [x] Verify `sid` is host (first joined) and ≥2 players in lobby
      * [x] Initialize `current_turn["main"] = { round:1, submissions:{} }`
      * [x] Initialize `assets` with all five Strategic Assets set to `null`
      * [x] Emit `gameStarted` to all with:

        * [x] `gameConfig:{ initialIP:5, roundTimer:90, maxPlayers:6 }`
        * [x] `currentPlayers:[ { codename,status,ip,gadgets,intel }… ]`
    * [x] **`submitAction`** (payload `{ offenseId, defenseId, targetCodename, ipToSpend, bannerMessage }`):

      * [x] If player's status ∈ {"captured","eliminated"}, ignore
      * [x] Clamp `ipToSpend` ≤ player's current IP; deduct from `users[sid]["ip"]`
      * [x] Store in `current_turn["main"]["submissions"][codename]`
      * [x] Emit `playerSubmitted` to all with `{ codename }`
      * [x] If all active players have submitted, invoke Turn Resolution
    * [x] **`requestGameState`**:

      * [x] Look up `sid` in `users`; compile snapshot:

        * [x] `{ round, players:[ { codename,status,ip,gadgets,intel }… ] }`
      * [x] Emit `gameStateSnapshot` back to that `sid`
  * [x] **Turn Resolution Logic** (internal):

    1. [x] **Timer Expiry**: auto-submit defaults for any active players missing submission
    2. [x] **Banner Phase**:

       * [x] If any submission has `defenseId="informationWarfare"`:

         * [x] Emit custom `"showBanner"` event with `{ broadcasterCodename, bannerMessage }`
         * [x] Wait up to 10 sec for `"bannerDecision"` from each player who targeted the broadcaster
         * [x] Adjust each affected player's `targetCodename` or apply "–1 penalty" or mark offense "wasted" as documented
    3. [x] **Apply Offense vs. Defense**:

       * [x] For each submission `s` with `offenseId != ""`:

         * [x] Identify offender and target objects
         * [x] Determine `defenseId` from target's submission (or `"default"` if missing)
         * [x] Look up `interaction_matrix[offenseId][defenseId]` (or fallback to `"default"`)
         * [x] If offender had "–1 penalty," enforce penalty on success probability
         * [x] Apply outcome:

           * [x] `offender["ip"] += outcome.ipChangeOffender`
           * [x] `target["ip"]  += outcome.ipChangeDefender`
           * [x] `offender["status"] = outcome.newStatusOffender`
           * [x] `target["status"]   = outcome.newStatusDefender`
           * [x] Append `intelOffender` to `offender["intel"]`
           * [x] Append `intelDefender` to `target["intel"]`
       * [x] For each submission with `offenseId == ""` (Safe Turn):

         * [x] Award that player `+1 IP`
       * [x] If multiple attackers target the same defender, process in descending IP order, then lexicographic codename
    4. [x] **Process Strategic Asset Captures** (for "Network Attack" or "Alliance Operation" offenses)

       * [x] Update `assets[assetName] = offenderCodename` and grant IP yield
    5. [x] **Compile `turnResult`**:

       * [x] Build payload:

         * [x] `{ round:current_round, results:[ { codename, ipDelta, newIP, newStatus, intelGained }… ] }`
       * [x] Emit `turnResult` to all
    6. [x] **Post-Resolution Updates**:

       * [x] Increment `current_turn["main"]["round"]`
       * [x] Clear `current_turn["main"]["submissions"]`
       * [x] Deduct gadget upkeep IP (players pay 1 IP per gadget needing recharge; if insufficient IP, gadget is removed)
       * [x] Award passive IP yields from Strategic Assets
       * [x] Decrement rounds remaining on each Non-Aggression Pact; break expired pacts
       * [x] Convert any Captured players who have skipped one turn into Burned status
    7. [x] **Check Victory Conditions**:

       * [x] **Last Spy Standing**: If exactly one player's status ∉ {"captured","eliminated"}, declare them winner
       * [x] **Intelligence Supremacy**: If any player has ≥3 Intel Cards about every other Active agent, declare winner
       * [x] **Network Control**: If any player controls ≥3 Strategic Assets, declare winner
       * [x] **Mission Completion**: If any player's Master Plan conditions are satisfied, declare winner
       * [x] **Alliance Victory**: If two allied players share an active joint objective and both have met requirements, they become joint winners → trigger Final Showdown

         * [x] Both allied players `ip += 3`
         * [x] Both choose Assassination or Sabotage (no defense)
         * [x] Resolve both attacks simultaneously (compare success or IP on tie)
       * [x] If any condition met, emit `gameOver` with `{ winners:[…], condition:"<string>" }` and halt rounds
  * [x] **Run Server**:

    * [x] In `if __name__ == "__main__":`, start Flask-SocketIO on `host="0.0.0.0", port=5000`, `debug=False`

* [x] **Requirements (`requirements.txt`)**

  * [x] Add exactly:

    ```
    Flask==2.2.5
    Flask-SocketIO==5.3.4
    eventlet==0.33.0
    ```

* [x] **Tests (`tests/`)**

  * [x] Create `tests/test_interaction_matrix.py`

    * [x] Test known offense/defense pairings:

      * [x] "Assassination" vs "Safe House": confirm failure, attacker loses 1 IP, defender gains 1 IP, attacker → Exposed, defender stays Active, intel lists match
      * [x] "Assassination" vs "Mobile Operations": confirm success, attacker gains 2 IP, defender loses 2 IP, defender → Compromised, intel lists match
      * [x] "Surveillance" vs "Counter-Surveillance": confirm surveillance fails, attacker loses 1 IP, defender gains 2 IP, defender draws intel revealing attacker's identity
      * [x] Offense vs nonexistent defense: returns `"default"` outcome
    * [x] Test missing offense key: returns generic failure outcome (attacker loses IP & becomes Exposed; defender gains IP; no intel)
  * [x] Create `tests/test_action_resolver.py`

    * [x] Test single-player Safe Turn: no offense, `defenseId="underground"` → player gains 1 IP
    * [x] Test two-player Assassination vs Safe House:

      * [x] Player A: `offenseId="assassination"`, target=B, `ipToSpend=0`
      * [x] Player B: `offenseId=""`, `defenseId="safeHouse"`, `ipToSpend=0`
      * [x] Confirm A loses 1 IP, A → Exposed; B gains 1 IP, stays Active
    * [x] Test three players attacking one target:

      * [x] Players A & B target C, C chooses `safeHouse`
      * [x] IPs: A=6, B=5, C starts at 5
      * [x] Confirm resolution order (A then B) and final IP/status for A, B, and C
    * [x] Test failed Infiltration vs Sweep & Clear:

      * [x] Player A: `offenseId="infiltration"`, target=B
      * [x] Player B: `defenseId="sweepAndClear"`, `ipToSpend=0`
      * [x] Confirm A loses 1 IP, A → Exposed; B gains 2 IP, draws intel
  * [x] Create `tests/test_game_loop.py`

    * [x] Test IP economy over multiple rounds:

      * [x] Two players both choose Safe Turn (`offenseId=""`, `defenseId="underground"`) for 3 rounds
      * [x] Confirm each gains +1 IP per round (total +3)
    * [x] Test Compromise chain:

      * [x] Player A fails an assassination vs B's `bodyguardDetail`, A → Compromised
      * [x] Next round, confirm A cannot choose `defenseId="falseIdentity"` (reject or clamp)
    * [x] Test victory – Last Spy Standing:

      * [x] 3 players: Round 1, A captures B (B → Captured); Round 2, A captures C
      * [x] Confirm after Round 2, server would emit `gameOver` with A as winner by "Last Spy Standing"
    * [x] Test victory – Network Control:

      * [x] Player A captures Strategic Assets one by one for three consecutive rounds
      * [x] Confirm immediate `gameOver` with `{ winners:["PlayerA"], condition:"Network Control" }`
  * [x] Create `tests/test_utils.py`

    * [x] Test random weighted choice helper: over many iterations, confirm distribution matches weights (±5%)
    * [x] Test IP clamping helper: input 25, max=20 → output 20; input −15, min=−10 → output −10; input 5 → output 5
  * [x] Create `tests/test_load_stress.py`

    * [x] Test maximum player capacity (6 concurrent players)
    * [x] Test 7th player rejection
    * [x] Test long-duration session stability
    * [x] Test network interruption recovery
    * [x] Test memory leak detection

* [x] **Scripts (`scripts/`)**

  * [x] Create `scripts/build_assets.sh`

    * [x] Optionally optimize PNGs under `assets/images/` using `optipng` or `pngquant` (skip if unavailable)
    * [x] Ensure `static/audio/sfx/` and `static/audio/music/` exist; create if needed
    * [x] Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`
    * [x] Copy `assets/audio/music/*.mp3` → `static/audio/music/`
    * [x] Ensure `static/fonts/` exists; create if needed
    * [x] Copy `assets/fonts/*.ttf` → `static/fonts/`
    * [x] Ensure `static/images/UI/`, `static/images/board_tiles/`, `static/images/gadgets/` exist; create if needed
    * [x] Copy `assets/images/UI/*.png` → `static/images/UI/`
    * [x] Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`
    * [x] Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`
    * [x] Print "Assets successfully built and copied to static/"
    * [x] Make script executable with `chmod +x build_assets.sh`
  * [x] Create `scripts/generate_intel_deck.py`

    * [x] Attempt to load `assets/data/intel_definitions.json`; if missing, define default list in memory
    * [x] Default definitions include `id`, `type`, `uses`, `description`, `copies` (default 10)
    * [x] Build deck by replicating each definition `copies` times, then shuffle
    * [x] Ensure `static/data/` exists; create if needed
    * [x] Write shuffled deck to `static/data/intel_deck.json` (each object: `id`, `type`, `usesLeft`, `description`)
    * [x] (Optional) Generate `static/data/intel_deck.pdf` via a PDF library:

      * [x] One card per page, large `id` in AcmeCartoon 24 pt, description in 14 pt
    * [x] Confirm `static/data/intel_deck.json` (and optional PDF) exist
  * [x] Create `scripts/run_stress_tests.py`

    * [x] Comprehensive load and stress testing automation
    * [x] Maximum player capacity testing
    * [x] Long-duration session stability testing  
    * [x] Network interruption recovery testing
    * [x] Memory leak detection and monitoring
    * [x] Automated test report generation with JSON output
    * [x] System resource monitoring and performance analysis

* [x] **.gitignore**

  * [x] Add entries:

    ```
    # Python
    venv/
    __pycache__/
    *.pyc

    # Flask logs or DB files
    *.log

    # Node
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

* [x] **2-Player vs 6-Player Adjustments**

  * [x] Lobby allows 2–6 players; display "(2–6 players)" in lobby UI
  * [x] If 2 players:

    * [x] Set Planning timer to 60 sec instead of 90 sec
    * [x] Disable alliance-related offenses/defenses:

      * [x] Offenses removed: Alliance Disruption, False Flag, Network Attack on other players' assets
      * [x] Defenses removed: Alliance Building, Honeypot Operations
    * [x] Starting IP = 7 each (instead of 5)
    * [x] Each starts with two random starting gadgets (e.g., Spring-Loaded Anvil & Jetpack Skates)
    * [x] Victory conditions limited to Last Spy Standing and Intelligence Supremacy
  * [x] If 6 players:

    * [x] Planning timer = 90 sec
    * [x] All 11 offenses and 12 defenses are available
    * [x] Starting IP = 5 each
    * [x] Each starts with two random basic gadgets chosen from \[Spring-Loaded Anvil, Jetpack Skates, Robo-Duck, Bug Detector]
    * [x] All 5 victory paths enabled (including Alliance Victory)

* [x] **Mobile-First Design Checklist**

  * [x] Responsive UI:

    * [x] Use `%` or `rem` for widths/heights
    * [x] Buttons/inputs fill \~80% width with ≥0.5 rem padding
    * [x] HUD is a flex container with `overflow-x: auto` and no wrap
  * [x] Touch-Friendly Elements:

    * [x] All clickable items ≥44×44 px
    * [x] Avoid hover states; rely exclusively on taps
  * [x] Font Size & Legibility:

    * [x] Main text ≈ 1 rem (16 px)
    * [x] Headings/buttons ≈ 1.2–1.5 rem
    * [x] HUD codename/IP ≈ 0.9 rem bold
  * [x] Autoplay Restrictions:

    * [x] Audio must be initiated by user interaction (e.g., on "Start Game" tap)
  * [x] Performance:

    * [x] Keep SFX ≤300 KB, loops ≤1 MB
    * [x] Icon PNGs ≤100 KB
    * [x] Prefer CSS keyframes over heavy GIFs; if using GIFs, keep ≤50 KB, ≤15 frames
  * [x] Orientation:

    * [x] Test in portrait and landscape
    * [x] In portrait, Planning UI stacks; HUD scrolls horizontally if needed
    * [x] In landscape, HUD may shrink to a vertical bar or remain at top
  * [x] Touch Events:

    * [x] Use only `click` event listeners
    * [x] For tooltips on gadget icons, use "long-press" or tap toggles, not hover

* [x] **Playtester Checklist & Final Validation**

  * [x] **Lobby Flow**

    * [x] ≥2 devices connect to `http://<host_ip>:5000`
    * [x] Each enters a unique codename and clicks "Join Lobby"
    * [x] Lobby list updates on all devices (codename, status=Active, IP=5 or 7 for 2-player)
    * [x] When ≥2 players are in lobby, "Start Game" button on host is enabled
    * [x] Host clicks "Start Game" and all devices switch to game screen
  * [x] **Gameplay Flow (Round 1)**

    * [x] HUD shows each player's codename, IP, status dot (green Active), and starting gadget icons
    * [x] Planning Phase countdown starts (90 sec or 60 sec for 2-player)
    * [x] `#select-offense` lists correct offense options (omit alliance ones when 2 players)
    * [x] `#select-defense` lists correct defense options (omit alliance ones when 2 players)
    * [x] `#select-target` lists valid targets (exclude self, Captured, Eliminated)
    * [x] `#input-ip` clamps between 0 and current IP
    * [x] If "Information Warfare" is selected, `#input-banner` appears and `#input-ip` sets to 2
    * [x] Clicking "Confirm Choices" disables Planning inputs and shows "Action Submitted"
    * [x] When server emits `playerSubmitted`, HUD shows a checkmark next to that codename
    * [x] Once all players have submitted (or timer expires), server resolves without waiting full time
  * [x] **Resolution Phase**

    * [x] Planning UI hides, Resolution UI (`#resolution`) shows
    * [x] `#resolution-content` lists lines like:

      * "AgentX → IP Δ: +2 (now Y), Status: Active, Intel: ['…']"
    * [x] If an assassination landed, `piano_launch.mp3` plays; if an anvil bounced, `anvil_drop.mp3` plays; if explosion, `explosion_sizzle.mp3` plays
    * [x] After \~1 sec, `#btn-continue` appears
  * [x] **Continue to Next Round**

    * [x] Tapping `#btn-continue` hides Resolution UI, resets Planning UI fields (offense="", defense="", target="", IP=0, banner hidden)
    * [x] Server's next Planning Phase begins automatically on all clients
  * [x] **Biplane Banner Tests**

    * [x] Player selects "Information Warfare", types a ≤25-char message, spends 2 IP
    * [x] On resolution, banner animation appears on all clients, dragging the text
    * [x] Each player who targeted the bannerer sees "Believe Banner" vs. "Ignore Banner" with 10 sec countdown
    * [x] If "Believe" and banner genuine, offense reroutes; if "Ignore" and genuine, apply –1 penalty; if "Believe" but bluff, offense wasted and broadcaster +1 IP; if "Ignore" but bluff, nothing changes
  * [x] **State Updates**

    * [x] After `turnResult`, HUD updates each player's IP and changes status dot color (green→yellow=Compromised→orange=Burned→red=Captured→black=Eliminated)
    * [x] If a player is Captured, their mini-panel shows a distinct icon or is grayed out
    * [x] When a player gains an Intel Card, a pop-up or dialog appears showing the card name, and it's appended to their local intel list
  * [x] **Victory Scenarios**

    * [x] **Network Control**: Simulate a player capturing any three assets; confirm server emits `gameOver` with condition "Network Control" and correct winner
    * [x] **Mission Completion**: Simulate a player fulfilling a Master Plan (e.g., "Expose All Agents"); confirm `gameOver` with condition "Mission Completion"
    * [x] **Last Spy Standing**: In a 2-player match, one eliminates the other; confirm `gameOver` with "Last Spy Standing"
    * [x] **Intelligence Supremacy**: Simulate a player collecting a full dossier on all others; confirm `gameOver` with "Intelligence Supremacy"
    * [x] **Alliance Victory**: In a 6-player match, two allies fulfill a joint objective; confirm joint winners, then final showdown logic (both +3 IP, choose Assassination or Sabotage, resolve, rank 1st/2nd)
  * [x] **Reconnect Handling**

    * [x] During Planning Phase, disable Wi-Fi on one device → client disconnects
    * [x] Re-enable Wi-Fi within the 90 sec window → client reconnects, emits `requestGameState`, receives `gameStateSnapshot`, UI rebuilds with remaining timer
    * [x] If device fails to reconnect before timer expires, server auto-submits defaults for them
  * [x] **Edge Cases**

    * [x] If a player never clicks "Confirm," server auto-submits defaults at timer 0
    * [x] If multiple players target same defender, confirm correct resolution order (highest IP first) and sequential updates
    * [x] If offense/defense combination is missing in the Interaction Matrix, confirm fallback to `"default"`
    * [x] If a player attempts to spend more IP than available, client-side clamps `#input-ip`, server-side clamps again
  * [x] **Mobile Testing**

    * [x] Test on iOS Safari and Android Chrome:

      * [x] Dropdowns open native pickers
      * [x] Buttons are ≥44×44 px and responsive
      * [x] No text or UI clipped
      * [x] Portrait: Planning UI stacks, HUD scrolls horizontally
      * [x] Landscape: HUD displays properly (either smaller vertical bar or at top)
  * [x] **Code-Free Artifact Check**

    * [x] Verify that no code snippets appear in any `docs/*.md` files; they are all plain-English descriptions
    * [x] Confirm every asset listed in Asset Preparation exists under `assets/`
    * [x] Run `scripts/build_assets.sh` and confirm all assets copy into `static/` correctly

* [x] **Complete Folder & File Checklist**

  * [x] **JamesBland/**

    * [x] `README.md`
    * [x] `LICENSE`
    * [x] **docs/**

      * [x] `game_design.md`
      * [x] `protocol_spec.md`
      * [x] `art_style_guide.md`
      * [x] `network_topology.md`
    * [x] **assets/**

      * [x] **audio/**

        * [x] **sfx/**

          * [x] `anvil_drop.mp3`
          * [x] `piano_launch.mp3`
          * [x] `explosion_sizzle.mp3`
        * [x] **music/**

          * [x] `suspense_loop.mp3`
          * [x] `victory_fanfare.mp3`
      * [x] **images/**

        * [x] **UI/**

          * [x] `button_play.png`
          * [x] `button_settings.png`
          * [x] `panel_background.png`
        * [x] **board\_tiles/**

          * [x] `safe_house_icon.png`
          * [x] `anvil_crate.png`
          * [x] `spy_marker_default.png`
        * [x] **gadgets/**

          * [x] `spring_anvil.png`
          * [x] `jetpack_skates.png`
          * [x] `robo_duck.png`
          * [x] `bug_detector.png`
      * [x] **fonts/**

        * [x] `acme_cartoon.ttf`
        * [x] `monospace_console.ttf`
      * [x] (Optional) **data/** for Intel definitions
    * [x] **static/**

      * [x] **audio/**

        * [x] **sfx/** (copied from `assets/audio/sfx/`)

          * [x] `anvil_drop.mp3`
          * [x] `piano_launch.mp3`
          * [x] `explosion_sizzle.mp3`
        * [x] **music/** (copied from `assets/audio/music/`)

          * [x] `suspense_loop.mp3`
          * [x] `victory_fanfare.mp3`
      * [x] **css/**

        * [x] `style.css`
      * [x] **fonts/**

        * [x] `acme_cartoon.ttf`
        * [x] `monospace_console.ttf`
      * [x] **images/**

        * [x] **UI/**

          * [x] `button_play.png`
          * [x] `button_settings.png`
          * [x] `panel_background.png`
        * [x] **board\_tiles/**

          * [x] `safe_house_icon.png`
          * [x] `anvil_crate.png`
          * [x] `spy_marker_default.png`
        * [x] **gadgets/**

          * [x] `spring_anvil.png`
          * [x] `jetpack_skates.png`
          * [x] `robo_duck.png`
          * [x] `bug_detector.png`
      * [x] **js/**

        * [x] `app.js`
      * [x] **data/** (created by `generate_intel_deck.py`)

        * [x] `intel_deck.json`
        * [x] (Optional) `intel_deck.pdf`
    * [x] **templates/**

      * [x] `index.html`
    * [x] `server.py`
    * [x] `requirements.txt`
    * [x] **tests/**

      * [x] `test_interaction_matrix.py`
      * [x] `test_action_resolver.py`
      * [x] `test_game_loop.py`
      * [x] `test_utils.py`
      * [x] `test_load_stress.py`
    * [x] **scripts/**

      * [x] `build_assets.sh`
      * [x] `generate_intel_deck.py`
      * [x] `run_stress_tests.py`
    * [x] `.gitignore`
