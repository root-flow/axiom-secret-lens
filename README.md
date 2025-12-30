# Axiom-Secret-Lens (ASL)

ASL is a specialized post-exploitation tool designed to extract high-entropy secrets and sensitive credentials from live process memory and environment blocks on Linux systems. 

Unlike static secret scanners, ASL targets the runtime state, allowing researchers to capture session tokens, cloud keys, and database credentials that only exist in volatile memory.

## 🛠 Features
- **Process Memory Auditing:** Scans `/proc/[pid]/maps` and parses memory segments (heap/stack).
- **Environment Block Extraction:** Deep-dives into `/proc/[pid]/environ` for all active PIDs.
- **Contextual Pattern Matching:** Uses optimized regex patterns for AWS, GCP, Azure, Slack, and generic API tokens.
- **Zero-Dependency:** Pure Python 3 implementation. No external libraries required for the core scanner.

## 🚀 Usage

### Clone and Initialize

git clone [https://github.com/canmitm/axiom-secret-lens.git](https://github.com/canmitm/axiom-secret-lens.git)
cd axiom-secret-lens

Basic Scan	

python3 asl.py --all

Advanced Scanning with Verification

python3 asl.py --pid <PID> --verify


📂 Project Structure

    asl.py: Main entry point and CLI handler.

    core/: Core scanning logic and validation modules.

    db/: Signature database containing regex patterns for known providers.

    utils/: Logging and output formatting utilities.


 🛡 Disclaimer

This software is intended for educational purposes and authorized penetration testing only. The author is not responsible for any misuse or damage caused by this tool.

Author: canmitm  Version: 1.0.0
