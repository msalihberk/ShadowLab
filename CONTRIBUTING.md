# Contributing to ShadowLab

First off, thank you for considering contributing to ShadowLab! Contributions are what make the security community such a great place to learn and grow.

## Code of Conduct
By participating in this project, you agree to maintain a professional and respectful environment. This project is for educational research; any contributions aimed at making this tool easier to use for illegal activities will be rejected.

## How Can I Contribute?

> ⚠️ **CRITICAL SECURITY NOTE:** If you find a security vulnerability, logical flaw, or anything that could compromise the integrity of this framework, **DO NOT open a public issue or pull request.** Please immediately refer to our [SECURITY.md](SECURITY.md) guidelines to submit a confidential report via GitHub's Private Vulnerability Reporting infrastructure.

### 🪲 Reporting Bugs
- Check if the bug has already been reported in the **Issues** tab.
- If not, open a new issue with a clear title and a detailed description of the environment (OS, Python version).

### 🗺️ Supporting the Project Roadmap
If you want to help implement the core engine upgrades (such as the Async migration, FastAPI backend, or Tailwind dashboard), please review the detailed milestones in our **Project Roadmap** inside the main `README.md` and check the active issues.

### 🔥 Developing Post-Exploitation Modules
The heart of ShadowLab's extensibility is its modular Post-Exploit workflow. You can contribute new capability modules under the `modules/` directory:
- Study the existing `Keylogger/` template structure.
- Ensure your module contains a valid `config.json` manifest, a runtime template generator, and a corresponding server-side `controller.py`.

### 🛡️ Multi-Language Payload Research (Python, C, Go)
While the core framework is Python-based, we highly encourage expanding our educational payload research into lower-level languages to demonstrate native execution mechanics:
- **C Payloads:** Contributions exploring raw Win32 APIs, memory allocation, and minimal compiled binaries.
- **Go Payloads:** Contributions exploring cross-compilation, static binaries, and efficient low-level networking.
- **Python Agents:** Optimizing the existing Staged (`payload_staged.py`) and Unstaged (`payload.py`) core scripts.

### ✨ Suggesting Enhancements
- We welcome new post-exploitation modules or UI improvements.
- Explain why the enhancement would be useful for security research.

### 🤝 Pull Requests
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📜 Technical Guidelines
- **Python Version:** Ensure your code is compatible with Python 3.13.
- **Encryption:** Never commit hardcoded keys. Use the `system.getdata("KEY")` methods.
- **Dependencies:** If you add a new library, update `requirements.txt`.
- **Documentation:** Comment your code, especially when interacting with Windows APIs or complex socket logic.

## ⚖️ Legal Agreement & Ethical Code of Conduct

By contributing to ShadowLab, you explicitly agree to the following terms, affirming your commitment to legal and ethical software development:

### 1. Licensing & Ownership
You certify that you are the original author of the contributed code, or that you possess the explicit legal rights and permissions to distribute it. By submitting a Pull Request, you agree that all your contributions will be licensed under the project's open-source **MIT License**.

### 2. Strict Ethical Authorization & Non-Malicious Intent
You declare that your contributions are designed exclusively for **educational, academic, and authorized defensive/offensive security research**. You state that your code is not engineered, obfuscated, or optimized to facilitate unauthorized system access, data exfiltration, or illegal network infiltration. 

### 3. Compliance with Global Cyberlaws
You agree to comply with all regional and global cyber-regulations (such as the US Computer Fraud and Abuse Act (CFAA), the EU Cybercrime Directive, and local cyber-legislations). You certify that you will never test your contributions on any system or network without explicit, prior, and written authorization from the infrastructure owner.

### 4. Indemnification & Liability Waiver
You understand that the framework is provided "as-is." You agree that you are solely responsible for the code you contribute. The author and maintainers of ShadowLab assume zero liability and cannot be held responsible for any misuse, unintended side-effects, or damages caused by code contributed by the community.
