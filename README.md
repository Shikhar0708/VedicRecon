![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Version](https://img.shields.io/badge/Version-1.0.a--alpha-orange)
![Stars](https://img.shields.io/github/stars/Shikhar0708/VedicRecon?style=flat)
![Forks](https://img.shields.io/github/forks/Shikhar0708/VedicRecon?style=flat)
![Issues](https://img.shields.io/github/issues/Shikhar0708/VedicRecon)
![License](https://img.shields.io/badge/License-MIT-green)


**VedicRecon** is a lightweight, fast, offensive-security focused reconnaissance tool designed for real-world pentesters, bug bounty hunters, and red team operators.

Built with a modular engine, VedicRecon performs:

🔍 ARP-based host discovery

🚀 Profile-based Nmap scanning

🧠 Smart XML parsing & version extraction

🎯 Noise-reduced exploit enumeration via Searchsploit

📄 TXT, XML, and HTML report generation

🐍 100% Python — hackable, extendable, and built for automation

*Version: 1.0.a (Alpha)*
*Author: DEVIC / VEDIC*

# ⚡ Features (Alpha)
## 📌 1. ARP Discovery Mode

# Auto-detect devices on the network using ARP.
# Select the target interactively.

## 📌 2. Profile-Based Nmap Scanning

## Scan profiles:

| Profile     | Nmap Flags Used                        | Description                                                          |
| ----------- | -------------------------------------- | -------------------------------------------------------------------- |
| **fast**    | `-T4 -F`                               | Quick top-100 ports scan — fast recon for live targets.              |
| **full**    | `-T4 -p- -sV -sC`                      | Full port sweep (1–65535) + service detection + default NSE scripts. |
| **silent**  | `-T1 -sV -Pn`                          | Stealthy scan for IDS evasion — no ping, slow timing.                |
| **web**     | `-T4 -p 80,443,8080,8443,8000 -sV -sC` | Web-focused scan for common HTTP(S) ports.                           |
| **udp**     | `-sU --top-ports 50`                   | Fast UDP scan for top 50 UDP ports.                                  |
| **os**      | `-O -Pn`                               | OS detection without ping.                                           |
| **version** | `-sV`                                  | Service version detection only (quick, precise).                     |


## 📌 3. Unified XML Scan Engine

VedicRecon performs a single-shot Nmap XML scan with:

-sV forced

-oX - raw XML capture

Automatic parsing of:

port

service name

product

version

NSE output

## 📌 4. Smart Searchsploit Enumeration

No more dumping 900 irrelevant MySQL exploits when no version exists.

Rules:

Skips noisy services (e.g., mysql, msrpc, http) if version is missing.

Only enumerates when meaningful results expected.

Supports:

Interactive mode

Forced exploit mode (--exploits)

Forced skip mode (--no-exploits)

## 📌 5. Multi-Format Reporting

Generate professional reports:

TXT — structured, readable, includes exploit results

XML — raw Nmap XML

HTML — clean, human-friendly output

## 📌 6. GUI + CLI Support

vedicrecon.py → Interactive mode

vedicrecon-cli.py → CLI mode for automation

## 🧪 CLI Usage
Basic Scan
```bash
sudo python3 vedicrecon-cli.py -t <target> -p fast
```
Auto ARP Target Discovery
```bash
sudo python3 vedicrecon-cli.py --arp -p fast
```
Force Exploit Search
```bash
sudo python3 vedicrecon-cli.py -t <target> -p fast --exploits
```
Skip Exploit Search
```bash
sudo python3 vedicrecon-cli.py -t <target> -p fast --no-exploits
```
Auto-save Report
```bash
--save txt
--save xml
--save html
```

Example:
```bash
sudo python3 vedicrecon-cli.py -t 10.0.2.1 -p fast --exploits --save html
```
🧩 Installation
```bash
Clone Repository

git clone https://github.com/Shikhar0708/VedicRecon

cd VedicRecon
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run
```bash
sudo python3 vedicrecon.py
```

<img width="659" height="552" alt="Screenshot_2025-11-18_15-26-38" src="https://github.com/user-attachments/assets/8db27928-f11f-431e-ab21-79eb9d5d9bdd" />


# 🛠️ Roadmap (Upcoming)
## 🔥 v1.1 (Planned)

## User-selectable exploit targeting

## JSON output support

## Plugin-based service analyzers

## OSINT integration

## More scan profiles

# ⚡ v2.0 (Future)

* Interactive TUI dashboard

* Custom NSE runner

* Exploit module executor

* Fully pluggable recon framework

# 🐺 Disclaimer

# *VedicRecon is built for penetration testers, security researchers, and educational use only.*
# *Usage on unauthorized networks is strictly prohibited.*

## 👨‍💻 Author

**Shikhar Kant Sinha (DEVIC / VEDIC)**  
Aspiring Penetration Tester | IoT & Embedded Systems Background  
Building offensive security tools with a focus on automation and reliability.

- 🔗 GitHub: [Shikhar0708](https://github.com/Shikhar0708)  
- 🛠️ Projects: VedicRecon, IoT Security Tools, Recon Automations  
- 📧 Contact: *add your email if you want (optional)*  
- 🕉️ Motto: *“Knowledge is the first weapon.”*

