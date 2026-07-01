# ShadowLab
![Python Version](https://img.shields.io/badge/python-3.13.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Purpose](https://img.shields.io/badge/purpose-educational-orange.svg)
![New Feature](https://img.shields.io/badge/NEW-Post--Exploit%20Modules-red.svg)
> Python-based C2 Framework - Security Research Project

---

## ⚠️ Important Disclaimer

**THIS PROJECT IS FOR EDUCATIONAL AND AUTHORIZED SECURITY RESEARCH PURPOSES ONLY.**

This software is designed to help cybersecurity professionals, researchers, and students understand:
- Client-server architecture and network protocols
- Encryption and secure communication
- System-level programming concepts
- Red team operations and adversary emulation

**Usage Restrictions:**
- Only use on systems you own or have explicit written authorization to test
- Unauthorized access to computer systems is illegal and may result in criminal prosecution
- The author assumes no liability for any misuse or damage caused by this tool

By using this project, you agree to use it responsibly and ethically.

---

## 📋 Overview

![ShadowLab Tool Demo](assets/demo.gif)

> 📖 **Read the Technical Analysis:** [ShadowLab Architecture and Design](https://meetcyber.net/shadowlab-a-modular-c2-framework-architecture-built-with-python-for-modern-cybersecurity-research-7acb496e6784)

ShadowLab is a modular Command & Control (C2) framework built for hands-on cybersecurity research, red team lab practice, and defender education. It brings together encrypted transport, staged and unstaged payload generation, host reconnaissance, remote interaction, and a new extensible post-exploitation layer in one focused Python project.

### 🔥 NEW: Post-Exploit Module System

ShadowLab now includes a dedicated **Post-Exploit** workflow for extending an active session after the initial connection is established.

| Capability | What it adds |
|------------|--------------|
| **Dynamic Module Discovery** | Modules placed under `modules/` are discovered from their own `config.json` files |
| **Template-Based Payloads** | Module placeholders such as listener IP, port, and internal keys can be filled at runtime |
| **Agent-Side Registration** | Post-exploit modules can be staged, registered, and started through the encrypted session |
| **Controller Support** | Modules can expose their own server-side controller for interactive workflows |
| **Included Example** | Ships with a configurable `KEYLOGGER` module template and controller |

> Start a session, choose **Option 12 - Manage Post Exploits**, select a module, and launch it directly through the active agent channel.

ShadowLab demonstrates the lifecycle of remote administration tools, focusing on:

- **Socket Programming:** Low-level TCP communication using length-prefixed data packets.
- **Cryptography:** End-to-end encryption using the Fernet (AES-128) symmetric algorithm.
- **Payload Architecture:** Implementation of both Staged (dropper) and Unstaged (full-featured) delivery methods.
- **Post-Exploitation Modules:** Runtime module staging, template replacement, registration, and controller-backed execution.
- **Windows Integration:** Interacting with the OS via WMI, Registry, and Subprocess modules.

This project is ideal for:
- Cybersecurity students learning about C2 infrastructure
- Security researchers studying attack methodologies
- Red team professionals practicing adversary emulation
- Defenders understanding threats to build better defenses

---

## 🗺️ Educational Lab Roadmap & Engineering Evolution

> 🎯 **Educational Lab Mission:** ShadowLab is systematically architected not for malicious deployment, but as an **interactive, code-level educational laboratory**. The core mission is to dissect the internal mechanics of C2 (Command & Control) networks, exploring low-level socket communication, encryption lifecycles, and backend orchestration. It provides a hands-on environment for computer science students, educators, and security researchers to understand exactly *how* remote administration infrastructure operates from the inside out, bridging the gap between theoretical network concepts and practical software implementation.

<details>
<summary><b>📦 Phase 1: Core Lab Architecture & Synchronous Foundations (Click to expand)</b></summary>

- [x] **Fernet Encryption Pipeline:** End-to-end AES-128 transport layer encryption using unique symmetric keys to teach data-in-transit security hygiene.
- [x] **Length-Prefixed TCP Transport:** Built low-level socket communication utilizing structured data boundaries to demonstrate and solve the classic TCP packet fragmentation ("boundary") problem.
- [x] **Dual-Mode Payload Builder:** Automated compilation for both Staged (lightweight dropper) and Unstaged (standalone monolithic) payloads to analyze delivery chain mechanics.
- [x] **Host Reconnaissance:** Deep OS integration querying hardware metadata and active security software via native WMI structures for endpoint auditing simulation.
</details>

<details>
<summary><b>🔥 Phase 2: Dynamic Post-Exploitation Subsystem (Click to expand)</b></summary>

- [x] **Runtime Module Discovery:** Engineered an automated tracking engine that dynamically discovers standalone post-exploit plugins via modular config.json manifests, demonstrating runtime extensibility.
- [x] **Template-Based In-Memory Staging:** Implemented dynamic environment replacement (C2 IP, Ports, Keys) into staged payload templates to teach safe automation and obfuscation basics.
- [x] **Controller-Backed Session Extension:** Added specialized server-side interactive controller support (e.g., the integrated KEYLOGGER module) mapping dedicated sub-channels across the active transport session.
</details>

<details>
<summary><b>🏗️ Phase 3: Asynchronous Core Migration (Click to expand)</b></summary>

- [ ] **Asyncio Event Loop Core:** Migrating the blocking core loop into a fully non-blocking asynchronous architecture (asyncio.StreamReader/Writer) to demonstrate massive concurrent socket scaling. 🏗️ *In Progress*
- [ ] **Isolated Per-Agent Job Queues:** Implementing a multiplexed asynchronous queue structure to model background task scheduling and synchronization in high-performance networking. ⏳ *Planned*
- [ ] **Non-Blocking File I/O Workers:** Offloading heavy download/upload disk operations to background thread executors to study Event Loop thread preservation and bottleneck prevention. ⏳ *Planned*
</details>

<details>
<summary><b>💻 Phase 4: Tokenized Command Parsing & CLI Upgrade (Click to expand)</b></summary>

- [ ] **Advanced Argument Routing:** Replacing standard selection menus with an interactive command line using POSIX-compliant shlex and an application-bound argparse controller supporting custom runtime flags (e.g., recordmic -t 5). ⏳ *Planned*
- [ ] **One-to-Many Asynchronous Broadcasting:** Designing automated distribution modules to broadcast specific payload commands to entire clusters of connected implants simultaneously, modeling distributed systems architecture. ⏳ *Planned*
</details>

<details>
<summary><b>🌐 Phase 5: Interactive Web UI & FastAPI Gateway (Click to expand)</b></summary>

- [ ] **Asynchronous API Gateway:** Exposing internal session and job manager metrics via a robust FastAPI REST backend to demonstrate Full-Stack backend integration with lower-level network engines. ⏳ *Planned*
- [ ] **WebSocket Live Stream:** Developing a real-time notification engine to instantly stream terminal outputs and execution telemetry from implants to the web dashboard without polling, teaching event-driven protocols. ⏳ *Planned*
- [ ] **Control Dashboard:** Crafting a clean responsive administration interface utilizing Tailwind CSS for accessible lab manipulation. ⏳ *Planned*
</details>

<details>
<summary><b>📊 Phase 6: Operational Telemetry & Educational AV/EDR Simulator (Click to expand)</b></summary>

- [ ] **Visual Analysis Monitor:** Integrating real-time streaming charts (Chart.js / ApexCharts) to track network throughput (bytes/second) and protocol distributions, giving students a visual look into network payload telemetry. ⏳ *Planned*
- [ ] **Heuristic EDR/AV Threat Simulator:** Building a mock behavioral defense panel that calculates an internal "Threat Level Score" in real time based on agent actions, visually teaching students how blue teams spot anomalous behaviors. ⏳ *Planned*
</details>

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **Reverse Connection** | Client-initiated TCP architecture for firewall circumvention |
| **Interactive Shell** | Real-time remote command execution via encrypted channel |
| **Encrypted C2 Channel** | End-to-end AES-128 encryption using Fernet symmetric keys |
| **Audio Surveillance** | Remote microphone capture and exfiltration (sounddevice) |
| **Visual Capture** | Remote webcam snapshot acquisition (OpenCV) |
| **File Deployment** | Securely uploading files and tools from server to agent |
| **Geolocation Lookup** | IP-based geographical mapping via ipinfo.io |
| **Persistence Logic** | Windows Registry-based startup mechanisms for longevity |
| **Remote UI Interaction** | Delivering toast notifications to the target via plyer |
| **Screen Capture** | High-quality desktop screenshot acquisition (Pillow) |
| **Modular Deployment** | Support for both Staged (dropper) and Unstaged (standalone) payloads |
| **WMI Security Audit** | Detection of active Antivirus and Firewall products via WMI |
| **Host Reconnaissance** | Comprehensive hardware, OS, and network metadata collection |
| 🔥 **NEW: Post-Exploitation Modules** | Dynamic module discovery, template-based staging, encrypted agent registration, and controller-backed payload extensions |

---

## 📁 Project Structure

```
ShadowLab/
├── Shadow.py             # Main C2 Server Application
├── requirements.txt      # Python Package Dependencies
├── LICENSE               # Project License File
├── SECURITY.md           # Security Policy
├── FAQS.md               # Frequently Asked Questions
├── CONTRIBUTING.md       # Contribution Guidelines
├── README.md             # Project Documentation
├── assets/               # Media & Resources
├── confs/                # Configuration Files
│   └── conf.json         # Encryption Keys & Server Settings
├── mainclass/            # Core Server Modules
│   ├── builder.py        # Agent/Payload Builder
│   ├── comm.py           # Network Communication Handler
│   ├── encrypter.py      # Encryption & Decryption Utilities
│   ├── pyi_progress.py   # PyInstaller Integration & Progress Display
│   ├── options.py        # Command-Line Options & Menus
│   ├── shell.py          # Remote Command Handlers
│   ├── system.py         # System Utilities & Display
├── modules/              # Post-Exploit module templates and controllers
│   └── Keylogger/
│       ├── controller.py # Controller interface for remote keylogger modules
│       ├── config.json   # Keylogger module metadata and settings
│       ├── template.json # Template placeholders for module generation
│       └── keylogger.py  # Keylogger payload template
├── payloads/             # Agent/Implant Code
│   ├── payload.py        # Unstaged Payload (Full-Featured)
│   └── payload_staged.py # Staged Payload (Lightweight)
├── photos/               # Screenshot & Image Storage Directory
├── records/              # Audio Recording and Post Exploit Log Storage Directory
└── build/                # PyInstaller Build Output Directory
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/msalihberk/ShadowLab.git
cd ShadowLab
```

### 2. Install dependencies

Choose the installation method that best fits your environment:

**Standard Installation**
For environments with unrestricted package management:
```bash
pip install -r requirements.txt
```
**Virtual Environment Installation**
For strictly managed or isolation-required environments to avoid package conflicts:
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
---

## 💻 Usage

### Step 1: Start the C2 Server

```bash
python Shadow.py
```

### Step 2: Generate Auth Code
Run the server and select **Option 5 (Generate Conf)**. This initializes the `confs/conf.json` file, creating unique **Fernet Keys** and the **Auth Code** required for the secure agent-server handshake.

### Step 3: Configure Connection
- Select option `3` to set your IP address
- Select option `4` to set the listening port

### Step 4: Build Agent
- Choose option `1` to build an agent
- Select format (Python or EXE)
- Optionally bind to another application
- Choose Staged or UnStaged mode

### Step 5: Start Listener
- Choose option `2` to start listening
- Wait for incoming agent connection

### Step 6: Manage Session
Once connected, use these commands:

| Command | Action |
|---------|--------|
| `1` | Remote Shell |
| `2` | Create Persistence |
| `3` | Record Microphone |
| `4` | Upload File |
| `5` | Webcam Snapshot |
| `6` | Get Location |
| `7` | Remove Persistence |
| `8` | System Info |
| `9` | Send Notification |
| `10` | Get Screenshot |
| `11` | Security Info |
| `12` | 🔥 Manage Post Exploits |
| `q` | Quit |

### 🔥 Step 7: Launch Post-Exploit Modules

The new post-exploit manager turns `modules/` into an extension point for active sessions.

1. Choose command `12` from the connected agent menu
2. Select a discovered module such as `KEYLOGGER`
3. Fill runtime template values when prompted
4. Register and start the module through the encrypted C2 channel
5. Open the module controller when available for interactive output

Current included module:

| Module | Description | Controller |
|--------|-------------|------------|
| `KEYLOGGER` | Configurable post-exploit keylogger module template | Yes |

---

## 🔧 Requirements

- **Python 3.13.x**
- colorama
- cryptography
- pyinstaller
- opencv-python
- requests
- sounddevice
- wavio
- pillow
- pynput
- simplejson
- pyfiglet
- wmi
- plyer

---

## 🔒 [Security Policy](SECURITY.md)
Review our strict security protocols, ethical utilization boundaries, and our internal pipeline for **Responsible Disclosure**. Learn how to safely report any discovered framework vulnerabilities directly through GitHub's secure infrastructure without exposing telemetry data to the public.

---

## ❓ [Frequently Asked Questions](FAQS.md)
Serves as an operational directory covering the structural mechanics of the framework. It defines the architectural scope of Monolithic (Unstaged) versus Multi-stage (Staged) delivery, safe testing methods for handling Antivirus/EDR exclusions in research labs, and technical details regarding our **AES-128** transport layer encryption.

---

## 🤝 [Contributing Guidelines](CONTRIBUTING.md)
Want to improve the C2 framework? Read our technical contribution guidelines to understand our modular architectural standards, Python 3.13.x development environment rules, encryption key hygiene, and instructions on how to safely open a Pull Request.

## 📝 License

This project is provided for educational and research purposes only. See [LICENSE](LICENSE) for details.
