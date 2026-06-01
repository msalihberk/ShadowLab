# Security Policy

## ⚠️ Educational Purpose Only
ShadowLab is a framework designed strictly for educational purposes and authorized security research. The goal is to provide a platform for learning about C2 architectures, network protocols, and defensive security measures.

**Do not use this tool for any illegal activities.** The author is not responsible for any misuse or damage caused by this software.

## Reporting a Vulnerability

As an educational and security research project, we take the integrity of our source code seriously. If you discover a logical flaw, dynamic memory issue, or potential vulnerability in the server (`Shadow.py`) or agent infrastructure, please **do not open a public GitHub Issue.** Instead, utilize GitHub's built-in private reporting infrastructure:

1. Navigate to the main page of this repository on GitHub.
2. Click on the **Security** tab under the repository name.
3. On the left sidebar, click **Vulnerability reporting**.
4. Click **Report a vulnerability** to open a private advisory form.

By using this internal pipeline, you ensure that the security community and researchers practicing with this tool in isolated environments remain safe while we triage and patch the reported behavior. Thank you for practicing responsible disclosure!

## Supported Versions

We actively monitor and provide maintenance patches only for the latest stable release of this research framework.

| Version | Supported |
| ------- | --------- |
| v1.3.x  | ✅ Yes    |
| < v1.3  | ❌ No     |

## Best Practices for Users
- Always run the server and agents in an isolated laboratory environment (VMs).
- Never expose the C2 listener directly to the open internet without additional security layers (VPN, SSH Tunnels).
- Regularly rotate the `authcode` and `KEY` in `conf.json` during research sessions.
