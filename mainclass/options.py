from colorama import Fore, init, Style

class options():
    slot = ["DATA INPUT", "IP INPUT", "PORT INPUT", "AGENT IP: ", "AGENT PORT: ", "CREATE", "APP",
             "APP LOCATION", "STAGE MODE", "NOTIFICATION TITLE",
               "NOTIFICATION TEXT", "NOTIFICATION APP", "NOTIFICATION"]
    agent_options = f"""\n
            1   -   Shell
            2   -   Persistence
            3   -   Record Mic
            4   -   Upload File
            5   -   Cam
            6   -   Get Location
            7   -   Destroy Persistence
            8   -   System Info
            9   -   Send Notification
            10  -   Get Screenshot
            11  -   Security Info
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
        for f in data["Firewall"]:
            print(f'''
{Fore.LIGHTBLUE_EX}displayName: {Fore.LIGHTCYAN_EX}{f["displayName"]} 
{Fore.LIGHTBLUE_EX}instanceGuid: {Fore.LIGHTCYAN_EX}{f["instanceGuid"]} 
{Fore.LIGHTBLUE_EX}pathToSignedProductExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedProductExe"]} 
{Fore.LIGHTBLUE_EX}pathToSignedReportingExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedReportingExe"]} 
{Fore.LIGHTBLUE_EX}productState: {Fore.LIGHTCYAN_EX}{f["productState"]} 
{Fore.LIGHTBLUE_EX}timestamp: {Fore.LIGHTCYAN_EX}{f["timestamp"]}''')
        print(f'''{Fore.MAGENTA}{Style.BRIGHT}

---ANTIVIRUS---''')
        for f in data["Antivirus"]:
            print(f'''
{Fore.LIGHTBLUE_EX}displayName: {Fore.LIGHTCYAN_EX}{f["displayName"]} 
{Fore.LIGHTBLUE_EX}instanceGuid: {Fore.LIGHTCYAN_EX}{f["instanceGuid"]} 
{Fore.LIGHTBLUE_EX}pathToSignedProductExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedProductExe"]} 
{Fore.LIGHTBLUE_EX}pathToSignedReportingExe: {Fore.LIGHTCYAN_EX}{f["pathToSignedReportingExe"]} 
{Fore.LIGHTBLUE_EX}productState: {Fore.LIGHTCYAN_EX}{f["productState"]} 
{Fore.LIGHTBLUE_EX}timestamp: {Fore.LIGHTCYAN_EX}{f["timestamp"]}''')
        
    def getSystemInfoText(data):
        text = f'''{Style.BRIGHT}{Fore.GREEN} 
| SYSTEM INFO |{Style.NORMAL}
{Fore.LIGHTBLUE_EX}Platform:{Fore.LIGHTCYAN_EX} {data["Platform"]}
{Fore.LIGHTBLUE_EX}Platform Release:{Fore.LIGHTCYAN_EX} {data["Platform Release"]}
{Fore.LIGHTBLUE_EX}Platform Version:{Fore.LIGHTCYAN_EX} {data["Platform Version"]}
{Fore.LIGHTBLUE_EX}Architecture:{Fore.LIGHTCYAN_EX} {data["Architecture"]}
{Fore.LIGHTBLUE_EX}Hostname:{Fore.LIGHTCYAN_EX} {data["Hostname"]}
{Fore.LIGHTBLUE_EX}IP Address:{Fore.LIGHTCYAN_EX} {data["IP Address"]}
{Fore.LIGHTBLUE_EX}Processor:{Fore.LIGHTCYAN_EX} {data["Processor"]}
{Fore.LIGHTBLUE_EX}Python Build:{Fore.LIGHTCYAN_EX} {data["Python Build"]}
{Fore.LIGHTBLUE_EX}Python Version:{Fore.LIGHTCYAN_EX} {data["Python Version"]}
'''
        return text
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
        elif mode == 7:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[9]
        elif mode == 8:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[10]
        elif mode == 9:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[11]
        elif mode == 10:
            SLOT1 += options.slot[0]
            SLOT2 += options.slot[12]

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