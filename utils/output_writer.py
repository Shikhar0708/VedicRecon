#!/usr/bin/env python3
import re

# ============================================================
#                ANSI & XML CLEANING HELPERS
# ============================================================

ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

def strip_ansi(text):
    """Remove ANSI terminal color codes."""
    return ANSI_ESCAPE.sub('', text)


def clean_xml(xml_text):
    """
    Remove unnecessary clutter from XML:
    - XML declaration
    - DOCTYPE
    - Stylesheet
    - Comment headers
    """
    xml_text = strip_ansi(xml_text)

    # Remove XML comments <!-- -->
    xml_text = re.sub(r"<!--.*?-->", "", xml_text, flags=re.DOTALL)

    # Remove XML declaration
    xml_text = re.sub(r"<\?xml.*?\?>", "", xml_text)

    # Remove DOCTYPE
    xml_text = re.sub(r"<!DOCTYPE.*?>", "", xml_text)

    # Remove xml-stylesheet
    xml_text = re.sub(r"<\?xml-stylesheet.*?\?>", "", xml_text)

    # Remove empty lines at top
    return xml_text.strip()


def escape_html(text):
    """Escape HTML-sensitive characters."""
    text = strip_ansi(text)
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


# ============================================================
#                       TXT REPORT
# ============================================================

def save_txt(path, xml_output, exploit_results):
    """
    Save combined scan & exploit results in TXT format.
    """
    clean = clean_xml(xml_output)

    with open(path, "w", encoding="utf-8") as f:
        f.write("=== NMAP XML OUTPUT ===\n\n")
        f.write(clean)
        f.write("\n\n=== SEARCHSPLOIT RESULTS ===\n\n")

        for item in exploit_results:
            svc = item["service"]
            ver = item["version"]
            exp = strip_ansi(item["exploits"])

            f.write(f"[Service] {svc} {ver}\n")
            f.write(exp + "\n")
            f.write("-" * 80 + "\n")


# ============================================================
#                       XML REPORT
# ============================================================

def save_xml(path, xml_output):
    """
    Save a clean XML version of the Nmap output.
    """
    clean = clean_xml(xml_output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(clean)


# ============================================================
#                       HTML REPORT
# ============================================================

def save_html(path, services, exploit_results):
    """
    Create a clean HTML report with services + exploit data.
    """
    html = """
<!DOCTYPE html>
<html>
<head>
<title>VedicRecon Scan Report</title>
<style>
body { font-family: Arial; margin: 20px; background: #f4f4f4; }
.section { background: #fff; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
h1 { color: #222; }
pre { background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
.service-entry { margin-bottom: 10px; }
</style>
</head>
<body>

<h1>VedicRecon Scan Report</h1>
"""

    # SERVICES SECTION
    html += "<div class='section'><h2>Detected Services</h2>"
    if services:
        for s in services:
            html += (
                f"<div class='service-entry'><b>{s['port']}/tcp</b> — "
                f"{escape_html(s['service'])} "
                f"({escape_html(s['version'])})</div>"
            )
    else:
        html += "<p>No services detected.</p>"
    html += "</div>"

    # EXPLOIT SECTION
    html += "<div class='section'><h2>Searchsploit Results</h2>"

    if exploit_results:
        for item in exploit_results:
            svc = escape_html(item['service'])
            ver = escape_html(item['version'])
            exp = escape_html(item['exploits'])

            html += f"<h3>{svc} {ver}</h3>"
            html += f"<pre>{exp}</pre>"
    else:
        html += "<p>No exploits found.</p>"

    html += "</div></body></html>"

    # SAVE FILE
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
