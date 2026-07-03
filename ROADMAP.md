## 🗺️ Educational Lab Roadmap & Engineering Evolution

> 🎯 **Educational Lab Mission:** ShadowLab is systematically architected not for malicious deployment, but as an **interactive, code-level educational laboratory**. The core mission is to dissect the internal mechanics of C2 (Command & Control) networks, exploring low-level socket communication, encryption lifecycles, and backend orchestration. It provides a hands-on environment for computer science students, educators, and security researchers to understand exactly *how* remote administration infrastructure operates from the inside out, bridging the gap between theoretical network concepts and practical software implementation.

<details>
<summary><b>📦 Phase 1: Core Lab Architecture & Synchronous Foundations 🟢 [COMPLETED]</b></summary>

- [x] **Fernet Encryption Pipeline:** End-to-end AES-128 transport layer encryption using unique symmetric keys to teach data-in-transit security hygiene.
- [x] **Length-Prefixed TCP Transport:** Built low-level socket communication utilizing structured data boundaries to demonstrate and solve the classic TCP packet fragmentation ("boundary") problem.
- [x] **Dual-Mode Payload Builder:** Automated compilation for both Staged (lightweight dropper) and Unstaged (standalone monolithic) payloads to analyze delivery chain mechanics.
- [x] **Host Reconnaissance:** Deep OS integration querying hardware metadata and active security software via native WMI structures for endpoint auditing simulation.
</details>

<details>
<summary><b>🔥 Phase 2: Dynamic Post-Exploitation Subsystem 🟢 [COMPLETED]</b></summary>

- [x] **Runtime Module Discovery:** Engineered an automated tracking engine that dynamically discovers standalone post-exploit plugins via modular config.json manifests, demonstrating runtime extensibility.
- [x] **Template-Based In-Memory Staging:** Implemented dynamic environment replacement (C2 IP, Ports, Keys) into staged payload templates to teach safe automation and obfuscation basics.
- [x] **Controller-Backed Session Extension:** Added specialized server-side interactive controller support (e.g., the integrated KEYLOGGER module) mapping dedicated sub-channels across the active transport session.
</details>

<details>
<summary><b>🏗️ Phase 3: Asynchronous Core Migration 🟡 [IN PROGRESS]</b></summary>

- [ ] **Asyncio Event Loop Core:** Migrating the blocking core loop into a fully non-blocking asynchronous architecture (asyncio.StreamReader/Writer) to demonstrate massive concurrent socket scaling. 🏗️ *In Progress*
- [ ] **Isolated Per-Agent Job Queues:** Implementing a multiplexed asynchronous queue structure to model background task scheduling and synchronization in high-performance networking. ⏳ *Planned*
- [ ] **Non-Blocking File I/O Workers:** Offloading heavy download/upload disk operations to background thread executors to study Event Loop thread preservation and bottleneck prevention. ⏳ *Planned*
</details>

<details>
<summary><b>💻 Phase 4: Tokenized Command Parsing & CLI Upgrade 🔵 [PLANNED]</b></summary>

- [ ] **Advanced Argument Routing:** Replacing standard selection menus with an interactive command line using POSIX-compliant shlex and an application-bound argparse controller supporting custom runtime flags (e.g., recordmic -t 5). ⏳ *Planned*
- [ ] **One-to-Many Asynchronous Broadcasting:** Designing automated distribution modules to broadcast specific payload commands to entire clusters of connected implants simultaneously, modeling distributed systems architecture. ⏳ *Planned*
</details>

<details>
<summary><b>🌐 Phase 5: Interactive Web UI & FastAPI Gateway 🔵 [PLANNED]</b></summary>

- [ ] **Asynchronous API Gateway:** Exposing internal session and job manager metrics via a robust FastAPI REST backend to demonstrate Full-Stack backend integration with lower-level network engines. ⏳ *Planned*
- [ ] **WebSocket Live Stream:** Developing a real-time notification engine to instantly stream terminal outputs and execution telemetry from implants to the web dashboard without polling, teaching event-driven protocols. ⏳ *Planned*
- [ ] **Control Dashboard:** Crafting a clean responsive administration interface utilizing Tailwind CSS for accessible lab manipulation. ⏳ *Planned*
</details>

<details>
<summary><b>📊 Phase 6: Operational Telemetry & Educational AV/EDR Simulator 🔵 [PLANNED]</b></summary>

- [ ] **Visual Analysis Monitor:** Integrating real-time streaming charts (Chart.js / ApexCharts) to track network throughput (bytes/second) and protocol distributions, giving students a visual look into network payload telemetry. ⏳ *Planned*
- [ ] **Heuristic EDR/AV Threat Simulator:** Building a mock behavioral defense panel that calculates an internal "Threat Level Score" in real time based on agent actions, visually teaching students how blue teams spot anomalous behaviors. ⏳ *Planned*
</details>
