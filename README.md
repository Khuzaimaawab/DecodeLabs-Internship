# DecodeLabs Cybersecurity Internship Portfolio 🛡️

**Welcome to my central repository for the DecodeLabs Batch 2026 Cybersecurity Training Program.** This repository serves as a cumulative portfolio of the security engineering projects, cryptographic engines, and defensive logic terminals I am developing during my internship. All tools are built with a focus on real-world application, secure coding practices, defensive logic, and system efficiency.

---

## 🗂️ Project Index

### [Project 1: Defensive Security Gatekeeper](./DecodeLab-P1.py)
* **Focus:** Defensive Logic, Entropy Evaluation, Vulnerability Mitigation
* **Tech Stack:** Python (Standard Library: `string`, `hmac`)
* **Description:** A terminal-based Password Strength Checker engineered to evaluate string entropy. It moves beyond basic length checks by implementing constant-time comparison (`hmac.compare_digest`) to mitigate execution-time information leaks (Timing Attacks). It actively filters inputs against a mock database of leaked credentials and strictly enforces a "Validation Before Encryption" architecture.

### [Project 2: Advanced Cryptographic Engine](./DecodeLab-P2.py) 
* **Focus:** Data Confidentiality, Symmetric Encryption (Caesar Protocol), GUI Architecture
* **Tech Stack:** Python, CustomTkinter
* **Description:** A modular, enterprise-grade desktop application that visually demonstrates the Input-Process-Output (IPO) cycle of symmetric encryption. It utilizes strict ASCII mathematical baseline shifts (`ord()`, `chr()`, `% 26`) to obfuscate plaintext into ciphertext, while automatically handling edge cases (spaces, punctuation) and providing a dual-mode interactive display for decryption validation.

### [Project 3: Phishing Triage Toolkit](./DecodeLab-P3.py) 
* **Focus:** Human Firewall, Social Engineering Detection, Threat Triage
* **Tech Stack:** Python, CustomTkinter, `re`, `urllib`
* **Description:** An interactive, dual-pane SOC (Security Operations Center) dashboard designed to dissect deceptive communications. It features advanced regex parsing to detect "Subdomain Traps" (right-to-left URL root analysis), header mismatch detection to identify brand spoofing, and cognitive trigger analysis (Urgency, Fear, Authority). The engine calculates a dynamic threat score to output a strict, actionable triage decision (Safe, Suspicious, or Malicious).
---

## ⚙️ General Setup & Installation

To explore any of the tools in this repository locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Khuzaimaawab/DecodeLabs-Internship.git](https://github.com/Khuzaimaawab/DecodeLabs-Internship.git)
   cd DecodeLabs-Internship
Install required UI libraries (For GUI projects like):

Bash
pip install customtkinter

Run the individual security modules:

Bash
**Run Project 1 (Terminal)**
python DecodeLab-P1.py

**Run Project 2 (GUI)**
python DecodeLab-P2.py
(Note: Depending on your system environment, you may need to use python3 instead of python)

👨‍💻 Authorship
Sole Developer & Engineer: Khuzaima

Developed and continuously updated as part of the DecodeLabs industrial training curriculum.
