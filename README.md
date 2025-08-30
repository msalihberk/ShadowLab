# Shadow


Shadow is a Python-based remote administration tool (RAT) for Windows. It allows you to generate payloads and control remote machines via a command and control (C2) interface. This project is for educational and authorized testing purposes only.


## Features
- Reverse TCP connection
- Remote shell access
- Microphone recording
- Webcam snapshot (using OpenCV)
- File upload
- Geolocation (using ipinfo.io)
- Backdoor creation and removal (persistence via Windows registry)

# ShadowRAT

ShadowRAT is a modular Python-based remote administration tool (RAT) for Windows. It allows you to generate payloads, control remote machines, and perform post-exploitation tasks through a user-friendly command and control (C2) interface. This project is for educational and authorized security testing purposes only.

## Features
- Modular architecture (mainclass, payloads, postexploits)
- Reverse TCP connection
- Remote shell access
- Microphone recording
- Webcam snapshot (OpenCV)
- File upload
- Geolocation (ipinfo.io)
- Backdoor creation and removal (Windows registry persistence)
- Agent info display
- Keylogger (postexploits)

## Directory Structure

- `mainclass/` : Core modules (system, shell, builder, encrypter, options)
- `payloads/`  : Payload scripts for agents
- `postexploits/` : Post-exploitation tools (e.g., Keylogger)
- `confs/`     : Configuration files
- `settings/`  : Auth and key files

## Requirements
- Python 3.x
- colorama
- cryptography
- pyinstaller
- opencv-python
- requests
- sounddevice
- wavio
- pillow
- pynput (for keylogger)

Install dependencies:
```
pip install -r requirements.txt
```

## Usage

### 1. Generate Auth Code and Key
```
python Shadow.py --generate
```

### 2. Start the Main Menu
```
python Shadow.py
```
Follow the menu to select IP, port, build payloads, or listen for agents.

### 3. Build Payload
Use the menu to create a Python or EXE payload. You can optionally bind an application.

### 4. Listen for Agents
Select the listen option from the menu to accept incoming connections from payloads.

### 5. Post-Exploitation
Use tools in `postexploits/` (e.g., Keylogger) as needed.

## Disclaimer
This tool is intended for educational purposes and authorized penetration testing only. Unauthorized use is strictly prohibited.
