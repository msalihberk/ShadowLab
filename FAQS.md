# Frequently Asked Questions (FAQ)

### 1. What is the difference between Staged and Unstaged payloads?
- **Unstaged:** The generated file (agent.exe/py) contains the entire logic, libraries, and communication modules. It is larger but works independently once executed.
- **Staged:** A small "stager" is generated. When executed, it connects back to the server, receives the full payload over the network, and runs it in memory or on disk. This is used to simulate advanced persistent threat (APT) delivery methods.

### 2. Why does my Antivirus delete the generated Agent?
ShadowLab is a C2 framework. The techniques used (socket communication, registry persistence, shell execution) are frequently used by malware. For research purposes, you should add your project folder and lab environment to your AV exclusion list.

### 3. Which Operating Systems are supported?
- **Server:** Cross-platform (Windows, Linux, macOS) as long as Python 3.13 is installed.
- **Agent:** Currently optimized for **Windows**, as features like WMI security audits and Registry persistence are Windows-specific.

### 4. How is the communication secured?
All traffic between the server and the agent is encrypted using **AES-128 (Fernet)**. Every session requires a unique `authcode` generated via the configuration menu. If the code does not match, the server drops the connection immediately.

### 5. Can I use this for my penetration testing job?
Yes, provided you have explicit written consent from the target organization. However, remember this is primarily an educational tool; for professional engagements, consider using battle-tested frameworks like Sliver or Cobalt Strike.

### 6. I found a bug, what should I do?
Please check the `CONTRIBUTING.md` file and open a detailed issue on the GitHub repository including your OS version and Python logs.

### 7. How do I change the encryption keys?
Use **Option 5 (Generate Conf)** in the main menu. This will regenerate the `confs/conf.json` file with a new Fernet key and auth token.

### 8. Why is PyInstaller required?
PyInstaller is used to compile the Python agent into a standalone Windows executable (.exe), allowing it to run on systems without a Python interpreter installed.

### 9. Is ShadowLab a malicious software or malware?
No, ShadowLab is strictly an educational tool and security research framework designed for authorized testing, laboratory simulations, and purple-team training. While it implements techniques commonly found in remote administration tools (RATs) to demonstrate endpoint behavior, it lacks any malicious propagation or automated execution mechanisms. It is built entirely to help students and researchers analyze adversary methodologies and build better defensive controls in a controlled, legal environment.