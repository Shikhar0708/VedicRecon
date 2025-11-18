#!/usr/bin/env python3
import argparse
from colorama import Fore, Style, init
init(autoreset=True)

from utils.banner import banner
from utils.privilege_check import is_root
from utils.scan_engine import run_nmap_scan
from utils.arp_engine import arp_ip_loader


# ============================================================
#                      CLI INTERFACE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="VedicRecon CLI Scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # ------------------------------- Target -------------------------------
    parser.add_argument(
        "-t", "--target",
        help="Target IP or hostname"
    )

    parser.add_argument(
        "-p", "--profile",
        required=True,
        help="Scan profile (fast, full, silent, web, udp, os, version)"
    )

    # ------------------------------- ARP Mode ------------------------------
    parser.add_argument(
        "--arp",
        action="store_true",
        help="Use ARP scan to automatically discover a target"
    )

    # ----------------------------- Exploit Mode ---------------------------
    parser.add_argument(
        "--exploits",
        action="store_true",
        help="Automatically run Searchsploit without asking"
    )

    parser.add_argument(
        "--no-exploits",
        action="store_true",
        help="Skip Searchsploit enumeration entirely"
    )

    # ------------------------------- Save Mode ----------------------------
    parser.add_argument(
        "--save",
        choices=["txt", "xml", "html"],
        help="Save report automatically (txt/xml/html)"
    )

    # ------------------------------- Banner -------------------------------
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Disable banner output"
    )

    args = parser.parse_args()

    # ============================================================
    #                          ROOT CHECK
    # ============================================================
    if not is_root():
        print(Fore.RED + "[!] Root privileges are required!\n" + Style.RESET_ALL)
        exit(1)

    # ============================================================
    #                    SELECT TARGET / ARP MODE
    # ============================================================
    if args.arp:
        target_info = arp_ip_loader()
        target = target_info["ip"]
    else:
        if not args.target:
            print(Fore.RED + "[!] You must provide --target or use --arp" + Style.RESET_ALL)
            exit(1)
        target = args.target

    # ============================================================
    #                    SEARCHSPLOIT MODE DECISION
    # ============================================================
    if args.exploits and args.no_exploits:
        print(Fore.RED + "[!] You cannot use --exploits and --no-exploits at the same time." + Style.RESET_ALL)
        exit(1)

    if args.exploits:
        exploit_mode = "forced-yes"      # always run searchsploit
    elif args.no_exploits:
        exploit_mode = "forced-no"       # never run searchsploit
    else:
        exploit_mode = "ask"             # ask user interactively

    # ============================================================
    #                      REPORT SAVE MODE
    # ============================================================
    # args.save -> None / "txt" / "xml" / "html"
    report_type = args.save

    # ============================================================
    #                     RUN MAIN SCAN ENGINE
    # ============================================================
    run_nmap_scan(
        target=target,
        profile=args.profile,
        show_banner=not args.no_banner,
        exploit_mode=exploit_mode,
        save_report=report_type
    )


if __name__ == "__main__":
    main()
