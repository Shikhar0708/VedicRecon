import subprocess
from colorama import Fore, Style, init
init(autoreset=True)

OUI_FILE = r"./ieee-oui.txt"
MAC_FILE = r"./mac-vendor.txt"



# ---------------------------------------
# Network Interface Detection
# ---------------------------------------
def list_interfaces():
    result = subprocess.run(
        ["ip", "-o", "link", "show"],
        capture_output=True,
        text=True
    )

    interfaces = []
    for line in result.stdout.splitlines():
        iface = line.split(":")[1].strip()
        if iface != "lo":
            interfaces.append(iface)

    return interfaces


# ---------------------------------------
# Select Interface
# ---------------------------------------
def select_interface():
    interfaces = list_interfaces()

    if not interfaces:
        print(Fore.RED + "\n[-] No interfaces detected!\n")
        return None

    print(Fore.MAGENTA + "\n=== Select Network Interface ===\n")
    for idx, iface in enumerate(interfaces, start=1):
        print(Fore.CYAN + f"{idx}) " + Fore.YELLOW + f"{iface}")

    choice = input(Fore.GREEN + "\nChoice (press Enter for default): ")

    if choice.strip() == "":
        print(Fore.GREEN + f"\n[+] Using default interface: {interfaces[0]}\n")
        return interfaces[0]

    try:
        index = int(choice) - 1
        if 0 <= index < len(interfaces):
            print(Fore.GREEN + f"\n[+] Using interface: {interfaces[index]}\n")
            return interfaces[index]
    except:
        pass

    print(Fore.RED + "\n[-] Invalid choice! Using default.\n")
    return interfaces[0]


# ---------------------------------------
# Select Target Host
# ---------------------------------------
def select_target_host(hosts):
    print(Fore.MAGENTA + "\n=== Select Target Host ===\n")

    for idx, h in enumerate(hosts, start=1):
        print(Fore.CYAN + f"{idx}) " +
              Fore.YELLOW + f"{h['ip']:<15}" +
              Fore.GREEN + f"{h['vendor']}")

    choice = input(Fore.GREEN + "\nChoice (press Enter to cancel): ")

    if choice.strip() == "":
        print(Fore.RED + "\n[-] No target selected.\n")
        return None

    try:
        index = int(choice) - 1
        if 0 <= index < len(hosts):
            selected = hosts[index]
            print(Fore.GREEN + f"\n[+] Selected Target: {selected['ip']}\n")
            return selected
    except:
        pass

    print(Fore.RED + "\n[-] Invalid selection.\n")
    return None


# ---------------------------------------
# MAIN FUNCTION: ARP + SELECT TARGET
# ---------------------------------------
def arp_ip_loader():

    iface = select_interface()

    print(Fore.MAGENTA + "\n[*] Running ARP Scan...\n")

    arp_cmd = [
        "arp-scan",
        "--interface", iface,
        "-O", OUI_FILE,
        "-m", MAC_FILE,
        "-l"
    ]

    output = subprocess.run(arp_cmd, capture_output=True, text=True)
    raw = output.stdout
    hosts = []

    for line in raw.splitlines():
        parts = line.split(maxsplit=2)
        if len(parts) >= 2 and parts[0].count('.') == 3 and ":" in parts[1]:
            hosts.append({
                "ip": parts[0],
                "mac": parts[1],
                "vendor": parts[2] if len(parts) > 2 else "Unknown / Locally Administered"
            })

    print(Fore.MAGENTA + "\n=== CLEAN ARP SCAN RESULTS ===\n")
    for h in hosts:
        print(Fore.YELLOW + f"IP:     {h['ip']}")
        print(Fore.GREEN  + f"MAC:    {h['mac']}")
        print(Fore.CYAN   + f"Vendor: {h['vendor']}\n")

    return select_target_host(hosts)

