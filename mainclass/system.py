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
            input("OK")
    
    def getJson():
        try:
            with open("confs/conf.json", 'r') as f:
                return json.load(f)
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
            input("OK")
    
    def setJson(data):
        try:
            with open("confs/conf.json", 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
            input("OK")
        
    def printheader():
        font = system.getdata("header_font")
        line_char = system.getdata("line_char")
        line_size = system.getdata("line_size")
        version = system.getdata("version")
        
        header = pyfiglet.figlet_format(" SHADOW", font=font)

        print(Fore.CYAN + Style.BRIGHT + header)
        print(Fore.WHITE + line_char * line_size)
        
        author = "By Mustafa Salih Berk"
        ver_text = f"v{version}"

        space_count_1 = line_size - len(author) - len(ver_text) - 2
        print(f" {Fore.WHITE}{author}{' ' * space_count_1}{Fore.CYAN}{ver_text} ")
        print(Fore.LIGHTBLACK_EX + "-" * line_size)
        
        alert_text = "[!] Educational & Authorized Use Only"
        
        star_visible_text = "⭐ Leave a Star!" 
        star_url = "https://github.com/msalihberk/ShadowLab"
        
        space_count_2 = line_size - len(alert_text) - len(star_visible_text) - 2
        
        clickable_star = f"\033]8;;{star_url}\033\\{Fore.YELLOW}{Style.BRIGHT}{star_visible_text}\033]8;;\033\\"
        
        print(f" {Fore.RED}{alert_text}{' ' * space_count_2}{clickable_star} ")
        
        print(Fore.WHITE + line_char * line_size + Style.RESET_ALL)

    def printDisclaimer():
        font = system.getdata("header_font")
        line_char = system.getdata("line_char")
        line_size = system.getdata("line_size")
        os.system('cls' if os.name == 'nt' else 'clear')

        title_text = pyfiglet.figlet_format("SHADOW", font=font)
        print(Fore.CYAN + Style.BRIGHT + title_text)
        print(Fore.WHITE + line_char * line_size)
        
        print(f"{Fore.CYAN}[ CATEGORY  ] {Fore.WHITE}: CYBERSECURITY RESEARCH & EDUCATIONAL SIMULATION")
        print(f"{Fore.CYAN}[ DEVELOPER ] {Fore.WHITE}: Mustafa Salih Berk")
        print(f"{Fore.CYAN}[ PURPOSE   ] {Fore.WHITE}: Analyzing Network Sockets & Defensive Security Architectures")
        
        repo_url = "https://github.com/msalihberk/ShadowLab"
        repo_visible_text = "github.com/msalihberk/ShadowLab"
        clickable_repo = f"\033]8;;{repo_url}\033\\{Fore.LIGHTBLUE_EX}{repo_visible_text}\033]8;;\033\\"
        print(f"{Fore.CYAN}[ SOURCE    ] {Fore.WHITE}: {clickable_repo}")
        print(Fore.WHITE + line_char * line_size)

        print(f"\n{Fore.RED}{Style.BRIGHT}[!] LEGAL NOTICE:")
        print(f"{Fore.YELLOW}    Strictly for EDUCATIONAL / AUTHORIZED testing to build defensive software (EDR).")

        print(f"\n{Fore.RED}{Style.BRIGHT}[!] ETHICAL GUIDELINES:")
        print(f"{Fore.WHITE}    • Unauthorized use is {Fore.RED}ILLEGAL{Fore.WHITE}  • Developer assumes {Fore.RED}NO{Fore.WHITE} liability  • Use only in lab env.")

        print(f"\n{Fore.GREEN}{Style.BRIGHT}[i] RESEARCH MODE: ACTIVE")
        print(f"{Fore.GREEN}    Continuing implies agreement to use this knowledge for learning benefits.")

        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}[+] OPEN SOURCE COMMUNITY:")
        contrib_url = "https://github.com/msalihberk/ShadowLab/blob/main/CONTRIBUTING.md"
        contrib_text = "Click here to contribute on GitHub"
        clickable_contrib = f"\033]8;;{contrib_url}\033\\{Fore.LIGHTCYAN_EX}{contrib_text}\033]8;;\033\\"
        
        star_text = "If you appreciate this research, leave a Star!"
        clickable_star = f"\033]8;;{repo_url}\033\\{Fore.YELLOW}{Style.BRIGHT}{star_text}\033]8;;\033\\"
        
        print(f"{Fore.WHITE}    - {clickable_contrib}")
        print(f"{Fore.WHITE}    - {clickable_star}")

        print(Fore.WHITE + "\n" + line_char * line_size)
        print(Fore.CYAN + "Press ENTER to initialize the environment...", end="")
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
