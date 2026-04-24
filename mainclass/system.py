from colorama import Fore, init, Style
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
        font = system.getdata("header_font")
        line_char = system.getdata("line_char")
        line_size = system.getdata("line_size")
        version = system.getdata("version")
        
        header = pyfiglet.figlet_format(" SHADOW", font=font)

        print(Fore.CYAN + Style.BRIGHT + header)
        print(Fore.WHITE + "=" * 80)
        
        author = "By Mustafa Salih Berk"
        ver_text = f"v{version}"
        space_count = line_size - len(author) - len(ver_text) - 2
        
        print(f" {Fore.WHITE}{author}{' ' * space_count}{Fore.CYAN}{ver_text}")
        print(Fore.WHITE + "=" * 80)
        print(f" {Fore.RED}[!] {Fore.WHITE}Educational & Authorized Use Only\n")
    def printDisclaimer():
        os.system('cls' if os.name == 'nt' else 'clear')

        title_text = pyfiglet.figlet_format("SHADOW", font="slant")
        print(Fore.CYAN + Style.BRIGHT + title_text)
        print(Fore.WHITE + "=" * 80)
        print(f"{Fore.CYAN}[ CATEGORY ] {Fore.WHITE}: CYBERSECURITY RESEARCH & EDUCATIONAL SIMULATION")
        print(f"{Fore.CYAN}[ DEVELOPER ] {Fore.WHITE}: Mustafa Salih Berk")
        print(f"{Fore.CYAN}[ PURPOSE   ] {Fore.WHITE}: Analyzing Network Sockets & Defensive Security Architectures")
        print(Fore.WHITE + "=" * 80)

        print(f"\n{Fore.RED}{Style.BRIGHT}[!] LEGAL NOTICE:")
        print(f"{Fore.YELLOW}    This framework is strictly for EDUCATIONAL and AUTHORIZED testing only.")
        print(f"{Fore.YELLOW}    It has been developed to understand the mechanics of remote systems")
        print(f"{Fore.YELLOW}    to build better defensive security software (Antivirus/EDR).")

        print(f"\n{Fore.RED}{Style.BRIGHT}[!] ETHICAL GUIDELINES:")
        print(f"{Fore.WHITE}    1. Unauthorized usage on systems without explicit consent is {Fore.RED}ILLEGAL.")
        print(f"{Fore.WHITE}    2. The developer assumes {Fore.RED}NO{Fore.WHITE} liability for misuse or accidental damage.")
        print(f"{Fore.WHITE}    3. Use this tool only in controlled laboratory environments.")

        print(f"\n{Fore.GREEN}{Style.BRIGHT}[i] RESEARCH MODE: ACTIVE")
        print(f"{Fore.GREEN}    By continuing, you agree to use this knowledge for the benefit of")
        print(f"{Fore.GREEN}    information security and academic learning.")

        print(Fore.WHITE + "\n" + "=" * 80)
        print(Fore.CYAN + "Press ENTER to initialize the environment...")
        input()
    
    def printAgentOptions():
        print(Fore.LIGHTCYAN_EX + options.options.agent_options)

    def printBuildOptions(index):
        print(f"{Fore.MAGENTA}[{Fore.LIGHTGREEN_EX}{Style.BRIGHT}BUILD-{index}{Fore.MAGENTA}]")
    
        if index == 1:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options1)
        elif index == 2:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options2)
        elif index == 3:
            print(Fore.LIGHTCYAN_EX + options.options.createMenu_options3)

    def printMenuOptions(ip, port):
        status_ip = Fore.LIGHTGREEN_EX+ip+Fore.LIGHTCYAN_EX if ip else f"{Fore.RED}Not Selected{Fore.LIGHTCYAN_EX}"
        status_port = Fore.LIGHTGREEN_EX+port+Fore.LIGHTCYAN_EX if port != 0 else f"{Fore.RED}Not Selected{Fore.LIGHTCYAN_EX}"
        
        print(Fore.LIGHTCYAN_EX + options.options.getMenuOptions(status_ip, status_port))
    
    def input(mode, port=0, ip=""):
        return input(options.options.getInputText(mode, port, ip))

    def clear_screen():
        os.system("cls") if os.name == "nt" else os.system("clear")
