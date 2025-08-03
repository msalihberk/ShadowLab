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

## Usage


### Requirements
- Python 3.x
- colorama
- cryptography
- pyinstaller
- opencv-python
- requests
- sounddevice
- wavio
- pillow

Install dependencies:
```
pip install -r requirements.txt
```


### Generate Auth Code and Key
```
python Shadow.py --generate
```

### Start Listener
```
python Shadow.py --listen
```

### Generate Payload
```
python Shadow.py --ip <LHOST> --port <LPORT> --type py|exe
```


## Disclaimer
This tool is intended for educational purposes and authorized penetration testing only. Unauthorized use is strictly prohibited.
