from colorama import Fore, init, Style

class options():
    slot = ["DATA INPUT", "IP INPUT", "PORT INPUT", "AGENT IP: ", "AGENT PORT: ", "CREATE", "APP", "APP LOCATION", "STAGE MODE"]
    agent_options = f"""\n
            1 - Shell
            2 - Backdoor
            3 - Record Mic
            4 - Upload File
            5 - Cam
            6 - Get Location
            7 - Destroy Backdoor
            8 - Connection Info
            q - Quit
            """
    
    createMenu_options3 = f"""\n
            1 - Run App Template
            2 - Not Run App Template
            9 - Back Menu
            """

    createMenu_options2 = f"""\n
            1 - Windows/Staged
            2 - Windows/UnStaged
            9 - Back Menu
            """ 
    
    createMenu_options1 = f"""\n
            1 - Python File (.py)
            2 - Executable Format (.exe) 
            9 - Back Menu
            """
    
    build_formats = {'1':'py', '2':'exe'}

    def getMenuOptions(ip, port):
        return f"""\n
            1 - Create RAT
            2 - Listen
            3 - Select IP ({ip})
            4 - Select PORT ({port})
            5 - Generate Conf
            q - Quit
            """

    def getInputText(mode, port, ip):
        SLOT1 = Fore.CYAN
        SLOT2 = Fore.CYAN
        if mode == 0:
            SLOT1 += options.slot[6]
            SLOT2 += "NONE"
        elif mode == 1:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[1]
        elif mode == 2:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[2]
        elif mode == 3:
            SLOT1 += options.slot[6]
            SLOT2 += options.slot[5]
        elif mode == 4:
            SLOT1 += options.slot[3] + Fore.GREEN + str(port)
            SLOT2 += options.slot[4] + Fore.GREEN + str(ip)
        elif mode == 5:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[7]
        elif mode == 6:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[8]

        SHADOW  = f"{Fore.MAGENTA}{Style.BRIGHT}SHADOW"
        DIVIDER = f"{Fore.WHITE}│"
        AGENTS  = f"{Fore.CYAN}AGENTS:{Fore.GREEN}{1}"
        SESS    = f"{Fore.CYAN}SESS:{Fore.YELLOW}{"127.0.0.1"}"
        BRACKET_L = f"{Fore.WHITE}["
        BRACKET_R = f"{Fore.WHITE}]"
        POINTER = f"{Fore.MAGENTA}➤{Fore.RESET}"

        prompt_str = (
                f"{BRACKET_L}{SHADOW} {DIVIDER} {SLOT1} {DIVIDER} {SLOT2}{BRACKET_R} {POINTER}  "
        )
        
        return prompt_str