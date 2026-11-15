from colorama import Fore, init

init(autoreset=True)

class CLIPrinter:
    @staticmethod
    def error(msg: str):
        print(Fore.LIGHTRED_EX + f"[!] Error: {msg}")

    