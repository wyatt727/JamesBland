* [ ] **Project Root Setup**

  * [ ] Create folder `JamesBland/`
  * [ ] Inside `JamesBland/`, create:

    * [ ] `README.md`
    * [ ] `LICENSE`
    * [ ] Folder `docs/`
    * [ ] Folder `assets/`
    * [ ] Folder `static/`
    * [ ] Folder `templates/`
    * [ ] File `server.py`
    * [ ] File `requirements.txt`
    * [ ] Folder `tests/`
    * [ ] Folder `scripts/`
    * [ ] File `.gitignore`

* [ ] **README.md**

  * [ ] Write **Brief Description** of the game and tech stack
  * [ ] List **Prerequisites** (Python 3.7+ and modern browser on same Wi-Fi)
  * [ ] Outline **Installation Steps**

    * [ ] “Clone or download repository”
    * [ ] “Create and activate Python venv”
    * [ ] “Install dependencies from `requirements.txt`”
    * [ ] “Run `python server.py`”
    * [ ] “On each device, open `http://<HOST_IP>:5000`”
  * [ ] Provide **Folder Structure Overview** (names and purposes)
  * [ ] Summarize **How to Play**
  * [ ] Specify **License & Contributing Notes**

* [ ] **LICENSE**

  * [ ] Paste MIT text or “All Rights Reserved” notice

* [ ] **Documentation (`docs/`)**

  * [ ] Create `docs/game_design.md`

    * [ ] Introduction & Core Concept
    * [ ] Turn Structure: Planning → Resolution → Adaptation
    * [ ] Detailed list of **11 Offenses**, each with:

      * [ ] Name, Base Success, Cost in IP, Legal Targets
      * [ ] On-Success Effects
      * [ ] On-Failure Effects
    * [ ] Detailed list of **12 Defenses**, each with:

      * [ ] Name, Cost in IP, Offenses Countered
      * [ ] On-Block Effects and Secondary Notes
    * [ ] Interaction Matrix Overview + Example Excerpt
    * [ ] Resource Management & Equipment:

      * [ ] IP Economy (how IP is earned and spent, floor/ceiling rules)
      * [ ] Gadget List (10–12 gadgets with Name, Cost, Effect, Cooldown)
      * [ ] Statuses & Transitions (Active, Compromised, Burned, Captured, Eliminated)
      * [ ] Strategic Assets (names, control cost, yield)
      * [ ] Alliances & Betrayal mechanics (Non-Aggression Pact, Coordinated Operation)
    * [ ] Master Plans (5–10 examples: Name, Description, Reward/Win, Conditions)
    * [ ] Victory Conditions & Endgame (5 types, detailed descriptions)
    * [ ] Mode Variants (2-Player vs. 6-Player rules adjustments)
    * [ ] Sample Round Transcript (4-player example)
  * [ ] Create `docs/protocol_spec.md`

    * [ ] Overview of Flask + Flask-SocketIO setup (port 5000, CORS)
    * [ ] Event Definitions:

      * [ ] **Client → Server**: `joinLobby`, `startGame`, `submitAction`, `requestGameState`
      * [ ] **Server → Client**: `lobbyJoined`, `lobbyUpdate`, `gameStarted`, `playerSubmitted`, `turnResult`, `gameStateSnapshot`, `gameOver`
    * [ ] Sequence Flows:

      * [ ] Lobby Join Flow
      * [ ] Game Start Flow
      * [ ] Single Round Flow
      * [ ] Reconnect Flow
    * [ ] Error Handling Rules (invalid JSON, default submissions, host disconnect)
    * [ ] Versioning Notes (optional `"protocolVersion"` field)
    * [ ] Optional Future Automatic Discovery Sketch (UDP broadcast)
  * [ ] Create `docs/art_style_guide.md`

    * [ ] Overall ACME Cartoon Aesthetic description
    * [ ] Color Palette (Primary: Red #E53935, Yellow #FFEB3B, Blue #1E88E5; Secondary: Black, White, Light Gray)
    * [ ] Fonts:

      * [ ] `acme_cartoon.ttf` for headings/buttons
      * [ ] `monospace_console.ttf` for logs/chat
    * [ ] UI Components:

      * [ ] Buttons (size, corners, outlines, text)
      * [ ] Panels (background, borders, shadows)
      * [ ] Dropdowns & Inputs (styles, padding)
    * [ ] Icons & Board Tiles:

      * [ ] Tile Size: 128×128 px, transparent background, thick black outlines
      * [ ] Board Tile Icons: Safe House, Anvil Crate, Spy Marker
      * [ ] Gadget Icons: Spring-Loaded Anvil, Jetpack Skates, Robo-Duck, Bug Detector, Mirror Drone Squadron, plus 4–6 more
      * [ ] Status Icons: Active (green), Compromised (yellow), Burned (orange), Captured (red), Eliminated (black) (32×32 px)
    * [ ] Animations:

      * [ ] Piano Drop (64×64 px GIF or CSS keyframes, \~1 sec, 12 fps)
      * [ ] Anvil Bounce (64×64 px, \~0.8 sec, 10 fps)
      * [ ] Custard Pie Splash (64×64 px, 8–10 frames)
      * [ ] Explosion (64×64 px, 10 frames at 12 fps)
      * [ ] “2× scale” guideline: Create assets at 128×128 and scale down to 64×64
    * [ ] HUD Layout:

      * [ ] Top bar (\~10% viewport height, dark gray #333333)
      * [ ] Mini-panel for each player: Avatar Circle, Codename, IP Count (brain icon + number), Status Dot, Gadget Icons (up to 3)
      * [ ] Horizontal scroll if >6 players (`overflow-x: auto; white-space: nowrap;`)
      * [ ] Mini-panel width ≥80 px
    * [ ] Touch & Mobile Considerations:

      * [ ] Tap Targets ≥44×44 px
      * [ ] Font Sizes: Main \~1 rem, Headings/Buttons \~1.2–1.5 rem, HUD Codename/IP \~0.9 rem bold
      * [ ] Spacing: ≥8 px margins/padding between elements
      * [ ] Portrait stacking: Offense → Defense → Target → IP Slider → Confirm
      * [ ] Use media queries (`@media (max-width: 480px) { … }`)
    * [ ] Export & File Formats:

      * [ ] PNG 24-bit for icons/UI (transparency)
      * [ ] MP3 for audio (SFX ≤300 KB; loops ≤1 MB)
      * [ ] TTF and WOFF for fonts
      * [ ] GIF optional for animations but prefer CSS keyframes
  * [ ] Create `docs/network_topology.md`

    * [ ] LAN Assumptions (same subnet `192.168.1.x/24`, host IP known)
    * [ ] Manual Join Flow:

      * [ ] Host runs `python server.py` → “Server listening on 0.0.0.0:5000 (LAN IP: 192.168.1.42)”
      * [ ] Clients open browser to `http://192.168.1.42:5000`
      * [ ] ASCII/diagram showing Host PC and three devices (Phone, Tablet, Laptop) connecting
    * [ ] WebSocket Topology:

      * [ ] Single central server; no P2P
      * [ ] Each client opens one WebSocket to server
      * [ ] All real-time events use that WebSocket
      * [ ] On disconnect, server auto-submits defaults; on reconnect, server sends `gameStateSnapshot`
    * [ ] Failure Modes & Recovery:

      * [ ] Client Disconnect: auto-submit defaults if not reconnected before timer expires; reconnect triggers `requestGameState` → `gameStateSnapshot`
      * [ ] Server/Host Disconnect: clients show “Host disconnected—please restart”
      * [ ] No automatic host failover in v1
    * [ ] (Optional) Future Automatic Discovery Sketch: UDP broadcast “GameAvailable” on port 9999, clients listen and populate “Join Game” dropdown

* [ ] **Asset Preparation (`assets/`)**

  * [ ] **Audio SFX** (`assets/audio/sfx/`)

    * [ ] Obtain or record `anvil_drop.mp3` (≤200 KB, cartoon anvil thud)
    * [ ] Obtain or record `piano_launch.mp3` (≤300 KB, whoosh + descending piano gliss)
    * [ ] Obtain or record `explosion_sizzle.mp3` (≤250 KB, comedic boom)
  * [ ] **Music Loops** (`assets/audio/music/`)

    * [ ] Obtain or create `suspense_loop.mp3` (30–60 sec loop, ≤1 MB)
    * [ ] Obtain or create `victory_fanfare.mp3` (10–15 sec fanfare, ≤500 KB)
  * [ ] **Images – UI** (`assets/images/UI/`)

    * [ ] Design `button_play.png` (256×64 px, red fill #E53935, white “PLAY” uppercase text with black outline, rounded corners 8 px, thick black border)
    * [ ] Design `button_settings.png` (256×64 px, yellow fill #FFEB3B, black gear icon left, white “SETTINGS” uppercase text with black outline, rounded corners 8 px)
    * [ ] Design `panel_background.png` (1024×768 px tileable, light gray #F2F2F2 blueprint grid with thin white/light-blue lines)
  * [ ] **Images – Board Tiles** (`assets/images/board_tiles/`)

    * [ ] Design `safe_house_icon.png` (128×128 px, pastel blue fortress on cartoon white springs, thick black outline)
    * [ ] Design `anvil_crate.png` (128×128 px, brown wooden crate with silver anvil popping out, thick black outline)
    * [ ] Design `spy_marker_default.png` (64×64 px, black fedora silhouette with large white googly eyes, thick black outline)
  * [ ] **Images – Gadgets** (`assets/images/gadgets/`)

    * [ ] Design `spring_anvil.png` (128×128 px, silver anvil on big coiled yellow spring, thick black outline)
    * [ ] Design `jetpack_skates.png` (128×128 px, bright red roller skates with small rocket thrusters and stylized orange flame, thick black outline)
    * [ ] Design `robo_duck.png` (128×128 px, cartoon yellow duck wearing a small metal helmet, big googly eyes, thick black outline)
    * [ ] Design `bug_detector.png` (128×128 px, handheld radar device with blinking red LED, gray metallic body, thick black outline)
    * [ ] (Optional) Add 1–2 more gadget icons as needed
  * [ ] **Fonts** (`assets/fonts/`)

    * [ ] Obtain or create `acme_cartoon.ttf` (bold quirky cartoon display font)
    * [ ] Obtain or create `monospace_console.ttf` (classic monospaced font for logs/chat)

* [ ] **Static Files (`static/`)**

  * [ ] **Audio**

    * [ ] Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`
    * [ ] Copy `assets/audio/music/*.mp3` → `static/audio/music/`
  * [ ] **Fonts**

    * [ ] Copy `assets/fonts/acme_cartoon.ttf` → `static/fonts/`
    * [ ] Copy `assets/fonts/monospace_console.ttf` → `static/fonts/`
  * [ ] **Images**

    * [ ] Copy `assets/images/UI/*.png` → `static/images/UI/`
    * [ ] Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`
    * [ ] Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`
  * [ ] **CSS**

    * [ ] Create `static/css/style.css` with:

      * [ ] Mobile-first flex/grid layout
      * [ ] HUD styling (scrollable flex, mini-panels with `.hud-player`, status dot classes)
      * [ ] Planning & Resolution panels (`.planning-panel`, `.resolution-panel` styles)
      * [ ] Inputs/dropdowns/buttons styles (font sizes, padding, borders, radius)
      * [ ] Font imports (`@font-face` for AcmeCartoon and MonoConsole)
      * [ ] Media queries for screens ≤480 px
  * [ ] **JavaScript**

    * [ ] Create `static/js/app.js` to implement client-side logic in plain JS:

      * [ ] WebSocket connection (`io('<SERVER_URL>')`, handle `connect`/`disconnect`)
      * [ ] Lobby logic (`joinLobby`, `lobbyJoined`, `lobbyUpdate`, enable “Start Game” when ≥2 players)
      * [ ] Game logic:

        * [ ] Handle `gameStarted` → build HUD (`#hud`) and Planning UI (`#select-offense`, `#select-defense`, `#select-target`, `#input-ip`, `#input-banner`, `#btn-confirm`, `#timerDisplay`, `#planning-status`)
        * [ ] Start Planning Phase timer (90 sec or 60 sec for 2-player)
        * [ ] On “Confirm Choices” → disable inputs, show “Action Submitted,” emit `submitAction`
        * [ ] Listen for `playerSubmitted` → show checkmark in HUD
      * [ ] Biplane Banner logic:

        * [ ] If defense = “informationWarfare,” show `#input-banner`, set `ipToSpend = 2`
        * [ ] Listen for custom `"showBanner"` event → play banner animation, prompt “Believe” or “Ignore” for affected players
        * [ ] Emit `"bannerDecision"`
      * [ ] Turn Resolution:

        * [ ] Listen for `turnResult` → hide Planning UI, show `#resolution`, append lines to `#resolution-content`, play SFX (`anvil_drop.mp3`, `piano_launch.mp3`, `explosion_sizzle.mp3`), show `#btn-continue` after \~1 sec
      * [ ] On `#btn-continue` click → hide `#resolution`, reset Planning UI fields, wait for next round
      * [ ] Reconnect handling:

        * [ ] On `disconnect`, show “Reconnecting…” overlay
        * [ ] On `connect`, emit `requestGameState`
        * [ ] On `gameStateSnapshot`, rebuild HUD and UI, restart timer if applicable
      * [ ] Victory handling:

        * [ ] Listen for `gameOver` → hide all UIs, show full-screen “Winner(s): … by …” modal, play `victory_fanfare.mp3`, offer “Return to Lobby” or “Restart”
      * [ ] Asset preloading (optional): load `Audio` objects and call `.load()`
      * [ ] Mobile-first: use only `click` events, ensure all interactive elements ≥44×44 px, audio playback triggered by user

* [ ] **HTML Template (`templates/index.html`)**

  * [ ] `<head>`

    * [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
    * [ ] `<link rel="stylesheet" href="/static/css/style.css">`
    * [ ] `<script src="https://cdn.socket.io/4.5.1/socket.io.min.js"></script>`
    * [ ] `<script defer src="/static/js/app.js"></script>`
    * [ ] `<title>James Bland: ACME Edition</title>`
  * [ ] `<body>`

    * [ ] **Lobby Overlay** (`<div id="overlay-lobby">`)

      * [ ] `<h1>James Bland: ACME Edition</h1>`
      * [ ] `<input type="text" id="input-codename" placeholder="Your Codename" maxlength="16">`
      * [ ] `<button id="btn-join">Join Lobby</button>`
      * [ ] `<div id="lobby-status"></div>`
      * [ ] `<div id="player-list-lobby"></div>`
      * [ ] `<button id="btn-start" disabled>Start Game</button>`
      * [ ] Optional help icon or instructions link
    * [ ] **Game Overlay** (`<div id="overlay-game" class="hidden">`)

      * [ ] **HUD** (`<div id="hud"></div>`) containing up to 6 mini-panels with class `hud-player`, each with:

        * [ ] Avatar circle (`<div class="avatar-circle"></div>`)
        * [ ] Codename label (`<div class="codename-label">AgentX</div>`)
        * [ ] Brain icon + `<span class="ip-count">5</span>`
        * [ ] Status dot (`<div class="status-dot status-active"></div>`)
        * [ ] Gadget icons container (`<div class="gadget-icons"></div>`)
      * [ ] **Board Placeholder** (`<div id="board">Board (Placeholder)</div>`)
      * [ ] **Planning Panel** (`<div id="planning" class="planning-panel">`)

        * [ ] “Round: <span id="roundNumber">0</span>”
        * [ ] Offense dropdown: `<select id="select-offense"><option value="">Select Offense</option>…</select>`
        * [ ] Defense dropdown: `<select id="select-defense"><option value="">Select Defense</option>…</select>`
        * [ ] Target dropdown: `<select id="select-target"><option value="">Select Target</option>…</select>`
        * [ ] IP numeric input: `<input type="number" id="input-ip" min="0" value="0">`
        * [ ] Banner text input (hidden initially): `<input type="text" id="input-banner" maxlength="25" placeholder="Banner Message" class="hidden">`
        * [ ] Confirm button: `<button id="btn-confirm" disabled>Confirm Choices</button>`
        * [ ] Timer display: `<div id="planning-timer">Time: <span id="timerDisplay">90</span>s</div>`
        * [ ] Planning status: `<div id="planning-status"></div>`
      * [ ] **Resolution Panel** (`<div id="resolution" class="resolution-panel hidden">`)

        * [ ] `<h2>Resolution</h2>`
        * [ ] `<div id="resolution-content"></div>`
        * [ ] `<button id="btn-continue" class="hidden">Continue to Next Round</button>`

* [ ] **Backend Script (`server.py`)**

  * [ ] Initialize Flask + Flask-SocketIO (`async_mode="eventlet"`, `cors_allowed_origins="*"`)
  * [ ] Maintain in-memory state:

    * [ ] Dictionary `users`: `sid → { codename, status, ip, gadgets, intel }`
    * [ ] Dictionary `connections["main"]`: set of `sid` in lobby/game
    * [ ] Dictionary `current_turn["main"]`: `{ round: int, submissions: { codename → submission } }`
    * [ ] Dictionary `assets`: `{ assetName → codename or null }`
  * [ ] Define Interaction Matrix as nested dict:

    * [ ] Each `offenseId` → `defenseId` → outcome object with:

      * [ ] `offenseSucceeds` (bool)
      * [ ] `ipChangeOffender` (int)
      * [ ] `ipChangeDefender` (int)
      * [ ] `newStatusOffender` (string)
      * [ ] `newStatusDefender` (string)
      * [ ] `intelOffender` (list of strings)
      * [ ] `intelDefender` (list of strings)
    * [ ] Include `"default"` fallback under each offense
  * [ ] WebSocket event handlers:

    * [ ] **`connect`**: do nothing immediately
    * [ ] **`disconnect`**:

      * [ ] If in lobby: remove `sid` from `connections["main"]` and `users`, broadcast `lobbyUpdate`
      * [ ] If game started:

        * [ ] Mark player as “disconnected”
        * [ ] If no submission for this round: auto-submit defaults (`offenseId=""`, `defenseId="underground"`, `targetCodename=""`, `ipToSpend=0`, `bannerMessage=""`), broadcast `playerSubmitted`
    * [ ] **`joinLobby`** (payload `{ codename }`):

      * [ ] Ensure codename is unique (generate one if empty or taken)
      * [ ] Create `users[sid] = { codename, status="active", ip=5, gadgets=["springAnvil","jetpackSkates"], intel=[] }`
      * [ ] Add `sid` to `connections["main"]`
      * [ ] Emit to `sid`: `lobbyJoined` with `{ yourCodename, allPlayers:[ {codename,status,ip}… ], roundTimer:90, maxPlayers:6 }`
      * [ ] Broadcast `lobbyUpdate` with updated `{ allPlayers }`
    * [ ] **`startGame`** (host only):

      * [ ] Verify `sid` is host (first joined) and ≥2 players in lobby
      * [ ] Initialize `current_turn["main"] = { round:1, submissions:{} }`
      * [ ] Initialize `assets` with all five Strategic Assets set to `null`
      * [ ] Emit `gameStarted` to all with:

        * [ ] `gameConfig:{ initialIP:5, roundTimer:90, maxPlayers:6 }`
        * [ ] `currentPlayers:[ { codename,status,ip,gadgets,intel }… ]`
    * [ ] **`submitAction`** (payload `{ offenseId, defenseId, targetCodename, ipToSpend, bannerMessage }`):

      * [ ] If player’s status ∈ {“captured”,“eliminated”}, ignore
      * [ ] Clamp `ipToSpend` ≤ player’s current IP; deduct from `users[sid]["ip"]`
      * [ ] Store in `current_turn["main"]["submissions"][codename]`
      * [ ] Emit `playerSubmitted` to all with `{ codename }`
      * [ ] If all active players have submitted, invoke Turn Resolution
    * [ ] **`requestGameState`**:

      * [ ] Look up `sid` in `users`; compile snapshot:

        * [ ] `{ round, players:[ { codename,status,ip,gadgets,intel }… ] }`
      * [ ] Emit `gameStateSnapshot` back to that `sid`
  * [ ] **Turn Resolution Logic** (internal):

    1. **Timer Expiry**: auto-submit defaults for any active players missing submission
    2. **Banner Phase**:

       * [ ] If any submission has `defenseId="informationWarfare"`:

         * [ ] Emit custom `"showBanner"` event with `{ broadcasterCodename, bannerMessage }`
         * [ ] Wait up to 10 sec for `"bannerDecision"` from each player who targeted the broadcaster
         * [ ] Adjust each affected player’s `targetCodename` or apply “–1 penalty” or mark offense “wasted” as documented
    3. **Apply Offense vs. Defense**:

       * [ ] For each submission `s` with `offenseId != ""`:

         * [ ] Identify offender and target objects
         * [ ] Determine `defenseId` from target’s submission (or `"default"` if missing)
         * [ ] Look up `interaction_matrix[offenseId][defenseId]` (or fallback to `"default"`)
         * [ ] If offender had “–1 penalty,” enforce penalty on success probability
         * [ ] Apply outcome:

           * [ ] `offender["ip"] += outcome.ipChangeOffender`
           * [ ] `target["ip"]  += outcome.ipChangeDefender`
           * [ ] `offender["status"] = outcome.newStatusOffender`
           * [ ] `target["status"]   = outcome.newStatusDefender`
           * [ ] Append `intelOffender` to `offender["intel"]`
           * [ ] Append `intelDefender` to `target["intel"]`
       * [ ] For each submission with `offenseId == ""` (Safe Turn):

         * [ ] Award that player `+1 IP`
       * [ ] If multiple attackers target the same defender, process in descending IP order, then lexicographic codename
    4. **Process Strategic Asset Captures** (for “Network Attack” or “Alliance Operation” offenses)

       * [ ] Update `assets[assetName] = offenderCodename` and grant IP yield
    5. **Compile `turnResult`**:

       * [ ] Build payload:

         * [ ] `{ round:current_round, results:[ { codename, ipDelta, newIP, newStatus, intelGained }… ] }`
       * [ ] Emit `turnResult` to all
    6. **Post-Resolution Updates**:

       * [ ] Increment `current_turn["main"]["round"]`
       * [ ] Clear `current_turn["main"]["submissions"]`
       * [ ] Deduct gadget upkeep IP (players pay 1 IP per gadget needing recharge; if insufficient IP, gadget is removed)
       * [ ] Award passive IP yields from Strategic Assets
       * [ ] Decrement rounds remaining on each Non-Aggression Pact; break expired pacts
       * [ ] Convert any Captured players who have skipped one turn into Burned status
    7. **Check Victory Conditions**:

       * [ ] **Last Spy Standing**: If exactly one player’s status ∉ {“captured”,“eliminated”}, declare them winner
       * [ ] **Intelligence Supremacy**: If any player has ≥3 Intel Cards about every other Active agent, declare winner
       * [ ] **Network Control**: If any player controls ≥3 Strategic Assets, declare winner
       * [ ] **Mission Completion**: If any player’s Master Plan conditions are satisfied, declare winner
       * [ ] **Alliance Victory**: If two allied players share an active joint objective and both have met requirements, they become joint winners → trigger Final Showdown

         * [ ] Both allied players `ip += 3`
         * [ ] Both choose Assassination or Sabotage (no defense)
         * [ ] Resolve both attacks simultaneously (compare success or IP on tie)
       * [ ] If any condition met, emit `gameOver` with `{ winners:[…], condition:"<string>" }` and halt rounds
  * [ ] **Run Server**:

    * [ ] In `if __name__ == "__main__":`, start Flask-SocketIO on `host="0.0.0.0", port=5000`, `debug=False`

* [ ] **Requirements (`requirements.txt`)**

  * [ ] Add exactly:

    ```
    Flask==2.2.5
    Flask-SocketIO==5.3.4
    eventlet==0.33.0
    ```

* [ ] **Tests (`tests/`)**

  * [ ] Create `tests/test_interaction_matrix.py`

    * [ ] Test known offense/defense pairings:

      * [ ] “Assassination” vs “Safe House”: confirm failure, attacker loses 1 IP, defender gains 1 IP, attacker → Exposed, defender stays Active, intel lists match
      * [ ] “Assassination” vs “Mobile Operations”: confirm success, attacker gains 2 IP, defender loses 2 IP, defender → Compromised, intel lists match
      * [ ] “Surveillance” vs “Counter-Surveillance”: confirm surveillance fails, attacker loses 1 IP, defender gains 2 IP, defender draws intel revealing attacker’s identity
      * [ ] Offense vs nonexistent defense: returns `"default"` outcome
    * [ ] Test missing offense key: returns generic failure outcome (attacker loses IP & becomes Exposed; defender gains IP; no intel)
  * [ ] Create `tests/test_action_resolver.py`

    * [ ] Test single-player Safe Turn: no offense, `defenseId="underground"` → player gains 1 IP
    * [ ] Test two-player Assassination vs Safe House:

      * [ ] Player A: `offenseId="assassination"`, target=B, `ipToSpend=0`
      * [ ] Player B: `offenseId=""`, `defenseId="safeHouse"`, `ipToSpend=0`
      * [ ] Confirm A loses 1 IP, A → Exposed; B gains 1 IP, stays Active
    * [ ] Test three players attacking one target:

      * [ ] Players A & B target C, C chooses `safeHouse`
      * [ ] IPs: A=6, B=5, C starts at 5
      * [ ] Confirm resolution order (A then B) and final IP/status for A, B, and C
    * [ ] Test failed Infiltration vs Sweep & Clear:

      * [ ] Player A: `offenseId="infiltration"`, target=B
      * [ ] Player B: `defenseId="sweepAndClear"`, `ipToSpend=0`
      * [ ] Confirm A loses 1 IP, A → Exposed; B gains 2 IP, draws intel
  * [ ] Create `tests/test_game_loop.py`

    * [ ] Test IP economy over multiple rounds:

      * [ ] Two players both choose Safe Turn (`offenseId=""`, `defenseId="underground"`) for 3 rounds
      * [ ] Confirm each gains +1 IP per round (total +3)
    * [ ] Test Compromise chain:

      * [ ] Player A fails an assassination vs B’s `bodyguardDetail`, A → Compromised
      * [ ] Next round, confirm A cannot choose `defenseId="falseIdentity"` (reject or clamp)
    * [ ] Test victory – Last Spy Standing:

      * [ ] 3 players: Round 1, A captures B (B → Captured); Round 2, A captures C
      * [ ] Confirm after Round 2, server would emit `gameOver` with A as winner by “Last Spy Standing”
    * [ ] Test victory – Network Control:

      * [ ] Player A captures Strategic Assets one by one for three consecutive rounds
      * [ ] Confirm immediate `gameOver` with `{ winners:["PlayerA"], condition:"Network Control" }`
  * [ ] Optionally, create `tests/test_utils.py`

    * [ ] Test random weighted choice helper: over many iterations, confirm distribution matches weights (±5%)
    * [ ] Test IP clamping helper: input 25, max=20 → output 20; input −15, min=−10 → output −10; input 5 → output 5

* [ ] **Scripts (`scripts/`)**

  * [ ] Create `scripts/build_assets.sh`

    * [ ] Optionally optimize PNGs under `assets/images/` using `optipng` or `pngquant` (skip if unavailable)
    * [ ] Ensure `static/audio/sfx/` and `static/audio/music/` exist; create if needed
    * [ ] Copy `assets/audio/sfx/*.mp3` → `static/audio/sfx/`
    * [ ] Copy `assets/audio/music/*.mp3` → `static/audio/music/`
    * [ ] Ensure `static/fonts/` exists; create if needed
    * [ ] Copy `assets/fonts/*.ttf` → `static/fonts/`
    * [ ] Ensure `static/images/UI/`, `static/images/board_tiles/`, `static/images/gadgets/` exist; create if needed
    * [ ] Copy `assets/images/UI/*.png` → `static/images/UI/`
    * [ ] Copy `assets/images/board_tiles/*.png` → `static/images/board_tiles/`
    * [ ] Copy `assets/images/gadgets/*.png` → `static/images/gadgets/`
    * [ ] Print “Assets successfully built and copied to static/”
    * [ ] Make script executable with `chmod +x build_assets.sh`
  * [ ] Create `scripts/generate_intel_deck.py`

    * [ ] Attempt to load `assets/data/intel_definitions.json`; if missing, define default list in memory
    * [ ] Default definitions include `id`, `type`, `uses`, `description`, `copies` (default 10)
    * [ ] Build deck by replicating each definition `copies` times, then shuffle
    * [ ] Ensure `static/data/` exists; create if needed
    * [ ] Write shuffled deck to `static/data/intel_deck.json` (each object: `id`, `type`, `usesLeft`, `description`)
    * [ ] (Optional) Generate `static/data/intel_deck.pdf` via a PDF library:

      * [ ] One card per page, large `id` in AcmeCartoon 24 pt, description in 14 pt
    * [ ] Confirm `static/data/intel_deck.json` (and optional PDF) exist

* [ ] **.gitignore**

  * [ ] Add entries:

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

* [ ] **2-Player vs 6-Player Adjustments**

  * [ ] Lobby allows 2–6 players; display “(2–6 players)” in lobby UI
  * [ ] If 2 players:

    * [ ] Set Planning timer to 60 sec instead of 90 sec
    * [ ] Disable alliance-related offenses/defenses:

      * [ ] Offenses removed: Alliance Disruption, False Flag, Network Attack on other players’ assets
      * [ ] Defenses removed: Alliance Building, Honeypot Operations
    * [ ] Starting IP = 7 each (instead of 5)
    * [ ] Each starts with two random starting gadgets (e.g., Spring-Loaded Anvil & Jetpack Skates)
    * [ ] Victory conditions limited to Last Spy Standing and Intelligence Supremacy
  * [ ] If 6 players:

    * [ ] Planning timer = 90 sec
    * [ ] All 11 offenses and 12 defenses are available
    * [ ] Starting IP = 5 each
    * [ ] Each starts with two random basic gadgets chosen from \[Spring-Loaded Anvil, Jetpack Skates, Robo-Duck, Bug Detector]
    * [ ] All 5 victory paths enabled (including Alliance Victory)

* [ ] **Mobile-First Design Checklist**

  * [ ] Responsive UI:

    * [ ] Use `%` or `rem` for widths/heights
    * [ ] Buttons/inputs fill \~80% width with ≥0.5 rem padding
    * [ ] HUD is a flex container with `overflow-x: auto` and no wrap
  * [ ] Touch-Friendly Elements:

    * [ ] All clickable items ≥44×44 px
    * [ ] Avoid hover states; rely exclusively on taps
  * [ ] Font Size & Legibility:

    * [ ] Main text ≈ 1 rem (16 px)
    * [ ] Headings/buttons ≈ 1.2–1.5 rem
    * [ ] HUD codename/IP ≈ 0.9 rem bold
  * [ ] Autoplay Restrictions:

    * [ ] Audio must be initiated by user interaction (e.g., on “Start Game” tap)
  * [ ] Performance:

    * [ ] Keep SFX ≤300 KB, loops ≤1 MB
    * [ ] Icon PNGs ≤100 KB
    * [ ] Prefer CSS keyframes over heavy GIFs; if using GIFs, keep ≤50 KB, ≤15 frames
  * [ ] Orientation:

    * [ ] Test in portrait and landscape
    * [ ] In portrait, Planning UI stacks; HUD scrolls horizontally if needed
    * [ ] In landscape, HUD may shrink to a vertical bar or remain at top
  * [ ] Touch Events:

    * [ ] Use only `click` event listeners
    * [ ] For tooltips on gadget icons, use “long-press” or tap toggles, not hover

* [ ] **Playtester Checklist & Final Validation**

  * [ ] **Lobby Flow**

    * [ ] ≥2 devices connect to `http://<host_ip>:5000`
    * [ ] Each enters a unique codename and clicks “Join Lobby”
    * [ ] Lobby list updates on all devices (codename, status=Active, IP=5 or 7 for 2-player)
    * [ ] When ≥2 players are in lobby, “Start Game” button on host is enabled
    * [ ] Host clicks “Start Game” and all devices switch to game screen
  * [ ] **Gameplay Flow (Round 1)**

    * [ ] HUD shows each player’s codename, IP, status dot (green Active), and starting gadget icons
    * [ ] Planning Phase countdown starts (90 sec or 60 sec for 2-player)
    * [ ] `#select-offense` lists correct offense options (omit alliance ones when 2 players)
    * [ ] `#select-defense` lists correct defense options (omit alliance ones when 2 players)
    * [ ] `#select-target` lists valid targets (exclude self, Captured, Eliminated)
    * [ ] `#input-ip` clamps between 0 and current IP
    * [ ] If “Information Warfare” is selected, `#input-banner` appears and `#input-ip` sets to 2
    * [ ] Clicking “Confirm Choices” disables Planning inputs and shows “Action Submitted”
    * [ ] When server emits `playerSubmitted`, HUD shows a checkmark next to that codename
    * [ ] Once all players have submitted (or timer expires), server resolves without waiting full time
  * [ ] **Resolution Phase**

    * [ ] Planning UI hides, Resolution UI (`#resolution`) shows
    * [ ] `#resolution-content` lists lines like:

      * “AgentX → IP Δ: +2 (now Y), Status: Active, Intel: \[‘…’]”
    * [ ] If an assassination landed, `piano_launch.mp3` plays; if an anvil bounced, `anvil_drop.mp3` plays; if explosion, `explosion_sizzle.mp3` plays
    * [ ] After \~1 sec, `#btn-continue` appears
  * [ ] **Continue to Next Round**

    * [ ] Tapping `#btn-continue` hides Resolution UI, resets Planning UI fields (offense="", defense="", target="", IP=0, banner hidden)
    * [ ] Server’s next Planning Phase begins automatically on all clients
  * [ ] **Biplane Banner Tests**

    * [ ] Player selects “Information Warfare,” types a ≤25-char message, spends 2 IP
    * [ ] On resolution, banner animation appears on all clients, dragging the text
    * [ ] Each player who targeted the bannerer sees “Believe Banner” vs. “Ignore Banner” with 10 sec countdown
    * [ ] If “Believe” and banner genuine, offense reroutes; if “Ignore” and genuine, apply –1 penalty; if “Believe” but bluff, offense wasted and broadcaster +1 IP; if “Ignore” but bluff, nothing changes
  * [ ] **State Updates**

    * [ ] After `turnResult`, HUD updates each player’s IP and changes status dot color (green→yellow=Compromised→orange=Burned→red=Captured→black=Eliminated)
    * [ ] If a player is Captured, their mini-panel shows a distinct icon or is grayed out
    * [ ] When a player gains an Intel Card, a pop-up or dialog appears showing the card name, and it’s appended to their local intel list
  * [ ] **Victory Scenarios**

    * [ ] **Network Control**: Simulate a player capturing any three assets; confirm server emits `gameOver` with condition “Network Control” and correct winner
    * [ ] **Mission Completion**: Simulate a player fulfilling a Master Plan (e.g., “Expose All Agents”); confirm `gameOver` with condition “Mission Completion”
    * [ ] **Last Spy Standing**: In a 2-player match, one eliminates the other; confirm `gameOver` with “Last Spy Standing”
    * [ ] **Intelligence Supremacy**: Simulate a player collecting a full dossier on all others; confirm `gameOver` with “Intelligence Supremacy”
    * [ ] **Alliance Victory**: In a 6-player match, two allies fulfill a joint objective; confirm joint winners, then final showdown logic (both +3 IP, choose Assassination or Sabotage, resolve, rank 1st/2nd)
  * [ ] **Reconnect Handling**

    * [ ] During Planning Phase, disable Wi-Fi on one device → client disconnects
    * [ ] Re-enable Wi-Fi within the 90 sec window → client reconnects, emits `requestGameState`, receives `gameStateSnapshot`, UI rebuilds with remaining timer
    * [ ] If device fails to reconnect before timer expires, server auto-submits defaults for them
  * [ ] **Edge Cases**

    * [ ] If a player never clicks “Confirm,” server auto-submits defaults at timer 0
    * [ ] If multiple players target same defender, confirm correct resolution order (highest IP first) and sequential updates
    * [ ] If offense/defense combination is missing in the Interaction Matrix, confirm fallback to `"default"`
    * [ ] If a player attempts to spend more IP than available, client-side clamps `#input-ip`, server-side clamps again
  * [ ] **Mobile Testing**

    * [ ] Test on iOS Safari and Android Chrome:

      * [ ] Dropdowns open native pickers
      * [ ] Buttons are ≥44×44 px and responsive
      * [ ] No text or UI clipped
      * [ ] Portrait: Planning UI stacks, HUD scrolls horizontally
      * [ ] Landscape: HUD displays properly (either smaller vertical bar or at top)
  * [ ] **Code-Free Artifact Check**

    * [ ] Verify that no code snippets appear in any `docs/*.md` files; they are all plain-English descriptions
    * [ ] Confirm every asset listed in Asset Preparation exists under `assets/`
    * [ ] Run `scripts/build_assets.sh` and confirm all assets copy into `static/` correctly

* [ ] **Complete Folder & File Checklist**

  * [ ] **JamesBland/**

    * [ ] `README.md`
    * [ ] `LICENSE`
    * [ ] **docs/**

      * [ ] `game_design.md`
      * [ ] `protocol_spec.md`
      * [ ] `art_style_guide.md`
      * [ ] `network_topology.md`
    * [ ] **assets/**

      * [ ] **audio/**

        * [ ] **sfx/**

          * [ ] `anvil_drop.mp3`
          * [ ] `piano_launch.mp3`
          * [ ] `explosion_sizzle.mp3`
        * [ ] **music/**

          * [ ] `suspense_loop.mp3`
          * [ ] `victory_fanfare.mp3`
      * [ ] **images/**

        * [ ] **UI/**

          * [ ] `button_play.png`
          * [ ] `button_settings.png`
          * [ ] `panel_background.png`
        * [ ] **board\_tiles/**

          * [ ] `safe_house_icon.png`
          * [ ] `anvil_crate.png`
          * [ ] `spy_marker_default.png`
        * [ ] **gadgets/**

          * [ ] `spring_anvil.png`
          * [ ] `jetpack_skates.png`
          * [ ] `robo_duck.png`
          * [ ] `bug_detector.png`
      * [ ] **fonts/**

        * [ ] `acme_cartoon.ttf`
        * [ ] `monospace_console.ttf`
      * [ ] (Optional) **data/** for Intel definitions
    * [ ] **static/**

      * [ ] **audio/**

        * [ ] **sfx/** (copied from `assets/audio/sfx/`)

          * [ ] `anvil_drop.mp3`
          * [ ] `piano_launch.mp3`
          * [ ] `explosion_sizzle.mp3`
        * [ ] **music/** (copied from `assets/audio/music/`)

          * [ ] `suspense_loop.mp3`
          * [ ] `victory_fanfare.mp3`
      * [ ] **css/**

        * [ ] `style.css`
      * [ ] **fonts/**

        * [ ] `acme_cartoon.ttf`
        * [ ] `monospace_console.ttf`
      * [ ] **images/**

        * [ ] **UI/**

          * [ ] `button_play.png`
          * [ ] `button_settings.png`
          * [ ] `panel_background.png`
        * [ ] **board\_tiles/**

          * [ ] `safe_house_icon.png`
          * [ ] `anvil_crate.png`
          * [ ] `spy_marker_default.png`
        * [ ] **gadgets/**

          * [ ] `spring_anvil.png`
          * [ ] `jetpack_skates.png`
          * [ ] `robo_duck.png`
          * [ ] `bug_detector.png`
      * [ ] **js/**

        * [ ] `app.js`
      * [ ] **data/** (created by `generate_intel_deck.py`)

        * [ ] `intel_deck.json`
        * [ ] (Optional) `intel_deck.pdf`
    * [ ] **templates/**

      * [ ] `index.html`
    * [ ] `server.py`
    * [ ] `requirements.txt`
    * [ ] **tests/**

      * [ ] `test_interaction_matrix.py`
      * [ ] `test_action_resolver.py`
      * [ ] `test_game_loop.py`
      * [ ] (Optional) `test_utils.py`
    * [ ] **scripts/**

      * [ ] `build_assets.sh`
      * [ ] `generate_intel_deck.py`
    * [ ] `.gitignore`
