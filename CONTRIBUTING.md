# Contributing to ShadowLab

First off, thank you for considering contributing to ShadowLab! Contributions are what make the security research community such a great place to learn and grow.

---

> [!IMPORTANT]
> **🚀 ACTIVE ARCHITECTURE REFACTOR**
> ShadowLab is actively transitioning from a synchronous network model to a fully **asynchronous (`asyncio`) architecture and modernized API layer**. 
>
> All active engineering and contribution efforts are concentrated on the **`refactor/async-api-architecture`** branch. If you are contributing new code, modules, or core fixes, please target this branch.

---

## Code of Conduct
By participating in this project, you agree to maintain a professional and respectful environment. This project is created strictly for **educational research and authorized testing**. Any contributions aimed at making this framework easier to use for malicious or unauthorized activities will be rejected.

---

## How Can I Contribute?

> ⚠️ **CRITICAL SECURITY NOTE:** If you find a security vulnerability, logical flaw, or anything that could compromise the integrity of this framework, **DO NOT open a public issue or pull request.** Please immediately refer to our [SECURITY.md](SECURITY.md) guidelines to submit a confidential report via GitHub's Private Vulnerability Reporting infrastructure.

### Reporting Bugs
- Check if the bug has already been reported in the **Issues** tab.
- Specify whether the issue occurs on the legacy synchronous `main` branch or the asynchronous `refactor/async-api-architecture` branch.
- Open a new issue with a clear title and environment context (OS, Python version, log outputs).

### Suggesting Enhancements
- Ideas for async protocol improvements, post-exploitation controllers, modular REST API endpoints, or CLI workflows are welcome.
- Detail why the enhancement benefits modular C2 design or educational research.

### Pull Requests & Branching Strategy
1. **Fork** the repository.
2. **Target Branch:** All pull requests **must** be submitted against the `refactor/async-api-architecture` branch.
3. Check out the development branch and create a feature branch:
   `git checkout refactor/async-api-architecture`
   `git checkout -b feature/async-amazing-feature`
4. Commit your changes following clean, descriptive commit messages:
   `git commit -m 'feat: implement async task dispatching in session manager'`
5. Push to your fork and open a **Pull Request** targeting `refactor/async-api-architecture`.

---

## Technical & Asynchronous Guidelines

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
- **Encryption:** Never commit hardcoded secrets or keys. Utilize `core/crypto` helpers and `system.getdata("KEY", "user_data")` methods.
- **Documentation:** Document any low-level socket, custom protocol stream, or Windows API interaction with clear comments.

---

## Legal Agreement
By contributing to ShadowLab, you agree that your contributions are licensed under the project's **MIT License** and that you are the author of the code or have the legitimate right to contribute it.
