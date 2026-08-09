<div align="center">

<img src="assets/banner.png" alt="ShadowLab Banner" width="100%"/>

# ShadowLab

### Educational Command & Control Framework

*Stable code on main • Active refactor on refactor/async-api-architecture*

<br>

<p>

[Overview](#-overview) •
[Branch Status](#-branch-status) •
[Project Structure](#-project-structure) •
[Current Features](#-current-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Contributing](#-contributing) •
[Documentation](#-documentation)

</p>

<br>

[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)]()
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Main%20Stable-orange?style=for-the-badge)]()
[![Dev](https://img.shields.io/badge/Dev%20Branch-refactor%2Fasync--api--architecture-blue?style=for-the-badge)]()

<br><br>

**🔐 Encrypted Communications** •
**⚡ Async API / Async Server Refactor** •
**📦 Payload Builder** •
**🧩 Post-Exploitation Modules** •
**🎓 Cybersecurity Education**

</div>

---

> [!IMPORTANT]
>
> ShadowLab is an educational Command & Control (C2) framework designed for cybersecurity research, authorized lab testing, and controlled technical learning.
>
> The latest stable implementation is kept on the `main` branch. The active development work is happening on the `refactor/async-api-architecture` branch, where the project is being modernized around asynchronous server and API patterns.
>
> **This project must never be used against systems without explicit authorization.**

# Overview

ShadowLab is a Python-based modular C2 framework for studying how modern remote management systems are structured, implemented, and operated in a controlled environment.

The project contains encrypted communications, payload generation, session management, asynchronous networking, and modular post-exploitation workflows in a single educational codebase. It is designed to help students, researchers, and developers understand the internal mechanics of a C2 system without turning the repository into a real-world offensive toolkit.

The repository currently exists in two states:

- `main`: the stable branch with the most reliable baseline state
- `refactor/async-api-architecture`: the active development branch for async refactoring and API modernization

# Branch Status

## Stable branch

```bash
git checkout main
```

This is the stable branch and reflects the last known-good implementation for the project.

## Active development branch

```bash
git checkout refactor/async-api-architecture
```

This branch is currently the engineering focus for the project. It contains the ongoing work to move communication flow, session handling, and API integration toward a more asynchronous and modular architecture.

> If you want to contribute to the current architecture work, this is the branch to target.

# Project Structure

The codebase is split into functional areas for the C2 server, API layer, crypto logic, builder, session management, and post-exploitation modules.

```text
ShadowLab/
├── agent/
│   ├── builder/
│   │   ├── builder.py
│   │   └── pyi_progress.py
│   └── post_exploit/
│       └── post_exploit_controller.py
├── api/
│   ├── __init__.py
│   ├── connection_protocol.py
│   └── main.py
├── assets/
├── cli/
│   ├── options.py
│   ├── shell.py
│   └── system.py
├── confs/
│   ├── conf.json
│   ├── data.json
│   └── user_data.json
├── core/
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── encrypter.py
│   ├── enums/
│   │   └── Modules.py
│   ├── management/
│   │   ├── __init__.py
│   │   ├── session_manager.py
│   │   └── session.py
│   ├── server/
│   │   ├── __init__.py
│   │   ├── async_comm.py
│   │   ├── async_server.py
│   │   └── protocol.py
│   └── utils/
│       ├── __init__.py
│       └── paths.py
├── modules/
│   └── Keylogger/
│       ├── config.json
│       ├── controller.py
│       ├── keylogger.py
│       └── template.json
├── storage/
│   ├── binaries/
│   │   └── agent.py
│   └── loot/
│       ├── logs/
│       ├── photos/
│       └── records/
├── Shadow.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── FAQS.md
├── LICENSE
├── SECURITY.md
├── ROADMAP.md
└── .gitignore
```

# Current Features

ShadowLab includes a practical set of capabilities aligned with a modular C2 framework.

## Core capabilities

- Encrypted communication flow between agent and server
- Session creation and tracking for connected clients
- Async TCP listener implementation
- REST API layer for listing agents and sending tasks
- CLI-driven configuration and startup workflow

## Payload and builder features

- Staged payload generation
- Unstaged payload generation
- Embedded configuration values such as IP and port
- Payload generation utilities for executable deployment scenarios

## Session and management features

- Agent connection management with session IDs
- Multi-session tracking through the session manager
- Session cleanup when a client disconnects
- Task dispatching from control plane to connected agent

## Post-exploitation module system

- Module discovery and integration flow
- Runtime controller pattern for post-exploit operations
- Example Keylogger module included in the repository
- Template-driven module architecture for future expansion

## Async refactor focus

The `refactor/async-api-architecture` branch is specifically focused on:

- asynchronous network communication
- cleaner event-driven session handling
- API-oriented control-plane interaction
- improved service separation between server runtime and control logic
- maintainability and scalability for future integrations

# Installation

ShadowLab targets Python 3.13.x.

## 1. Clone the repository

```bash
git clone https://github.com/msalihberk/ShadowLab.git
cd ShadowLab
```

## 2. Check out the correct branch

For the stable project state:

```bash
git checkout main
```

For the active development/refactor branch:

```bash
git checkout refactor/async-api-architecture
```

## 3. Install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## 4. Start the framework

```bash
python Shadow.py
```

# Usage

The project is designed around a menu-driven workflow for configuration and startup.

## Typical lifecycle

```text
Generate configuration
    │
    ▼
Set IP and port
    │
    ▼
Build payload
    │
    ▼
Start listener
    │
    ▼
Agent connects
    │
    ▼
Manage session
    │
    ▼
Deploy module or task
```

## Main actions

- Build payload
- Start listener and API service
- Configure IP address
- Configure port
- Generate config data

## API usage

The service exposes control endpoints such as:

- `GET /api/v1/agents`
- `POST /api/v1/agents/{session_id}/task`

These endpoints are used to inspect connected agents and send tasks in a lab environment.

# Contributing

Contributions are welcome, especially for the active development branch.

## Recommended workflow

1. Fork the repository
2. Check out the development branch:

```bash
git checkout refactor/async-api-architecture
```

3. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

4. Implement and test your changes
5. Open a pull request against the development branch

## Contribution areas

- async architecture cleanup
- session management improvements
- API stability and endpoint design
- module expansion and controller logic
- documentation and clarity improvements
- security-focused validation in isolated lab environments

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

# Documentation

| Document | Purpose |
| :--- | :--- |
| [README.md](README.md) | Project overview and branch status |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [FAQS.md](FAQS.md) | Frequently asked questions |
| [SECURITY.md](SECURITY.md) | Responsible disclosure and vulnerability reporting |
| [ROADMAP.md](ROADMAP.md) | Project direction and future milestones |
| [LICENSE](LICENSE) | MIT license terms |

# Legal and Safety Notice

ShadowLab is intended exclusively for:

- cybersecurity education
- ethical research
- controlled lab work
- authorized security assessments

Unauthorized use against systems or networks without explicit permission is outside the intended purpose of this project.

---

<div align="center">

### Support the Project

If ShadowLab helps you learn, study, or build research tooling in a controlled environment, consider giving the project a GitHub star.

Made with ❤️ for the cybersecurity education community.

</div>
