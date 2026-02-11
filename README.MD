# 🚨 DisasterNet – Offline-First Emergency Communication System (Python)

> **An offline-first, peer-to-peer emergency messaging platform designed for disaster scenarios where internet connectivity is unreliable or unavailable.**

This project demonstrates **distributed systems design, peer-to-peer networking, real-time APIs, and offline-first architecture** using Python.

---

##  System Overview

DisasterNet allows devices on the same local network (LAN / ad-hoc WiFi) to discover each other, form peer-to-peer connections, exchange messages, and sync data — **without requiring the internet**.

A Python backend exposes the P2P network through a **REST API and WebSockets**, enabling a modern web dashboard for monitoring and communication.

---

## 🗺️ Full System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Web Dashboard                        │
│                     (React / Vue Frontend)                  │
│                                                             │
│  • Peer List              • Rooms                           │
│  • Live Messages          • Network Status                  │
│  • Offline Indicator      • User Identity                   │
└───────────────▲───────────────────────▲─────────────────────┘
                │ REST API               │ WebSockets (Realtime)
                │                        │
┌───────────────┴────────────────────────┴────────────────────┐
│                    Python Backend API                        │
│                        (FastAPI)                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ API Layer                                              │  │
│  │ • Authentication & Identity                            │  │
│  │ • Rooms & Membership                                   │  │
│  │ • Message History                                      │  │
│  │ • Peer Status                                          │  │
│  └───────────────────────▲───────────────────────────────┘  │
│                          │ Internal Events                   │
│  ┌───────────────────────┴───────────────────────────────┐  │
│  │ Realtime Event Bus                                     │  │
│  │ • WebSocket Broadcast                                  │  │
│  │ • Message Fan-out                                      │  │
│  └───────────────────────▲───────────────────────────────┘  │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────────────┐  │
│  │ P2P Networking Engine                                  │  │
│  │ • Peer Discovery (LAN / mDNS / UDP)                    │  │
│  │ • Node Identity (Public/Private Keys)                  │  │
│  │ • Gossip-based Message Propagation                     │  │
│  │ • Room-based Routing                                   │  │
│  └───────────────────────▲───────────────────────────────┘  │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────────────┐  │
│  │ Local Persistence Layer                                │  │
│  │ • Messages (Append-only)                               │  │
│  │ • Rooms                                                │  │
│  │ • Peers                                                │  │
│  │ • Sync State                                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Other DisasterNet Nodes                  │
│            (Same Stack Running on Other Devices)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Design Principles

### 1️⃣ Offline-First Architecture

* Internet connectivity is **optional**
* Each node works independently
* Messages are written to local storage first
* Automatic sync when peers reconnect

### 2️⃣ Peer-to-Peer Networking

* No central server required for communication
* LAN-based peer discovery
* Direct peer message exchange
* Gossip-style message propagation

### 3️⃣ API-Driven Design

* P2P complexity hidden behind REST APIs
* Clean separation between networking and UI
* Easy to extend or replace components

### 4️⃣ Real-Time Communication

* WebSockets used for:

  * Live messages
  * Peer join/leave events
  * Network health updates

---

## 🔐 Identity & Security Model

* Each node generates a **public/private key pair**
* User identity is derived from the public key
* Messages are:

  * Signed by sender
  * Verifiable by peers
* No central authentication server required

This model works **fully offline** and can optionally integrate with JWT/OAuth when internet access is available.

---

## 🗄️ Data Persistence Strategy

All data is stored locally to ensure availability during outages.

### Stored Entities

* Nodes / Peers
* Users & Identities
* Rooms
* Messages (append-only)
* Sync metadata

### Conflict Handling

* Messages are immutable
* Ordering via timestamp + sender ID
* Duplicate detection using message hashes

---

## 📡 API Capabilities (High-Level)

* Peer discovery & status
* Room creation & membership
* Message history retrieval
* Live message streaming
* Network health monitoring

---

## 🧪 Failure & Recovery Scenarios

✔ Network partitioning
✔ Sudden peer disconnects
✔ Device restarts
✔ Partial message delivery

System automatically recovers and resynchronizes when peers rejoin.

---

## 🚀 Why This Project Stands Out

This project demonstrates:

* ✅ Distributed systems thinking
* ✅ Peer-to-peer networking
* ✅ Offline-first design
* ✅ Real-time backend APIs
* ✅ Security-conscious identity handling
* ✅ Production-ready architecture

It goes far beyond basic CRUD applications and reflects **real-world system design skills**.

---

## 📑 API Contract (High-Level)

The backend exposes a clean REST + WebSocket interface that abstracts the peer-to-peer network.

### 🔐 Authentication & Identity

| Method | Endpoint     | Description                               |
| ------ | ------------ | ----------------------------------------- |
| POST   | `/auth/init` | Initialize node identity (key generation) |
| GET    | `/auth/me`   | Fetch local node identity                 |

> Authentication is local-first and works fully offline. Optional JWT/OAuth can be layered when internet access is available.

---

### 👥 Peer Management

| Method | Endpoint           | Description                    |
| ------ | ------------------ | ------------------------------ |
| GET    | `/peers`           | List currently connected peers |
| GET    | `/peers/{peer_id}` | Get peer details & status      |

Peers are discovered automatically via LAN discovery and updated in real time.

---

### 🏠 Rooms

| Method | Endpoint                 | Description          |
| ------ | ------------------------ | -------------------- |
| POST   | `/rooms`                 | Create a new room    |
| GET    | `/rooms`                 | List available rooms |
| POST   | `/rooms/{room_id}/join`  | Join a room          |
| POST   | `/rooms/{room_id}/leave` | Leave a room         |

Rooms are logical groupings used for message routing across the P2P network.

---

### 💬 Messages

| Method | Endpoint                    | Description           |
| ------ | --------------------------- | --------------------- |
| POST   | `/rooms/{room_id}/messages` | Send a message        |
| GET    | `/rooms/{room_id}/messages` | Fetch message history |

Messages are written locally first and then propagated to peers asynchronously.

---

### 📡 Network & Health

| Method | Endpoint      | Description                    |
| ------ | ------------- | ------------------------------ |
| GET    | `/status`     | Local node & network health    |
| GET    | `/sync/state` | Message synchronization status |

---

### 🔁 WebSocket Channels

| Channel        | Purpose                 |
| -------------- | ----------------------- |
| `/ws/messages` | Live message stream     |
| `/ws/peers`    | Peer join/leave updates |
| `/ws/status`   | Network health changes  |

---

## ⚙️ How It Works Internally (Message Lifecycle)

This section explains what happens end-to-end when a user sends a message.

---

### ✉️ Message Creation

1. User submits a message from the web dashboard
2. Frontend sends a request to the backend API
3. Backend assigns:

   * Message ID
   * Timestamp
   * Sender identity
   * Room ID
4. Message is cryptographically signed

---

### 💾 Local Persistence (Offline-First Rule)

5. Message is immediately stored in the local database
6. UI is updated optimistically via WebSocket

> At this point, the message is considered **successfully sent**, even if no peers are online.

---

### 🌐 Peer-to-Peer Propagation

7. P2P engine broadcasts the message to connected peers
8. Peers verify message signature
9. Valid messages are stored locally on each peer

Propagation uses a gossip-style approach to avoid reliance on a single node.

---

### 🔄 Synchronization & Recovery

10. If a peer was offline:

    * Missed messages are requested using sync metadata
    * Only unseen messages are transmitted
11. Duplicate messages are discarded using message hashes

---

### 📢 Real-Time Updates

12. Incoming messages trigger internal events
13. Events are pushed to all connected dashboards via WebSockets
14. UI updates instantly with new messages or peer changes

---

### 🧠 Failure Handling

* Network partition → messages queue locally
* Peer disconnect → no message loss
* Node restart → state restored from DB
* Partial delivery → automatic resync

This guarantees **eventual consistency** across peers.

---

## 🧭 Potential Extensions

* Internet relay nodes for WAN communication
* Mobile client (Android/iOS)
* Mesh network support
* Encrypted message storage
* Admin dashboard & analytics

---

## 👨‍💻 Author

**Skanda**
Bachelor of Engineering (BE)
Focus: Backend Systems, Distributed Systems, Python, Django, APIs

---

> *"Designed for chaos. Built for resilience."*
