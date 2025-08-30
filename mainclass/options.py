from colorama import Fore, init

class options():
    agent_options = f"""\n
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
    
    createMenu_options3 = f"""\n
            1 - Run App Template
            2 - Not Run App Template
            9 - Back Menu
            """

    createMenu_options2 = f"""\n
            1 - Windows/Staged
            2 - Windows/UnStaged
            9 - Back Menu
            """ # New Feature in Future
    
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

    def getInputText(string):
        return f"\n({string}):> "