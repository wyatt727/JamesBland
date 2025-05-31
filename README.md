# James Bland: ACME Edition (Browser-Based)

**James Bland: ACME Edition** is a browser-based, mobile-friendly competitive espionage game for 2–6 players on the same local network (WLAN). One device (the "host") runs the server application—typically via `npm`, `node.js`, Python, or a similar runtime. Each player opens their mobile (or tablet) browser, navigates to the host's LAN IP and designated port, and joins in. All game logic (action resolution, IP tracking, asset control, banner broadcasts, etc.) executes on the host; players see only the UI and send/receive updates via web sockets or HTTP. No app installation is required—just a modern browser on each device.

This README explains how to set up the server locally, connect players via browser, and navigate/play the game on mobile devices. It covers environment setup, network configuration, user interface conventions, gameplay flow, and mobile-specific optimizations.

## Developer Documentation

For detailed technical information, see the comprehensive documentation in the `docs/` folder:

- **[Game Design Document](docs/game_design.md)**: Complete rules, mechanics, and gameplay flow
- **[Protocol Specification](docs/protocol_spec.md)**: WebSocket events and network communication
- **[Art Style Guide](docs/art_style_guide.md)**: Visual design, colors, fonts, and UI components
- **[Network Topology](docs/network_topology.md)**: LAN architecture, security, and troubleshooting

---

## Table of Contents

1. [Overview](#overview)  
2. [Server Installation & Launch](#server-installation--launch)  
3. [Client Connection & Lobby](#client-connection--lobby)  
4. [User Interface & Controls](#user-interface--controls)  
   - [Main Menu (in Browser)](#main-menu-in-browser)  
   - [Lobby Screen](#lobby-screen)  
   - [Game Screen](#game-screen)  
   - [HUD & Status Bars](#hud--status-bars)  
   - [Dialogs & Pop-Ups](#dialogs--pop-ups)  
5. [Gameplay Flow](#gameplay-flow)  
   - [Planning Phase](#planning-phase)  
   - [Execution Phase](#execution-phase)  
   - [Resolution & Adaptation Phase](#resolution--adaptation-phase)  
6. [Offensive Operations](#offensive-operations)  
7. [Defensive Countermeasures](#defensive-countermeasures)  
8. [Biplane Banner Broadcast](#biplane-banner-broadcast)  
9. [Intelligence & Dossiers](#intelligence--dossiers)  
10. [Intelligence Point (IP) Economy](#intelligence-point-ip-economy)  
11. [Gadgets & Equipment](#gadgets--equipment)  
12. [Alliances & Betrayal](#alliances--betrayal)  
13. [Victory Conditions](#victory-conditions)  
14. [Status Track & Elimination](#status-track--elimination)  
15. [Mobile-Specific Considerations](#mobile-specific-considerations)  
16. [Tips & Best Practices](#tips--best-practices)  
17. [Credits & Acknowledgments](#credits--acknowledgments)  

---

## 1. Overview

**James Bland: ACME Edition (Browser-Based)** transforms slapstick espionage into a single-page, mobile-first web experience. The entire game—simultaneous action resolution, IP tracking, asset updates, banner logic, and win-condition checks—runs on a local server. Players only need a modern mobile or tablet browser to connect and participate. Each round proceeds in real time (with a configurable Planning Phase timer, default 90 seconds), and all participants communicate bi-directionally via WebSockets or long polling. As you deploy exploding pianos, spring-loaded anvils, and biplane banner broadcasts, the server synchronizes state so you can focus on strategy and satire.

Key features:
- **Local Network Play**: Host runs a local web server; players join via browser on the same Wi-Fi.  
- **Mobile-First UI**: Touch-friendly, responsive HTML/CSS/JavaScript—no installation required.  
- **Simultaneous Actions**: Plan offense/defense in parallel; the server reveals and resolves all at once.  
- **Psychological Banner Logic**: No random dice—players must decide whether to trust a banner message.  
- **Cartoonish Animations & Audio**: CSS/Canvas animations and HTML5 audio bring each confrontation to life.  
- **Persistent Dossiers & Intel**: Interactive screens let you track known gadgets, safe houses, and rumors for every opponent.  

---

## 2. Server Installation & Launch

### 2.1 Prerequisites

- **Node.js** (v14+ recommended) **or** **Python 3.7+** (if using a Python-based server).  
- A modern mobile browser on each client device (Chrome, Safari, or Firefox).  
- All participants' devices must share the same local network (Wi-Fi).  

### 2.2 Clone or Download the Repository

Open a terminal on your "host" device (laptop or desktop):

```bash
git clone https://github.com/yourusername/james-bland-acme.git
cd james-bland-acme
```

### 2.3 Install Dependencies

#### If Using Node.js

```bash
cd server   # or wherever package.json lives
npm install
```

* **Key dependencies** may include:

  * `express` (lightweight HTTP server)
  * `ws` or `socket.io` (WebSocket library for real-time updates)
  * `cors` (if needed to allow local network traffic)
  * `nodemon` (optional, for hot-reloading during development)

#### If Using Python

```bash
cd server   # or folder with requirements.txt
pip install -r requirements.txt
```

* **Key dependencies** may include:

  * `Flask` or `FastAPI` (web framework)
  * `uvicorn` or `gunicorn` (ASGI/WSGI server)
  * `aiohttp` or `websockets` for real-time communication
  * `jinja2` (if using HTML templating)

### 2.4 Configuration

By default, the server listens on port **3000** (Node.js) or **8000** (Python). You can override via environment variables:

* **Node.js**:

  ```bash
  export PORT=4000
  npm start
  ```

* **Python**:

  ```bash
  export PORT=5000
  python3 main.py   # or uvicorn main:app --host 0.0.0.0 --port 5000
  ```

Ensure your firewall allows inbound connections to the chosen port.

### 2.5 Launch the Server

* **Node.js**:

  ```bash
  npm start
  ```

  * Usually runs something like `node server.js` or `nodemon server.js`.
  * You should see logs like:

    ```
    [INFO] James Bland: ACME Edition server starting on port 3000
    [INFO] Waiting for players to connect...
    ```

* **Python** (Flask example):

  ```bash
  python3 main.py
  ```

  * You should see:

    ```
    * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
    ```

### 2.6 Verify Local Host Access

On the host device itself, open a browser and navigate to:

```
http://localhost:3000
```

(or replace port if changed). You should see the **James Bland: ACME Edition** landing page (Main Menu) prompting to Host or Join.

---

## 3. Client Connection & Lobby

### 3.1 Finding the Host's IP

All players must connect to the host's LAN IP. To find it:

* **Windows**:
  Run `ipconfig` in Command Prompt, note the IPv4 address under your Wi-Fi adapter (e.g., `192.168.1.42`).

* **macOS / Linux**:
  Run `ifconfig` or `ip a`, note the address under `wlan0` or `en0` (e.g., `192.168.1.42`).

### 3.2 Joining from a Mobile Browser

1. Open a browser (Chrome, Safari, or Firefox) on each player's device.

2. Enter the URL:

   ```
   http://<HOST_IP>:<PORT> 
   ```

   For example: `http://192.168.1.42:3000`

3. You should see the **Main Menu** (same as host). Tap **Join Game**.

### 3.3 Lobby Screen

* **Player List**: Displays all connected codenames and avatars.
* **Ready Button**: A "Ready" toggle appears under your avatar—tap once you've chosen your codename and avatar.
* **Host View**: The host sees a **Start Game** button once at least 2 players have joined and marked Ready.
* **Chat Panel** (optional): Type quick messages or select emojis; synchronized via WebSockets so everyone sees pre-game chatter.
* **Disconnect Warning**: If a player leaves, their avatar disappears; host can reassign screen positions.

---

## 4. User Interface & Controls

The web UI is designed for small screens, with touch-friendly elements and minimal scrolling.

### Main Menu (in Browser)

* **Buttons**:

  * **Host Game** (green): The host clicks this (or taps) to launch the lobby.
  * **Join Game** (blue): Other players tap this to enter the lobby setup screen.
  * **Settings** (gear icon): Adjust audio volume, toggle animations, set planning timer length (default 90 seconds).
  * **Instructions** (info icon): Opens a scrollable help overlay summarizing rules and controls.

### Lobby Screen

* **Player Tiles**: Each player sees a tile with:

  * **Avatar** (cartoon sprite)
  * **Codename** (editable via text input)
  * **Ready Toggle** (gray until tapped, then turns green)
* **Start Game** (host only): Grayed out until at least 2 players are both "connected" and "Ready."
* **Leave Lobby**: Small link at bottom that returns you to the Main Menu.

### Game Screen

Once the match begins, the screen is organized into three horizontal sections:

1. **Top Status Bar** (\~10% Height):

   * A row of **player avatars**, each with:

     * **Codename** (below avatar)
     * **Current IP** (small brain icon & number)
     * **Status Icon** (circle colored by status: green/yellow/orange/red/black)
     * **Gadget Counter** (tiny gear icon + number of gadgets held)
   * Tapping an avatar briefly shows a tooltip: "Last known gadgets: …", "Last turn status: …".

2. **Center Board Area** (\~60% Height):

   * A stylized ACME blueprint background—zones with icons for "Safe Houses,", "Asset Locations," and "Tunnels."
   * **Agent Markers**: Animated SVG or Canvas sprites at grid positions.
   * **Interactive Elements**:

     * Tappable grid cells highlight if they correspond to an effect (e.g., dropping an anvil onto that cell).
     * During resolution, CSS animations or Canvas draws show pianos falling, anvils bouncing, banners flying overhead.

3. **Bottom Action Panel** (\~30% Height):

   * **Offense Tab** (default view on left):

     * **Dropdown Menu** listing all available offenses; tap to expand.
     * **Target Selector**: If an offense needs a target, a second dropdown shows codenames of other players.
     * **IP Slider**: Horizontal slider (0–current IP) with a numeric badge. Drag or tap to set.
     * **Confirm Button** (green checkmark): Locks in offense. Once tapped, it collapses into a small icon indicating "Locked: \[Offense Icon]."

   * **Defense Tab** (swipe left or tap "Defense"):

     * **Dropdown Menu** listing defenses.
     * **IP Slider**: Adjust for defenses requiring IP (e.g., Banner always sets slider to 2).
     * **Confirm Button** (red shield icon): Locks in defense; collapses to a small "Locked: \[Defense Icon]."

   * **Gadget Inventory Icon** (bag icon in bottom center):

     * Tapping opens a full-screen overlay (modal) listing all gadgets you own, their statuses (active or needing recharge), and purchase options (if you have enough IP).

   * **Timer Countdown** (centered above Confirm buttons):

     * Large digital display (e.g., "00:45") with a progress bar along the bottom of the action panel that shrinks as time elapses.

---

## 5. Gameplay Flow

### Planning Phase

* **Duration**: Default 90 seconds (configurable by host).

* **What Players Do**:

  1. **Offense Selection**:

     * Tap **Offense Tab**.
     * Select an offensive operation from the dropdown.
     * If the chosen offense requires a target, select from the **Target Selector**.
     * Use **IP Slider** to allocate IP toward upgrades or bribery for this offense (if desired).
     * Tap **Confirm**; the offense locks.

  2. **Defense Selection**:

     * Tap **Defense Tab**.
     * Select a defensive measure.
     * Use **IP Slider** if defense has a cost (e.g., Biplane Banner is always 2 IP).
     * Tap **Confirm**; the defense locks.

  3. **Gadget Purchase / Recharge (Optional)**:

     * If you have leftover IP after locking offense/defense, tap the **Gadget Inventory Icon**.
     * In the modal, you can purchase new gadgets (if you meet cost/prerequisites) or recharge owned ones (1 IP each).
     * After purchase/recharge, tap "Close" to return to the action panel.

* **Banner Message Entry**:

  * If you selected **Biplane Banner** as defense, a text field appears. Type a message (max 25 characters), then tap "OK" to store it. Your slider locks at 2 IP automatically.

* **Lock-In Feedback**:

  * Once both offense and defense are confirmed, your action panel dims and shows two small icons (offense icon + defense icon) to indicate you are locked.
  * If you fail to confirm both by timer expiration, defaults apply:

    * Offense → **Safe Turn** (no operation, +1 IP)
    * Defense → **Underground** (costs 1 IP)

### Execution Phase

* **Reveal**: When the timer reaches zero, all clients display "All Choices Locked" and switch to a brief blackout (e.g., the screen dims for 1 second).

* **Preemptive Actions**: Any **Preemptive Strikes** or **Bribe ACME Guard** actions run first. The server computes outcomes, updates state, and broadcasts the results.

* **Banner Display & Psychological Resolution**:

  1. **Banner Animation**: If any player used Biplane Banner, clients play a top-of-screen animation: a small plane flies across, dragging the typed text. Simultaneously, a soft "propeller whir" audio plays.
  2. **Affected Players Prompt**: Each player who originally targeted the banner-caster sees a floating modal with two buttons: **Believe Banner** and **Ignore Banner**. A 10-second timer counts down.

     * **Choosing "Believe"**: Their locked offense is rerouted according to the banner's claim (e.g., if the banner said "BLACKBIRD BUNKER AT BANK," and they trust it, their offense is applied to the Bank zone rather than the original target).
     * **Choosing "Ignore"**: Their locked offense remains pointed at the banner-caster (no reroute), but if the banner was genuine, they incur a "–1 Penalty" on their dice roll or success chance.
     * **Timeout**: If no choice by 10 seconds, default to **Ignore** (models hesitation as suspicion).

* **Standard Matchups**: After banner resolution, the server resolves each attacker's (or redirected attacker's) offense against their chosen defender's locked defense. If multiple attackers target the same defender, a small initiative order is determined (highest current IP first; ties broken by avatar color or random). The server calculates outcomes (success/failure, IP awards, gadget losses, status changes) and pushes updates.

### Resolution & Adaptation Phase

* **Applying Outcomes**:

  1. **IP Adjustments**: On each client, floating colored numbers ("+2 IP" or "–1 IP") appear above relevant avatars, and the Top Status Bar updates.
  2. **Gadget Loss/Consumption**: Destroyed gadgets shake red briefly, then disappear from the player's inventory UI.
  3. **Status Changes**: If a player becomes **Compromised**, **Burned**, **Captured**, or **Eliminated**, their avatar border color changes accordingly, and a text banner appears: "Agent \[Codename] is now \[Status]."
  4. **Intel Cards**: When an operation grants an Intel Card (successful infiltration, counter-intel, Witness Bonuses), a card-back slide-in animation appears at the bottom—tapping it reveals the card.

* **Dossier Update & Draw Phase**:

  * If you gained Intel, a dialog pops up: "You drew: \[Card Name]." Tap to inspect.
  * If you earned a **Witness Bonus**, a toast reads "+1 IP for Safe Turn" or "+2 IP for Prediction Bonus."

* **Alliance Adjustments**:

  * A small "Alliance" icon appears between any allied avatars who remain allied. Tapping either icon allows renegotiation: extend, break, or form new pacts.
  * Breaking mid-round is not permitted—alliances end at the start of the next Planning Phase or when betrayal occurs.

* **Captured & Ghost Agents**:

  * **Captured**: Your screen shows "You Are Captured—Skip Next Round." You draw 1 Intel Card as a Ghost, then your interface becomes a minimal "Wait" view until the next round. After skipping one round, you return as **Burned** (Orange).
  * **Eliminated**: Your screen shifts to a semi-transparent overlay showing the board and players. You draw 1 Intel Card each round and can use the **Haunt** button (requires spending 2 Intel Cards) to force any living agent to lose 1 IP. You cannot win but remain engaged.

* **Asset Control Updates**:

  * If a **Network Attack** or **Alliance Operation** captured a Strategic Asset, the corresponding asset icon on the shared board area changes to that agent's color, and an influence marker appears. A brief toast: "\[Codename] captured ACME Armory."

* **Victory Check**:

  * At the end of Adaptation Phase, the server runs victory-condition checks. If any condition is met, it broadcasts a "Victory" event to all clients, triggering the endgame overlay.

---

## 6. Offensive Operations

Below is a concise summary of each offensive option available in the browser UI. Tooltips appear on hover/tap to clarify cost and mechanics.

1. **Assassination**

   * **Cost**: 0 IP.
   * **Mechanic**: Server compares a random 10-sided result for attacker vs. a random defender roll (defense-specific modifiers apply).

     * **Success**: Defender → **Compromised** (loses one gadget, –1 IP next round), attacker +3 IP.
     * **Failure**: Attacker's identity is revealed (shifts defenders' dossier knowledge), attacker loses –1 IP and discards the attacking gadget.

2. **Sabotage**

   * **Cost**: 0 IP.
   * **Mechanic**: Server rolls attacker vs. target's counter-intel roll.

     * **Success**: Target's next-round IP generation halved; attacker +2 IP.
     * **Failure**: If defender has "Counter-Surveillance" or "Bug Detectors" active, attacker loses –1 IP.

3. **Exposure**

   * **Cost**: 1 IP.
   * **Mechanic**: Server rolls (d10 + attacker gadget modifiers) vs. target's "False Identity" or "Signal Jammers."

     * **Success**: Target's codename revealed for 2 rounds; attacker draws 1 Intel Card and +2 IP.
     * **Failure**: Attacker's cover is blown: everyone's dossier gets an "Exposed" marker for that attacker; attacker loses –1 IP.

4. **Capture**

   * **Cost**: 2 IP.
   * **Prerequisite**: Target must have chosen a "weak defense" (e.g., no bodyguard).
   * **Mechanic**: Server rolls d10 vs. target's "Bodyguard Detail" or "Mobile Operations."

     * **Success**: Target → **Captured** (skips next round, can escape to Burned by spending 2 Intel Cards), attacker +2 IP.
     * **Failure**: Both attacker and defender lose –1 IP.

5. **Surveillance**

   * **Cost**: 1–2 IP.
   * **Mechanic**: Server rolls attacker's d10 vs. target's "Sweep & Clear" or "Counter-Surveillance.

     * **Success**: Reveal target's chosen defense; if your pre-guess matched, +2 IP; draw 1 Intel Card.
     * **Failure**: Spent IP is lost; defender draws 1 Intel Card.

6. **Infiltration**

   * **Cost**: 1 IP.
   * **Mechanic**: Server rolls d10 vs. target's "Sweep & Clear" or "Bug Detectors.

     * **Success**: Add a permanent "Bugged" token to target (server flags them); draw 1 Secret Intel Card; +1 IP.
     * **Failure**: Defender confiscates one random Intel Card; attacker loses –1 IP.

7. **Asset Theft**

   * **Cost**: 1 IP.
   * **Mechanic**: Server rolls d10 vs. target's "Asset Lockdown" or "Underground.

     * **Success**: Steal half of target's unspent IP (rounded down) plus one random gadget; attacker +1 IP.
     * **Failure**: Spent IP is lost; defender draws 1 Intel Card.

8. **Misinformation**

   * **Cost**: 1 IP.
   * **Mechanic**: No roll; target may spend 1 IP on "Disinformation Counter.

     * **If unblocked**: Attacker +2 IP next round when defender wastes resources.
     * **If blocked**: Attacker loses –1 IP; defender draws 1 Intel Card.

9. **Network Attack**

   * **Cost**: 2 IP.
   * **Mechanic**: Server rolls d10 vs. target's "Alliance Building.

     * **Success**: Remove one Alliance Token from target; attacker +1 IP per link removed.
     * **Failure**: Attacker loses –2 IP; defender draws 1 Intel Card.

10. **Resource Denial**

    * **Cost**: 2 IP.
    * **Mechanic**: Server rolls d10 vs. target's "Forgery Rings" or "Safe House.

      * **Success**: Target loses IP gains from Safe Turns or Witness Bonuses next round; attacker +1 IP.
      * **Failure**: Attacker loses –2 IP; defender draws 1 Intel Card.

11. **Alliance Disruption**

    * **Cost**: 2 IP.
    * **Prerequisite**: Two other players share an active Alliance Token.
    * **Mechanic**: Server rolls d10.

      * **4–6**: Breaks their alliance—both allied players lose 1 IP and discard shared intel; attacker +1 IP.
      * **1–3**: Attacker loses –2 IP; both allied defenders draw 1 Intel Card.

12. **False Flag**

    * **Cost**: 2 IP.
    * **Mechanic**: Choose two players, X (to frame) and Y (actual target). If Y did not select a "Counter-Intel" defense:

      * Y believes X attacked: X → **Exposed** (everyone sees X on next two rounds), X loses –1 IP; attacker +2 IP.
      * If Y chose Counter-Intel: Attacker loses –2 IP; defender draws 1 Intel Card.

13. **Master Plan Action**

    * **Cost & Mechanic**: Varies per secret objective. The Master Plan modal shows exact conditions and any additional IP or roll requirements.

14. **Safe Turn (No Operation)**

    * **Cost**: 0 IP.
    * **Mechanic**: Automatically gains +1 IP; no offense declared. Can still choose a defense and spend IP on gadgets, alliances, or banners.

---

## 7. Defensive Countermeasures

Players choose one defense per round. Each appears in the Defense dropdown with a tooltip explaining cost, effect, and prerequisites.

### 7.1 Physical Security

1. **Safe House (Fortress of Trampolines)**

   * **Cost**: 0 IP (repair costs 1 IP if breached).
   * **Mechanic**: When targeted by Assassination or Sabotage, server rolls d10 vs. attack. Tie or higher: defense wins—attacker discards attacking gadget and loses –1 IP; defender loses –1 IP repairing. If attacker wins: defender → **Compromised**, loses –1 IP.

2. **Bodyguard Detail (Robo-Duck Patrol)**

   * **Cost**: 2 IP per round + 1 "Duck Ammo" gadget per block.
   * **Mechanic**: Automatically counters one Assassination or Infiltration. On block: defender draws 1 Intel Card. Cannot stop long-range Sabotage unless "Mobile Operations" also chosen.

3. **Mobile Operations (Jet-Powered Roller Skates)**

   * **Cost**: 0 IP (foregoes Safe Turn bonus).
   * **Mechanic**: Attacks against you incur a –2 penalty; attacker must guess your position first (tie = you escape). If misguessed: attack fails. You do not earn IP from Safe Turn.

4. **Underground (Secret Tunnel Network)**

   * **Cost**: 1 IP.
   * **Mechanic**: untargetable by direct offenses (Assassination, Sabotage, Exposure, Capture) unless attacker spends 3 IP on "Network Attack" or uses an "All-Points Bulletin" gadget. Grants a "Tunnel Map" token (resurface anywhere next turn).

### 7.2 Counter-Intelligence

5. **Sweep & Clear (Bug-Sweeping Robot Vacuum)**

   * **Cost**: 0 IP.
   * **Mechanic**: Automatically counters one Surveillance or Infiltration. On success: defender draws 1 Intel Card showing attacker's identity and gadget. If facing Misinformation: must discard 1 Intel Card (robot sucks up real intel too).

6. **False Identity (Switchable Mask Rack)**

   * **Cost**: 2 IP if an Exposure is attempted; otherwise free.
   * **Mechanic**: Any Exposure attempt fails—attacker is exposed instead (everyone's dossier tags attacker). Any assassination of "Masked Figure" auto-fails and attacker loses –1 IP.

7. **Counter-Surveillance (Mirror Drone Squadron)**

   * **Cost**: 2 IP (usable every other round).
   * **Mechanic**: If targeted by Surveillance, attacker loses spent IP and their Surveillance gadget is destroyed; defender draws 1 Intel Card showing attacker's details.

8. **Disinformation (ACME Fake News Broadcaster)**

   * **Cost**: 1 IP.
   * **Mechanic**: Broadcast a false rumor to all players. Next round, any attack on you has a 50% chance to misfire (same logic as banners but everyone sees the rumor, not a personalized banner). If two or more players broadcast Disinformation same round, they collide: both lose 1 IP; no further effect.

### 7.3 Active Defense

9. **Preemptive Strike (ACME Bat-Torpedo Launch)**

   * **Cost**: 3 IP.
   * **Mechanic**: Before standard matchups, you choose whichever opponent you believe targeted you (based on prior intel or guess). Server rolls d10 vs. their defense. If correct & successful: they lose 2 IP and reveal one gadget; if wrong: you lose 3 IP; they gain +1 IP.

10. **Alliance Building (Mutual Booby Trap Setup)**

    * **Cost**: 2 IP per partner.
    * **Mechanic**: For the next 2 rounds, neither agent may target the other. Share any Intel Cards drawn. If betrayal occurs mid-round: betrayer → **Compromised**, loses 2 IP; cannot form new alliances for 3 rounds.

11. **Honeypot Operations (Cartoon Bear Trap Suite)**

    * **Cost**: 3 IP; must discard one gadget if unused.
    * **Mechanic**: Place a visible lure (e.g., "FREE ACME Golden Anvil") in a chosen board zone. Any opponent who selected Asset Theft or Sabotage against you who enters that zone becomes **Stuck** (lose next action), and you draw 2 Intel Cards. If no one triggers: discard one gadget due to wasted setup.

12. **Information Warfare (ACME Biplane Banner Broadcast)**

    * **Cost**: 2 IP.
    * **Mechanic**: See [Section 8](#8-biplane-banner-broadcast) for the full psychological-resolution process.

---

## 8. Biplane Banner Broadcast

The **Biplane Banner** leverages human psychology instead of chance:

1. **Declaration & Entry**

   * In the Defense dropdown, select **Information Warfare (Biplane Banner)**. The IP Slider locks at 2. A text field appears: type up to 25 characters.

2. **Hidden Payment**

   * Only you know that 2 IP has been deducted. Opponents see the banner content during resolution but won't know who paid for it.

3. **Banner Animation**

   * As the timer ends, the server broadcasts a "Show Banner" event. Each client renders a small plane sprite flying across the top of the board area, dragging the banner text behind it. A soft "propeller" audio loop plays.

4. **Psychological Resolution (No Dice)**

   * Each player who had originally chosen an offense targeting you receives a floating modal with two buttons: **"Believe Banner"** and **"Ignore Banner"**. A 10-second countdown begins.
   * **Options & Outcomes**:

     * **If they tap "Believe"** and the banner was **Genuine** (you intended to misdirect them), their offense is automatically rerouted to whatever the banner indicated (e.g., "BANK"), failing to affect you. No further penalty.
     * **If they tap "Believe"** but the banner was a **Bluff**, their offense is wasted on the false location; they gain no IP and you gain +1 IP for a successful deception.
     * **If they tap "Ignore"** and the banner was **Genuine**, their offense proceeds against you as planned but with a **–1 penalty** (UI shows a small "–1" badge on their offense icon).
     * **If they tap "Ignore"** and the banner was a **Bluff**, their offense proceeds normally with no penalty.
     * **Timeout** (after 10s): defaults to "Ignore."

5. **Server Coordination**

   * The server tracks each affected player's choice (or default). Once all have responded, the server finalizes the rerouting (if any) and proceeds to matchups.
   * A short broadcast describes the outcome:

     > "\[Officer Raven tried to attack you but believed the banner and moved to the bank—attack failed.]"
     > or
     > "\[Finch ignored the banner and attacks you, but you prepared—Finch suffers a –1 penalty.]"

---

## 9. Intelligence & Dossiers

* **Agent Dossier Overlay**

  * Accessible by tapping the **Dossier** icon near your avatar (or via a persistent "Dossier" button in the HUD).
  * Shows a table for each opponent, with columns:

    * **Known Gadgets** (icons).
    * **Known Defense Patterns** (e.g., "Often picks Mobile Ops on round 2").
    * **IP Estimates** (exact if revealed; "~3–5" if only partial).
    * **Known Hidden Status** (e.g., "Currently Underground, Tunnel Exit: Zone 4").
    * **Alliance Links** (chain icons connecting allied agents).
    * **Collected Intel Cards** (face-up grid).

* **Drawing Intel Cards**

  * When you earn an Intel Card (successful infiltration, counter-intel success, or Witness Bonus), a dialog pops up:

    > "You drew: \[Card Name]!"
  * Tap to view the card's effect (e.g., "Reveal target's next chosen defense"). You hold up to 5 cards; drawing beyond capacity forces you to discard one.

* **Playing Intel Cards**

  * At the beginning of any Planning Phase (once your screen refreshes), a small **Intel** button appears near the Offense tab. Tapping opens a modal listing your Intel Cards.
  * Choose one to play before making offense/defense selections; the card's description explains its immediate effect. For instance, "Reveal Next Defense" reveals another player's locked defense pane immediately.

* **Ghost Agent View**

  * If you become **Eliminated**, your browser switches to a "Ghost Mode" overlay. You see the live game board and all public statuses. Each round, you draw 1 Intel Card automatically.
  * A **Haunt** button appears: tap it, then tap any living agent's avatar to force them to lose 1 IP (animated as a transparent ghost reaching out and zapping). Costs 2 Intel Cards. You remain a spectator otherwise.

---

## 10. Intelligence Point (IP) Economy

1. **Earning IP**

   * **Successful Operations**:

     * **Assassination**: +3 IP
     * **Sabotage / Exposure / Capture**: +2 IP each
   * **Defensive Success**:

     * Fully neutralizing an attack: +1 IP
     * Counter-intel intercept (Sweep & Clear, Counter-Surveillance): +2 IP
   * **Witness Bonuses**:

     * **Safe Turn** (didn't attack or get attacked): +1 IP
     * **Prediction Bonus** (guessing two opponents' offense & defense correctly): +2 IP
   * **Asset Control**:

     * Holding any Strategic Asset yields +1 IP per round.

2. **Spending IP**

   * **Gadget Purchases & Recharges** (1–5 IP each; see Gadget Catalog).
   * **Alliance Funding**:

     * **Non-Aggression Pact**: 2 IP per partner for 2 rounds.
     * **Coordinated Operation**: 3 IP per partner (split stolen IP on success).
   * **Bribing NPCs**: 1–2 IP (ACME Guard Dog, ACME Mailman).
   * **Gadget Upkeep**: 1 IP per active gadget needing recharge (e.g., Mirror Drones, Robo-Ducks).
   * **False Identity Maintenance**: 2 IP if someone attempts Exposure on you.
   * **Underground Maintenance**: 1 IP per round.
   * **Biplane Banner Broadcast**: 2 IP.
   * **Saving IP**: Any unspent IP carries over to next round.

* **UI Note**: The **Gadget Inventory** modal displays each gadget's cost clearly. If you attempt to select an option that would exceed your current IP, the slider or button flashes red, and a tooltip "Not enough IP" appears.

---

## 11. Gadgets & Equipment

The **ACME Catalog** displays all purchasable gadgets. Below are representative examples; the in-game help provides the complete list.

### Surveillance Gear

* **Listening Devices** (1 IP, one-time)

  * **Effect**: Next Surveillance attempt succeeds automatically unless the target has "Sweep & Clear." Icon is removed on use.

* **Camera Networks** (3 IP)

  * **Effect**: Takes one entire Planning Phase to assemble. In the following round, automatically reveals one opponent's chosen defense. During assembly, cannot be used or recharged.

* **Communication Intercepts** (2 IP, one-time)

  * **Effect**: When any two players form or renew an alliance, automatically steal and reveal that intel before they confirm. Icon is removed on use.

### Combat Equipment

* **Silenced Weapons** (2 IP)

  * **Effect**: Grants +1 success modifier on Assassination rolls; on ties, treats as attacker win against "Safe House." No cooldown.

* **Explosives Box** (3 IP)

  * **Effect**: One-time Sabotage with +2 success modifier. 50% chance of misfire—if misfire, attacker → **Compromised**, loses –2 IP. Icon removed on use.

* **Body Armor** (2 IP)

  * **Effect**: When targeted by a direct attack, treat your defense roll as +1 higher. Cannot combine with "Underground."

### Counter-Intelligence Tools

* **Bug Detectors** (2 IP)

  * **Effect**: Automatically nullify one Infiltration or Surveillance attempt per round; defender draws 1 Intel Card. No cooldown.

* **Signal Jammers** (3 IP)

  * **Effect**: Blocks any one remote-wired gadget (e.g., Bagpipe Bomb) for that round. If triggered, attacker's gadget destroyed. No cooldown.

* **Fake Documents Kit** (2 IP)

  * **Effect**: If targeted by Exposure, treat as a failure: attacker loses –1 IP, you remain hidden. Icon removed on use.

### Advanced Gadgets

* **ACME Mobile Fortress** (5 IP)

  * **Prerequisites**: Own both "Robo-Duck Patrol" and "Portable Safe House Kit."
  * **Effect**: One-turn invincibility—all attacks automatically fail. You earn no IP that round. Icon grays out until the next round ends.

* **ACME Time-Bomb Beetle** (3 IP)

  * **Effect**: On successful Infiltration vs. non–Counter-Intel defense, plant a time bomb—target starts next round as **Compromised** (–2 IP). Icon persists until detonated next round.

* **ACME Anvil Drone** (4 IP)

  * **Prerequisite**: Own "Jetpack Roller Skates."
  * **Effect**: One-time long-range Assassination with +2 success modifier; 25% chance to misfire (drops an anvil on a random adjacent agent). Icon removed on use.

* **Jetpack Roller Skates** (3 IP)

  * **Effect**: Grants +1 initiative when using "Mobile Operations" (you act first among ties). No cooldown.

---

## 12. Alliances & Betrayal

Agents can forge—or break—alliances between rounds. Alliances appear as chain icons connecting avatar tiles in the Top Status Bar and on the board.

### Non-Aggression Pact

* **Cost**: 2 IP per partner.
* **Effect**:

  * For 2 rounds, allied agents cannot target each other. (UI shows chain link icon and "Pact Rounds Left: 2.")
  * Whenever either draws an Intel Card, the partner receives a copy. A "Shared Intel" badge appears in both dossiers.
* **Betrayal**:

  * If one attacks the other mid-pact, a red "Trust Betrayal" banner appears: "Betrayer → **Compromised**, –2 IP."
  * The chain link icon disappears. The betrayer cannot form new alliances for the next 3 rounds.

### Coordinated Operation

* **Cost**: 3 IP per partner.
* **Effect**:

  * Both partners must select the same target in Planning Phase. The UI highlights their offense target boxes in yellow to indicate alignment.
  * If both succeed, stolen IP is split equally (e.g., "+4 IP" splits as +2/+2).
* **Failure**:

  * If either fails, both lose spent IP; no shared rewards.

### Ending an Alliance

* Alliances auto-expire after their duration (2 rounds for pacts).
* To end early at the start of Adaptation Phase, a partner taps the chain icon on their avatar and selects **"End Pact"**, spending 1 IP. The link dissolves; a "Pact Ended—Cannot Target Until Next Round" badge appears on both avatars.
* Mid-round betrayals (attacking an ally) immediately trigger the betrayal penalty (Compromised, –2 IP) and break the alliance.

---

## 13. Victory Conditions

The server checks for these conditions at the end of each Adaptation Phase. When one is met, the server broadcasts a `gameOver` event, and all clients display the corresponding victory overlay.

1. **Last Spy Standing**

   * All other agents are **Eliminated** or **Captured**. The sole remaining **Active** agent wins.
   * Overlay shows a triumphant "Last Spy Standing" animation (agent holding a golden anvil).

2. **Intelligence Supremacy**

   * An agent collects a **Full Dossier** on every other active agent—three distinct Intel Cards per opponent (Identity, Safe House Location, Preferred Gadget).
   * When conditions met, a "Declare Supremacy" button appears in their UI. Tapping it ends the match.
   * Overlay shows "Intelligence Supremacy" with a dossier bursting into confetti.

3. **Network Control**

   * An agent controls **three** of the five Strategic Assets simultaneously.
   * To capture an asset:

     1. Win a "Network Attack" vs. its controller.
     2. Form an "Alliance" pact splitting control (each places an Influence Token).
   * Once three assets bear your Influence Token, a "Network Control Achieved" banner appears—tap it to claim victory.
   * Overlay: five asset icons light up; yours shine gold.

4. **Mission Completion (Master Plan)**

   * Each agent is dealt a private **Master Plan** at game start. A small "Objective Tracker" appears next to their profile.
   * When the single-player conditions are satisfied (e.g., "Expose all active agents in one turn"), a "Complete Master Plan" button appears. Tapping reveals the plan to everyone and ends the match.
   * Overlay: a parchment scroll unrolls, and fireworks burst.

5. **Alliance Victory**

   * If two agents form a **Binding Alliance** and fulfill a shared objective (e.g., "Together, eliminate all non-allied agents in one round"), a "Alliance Success" banner appears.
   * Server then enters **Final Showdown** mode:

     * Both allied agents gain +3 IP.
     * Both choose between Assassination or Sabotage (no defense allowed).
     * Server resolves both simultaneously; higher success (or higher d10 if tied) wins 1st place; other is runner-up.
     * Overlay: allied avatars exchange a victorious handshake, then face off in a split-screen duel animation.

---

## 14. Status Track & Elimination

Agents cycle through five statuses. Each status has clear UI indicators and local effects.

1. **Active (Green)**

   * Full offensive/defensive options; 100% IP generation.
   * UI: Avatar border glows green; no penalty badges.

2. **Compromised (Yellow)**

   * Triggered by losing a direct attack (Assassination, severe Sabotage, gadget misfire).
   * IP generation at 80% (UI shows small "–20%" badge on IP counter).
   * Cannot select "False Identity" or "Honeypot Operations."
   * Recovery: During Adaptation Phase, tap "Bribe ACME Rumor Mill (2 IP)" to return to Active.

3. **Burned (Orange)**

   * Triggered by repeated Compromises or failing a Capture.
   * IP generation at 50% (UI shows "–50%" badge).
   * Only permitted defenses: **Mobile Operations** or **Sweep & Clear** (other options disabled).
   * Cannot purchase new gadgets or broadcast banners.
   * Recovery: During Adaptation Phase, tap "Bribe ACME Rumor Mill (3 IP)" to return to Active.

4. **Captured (Red)**

   * Triggered by a successful Capture.
   * During next Planning Phase, your browser displays "You Are Captured—Skip This Round" (no offense or defense choices). You automatically draw 1 Intel Card as a Ghost.
   * In Adaptation Phase, you may tap "Spend 2 Intel to Escape"—if chosen, you return as **Burned** next round. Otherwise, remain Captured and skip another Planning Phase.

5. **Eliminated (Black)**

   * Occurs when:

     1. You are Captured twice without escape; or
     2. You are Burned and your IP drops to 0.
   * Your browser switches to **Ghost Mode**:

     * You view the board and all public statuses (semi-transparent overlay).
     * Each round, you automatically draw 1 Intel Card into your ghost hand.
     * You can tap **Haunt** and then a living agent's avatar to force them to lose 1 IP (animated as a ghostly zap). Costs 2 Intel Cards.
   * You remain involved in endgame tension but cannot win.

Whenever a status changes, all clients display a toast:

> "Agent Raven is now COMPROMISED! All opponents draw 1 Intel Card about Raven."

---

## 15. Mobile-Specific Considerations

The web UI is optimized for touch-based mobile devices, ensuring ease of use on phones and tablets.

1. **Responsive Layout**

   * The page uses a fluid, mobile-first CSS grid. All key elements scale or reflow based on viewport width.
   * Text sizes: primary buttons at ~20px; tooltips and labels at ~14px.

2. **Touch-Friendly Controls**

   * Large dropdowns with 44px height, easy to tap.
   * IP slider supports both drag and tap (tap to move in increments of 1).
   * "Swipe" gestures:

     * **Swipe Left/Right** toggles Offense/Defense tabs.
     * **Swipe Up** opens Gadget Inventory.
     * **Swipe Down** closes any open modal or overlay.

3. **Minimal Scrolling**

   * All core actions fit within one screen. The Gadget Inventory or Dossier modals scroll internally if the content exceeds the viewport.

4. **Local Storage for Preferences**

   * Browser localStorage retains:

     * Last-used codename and avatar.
     * Settings (sound on/off, timer length, reduced-motion preference).
   * Upon reconnection (e.g., refreshing the page), these preferences auto-populate.

5. **Network Efficiency**

   * Real-time updates use WebSocket frames of minimal JSON payload (e.g., `{ playerId: 3, action: "Assassination", targetId: 1, ipSpent: 0 }`).
   * Animations use CSS transitions or lightweight Canvas to minimize CPU and battery drain.
   * Audio uses compressed OGG format; auto-muted if mobile data is detected (but on LAN-only, allowed).

6. **Haptic Feedback via Vibration API**

   * On supported mobile browsers, small vibrations occur:

     * Final 5 seconds of Planning Phase (short buzz).
     * Successful gadget block (single pulse).
     * Banner successfully fools you (two quick pulses).
   * Users can disable vibrations in Settings (affects localStorage).

---

## 16. Tips & Best Practices

* **Timer Awareness**: Keep an eye on the 90-second countdown. Drag the IP slider early, type banner text promptly, and confirm decisions with at least 10 seconds to spare.
* **Psychological Banners**: Because the banner's payer is hidden, any credible-sounding message can sow doubt. If you suspect two or more opponents plan to attack you, a banner can fracture their coordination.
* **Gadget Synergies**: Combining complementary gadgets amplifies impact. For instance, using **Silenced Weapons** alongside a **Preemptive Strike** can catch a bodyguard unaware.
* **Alliance Timing**: Alliances cost IP but can buy you breathing room to build powerful gadgets. Consider forming a **Non-Aggression Pact** if you want to accumulate without early aggression.
* **Dossier Maintenance**: After each round, update your mental notes based on revealed defenses, gadget usage, and IP changes. Over time, patterns emerge (e.g., Finch always picks **Mobile Operations** when IP ≥ 4).
* **Ghost Agent Engagement**: If you become a ghost, stay active by haunting living agents; those –1 IP zaps can swing a close match and keep you involved in the drama.
* **Network Stability**: If your Wi-Fi network is congested, reduce animation quality in Settings or disable haptics to lighten bandwidth.
* **Use Headphones**: SFX like piano crashes and anvil clangs are most effective with headphones—listen for audio cues to react before seeing the full animation.

---

## 17. Credits & Acknowledgments

* **Design Team**

  * Lead Designer & Project Owner: \[Your Name]
  * Content Designer & Scripter: \[Collaborator Name]
  * UX/UI Designer: \[Designer Name]
  * QA & Playtesters: Family, Friends, Local Gaming Group

* **Artwork & Audio Assets**

  * Cartoon Sprites & Icons: Hand-illustrated by \[Artist Name]
  * Sound Effects:

    * Anvil Clang & Piano Crash: Free SFX Library (modified)
    * Biplane Engine Loop: Field Recording by \[Sound Designer]

* **Programming & Networking**

  * Peer Discovery & WebSocket Engine: Custom WebSocket stack by \[Developer Name]
  * Frontend Framework: HTML5/CSS3/Vanilla JavaScript (no heavy libraries)
  * Optimization & Performance Tuning: \[Developer Name]

* **Acknowledgments**

  * Inspired by ACME's classic cartoons and slapstick humor.
  * Homage to "Spy vs Spy" simultaneous-action mechanics and social deduction games.
  * Thanks to everyone who volunteered as beta testers and provided feedback on balance, pacing, and mobile UI.

* **License & Distribution**

  * **James Bland: ACME Edition (Browser-Based)** remains proprietary.
  * The server application and assets may not be redistributed or modified without permission.
  * House-ruled variations are encouraged; please credit the original team and note your changes.

---

**Ready to unleash cartoon mayhem?**

1. Run the server on a host device (`npm start` or `python main.py`).
2. Have each player open a browser to `http://<HOST_IP>:<PORT>`.
3. Join the lobby, ready up, and let the bidding, bluffing, and biplane banners begin.
4. May the cleverest spy (or the most cunning bluff) prevail!

