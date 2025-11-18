#!/usr/bin/env python3
import sys
from colorama import Fore, Style, init
init(autoreset=True)

from utils.banner import banner
from utils.privilege_check import is_root
from utils.config_loader import load_profile
from utils.scan_engine import run_nmap_scan
from utils.arp_engine import arp_ip_loader

# ============================================================
#                  INTERACTIVE MODE SELECTOR
# ============================================================

def manual_mode():
    if not is_root():
        print(Fore.RED + "[!] Root privileges required!\nUsage:\n\tsudo python3 vedicrecon.py" + Style.RESET_ALL)
        return

    target = input(Fore.RED + "Enter target IP/hostname: ")
    profile = input(Fore.GREEN + "Enter scan profile (fast, full, silent, web, udp, os, version): ")

    run_nmap_scan(target=target, profile=profile)


def automated_mode():
    if not is_root():
        print(Fore.RED + "[!] Root privileges required!\n" + Style.RESET_ALL)
        return

    target_info = arp_ip_loader()
    target = target_info["ip"]

    profile = input(Fore.GREEN + "Enter scan profile (fast, full, silent, web, udp, os, version): ")

    run_nmap_scan(target=target, profile=profile)


def mode_selector():
    banner()

    print(Fore.GREEN+"\n=== Select Mode ===\n")
    print(Fore.GREEN+"1) Manual Scan")
    print(Fore.GREEN+"2) Automatic ARP Scan\n")

    choice = input(Fore.CYAN+"Enter choice: ").strip()

    if choice == "1":
        print(Fore.BLUE+"=========== MANUAL MODE STARTED ===========")
        manual_mode()
    elif choice == "2":
        automated_mode()
    else:
        print(Fore.RED + "Invalid choice.\n")


if __name__ == "__main__":
    mode_selector()
