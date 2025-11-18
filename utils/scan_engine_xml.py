#!/usr/bin/env python3
import subprocess
import xml.etree.ElementTree as ET

# ============================================
#       RUN NMAP XML SCAN
# ============================================

def run_nmap_xml(target, flags):
    """
    Runs Nmap with XML output (-oX -) to STDOUT.
    Useful for parsing service version information.
    
    Example:
        run_nmap_xml("10.0.2.1", "-sV -F")
    """
    cmd = ["nmap"] + flags.split() + ["-oX", "-", target]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"<error>Failed to execute Nmap: {e}</error>"


# ============================================
#       PARSE XML SERVICE OUTPUT
# ============================================

def parse_nmap_services(xml_data):
    """
    Extract services from XML scan output.
    
    Returns list of:
    {
        'port': '80',
        'service': 'http',
        'version': 'Apache 2.4.51'
    }
    """
    services = []

    try:
        root = ET.fromstring(xml_data)
    except Exception:
        return services

    for host in root.findall("host"):
        ports = host.find("ports")
        if ports is None:
            continue

        for port in ports.findall("port"):
            portid = port.get("portid", "")
            proto = port.get("protocol", "")

            svc = port.find("service")
            if svc is None:
                continue

            name = svc.get("name", "")
            product = svc.get("product", "")
            version = svc.get("version", "")

            full_version = f"{product} {version}".strip()

            services.append({
                "port": portid,
                "service": name,
                "version": full_version
            })

    return services
