# Contributing to ShadowLab

First off, thank you for considering contributing to ShadowLab! Contributions are what make the security community such a great place to learn and grow.

## Code of Conduct
By participating in this project, you agree to maintain a professional and respectful environment. This project is for educational research; any contributions aimed at making this tool easier to use for illegal activities will be rejected.

## How Can I Contribute?

### Reporting Bugs
- Check if the bug has already been reported in the **Issues** tab.
- If not, open a new issue with a clear title and a detailed description of the environment (OS, Python version).

### Suggesting Enhancements
- We welcome new post-exploitation modules or UI improvements.
- Explain why the enhancement would be useful for security research.

### Pull Requests
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Technical Guidelines
- **Python Version:** Ensure your code is compatible with Python 3.10+.
- **Encryption:** Never commit hardcoded keys. Use the `system.getdata("KEY")` methods.
- **Dependencies:** If you add a new library, update `requirements.txt`.
- **Documentation:** Comment your code, especially when interacting with Windows APIs or complex socket logic.

## Legal Agreement
By contributing to ShadowLab, you agree that your contributions are licensed under the project's MIT License and that you are the author of the code or have the right to contribute it.
