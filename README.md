# BitRSA - RSA CTF Challenge Tool 🚀

BitRSA is an advanced RSA challenge tool designed for CTF challenges and security research. It provides a collection of RSA attacks and utilities that can be used to test and exploit RSA vulnerabilities in various scenarios. 🔐


![GitHub commit activity](https://img.shields.io/github/commit-activity/m/BitravenS/BitRSA)
![Visitor Count](https://visitor-badge.glitch.me/badge?page_id=BitravenS.BitRSA)
![GitHub Repo stars](https://img.shields.io/github/stars/BitravenS/BitRSA?style=social)
![GitHub forks](https://img.shields.io/github/forks/BitravenS/BitRSA?style=social)
---

## Table of Contents 📚

- [Features](#features)
- [Installation](#installation)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Interactive Mode](#interactive-mode)
- [JSON Input Mode](#json-input-mode)
- [PEM Key Extraction](#pem-key-extraction)
- [Command-Line Arguments](#command-line-arguments)
- [Additional Arguments](#additional-arguments)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Features ✨

- **Multiple RSA Attacks:**
  - **Single-Keypair Attacks:**
    - Small e Attack
    - Wiener's Attack
    - Chosen Ciphertext Attack
    - Factorization Attack
    - Fermat's Factorization Attack
  - **Multi-Keypair Attacks:**
    - Common Modulus Attack
    - Common Factor Attack
    - Håstad's Broadcast Attack
    - Related Message Attack
    - Coppersmith's Attack
- **Key Extraction Tools:**
  - Public Key Extractor from PEM files.
  - Private Key Extractor from PEM files.
- **Flexible Input Modes:**
  - Interactive input.
  - JSON file input.
- **Modular & Maintainable:**
  - Clear separation of functionality into modules.
  - Comprehensive logging with colored terminal output. 🎨

---

## Installation 💻

1. **Clone the Repository:**
  ```bash
  git clone https://github.com/BitravenS/BitRSA
  cd BitRSA
  ```
2. **Ensure Python 3.7+ is Installed:**
  BitRSA requires Python version 3.7 or above.

3. **(Optional) Create a Virtual Environment:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

4. **Install Required Packages:**
```bash
pip install -r requirements.txt
```
  Otherwise, ensure that any dependencies (such as libraries used in utils.py) are installed.


> **Disclaimer:** *SageMath* is currently only supported on *Arch Linux*.
> If you find difficulties installing it, try looking online for fixes for your specific distro.
> Otherwise, most of the SageMath functionality could be substituted with **NumPy, gympy2 and sympy**.
> If you make any fixes, feel free to fork the Repository to include them.


## File Structure 📁

```bash

BitRSA/
├── BitRSA.py              # Main entry point for the tool
├── input_handler.py     # Handles interactive and JSON-based input
├── attack_runner.py     # Contains the logic for validating, displaying, and executing attacks
├── utils.py             # Utility functions (logging, colored output, etc.)
├── multi/               # RSA attack implementations for multi-keypair attacks
│   ├── common_e.py
│   ├── common_fact.py
│   ├── common_n.py
│   ├── coopersmith.py
│   └── related_m.py
├── single/              # RSA attack implementations for single-keypair attacks
│   ├── chosen.py
│   ├── factor.py
│   ├── small_e.py
│   └── wiener.py
└── tools/               # Tools for key extraction from PEM files
    ├── priv_ext.py
    └── pub_ext.py
```

## Usage 🚀

### Interactive Mode
Run the tool without any arguments to use interactive mode:
```bash
python BitRSA.py
```
The program will display help information and then prompt you for RSA parameters (moduli, exponents, ciphertexts) as well as any additional arguments.

### JSON Input Mode
Provide RSA parameters via a JSON file using the -f or --file option:
```bash
python BitRSA.py -f parameters.json
```
Follow this template:
```json
{
    "data": {
        "n": [
            // List of moduli
        ],
        "e": [
            // List of exponents
        ],
        "c": [
            // List of ciphertexts
        ]
    },
    // Optional
    "prefix": // Prefix,
    "len_flag": // Flag length,
    "timeout": // Timeout,
    "cpu": // Number of CPU cores to use
}
```

### PEM Key Extraction
You can extract keys directly from PEM files:
- Extract a Public Key:
  ```bash
  python BitRSA.py -pub my_public.pem
  ```
- Extract a Private Key:
  ```bash
  python BitRSA.py -priv my_private.pem
  ```

## Additional Arguments ⚙️
When entering RSA parameters interactively, you will be asked if you want to provide additional arguments. These may include:

- **Flag Prefix**: Optional string prefix for the flag.
- **Flag Length**: Optional integer representing the length of the flag.
- **Timeout**: Timeout for each attack in seconds (defaults to 10 seconds).
- **CPU Cores**: Number of CPU cores to use (defaults to using the maximum available).

These additional parameters help fine-tune the behavior of certain attacks.

## Contributing 🤝
Contributions to BitRSA are welcome! To contribute:

1. Fork the repository.
2. Create a feature or bugfix branch.
3. Commit your changes and push to your branch.
4. Open a pull request detailing your changes.

Please follow the coding style used in the project for consistency.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Disclaimer ⚠️

**BitRSA is intended for educational purposes and legal security testing only!**
Make sure you have explicit permission before using this tool on any network or system. The authors are not responsible for any misuse or damage caused by this software.
And before using this tool, make sure to understand the process behind all of these attacks. *Learning is more fun than capturing those flags!*

Enjoy and happy hacking! 😄

