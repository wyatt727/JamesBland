# James Bland: ACME Edition - Network Topology

## 1. Overview

James Bland: ACME Edition operates as a **local area network (LAN) only** application, designed for players connected to the same Wi-Fi network. This approach ensures low latency, eliminates internet dependencies, and provides a more intimate gaming experience for family/friend groups.

The network architecture follows a **centralized server model** where one device acts as the game host, running the Flask-SocketIO server, while all other devices connect as clients via WebSocket connections.

## 2. Network Architecture

### 2.1 Basic Topology

```
                     Wi-Fi Router
                         |
           +-------------+-------------+
           |             |             |
    [Host Device]   [Client 1]   [Client 2-6]
    (Game Server)   (Player)      (Players)
     Flask App      Browser       Browsers
```

**Components**:
- **Wi-Fi Router**: Provides local network infrastructure (192.168.x.x or 10.x.x.x)
- **Host Device**: Laptop/desktop running the Flask-SocketIO server
- **Client Devices**: Phones, tablets, or laptops with modern browsers
- **Network Protocol**: WebSocket over HTTP (ws://) for real-time communication

### 2.2 Detailed Network Flow

```
                           Router/Access Point
                          (192.168.1.1/24)
                                  |
                         Internal LAN Network
                                  |
           +----------------------+----------------------+
           |                      |                      |
    Host Machine               Client 1               Client 2-6
   (192.168.1.100)           (192.168.1.101)       (192.168.1.102-106)
        |                          |                      |
  Flask Server                 Browser                Browser
   Port 5000              WebSocket Client        WebSocket Client
        |                          |                      |
   Game Logic                   Game UI                Game UI
   State Management           Input Handling          Input Handling
   WebSocket Server           Event Processing        Event Processing
```

## 3. Connection Establishment

### 3.1 Server Startup Sequence

1. **Host Device Initialization**
   ```
   Host Device → Flask App starts on 0.0.0.0:5000
   Host Device → Binds to all network interfaces
   Host Device → WebSocket server ready for connections
   Host Device → Displays "Server running at http://[LAN_IP]:5000"
   ```

2. **Network Interface Detection**
   ```python
   # Server automatically detects LAN IP
   import socket
   
   def get_lan_ip():
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       s.connect(("8.8.8.8", 80))  # Connect to external address
       ip = s.getsockname()[0]     # Get local IP used for connection
       s.close()
       return ip
   ```

3. **Firewall Configuration**
   - Host firewall must allow inbound connections on port 5000
   - Router firewall typically allows internal LAN traffic by default
   - No port forwarding required (LAN-only operation)

### 3.2 Client Connection Sequence

1. **Client Discovery**
   ```
   Player → Opens browser on mobile device
   Player → Navigates to http://[HOST_IP]:5000
   Browser → Attempts HTTP connection to host
   Browser → Receives HTML/CSS/JS game assets
   Browser → Initiates WebSocket connection
   ```

2. **WebSocket Handshake**
   ```
   Client → WebSocket connection request to ws://[HOST_IP]:5000/socket.io/
   Server → Validates connection (same subnet check)
   Server → Accepts WebSocket upgrade
   Client → Connection established
   Server → Adds client to lobby
   ```

3. **Authentication & Registration**
   ```
   Client → Emits 'joinLobby' event with codename
   Server → Validates codename uniqueness
   Server → Assigns client ID and session
   Server → Broadcasts lobby update to all clients
   ```

## 4. Network Security

### 4.1 LAN-Only Restrictions

**IP Address Validation**
- Server only accepts connections from private IP ranges:
  - 192.168.0.0/16 (most home networks)
  - 10.0.0.0/8 (enterprise/advanced home networks) 
  - 172.16.0.0/12 (less common home networks)
- Rejects connections from public IP addresses
- Prevents accidental exposure to internet

**Subnet Enforcement**
```python
import ipaddress

def is_lan_connection(client_ip, server_ip):
    client = ipaddress.IPv4Address(client_ip)
    server = ipaddress.IPv4Address(server_ip)
    
    # Check if both are in same /24 subnet
    client_network = ipaddress.IPv4Network(f"{client_ip}/24", strict=False)
    return server in client_network
```

### 4.2 Data Protection

**Input Sanitization**
- All client input validated and sanitized
- Codenames: alphanumeric + spaces only, 3-15 characters
- Banner messages: plain text only, 50 character limit
- No executable code accepted from clients

**Session Management**
- Each client assigned unique session ID
- Session expires after 30 minutes of inactivity
- Reconnection requires re-authentication
- No persistent user accounts or stored credentials

### 4.3 Denial of Service Prevention

**Rate Limiting**
- Maximum 10 WebSocket messages per second per client
- Temporary ban (60 seconds) for excessive messaging
- Connection limit: 6 clients maximum per server

**Resource Protection**
- Game state stored in server memory only
- No database connections or file system writes
- Automatic cleanup of disconnected client data

## 5. Performance Considerations

### 5.1 Latency Optimization

**Local Network Advantages**
- Typical LAN latency: 1-5ms (vs 50-200ms internet)
- No ISP routing delays or bandwidth limitations
- Predictable performance characteristics

**WebSocket Efficiency**
- Persistent connections eliminate handshake overhead
- Binary data frames for game state updates
- Message compression for larger payloads

**Message Optimization**
```json
{
  "type": "turnResult",
  "data": {
    "r": 3,           // Round (compressed key)
    "res": [          // Results (compressed key)
      {
        "a": "Alice", "d": "Bob",
        "o": "assassination", "s": true,
        "ip": [3, -2]   // [attacker_delta, defender_delta]
      }
    ]
  }
}
```

### 5.2 Bandwidth Management

**Minimal Data Transfer**
- Game state updates: ~1-2KB per turn
- Real-time messages: ~100-500 bytes each
- Total bandwidth: <10KB/minute per client
- Suitable for basic Wi-Fi connections

**Asset Caching**
- All game assets (images, audio) cached on first load
- No streaming media or large file transfers
- Offline gameplay after initial asset download

### 5.3 Mobile Network Considerations

**Wi-Fi Requirements**
- 802.11n (Wi-Fi 4) or newer recommended
- 2.4GHz or 5GHz frequency bands supported
- Minimum 1 Mbps bandwidth per client (easily achievable)

**Battery Optimization**
- WebSocket keep-alive: 30 second intervals
- Reduced message frequency when possible
- Client-side animation throttling for performance

## 6. Network Troubleshooting

### 6.1 Common Connection Issues

**IP Address Discovery**
```bash
# Host discovers own IP
# Windows
ipconfig | findstr /i "IPv4"

# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Display format for players
echo "Players connect to: http://$(hostname -I | cut -d' ' -f1):5000"
```

**Firewall Configuration**
- **Windows**: Allow Python/Node.js through Windows Defender
- **macOS**: System Preferences → Security & Privacy → Firewall → Allow app
- **Linux**: `sudo ufw allow 5000` or equivalent

**Router Issues**
- AP/Client Isolation disabled (allow device-to-device communication)
- Guest network typically blocks inter-device communication
- Corporate/hotel Wi-Fi may block local connections

### 6.2 Network Diagnostics

**Connection Testing**
```bash
# Test basic connectivity
ping [HOST_IP]

# Test port accessibility  
telnet [HOST_IP] 5000

# Test HTTP access
curl http://[HOST_IP]:5000/
```

**Browser Console Diagnostics**
```javascript
// Check WebSocket connection status
console.log("Socket connected:", socket.connected);

// Monitor network events
socket.on('connect', () => console.log('Connected to server'));
socket.on('disconnect', () => console.log('Disconnected from server'));
socket.on('connect_error', (error) => console.log('Connection error:', error));
```

### 6.3 Performance Monitoring

**Server-Side Metrics**
```python
# Track active connections
active_connections = len(socketio.server.manager.rooms.get('/', {}))

# Monitor message rates
message_count_per_minute = 0
last_minute_timestamp = time.time()

# Memory usage tracking
import psutil
memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
```

**Client-Side Monitoring**
```javascript
// Network quality assessment
const pingStart = Date.now();
socket.emit('ping', pingStart);
socket.on('pong', (timestamp) => {
  const latency = Date.now() - timestamp;
  console.log(`Network latency: ${latency}ms`);
});
```

## 7. Network Reliability

### 7.1 Disconnection Handling

**Automatic Reconnection**
```javascript
// Client-side reconnection logic
socket.on('disconnect', () => {
  console.log('Connection lost, attempting to reconnect...');
  setTimeout(() => {
    socket.connect();
  }, 1000);  // Retry after 1 second
});

// Exponential backoff for repeated failures
let reconnectDelay = 1000;
const maxReconnectDelay = 10000;

socket.on('connect_error', () => {
  setTimeout(() => {
    socket.connect();
    reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay);
  }, reconnectDelay);
});
```

**Game State Recovery**
- Server maintains game state for 5 minutes after client disconnection
- Reconnecting clients receive complete state snapshot
- Game continues with remaining connected players
- Disconnected players can rejoin mid-game

### 7.2 Host Failure Recovery

**Host Migration** (Future Enhancement)
- Current design: single host failure ends game
- Potential improvement: migrate server state to new host
- Requires peer-to-peer state synchronization
- Not implemented in initial version

**Graceful Shutdown**
```python
# Server shutdown procedure
@atexit.register
def cleanup():
    socketio.emit('server_shutdown', {'message': 'Server shutting down'})
    time.sleep(2)  # Allow clients to receive message
    socketio.stop()
```

## 8. Scalability Limitations

### 8.1 Design Constraints

**Maximum Players**: 6 players per game server
- WebSocket connection limit based on server hardware
- Game design optimized for small group play
- More players would require UI/UX redesign

**Single Game Instance**
- Server runs one game at a time
- No multi-game lobby or matchmaking
- Focused on family/friend groups

### 8.2 Hardware Requirements

**Host Device Minimum Specs**
- **CPU**: Dual-core 1.5GHz or equivalent
- **RAM**: 2GB available memory
- **Network**: 802.11n Wi-Fi or Ethernet
- **OS**: Windows 10, macOS 10.14, or Ubuntu 18.04+

**Client Device Minimum Specs**
- **Browser**: Chrome 80+, Safari 13+, Firefox 75+
- **Network**: 802.11n Wi-Fi connection
- **RAM**: 1GB available memory
- **Display**: 320px minimum width (smartphone)

## 9. Future Network Enhancements

### 9.1 Potential Improvements

**Network Discovery**
- Automatic host detection via multicast/broadcast
- QR code generation for easy client connection
- mDNS/Bonjour service advertisement

**Connection Quality**
- Real-time latency monitoring and display
- Adaptive message compression based on network conditions
- Client-side prediction for improved responsiveness

**Peer-to-Peer Options**
- WebRTC data channels for direct client communication
- Distributed game state for improved reliability
- Reduced server load for large groups

### 9.2 Advanced Features

**Network Diagnostics Dashboard**
- Real-time connection status for all players
- Network quality metrics and alerts
- Automatic troubleshooting suggestions

**Offline Mode**
- Local storage of game state
- Sync when connection restored
- Support for temporary network interruptions

This network topology ensures reliable, low-latency gameplay while maintaining simplicity and security for local network environments. 