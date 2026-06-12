# ShadowLab
![Python Version](https://img.shields.io/badge/python-3.13.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Purpose](https://img.shields.io/badge/purpose-educational-orange.svg)
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

ShadowLab is a modular Command & Control (C2) framework developed for security research and educational purposes. The project demonstrates the lifecycle of remote administration tools, focusing on:

- **Socket Programming:** Low-level TCP communication using length-prefixed data packets.
- **Cryptography:** End-to-end encryption using the Fernet (AES-128) symmetric algorithm.
- **Payload Architecture:** Implementation of both Staged (dropper) and Unstaged (full-featured) delivery methods.
- **Windows Integration:** Interacting with the OS via WMI, Registry, and Subprocess modules.

This project is ideal for:
- Cybersecurity students learning about C2 infrastructure
- Security researchers studying attack methodologies
- Red team professionals practicing adversary emulation
- Defenders understanding threats to build better defenses

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
| **Post-Exploitation** | *(In Development)* Advanced modules like Keylogging |

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
├── payloads/             # Agent/Implant Code
│   ├── payload.py        # Unstaged Payload (Full-Featured)
│   └── payload_staged.py # Staged Payload (Lightweight)
├── postexploits/         # Post-Exploitation Modules (Future)
│   └── keystroke.py      # (In Development - Pending Security Review)
├── photos/               # Screenshot & Image Storage Directory
├── records/              # Audio Recording Storage Directory
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
| `q` | Quit |

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
