/**
 * JAMES BLAND: ACME EDITION - CLIENT APPLICATION
 * Mobile-First WebSocket Game Client
 */

class JamesBlandClient {
    constructor() {
        // WebSocket connection
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        // Game state
        this.gameState = {
            phase: 'lobby', // 'lobby', 'planning', 'resolution', 'bannerChoice', 'gameOver'
            players: {},
            currentRound: 0,
            timer: 0,
            isHost: false,
            myCodename: '',
            turnSubmitted: false
        };
        
        // Planning phase data
        this.planningData = {
            offense: '',
            defense: '',
            target: '',
            ipSpend: 0,
            bannerMessage: ''
        };
        
        // Audio system
        this.audioElements = {};
        this.audioEnabled = true;
        this.backgroundMusicEnabled = false;
        
        // UI elements (will be cached on init)
        this.elements = {};
        
        // Timer interval
        this.timerInterval = null;
        
        // Initialize the application
        this.init();
    }
    
    /**
     * Initialize the application
     */
    init() {
        this.cacheUIElements();
        this.setupEventListeners();
        this.initializeAudio();
        this.connectToServer();
        this.showLobby();
    }
    
    /**
     * Cache frequently used UI elements
     */
    cacheUIElements() {
        // Overlays
        this.elements.lobbyOverlay = document.getElementById('overlay-lobby');
        this.elements.gameOverlay = document.getElementById('overlay-game');
        
        // Lobby elements
        this.elements.codenameInput = document.getElementById('input-codename');
        this.elements.joinBtn = document.getElementById('btn-join');
        this.elements.startBtn = document.getElementById('btn-start');
        this.elements.playerListLobby = document.getElementById('player-list-lobby');
        this.elements.lobbyStatus = document.getElementById('lobby-status');
        
        // Game elements
        this.elements.hudContainer = document.querySelector('.hud-container');
        this.elements.planningUI = document.getElementById('planning-ui');
        this.elements.resolutionUI = document.getElementById('resolution');
        this.elements.bannerModal = document.getElementById('banner-modal');
        
        // Planning phase elements
        this.elements.selectOffense = document.getElementById('select-offense');
        this.elements.selectDefense = document.getElementById('select-defense');
        this.elements.selectTarget = document.getElementById('select-target');
        this.elements.ipSlider = document.getElementById('input-ip');
        this.elements.ipDisplay = document.getElementById('ip-display');
        this.elements.ipAvailable = document.getElementById('ip-available');
        this.elements.bannerInput = document.getElementById('input-banner');
        this.elements.bannerSection = document.getElementById('banner-section');
        this.elements.submitBtn = document.getElementById('btn-submit-turn');
        this.elements.submissionStatus = document.getElementById('submission-status');
        this.elements.timerDisplay = document.getElementById('timer-display');
        this.elements.charCount = document.querySelector('.char-count');
        
        // Resolution elements
        this.elements.resolutionContent = document.getElementById('resolution-content');
        this.elements.continueBtn = document.getElementById('btn-continue');
        
        // Banner modal elements
        this.elements.bannerMessage = document.querySelector('.banner-message');
        this.elements.believeBtn = document.getElementById('btn-believe');
        this.elements.ignoreBtn = document.getElementById('btn-ignore');
        
        // Connection status
        this.elements.connectionStatus = document.getElementById('connection-status');
        this.elements.statusDot = document.querySelector('.status-dot');
        this.elements.statusText = document.querySelector('#connection-status .status-text');
    }
    
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Lobby events
        this.elements.joinBtn.addEventListener('click', () => this.joinLobby());
        this.elements.startBtn.addEventListener('click', () => this.startGame());
        this.elements.codenameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.joinLobby();
        });
        
        // Planning phase events
        this.elements.selectDefense.addEventListener('change', () => this.handleDefenseChange());
        this.elements.ipSlider.addEventListener('input', () => this.updateIPDisplay());
        this.elements.bannerInput.addEventListener('input', () => this.updateCharCount());
        this.elements.submitBtn.addEventListener('click', () => this.submitTurn());
        
        // Resolution events
        this.elements.continueBtn.addEventListener('click', () => this.continueToNextRound());
        
        // Banner modal events
        this.elements.believeBtn.addEventListener('click', () => this.handleBannerChoice('believe'));
        this.elements.ignoreBtn.addEventListener('click', () => this.handleBannerChoice('ignore'));
        
        // Prevent form submission on Enter for most inputs
        document.querySelectorAll('input, select').forEach(element => {
            element.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && element !== this.elements.codenameInput) {
                    e.preventDefault();
                }
            });
        });
        
        // Handle page visibility changes (for reconnection)
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.isConnected) {
                this.connectToServer();
            }
        });
    }
    
    /**
     * Initialize audio system
     */
    initializeAudio() {
        const audioIds = ['anvil', 'piano', 'explosion', 'suspense', 'victory'];
        
        audioIds.forEach(id => {
            const element = document.getElementById(`audio-${id}`);
            if (element) {
                this.audioElements[id] = element;
                element.volume = 0.7;
                
                // Handle audio loading errors gracefully
                element.addEventListener('error', () => {
                    console.warn(`Failed to load audio: ${id}`);
                });
            }
        });
        
        // Test audio context on first user interaction
        document.addEventListener('click', this.enableAudio.bind(this), { once: true });
        document.addEventListener('touchstart', this.enableAudio.bind(this), { once: true });
    }
    
    /**
     * Enable audio context (required for mobile browsers)
     */
    enableAudio() {
        Object.values(this.audioElements).forEach(audio => {
            if (audio && audio.play) {
                audio.play().then(() => {
                    audio.pause();
                    audio.currentTime = 0;
                }).catch(() => {
                    // Audio playback failed, likely due to autoplay policy
                });
            }
        });
    }
    
    /**
     * Play audio effect
     */
    playAudio(audioId, options = {}) {
        if (!this.audioEnabled || !this.audioElements[audioId]) return;
        
        const audio = this.audioElements[audioId];
        const { volume = 0.7, loop = false } = options;
        
        try {
            audio.volume = volume;
            audio.loop = loop;
            audio.currentTime = 0;
            
            const playPromise = audio.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {
                    // Autoplay was prevented, that's okay
                });
            }
        } catch (error) {
            console.warn(`Error playing audio ${audioId}:`, error);
        }
    }
    
    /**
     * Stop audio
     */
    stopAudio(audioId) {
        if (this.audioElements[audioId]) {
            this.audioElements[audioId].pause();
            this.audioElements[audioId].currentTime = 0;
        }
    }
    
    /**
     * Connect to WebSocket server
     */
    connectToServer() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.updateConnectionStatus(true);
                console.log('Connected to server');
            });
            
            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                console.log('Disconnected from server');
                this.handleReconnection();
            });
            
            this.socket.on('connect_error', (error) => {
                console.error('Connection error:', error);
                this.updateConnectionStatus(false);
                this.handleReconnection();
            });
            
            // Game event handlers
            this.setupGameEventHandlers();
            
        } catch (error) {
            console.error('Failed to initialize WebSocket connection:', error);
            this.updateConnectionStatus(false);
        }
    }
    
    /**
     * Set up WebSocket event handlers for game events
     */
    setupGameEventHandlers() {
        // Lobby events
        this.socket.on('lobbyJoined', (data) => this.handleLobbyJoined(data));
        this.socket.on('lobbyUpdate', (data) => this.handleLobbyUpdate(data));
        this.socket.on('gameStarted', (data) => this.handleGameStarted(data));
        
        // Game events
        this.socket.on('playerSubmitted', (data) => this.handlePlayerSubmitted(data));
        this.socket.on('turnResult', (data) => this.handleTurnResult(data));
        this.socket.on('gameStateSnapshot', (data) => this.handleGameStateSnapshot(data));
        this.socket.on('gameOver', (data) => this.handleGameOver(data));
        
        // Banner events
        this.socket.on('bannerChoice', (data) => this.handleBannerChoiceRequest(data));
        
        // Master Plan system
        this.socket.on('masterPlanInfo', (data) => this.handleMasterPlanInfo(data));
        
        // Alliance system
        this.socket.on('allianceInfo', (data) => this.handleAllianceInfo(data));
        this.socket.on('allianceCreated', (data) => this.handleAllianceCreated(data));
        
        // Final Showdown
        this.socket.on('finalShowdownStarted', (data) => this.handleFinalShowdownStarted(data));
        this.socket.on('showdownActionSubmitted', (data) => this.handleShowdownActionSubmitted(data));
        
        // Error handling
        this.socket.on('error', (error) => this.handleServerError(error));
    }
    
    /**
     * Handle reconnection attempts
     */
    handleReconnection() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
            
            setTimeout(() => {
                if (!this.isConnected) {
                    console.log(`Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
                    this.connectToServer();
                }
            }, delay);
        } else {
            this.showError('Connection lost. Please refresh the page to reconnect.');
        }
    }
    
    /**
     * Update connection status indicator
     */
    updateConnectionStatus(connected) {
        if (connected) {
            this.elements.statusDot.className = 'status-dot connected';
            this.elements.statusText.textContent = 'Connected';
        } else {
            this.elements.statusDot.className = 'status-dot disconnected';
            this.elements.statusText.textContent = 'Disconnected';
        }
    }
    
    /**
     * Join lobby
     */
    joinLobby() {
        const codename = this.elements.codenameInput.value.trim();
        
        if (!codename) {
            this.showLobbyStatus('Please enter a codename', 'error');
            return;
        }
        
        if (codename.length > 16) {
            this.showLobbyStatus('Codename must be 16 characters or less', 'error');
            return;
        }
        
        if (!this.isConnected) {
            this.showLobbyStatus('Not connected to server. Please wait...', 'error');
            return;
        }
        
        this.socket.emit('joinLobby', { codename });
        this.elements.joinBtn.disabled = true;
        this.showLobbyStatus('Joining lobby...', 'info');
    }
    
    /**
     * Start game (host only)
     */
    startGame() {
        if (!this.gameState.isHost) return;
        
        this.socket.emit('startGame');
        this.elements.startBtn.disabled = true;
        this.showLobbyStatus('Starting game...', 'info');
    }
    
    /**
     * Handle lobby joined response
     */
    handleLobbyJoined(data) {
        if (data.success) {
            this.gameState.myCodename = data.codename;
            this.gameState.isHost = data.isHost;
            this.showLobbyStatus(`Welcome, Agent ${data.codename}!`, 'success');
            this.elements.codenameInput.disabled = true;
        } else {
            this.showLobbyStatus(data.message || 'Failed to join lobby', 'error');
            this.elements.joinBtn.disabled = false;
        }
    }
    
    /**
     * Handle lobby updates
     */
    handleLobbyUpdate(data) {
        this.gameState.players = data.players;
        this.updatePlayerList();
        this.updateStartButton();
    }
    
    /**
     * Handle game started
     */
    handleGameStarted(data) {
        console.log('Game started:', data);
        this.gameState.gameStarted = true;
        this.gameState.players = data.players || [];
        this.gameState.roundNumber = data.roundNumber || 1;
        
        this.showGame();
        this.startPlanningPhase();
        
        // Request Master Plan information
        this.socket.emit('getMasterPlan');
        
        // Request alliance information
        this.socket.emit('getAlliances');
    }
    
    /**
     * Show lobby interface
     */
    showLobby() {
        this.elements.lobbyOverlay.classList.remove('hidden');
        this.elements.lobbyOverlay.classList.add('active');
        this.elements.gameOverlay.classList.add('hidden');
        this.elements.gameOverlay.classList.remove('active');
    }
    
    /**
     * Show game interface
     */
    showGame() {
        this.elements.lobbyOverlay.classList.add('hidden');
        this.elements.lobbyOverlay.classList.remove('active');
        this.elements.gameOverlay.classList.remove('hidden');
        this.elements.gameOverlay.classList.add('active');
        
        this.updateHUD();
        this.showPlanningUI();
    }
    
    /**
     * Show lobby status message
     */
    showLobbyStatus(message, type = 'info') {
        const statusElement = this.elements.lobbyStatus.querySelector('.status-text');
        statusElement.textContent = message;
        
        // Add type-specific styling if needed
        const container = this.elements.lobbyStatus;
        container.className = 'status-messages';
        if (type === 'error') {
            container.style.background = '#ffebee';
            container.style.borderColor = '#f44336';
        } else if (type === 'success') {
            container.style.background = '#e8f5e8';
            container.style.borderColor = '#4caf50';
        } else {
            container.style.background = '';
            container.style.borderColor = '';
        }
    }
    
    /**
     * Update player list in lobby
     */
    updatePlayerList() {
        const container = this.elements.playerListLobby;
        container.innerHTML = '';
        
        Object.values(this.gameState.players).forEach(player => {
            const playerElement = document.createElement('div');
            playerElement.className = 'player-item';
            
            playerElement.innerHTML = `
                <span class="player-name">${player.codename}</span>
                <span class="player-status">${player.isHost ? 'Host' : 'Ready'}</span>
            `;
            
            container.appendChild(playerElement);
        });
    }
    
    /**
     * Update start button visibility
     */
    updateStartButton() {
        const playerCount = Object.keys(this.gameState.players).length;
        const canStart = this.gameState.isHost && playerCount >= 2;
        
        this.elements.startBtn.disabled = !canStart;
        this.elements.startBtn.style.display = this.gameState.isHost ? 'block' : 'none';
    }
    
    /**
     * Update HUD with current player states
     */
    updateHUD() {
        const container = this.elements.hudContainer;
        container.innerHTML = '';
        
        Object.values(this.gameState.players).forEach(player => {
            const hudElement = document.createElement('div');
            hudElement.className = 'hud-player';
            hudElement.innerHTML = `
                <div class="hud-avatar" style="background: ${this.getPlayerColor(player.codename)}"></div>
                <div class="hud-codename">${player.codename}</div>
                <div class="hud-ip">
                    <span class="ip-icon"></span>
                    <span>${player.ip || 0}</span>
                </div>
                <div class="hud-status status-${player.status || 'active'}"></div>
                <div class="hud-gadgets">
                    ${(player.gadgets || []).slice(0, 3).map(gadget => 
                        `<div class="gadget-icon" title="${gadget}"></div>`
                    ).join('')}
                </div>
            `;
            
            container.appendChild(hudElement);
        });
    }
    
    /**
     * Get a consistent color for a player based on their codename
     */
    getPlayerColor(codename) {
        const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3'];
        let hash = 0;
        for (let i = 0; i < codename.length; i++) {
            hash = codename.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }
    
    /**
     * Start planning phase
     */
    startPlanningPhase() {
        this.gameState.phase = 'planning';
        this.gameState.turnSubmitted = false;
        this.resetPlanningData();
        this.populateActionDropdowns();
        this.updateIPSlider();
        this.showPlanningUI();
        this.startTimer(90); // 90 second planning phase
    }
    
    /**
     * Reset planning data
     */
    resetPlanningData() {
        this.planningData = {
            offense: '',
            defense: '',
            target: '',
            ipSpend: 0,
            bannerMessage: ''
        };
        
        this.elements.selectOffense.value = '';
        this.elements.selectDefense.value = '';
        this.elements.selectTarget.value = '';
        this.elements.ipSlider.value = 0;
        this.elements.bannerInput.value = '';
        this.updateIPDisplay();
        this.updateCharCount();
        this.hideBannerSection();
        this.hideSubmissionStatus();
    }
    
    /**
     * Populate action dropdowns
     */
    populateActionDropdowns() {
        // Offensive operations
        const offensiveOptions = [
            { value: 'assassination', text: 'Assassination' },
            { value: 'sabotage', text: 'Sabotage' },
            { value: 'exposure', text: 'Exposure' },
            { value: 'surveillance', text: 'Surveillance' },
            { value: 'infiltration', text: 'Infiltration' },
            { value: 'assetTheft', text: 'Asset Theft' },
            { value: 'misinformation', text: 'Misinformation' },
            { value: 'networkAttack', text: 'Network Attack' },
            { value: 'resourceDenial', text: 'Resource Denial' },
            { value: 'falseFlag', text: 'False Flag' }
        ];
        
        // Add alliance disruption if more than 2 players
        if (Object.keys(this.gameState.players).length > 2) {
            offensiveOptions.push({ value: 'allianceDisruption', text: 'Alliance Disruption' });
        }
        
        this.populateSelect(this.elements.selectOffense, offensiveOptions);
        
        // Defensive measures
        const defensiveOptions = [
            { value: 'safeHouse', text: 'Safe House' },
            { value: 'bodyguardDetail', text: 'Bodyguard Detail' },
            { value: 'mobileOperations', text: 'Mobile Operations' },
            { value: 'underground', text: 'Underground' },
            { value: 'sweepClear', text: 'Sweep & Clear' },
            { value: 'falseIdentity', text: 'False Identity' },
            { value: 'counterSurveillance', text: 'Counter-Surveillance' },
            { value: 'disinformation', text: 'Disinformation' },
            { value: 'preemptiveStrike', text: 'Preemptive Strike' },
            { value: 'honeypotOps', text: 'Honeypot Operations' },
            { value: 'informationWarfare', text: 'Information Warfare (Biplane Banner)' }
        ];
        
        // Add alliance building if more than 2 players
        if (Object.keys(this.gameState.players).length > 2) {
            defensiveOptions.push({ value: 'allianceBuilding', text: 'Alliance Building' });
        }
        
        this.populateSelect(this.elements.selectDefense, defensiveOptions);
        
        // Target selection (exclude self, captured, and eliminated players)
        this.updateTargetDropdown();
    }
    
    /**
     * Populate a select element with options
     */
    populateSelect(selectElement, options) {
        // Keep the first default option
        const defaultOption = selectElement.querySelector('option[value=""]');
        selectElement.innerHTML = '';
        if (defaultOption) {
            selectElement.appendChild(defaultOption);
        }
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            selectElement.appendChild(optionElement);
        });
    }
    
    /**
     * Update target dropdown based on current game state
     */
    updateTargetDropdown() {
        const targetOptions = [];
        
        Object.values(this.gameState.players).forEach(player => {
            // Exclude self and non-targetable players
            if (player.codename !== this.gameState.myCodename && 
                (!player.status || ['active', 'compromised', 'burned'].includes(player.status))) {
                targetOptions.push({
                    value: player.codename,
                    text: player.codename
                });
            }
        });
        
        this.populateSelect(this.elements.selectTarget, targetOptions);
    }
    
    /**
     * Handle defense selection change
     */
    handleDefenseChange() {
        const defense = this.elements.selectDefense.value;
        
        if (defense === 'informationWarfare') {
            this.showBannerSection();
        } else {
            this.hideBannerSection();
        }
    }
    
    /**
     * Show banner message section
     */
    showBannerSection() {
        this.elements.bannerSection.classList.remove('hidden');
    }
    
    /**
     * Hide banner message section
     */
    hideBannerSection() {
        this.elements.bannerSection.classList.add('hidden');
    }
    
    /**
     * Update IP slider based on current player IP
     */
    updateIPSlider() {
        const currentPlayer = this.gameState.players[this.gameState.myCodename];
        const maxIP = currentPlayer ? currentPlayer.ip || 0 : 0;
        
        this.elements.ipSlider.max = maxIP;
        this.elements.ipAvailable.textContent = maxIP;
        this.updateIPDisplay();
    }
    
    /**
     * Update IP display
     */
    updateIPDisplay() {
        const value = this.elements.ipSlider.value;
        this.elements.ipDisplay.textContent = value;
        this.planningData.ipSpend = parseInt(value);
    }
    
    /**
     * Update character count for banner message
     */
    updateCharCount() {
        const length = this.elements.bannerInput.value.length;
        this.elements.charCount.textContent = `${length}/50`;
        this.planningData.bannerMessage = this.elements.bannerInput.value;
    }
    
    /**
     * Submit turn
     */
    submitTurn() {
        if (this.gameState.turnSubmitted) return;
        
        // Validate required fields
        if (!this.elements.selectOffense.value || !this.elements.selectDefense.value) {
            this.showError('Please select both offense and defense actions');
            return;
        }
        
        // If Information Warfare is selected, banner message is required
        if (this.elements.selectDefense.value === 'informationWarfare' && 
            !this.elements.bannerInput.value.trim()) {
            this.showError('Please enter a banner message for Information Warfare');
            return;
        }
        
        // Collect turn data
        const turnData = {
            offense: this.elements.selectOffense.value,
            defense: this.elements.selectDefense.value,
            target: this.elements.selectTarget.value || null,
            ipSpend: parseInt(this.elements.ipSlider.value),
            bannerMessage: this.elements.selectDefense.value === 'informationWarfare' ? 
                          this.elements.bannerInput.value.trim() : ''
        };
        
        // Submit to server
        this.socket.emit('submitAction', turnData);
        this.gameState.turnSubmitted = true;
        this.showSubmissionStatus();
        this.disablePlanningInputs();
    }
    
    /**
     * Show submission status
     */
    showSubmissionStatus() {
        this.elements.submissionStatus.classList.remove('hidden');
        this.elements.submitBtn.disabled = true;
        this.elements.submitBtn.textContent = 'TURN SUBMITTED';
    }
    
    /**
     * Hide submission status
     */
    hideSubmissionStatus() {
        this.elements.submissionStatus.classList.add('hidden');
        this.elements.submitBtn.disabled = false;
        this.elements.submitBtn.textContent = 'SUBMIT TURN';
    }
    
    /**
     * Disable planning inputs after submission
     */
    disablePlanningInputs() {
        this.elements.selectOffense.disabled = true;
        this.elements.selectDefense.disabled = true;
        this.elements.selectTarget.disabled = true;
        this.elements.ipSlider.disabled = true;
        this.elements.bannerInput.disabled = true;
    }
    
    /**
     * Enable planning inputs
     */
    enablePlanningInputs() {
        this.elements.selectOffense.disabled = false;
        this.elements.selectDefense.disabled = false;
        this.elements.selectTarget.disabled = false;
        this.elements.ipSlider.disabled = false;
        this.elements.bannerInput.disabled = false;
    }
    
    /**
     * Show planning UI
     */
    showPlanningUI() {
        this.elements.planningUI.classList.remove('hidden');
        this.elements.resolutionUI.classList.add('hidden');
        this.enablePlanningInputs();
    }
    
    /**
     * Show resolution UI
     */
    showResolutionUI() {
        this.elements.planningUI.classList.add('hidden');
        this.elements.resolutionUI.classList.remove('hidden');
    }
    
    /**
     * Start countdown timer
     */
    startTimer(seconds) {
        this.gameState.timer = seconds;
        this.updateTimerDisplay();
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        
        this.timerInterval = setInterval(() => {
            this.gameState.timer--;
            this.updateTimerDisplay();
            
            if (this.gameState.timer <= 0) {
                clearInterval(this.timerInterval);
                this.handleTimerExpired();
            }
        }, 1000);
    }
    
    /**
     * Update timer display
     */
    updateTimerDisplay() {
        const minutes = Math.floor(this.gameState.timer / 60);
        const seconds = this.gameState.timer % 60;
        const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        this.elements.timerDisplay.textContent = timeString;
        
        // Change color when time is running low
        if (this.gameState.timer <= 10) {
            this.elements.timerDisplay.style.color = '#F44336';
            this.elements.timerDisplay.style.animation = 'pulse 1s infinite';
        } else {
            this.elements.timerDisplay.style.color = '';
            this.elements.timerDisplay.style.animation = '';
        }
    }
    
    /**
     * Handle timer expiration
     */
    handleTimerExpired() {
        if (this.gameState.phase === 'planning' && !this.gameState.turnSubmitted) {
            // Auto-submit with defaults
            this.autoSubmitDefaults();
        }
    }
    
    /**
     * Auto-submit default actions when timer expires
     */
    autoSubmitDefaults() {
        const defaultTurn = {
            offense: 'surveillance',
            defense: 'safeHouse',
            target: null,
            ipSpend: 0,
            bannerMessage: ''
        };
        
        this.socket.emit('submitAction', defaultTurn);
        this.gameState.turnSubmitted = true;
        this.showLobbyStatus('Time expired - default actions submitted', 'info');
    }
    
    /**
     * Handle player submission notification
     */
    handlePlayerSubmitted(data) {
        // Update UI to show which players have submitted
        console.log(`Player ${data.codename} submitted their turn`);
        // Could add visual indication in HUD
    }
    
    /**
     * Handle turn results
     */
    handleTurnResult(data) {
        this.gameState.phase = 'resolution';
        this.gameState.players = data.players;
        this.gameState.currentRound = data.round;
        
        this.stopAudio('suspense');
        this.updateHUD();
        this.displayTurnResults(data.results);
        this.showResolutionUI();
        
        // Play appropriate sound effects based on results
        this.playResultSounds(data.results);
    }
    
    /**
     * Display turn results
     */
    displayTurnResults(results) {
        const container = this.elements.resolutionContent;
        container.innerHTML = '';
        
        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'resolution-item';
            
            resultElement.innerHTML = `
                <h4>${result.attacker} vs ${result.defender}</h4>
                <p><strong>Action:</strong> ${result.offense} vs ${result.defense}</p>
                <p><strong>Result:</strong> ${result.success ? 'Success' : 'Failed'}</p>
                <p><strong>Effects:</strong> ${result.description}</p>
                ${result.ipChanges ? `<p><strong>IP Changes:</strong> ${result.ipChanges}</p>` : ''}
                ${result.statusChanges ? `<p><strong>Status Changes:</strong> ${result.statusChanges}</p>` : ''}
            `;
            
            container.appendChild(resultElement);
        });
    }
    
    /**
     * Play sound effects based on results
     */
    playResultSounds(results) {
        // Play different sounds based on what happened
        const hasExplosion = results.some(r => r.offense === 'sabotage' && r.success);
        const hasAnvil = results.some(r => r.offense === 'assassination' && r.success);
        const hasPiano = results.some(r => r.defense === 'preemptiveStrike' && r.success);
        
        setTimeout(() => {
            if (hasExplosion) this.playAudio('explosion');
            else if (hasAnvil) this.playAudio('anvil');
            else if (hasPiano) this.playAudio('piano');
        }, 500);
    }
    
    /**
     * Continue to next round
     */
    continueToNextRound() {
        if (this.gameState.phase === 'resolution') {
            this.startPlanningPhase();
        }
    }
    
    /**
     * Handle banner choice request
     */
    handleBannerChoiceRequest(data) {
        this.gameState.phase = 'bannerChoice';
        this.elements.bannerMessage.textContent = data.message;
        this.elements.bannerModal.classList.remove('hidden');
        
        // Auto-timeout after 10 seconds
        setTimeout(() => {
            if (this.gameState.phase === 'bannerChoice') {
                this.handleBannerChoice('ignore'); // Default to ignore
            }
        }, 10000);
    }
    
    /**
     * Handle banner choice
     */
    handleBannerChoice(choice) {
        if (this.gameState.phase !== 'bannerChoice') return;
        
        this.socket.emit('bannerChoice', { choice });
        this.elements.bannerModal.classList.add('hidden');
        this.gameState.phase = 'waitingForResolution';
    }
    
    /**
     * Handle game state snapshot (for reconnection)
     */
    handleGameStateSnapshot(data) {
        this.gameState = { ...this.gameState, ...data };
        
        if (data.phase === 'lobby') {
            this.showLobby();
        } else {
            this.showGame();
            
            if (data.phase === 'planning') {
                this.startPlanningPhase();
                if (data.timeRemaining) {
                    this.startTimer(data.timeRemaining);
                }
            } else if (data.phase === 'resolution') {
                this.showResolutionUI();
            }
        }
        
        this.updateHUD();
    }
    
    /**
     * Handle game over
     */
    handleGameOver(data) {
        this.gameState.phase = 'gameOver';
        this.stopAudio('suspense');
        this.playAudio('victory');
        
        this.showGameOverScreen(data);
    }
    
    /**
     * Show game over screen
     */
    showGameOverScreen(data) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Mission Complete!</h2>
                </div>
                <div class="modal-body">
                    <h3>Victory: ${data.victoryType}</h3>
                    <p><strong>Winner:</strong> ${data.winner}</p>
                    <p>${data.description}</p>
                    
                    <h4>Final Standings:</h4>
                    <div class="final-standings">
                        ${Object.values(data.finalStandings || {}).map(player => `
                            <div class="player-final">
                                <span>${player.codename}</span>
                                <span>IP: ${player.ip}</span>
                                <span>Status: ${player.status}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="btn btn-primary" onclick="location.reload()">Play Again</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    /**
     * Handle server errors
     */
    handleServerError(error) {
        console.error('Server error:', error);
        this.showError(error.message || 'An unexpected error occurred');
    }
    
    /**
     * Show error message
     */
    showError(message) {
        // Create temporary error notification
        const errorElement = document.createElement('div');
        errorElement.className = 'error-notification';
        errorElement.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #f44336;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            border: 2px solid black;
            z-index: 9999;
            font-weight: bold;
            text-align: center;
            max-width: 300px;
        `;
        errorElement.textContent = message;
        
        document.body.appendChild(errorElement);
        
        setTimeout(() => {
            if (errorElement.parentNode) {
                errorElement.parentNode.removeChild(errorElement);
            }
        }, 5000);
    }
    
    /**
     * Handle Master Plan information
     */
    handleMasterPlanInfo(data) {
        this.gameState.masterPlan = data;
        this.updateMasterPlanUI();
    }
    
    /**
     * Handle Alliance information
     */
    handleAllianceInfo(data) {
        this.gameState.alliances = data;
        this.updateAllianceUI();
    }
    
    /**
     * Handle Alliance creation
     */
    handleAllianceCreated(data) {
        this.showNotification(`Alliance formed: ${data.members.join(' & ')}`, 'info');
        this.socket.emit('getAlliances'); // Refresh alliance data
    }
    
    /**
     * Handle Final Showdown start
     */
    handleFinalShowdownStarted(data) {
        this.gameState.phase = 'finalShowdown';
        this.gameState.showdown = data.showdown;
        this.showFinalShowdownUI(data);
    }
    
    /**
     * Handle Showdown action submission
     */
    handleShowdownActionSubmitted(data) {
        this.showNotification('Showdown action submitted!', 'success');
    }
    
    /**
     * Update Master Plan UI
     */
    updateMasterPlanUI() {
        const planData = this.gameState.masterPlan;
        if (!planData) return;
        
        // Create or update Master Plan indicator in HUD
        const planIndicator = document.getElementById('master-plan-indicator') || 
                             this.createMasterPlanIndicator();
        
        planIndicator.innerHTML = `
            <div class="master-plan-info">
                <h4>${planData.name}</h4>
                <p>${planData.description}</p>
                <div class="progress-indicator ${planData.completed ? 'completed' : ''}">
                    ${planData.completed ? '✓ COMPLETED' : 'IN PROGRESS'}
                </div>
            </div>
        `;
    }
    
    /**
     * Create Master Plan UI indicator
     */
    createMasterPlanIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'master-plan-indicator';
        indicator.className = 'master-plan-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: #E53935;
            color: white;
            padding: 0.5rem;
            border-radius: 8px;
            border: 2px solid black;
            max-width: 250px;
            z-index: 1000;
            font-size: 0.8rem;
        `;
        
        document.body.appendChild(indicator);
        return indicator;
    }
    
    /**
     * Update Alliance UI
     */
    updateAllianceUI() {
        const allianceData = this.gameState.alliances;
        if (!allianceData) return;
        
        // Update alliance indicators in HUD
        const playerAlliances = allianceData.playerAlliances || [];
        
        if (playerAlliances.length > 0) {
            const allianceIndicator = document.getElementById('alliance-indicator') || 
                                     this.createAllianceIndicator();
            
            allianceIndicator.innerHTML = `
                <div class="alliance-info">
                    <h4>Your Alliances</h4>
                    ${playerAlliances.map(alliance => `
                        <div class="alliance-item">
                            <strong>${alliance.partner}</strong>
                            <span class="alliance-type">${alliance.type}</span>
                            <span class="alliance-duration">Rounds: ${alliance.duration}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }
    
    /**
     * Create Alliance UI indicator
     */
    createAllianceIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'alliance-indicator';
        indicator.className = 'alliance-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 100px;
            left: 20px;
            background: #1E88E5;
            color: white;
            padding: 0.5rem;
            border-radius: 8px;
            border: 2px solid black;
            max-width: 250px;
            z-index: 1000;
            font-size: 0.8rem;
        `;
        
        document.body.appendChild(indicator);
        return indicator;
    }
    
    /**
     * Show Final Showdown UI
     */
    showFinalShowdownUI(data) {
        const showdownModal = document.createElement('div');
        showdownModal.className = 'modal showdown-modal';
        showdownModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>FINAL SHOWDOWN!</h2>
                </div>
                <div class="modal-body">
                    <h3>${data.alliance_victory.condition}</h3>
                    <p>${data.alliance_victory.description}</p>
                    
                    <div class="showdown-participants">
                        <h4>Participants:</h4>
                        ${data.showdown.participants.map(p => `<span class="participant">${p}</span>`).join(' vs ')}
                    </div>
                    
                    <div class="showdown-rules">
                        <h4>Rules:</h4>
                        <p>${data.showdown.rules}</p>
                        <p>Each participant receives +${data.showdown.ip_bonus} IP</p>
                    </div>
                    
                    <div class="showdown-actions">
                        <h4>Choose your action:</h4>
                        <button class="btn btn-danger" onclick="window.jamesBlandClient.submitShowdownAction('assassination')">
                            Assassination
                        </button>
                        <button class="btn btn-warning" onclick="window.jamesBlandClient.submitShowdownAction('sabotage')">
                            Sabotage
                        </button>
                    </div>
                    
                    <div class="showdown-timer">
                        Time remaining: <span id="showdown-timer">${data.showdown.time_limit}</span>s
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(showdownModal);
        
        // Start countdown timer
        this.startShowdownTimer(data.showdown.time_limit);
    }
    
    /**
     * Submit Final Showdown action
     */
    submitShowdownAction(action) {
        this.socket.emit('submitShowdownAction', { action });
        
        // Disable action buttons
        const buttons = document.querySelectorAll('.showdown-actions button');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });
    }
    
    /**
     * Start Final Showdown timer
     */
    startShowdownTimer(seconds) {
        const timerElement = document.getElementById('showdown-timer');
        let remaining = seconds;
        
        const interval = setInterval(() => {
            remaining--;
            if (timerElement) {
                timerElement.textContent = remaining;
                
                if (remaining <= 10) {
                    timerElement.style.color = '#f44336';
                    timerElement.style.fontWeight = 'bold';
                }
            }
            
            if (remaining <= 0) {
                clearInterval(interval);
                // Auto-submit if no action taken
                if (this.gameState.phase === 'finalShowdown') {
                    this.submitShowdownAction('assassination'); // Default action
                }
            }
        }, 1000);
    }
    
    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid black;
            z-index: 9999;
            font-weight: bold;
            max-width: 300px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 4000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.jamesBlandClient = new JamesBlandClient();
});

// Add CSS animation for timer pulse
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .error-notification {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translate(-50%, -50%) scale(0.8); opacity: 0; }
        to { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
`;
document.head.appendChild(style); 