#!/usr/bin/env python3
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

init(autoreset=True)

from utils.config_loader import load_profile
from utils.privilege_check import is_root
from utils.exploit_search import search_exploits
from utils.output_writer import save_txt, save_xml, save_html

# ====================================================
#                   NMAP SCAN ENGINE
# ====================================================

def run_nmap_scan(target, profile, show_banner=True,
                  exploit_mode="ask", save_report=None):

    if not is_root():
        print(Fore.RED + "[!] Root privileges are required!\n" +
              Fore.YELLOW + "Use sudo to run this tool.\n" + Style.RESET_ALL)
        return
    # if show_banner:
    #     from utils.banner import banner
    #     banner()
        
    # Load profile
    try:
        args = load_profile(profile)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to load scan profile '{profile}': {e}" + Style.RESET_ALL)
        return

    # Force XML output and version detection
    args_mod = list(args)
    if "-sV" not in args_mod:
        args_mod.append("-sV")
    args_mod = [a for a in args_mod if not (a.startswith("-oX") or a == "-oX")]

    # Final Nmap command
    cmd = ["nmap"] + args_mod + ["-oX", "-", target]

    print(Fore.MAGENTA + f"\n[*] Scanning IP: {Fore.YELLOW}{target}" + Style.RESET_ALL)
    start_time = datetime.now()
    print(Fore.CYAN + f"\nScan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print(Fore.RED + "[!] nmap not found. Install nmap and try again." + Style.RESET_ALL)
        return

    xml_output = proc.stdout
    end_time = datetime.now()
    print(Fore.CYAN + f"Scan finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Duration
    duration = end_time - start_time
    minutes, seconds = divmod(duration.seconds, 60)
    print(Fore.CYAN + f"Scan Duration: {Fore.GREEN}{minutes}m {seconds}s\n")

    # Parse XML
    services, open_ports = parse_nmap_xml(xml_output)

    # Print open ports
    print_scan_results(open_ports)

    # Print XML service enumeration
    print(Fore.BLUE + "\n=== XML SERVICE ENUMERATION ===\n")
    for s in services:
        port_str = f"{s.get('port','')}/tcp"
        svc = s.get('service', '')
        ver = s.get('version', '')
        print(
            Fore.GREEN + f"{port_str:<10}" +
            Fore.YELLOW + f"{svc:<14}" +
            Fore.CYAN + f"{ver}"
        )
    print()

    # ----------------------------
    #     Searchsploit Enumeration
    # ----------------------------
    exploit_results = []

    # Services that generate huge false-positive lists without versions
    NOISY_SERVICES = {
        "mysql", "http", "https", "ftp", "smtp", "pop3", "imap",
        "ssh", "rdp", "microsoft-ds", "msrpc", "domain", "netbios",
        "rpcbind", "snmp", "irc", "ldap", "dhcp"
    }

    # Determine exploit enumeration mode
    if exploit_mode == "forced-yes":
        exp_choice = "1"
    elif exploit_mode == "forced-no":
        exp_choice = "2"
    else:
        print(Fore.BLUE + "Do you want to enumerate exploits using Searchsploit?")
        print("1) Yes")
        print("2) No (skip exploit search)\n")
        exp_choice = input("Choice: ").strip()

    if exp_choice == "1":
        print(Fore.MAGENTA + "\n[*] Searching for exploits using Searchsploit...\n" + Style.RESET_ALL)

        for svc in services:
            name = svc.get("service", "").strip()
            version = svc.get("version", "").strip()

            if not name:
                continue

            # -----------------------------
            # SMART FILTERING RULES
            # -----------------------------

            # Skip noisy services when no version is available
            if name in NOISY_SERVICES and version == "":
                print(Fore.YELLOW + f"[!] Skipping noisy service: {name} (no version detected)" + Style.RESET_ALL)
                continue

            # If version missing → skip to avoid huge irrelevant exploit lists
            if version == "":
                print(Fore.YELLOW + f"[!] Skipping {name}: no version detected" + Style.RESET_ALL)
                continue

            query = f"{name} {version}".strip()
            print(Fore.YELLOW + f"[+] Searching: {query}" + Style.RESET_ALL)

            exp_out = search_exploits(name, version)

            exploit_results.append({
                "service": name,
                "version": version,
                "exploits": exp_out
            })

        # Display Results
        print(Fore.BLUE + "\n=== SEARCHSPLOIT RESULTS ===\n")
        if not exploit_results:
            print(Fore.YELLOW + "[!] No relevant services found for exploit enumeration.\n")
        else:
            for item in exploit_results:
                svc = item.get("service", "")
                ver = item.get("version", "")
                print(Fore.GREEN + f"[Service] {svc} {ver}")
                body = item.get("exploits", "").strip()
                if not body:
                    print("Exploits: No Results")
                    print("Shellcodes: No Results")
                else:
                    print(body)
                print("-" * 80)

    else:
        print(Fore.YELLOW + "\n[!] Skipping Searchsploit enumeration.\n")
        exploit_results = []


    # ====================================================
    #              REPORT SAVING (auto / ask)
    # ====================================================

    # CLI auto-save
    if save_report is not None:
        if save_report == "txt":
            save_txt("vedicrecon-report.txt", xml_output, exploit_results)
            print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.txt")

        elif save_report == "xml":
            save_xml("vedicrecon-report.xml", xml_output)
            print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.xml")

        elif save_report == "html":
            save_html("vedicrecon-report.html", services, exploit_results)
            print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.html")

        return open_ports

    # Interactive
    print(Fore.BLUE + "\n=== Save Report ===")
    print("1) TXT (includes parsed XML + exploits)")
    print("2) XML (raw Nmap XML output)")
    print("3) HTML (full human-readable)\n")

    choice = input("Choice (press Enter to skip): ").strip()

    if choice == "1":
        save_txt("vedicrecon-report.txt", xml_output, exploit_results)
        print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.txt")

    elif choice == "2":
        save_xml("vedicrecon-report.xml", xml_output)
        print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.xml")

    elif choice == "3":
        save_html("vedicrecon-report.html", services, exploit_results)
        print(Fore.GREEN + "\n[+] Report saved: vedicrecon-report.html")

    else:
        print(Fore.YELLOW + "\n[!] No report created (skipped).")

    return open_ports


# ====================================================
#               XML PARSER
# ====================================================

def parse_nmap_xml(xml_text):
    services = []
    open_ports = []

    xml_start = xml_text.find("<")
    if xml_start > 0:
        xml_text = xml_text[xml_start:]

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return services, open_ports

    for host in root.findall("host"):
        ports = host.find("ports")
        if ports is None:
            continue

        for port in ports.findall("port"):
            portid = port.get("portid", "")
            state_elem = port.find("state")

            if state_elem is None or state_elem.get("state", "").lower() != "open":
                continue

            svc_elem = port.find("service")
            svc_name = svc_elem.get("name", "") if svc_elem is not None else ""
            product = svc_elem.get("product", "") if svc_elem is not None else ""
            version = svc_elem.get("version", "") if svc_elem is not None else ""

            details = []
            for sc in port.findall("script"):
                if sc.get("output"):
                    details.append(sc.get("output"))

            services.append({
                "port": portid,
                "service": svc_name,
                "product": product,
                "version": version,
                "details": details
            })

            open_ports.append({
                "port": f"{portid}/tcp",
                "service": svc_name,
                "version": (product + " " + version).strip(),
                "details": details
            })

    return services, open_ports


# ====================================================
#               OUTPUT DISPLAY
# ====================================================

def print_scan_results(open_ports):

    print(Fore.BLUE + "\n=== OPEN PORTS WITH DETAILS ===\n")

    if not open_ports:
        print(Fore.RED + "No open ports found.\n")
        return

    for p in open_ports:
        print(
            Fore.GREEN + f"{p['port']:<10}" +
            Fore.YELLOW + f"{p['service']:<12}" +
            Fore.CYAN + f"{p['version']}"
        )
        for d in p["details"]:
            print("   " + Fore.LIGHTYELLOW_EX + d)
        print()
