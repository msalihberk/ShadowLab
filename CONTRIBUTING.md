# Contributing to ShadowLab

First off, thank you for considering contributing to ShadowLab! Contributions are what make the security research community such a great place to learn and grow.

---

> [!IMPORTANT]
> **🚀 ACTIVE ARCHITECTURE REFACTOR**
> ShadowLab is actively transitioning from a synchronous network model to a fully **asynchronous (`asyncio`) architecture and modernized API layer**.
> 
> All active engineering, module development, and core contribution efforts are concentrated on the **`refactor/async-api-architecture`** branch. Please target this branch for all Pull Requests.

---

## Code of Conduct
By participating in this project, you agree to maintain a professional and respectful environment. This project is created strictly for **educational research and authorized lab testing**. Any contributions aimed at making this framework easier to use for malicious or illegal activities will be rejected.

---

## How Can I Contribute?

> ⚠️ **CRITICAL SECURITY NOTE:** If you find a security vulnerability, logical flaw, or anything that could compromise the integrity of this framework, **DO NOT open a public issue or pull request.** Please immediately refer to our [SECURITY.md](SECURITY.md) guidelines to submit a confidential report via GitHub's Private Vulnerability Reporting infrastructure.

### 🪲 Reporting Bugs
- Check if the bug has already been reported in the **Issues** tab.
- Specify whether the issue occurs on the legacy synchronous `main` branch or the asynchronous `refactor/async-api-architecture` branch.
- Open a new issue with a clear title and environment context (OS, Python version, log outputs).

### 🗺️ Supporting the Async Refactor & Roadmap
If you want to help implement core engine upgrades (such as the Async migration, FastAPI endpoints, or UI dashboard), please review the detailed milestones in our **Project Roadmap** inside `README.md` and target the active `refactor/async-api-architecture` branch.

### 🔥 Developing Post-Exploitation Modules
The heart of ShadowLab's extensibility is its modular Post-Exploit workflow. You can contribute new capability modules under the `modules/` directory:
- Study the existing `Keylogger/` template structure.
- Ensure your module contains a valid `config.json` manifest, a runtime template generator, and a corresponding server-side `controller.py`.
- Ensure controller/communication flows adhere to non-blocking asynchronous patterns.

### 🛡️ Multi-Language Payload Research (Python, C, Go)
While the core framework is Python-based, we highly encourage expanding our educational payload research into lower-level languages to demonstrate native execution mechanics:
- **C Payloads:** Contributions exploring raw Win32 APIs, memory allocation, and minimal compiled binaries.
- **Go Payloads:** Contributions exploring cross-compilation, static binaries, and efficient low-level networking.
- **Python Agents:** Optimizing the existing Staged (`payload_staged.py`) and Unstaged (`payload.py`) core scripts for `asyncio` loop integration.

### ✨ Suggesting Enhancements
- Ideas for async protocol improvements, post-exploitation controllers, modular REST API endpoints, or CLI workflows are welcome.
- Detail why the enhancement benefits modular C2 design or educational research.

### 🤝 Pull Requests & Branching Strategy
1. **Fork** the repository.
2. **Target Branch:** All pull requests **must** be submitted against the `refactor/async-api-architecture` branch.
3. Check out the development branch and create a feature branch:
   `git checkout refactor/async-api-architecture`
   `git checkout -b feature/async-amazing-feature`
4. Commit your changes following clean, descriptive commit messages:
   `git commit -m 'feat: implement async task dispatching in session manager'`
5. Push to your fork and open a **Pull Request** targeting `refactor/async-api-architecture`.

---

## 📜 Technical & Asynchronous Guidelines

ShadowLab relies heavily on Python's native `asyncio` ecosystem for core network and API handling. Please adhere to the following technical rules:

### 1. Asynchronous Execution Rules
- **Non-blocking Operations:** **Never** execute synchronous, blocking I/O calls inside coroutines (`async def`).
  - ❌ Do NOT use `time.sleep()`, standard `requests`, or synchronous socket blocking loops.
  - ✅ Use `await asyncio.sleep()`, asynchronous HTTP clients, and native `asyncio` streams (`StreamReader` / `StreamWriter`).
- **Heavy I/O & External Modules:** If a post-exploitation module or Windows API wrapper *must* perform blocking operations, offload execution using `asyncio.to_thread()`.
- **Task Management:** Ensure background tasks handle cancellation cleanly and catch `asyncio.CancelledError` appropriately during shutdown sequences.

### 2. Python Environment & Code Base
- **Python Version:** Compatible strictly with **Python 3.13+**.
- **Dependencies:** If adding a library, verify it supports asynchronous execution and update `requirements.txt`.
- **Encryption:** Never commit hardcoded secrets or keys. Utilize `core/crypto` helpers and `system.getdata("KEY")` methods.
- **Documentation:** Document any low-level socket, custom protocol stream, or Windows API interaction with clear comments.

---

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
