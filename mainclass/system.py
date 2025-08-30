from colorama import Fore, init
from . import options
import pyfiglet
import json
import os

init(autoreset=True)

class system():
    def getdata(data):
        try:
            with open("confs/conf.json", 'r') as f:
                return json.load(f)[data]
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
    
    def getJson():
        try:
            with open("confs/conf.json", 'r') as f:
                return json.load(f)
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
    
    def setJson(data):
        try:
            with open("confs/conf.json", 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        
    def printheader():
        header = pyfiglet.figlet_format(" SHADOW", font=system.getdata("header_font"))
        print(Fore.LIGHTRED_EX + ' ' + system.getdata("line_char") * system.getdata("line_size") + f'\n')
        print(Fore.LIGHTRED_EX + header)
        print(Fore.LIGHTYELLOW_EX + f' By Mustafa Salih Berk                       Version {system.getdata("version")}')
        print(Fore.LIGHTRED_EX + ' ' + system.getdata("line_char") * system.getdata("line_size"))
    
    def printAgentOptions():
        print(Fore.LIGHTCYAN_EX + options.options.agent_options)

    def printBuildOptions(index):
        if index == 1:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options1)

        if index == 2:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options2)

        if index == 3:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options3)    

    def printMenuOptions(ip, port):
        if not ip:
            ip = 'Not Selected'
        if port == 0:
            port = 'Not Selected'
        print(Fore.LIGHTCYAN_EX + options.options.getMenuOptions(ip, port))
    
    def input(string=f'{Fore.LIGHTRED_EX}Shadow{Fore.RESET}@{Fore.LIGHTRED_EX}Shadow{Fore.RESET}'):
        return input(options.options.getInputText(string))

    def clear_screen():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
