import os
import shlex
from dotenv import load_dotenv

# Load .env from project root regardless of CWD
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".env"
)
load_dotenv(env_path)

def load_profile(name):
    key = name.upper()  # FULL, SILENT, FAST, etc.
    value = os.getenv(key)

    if value is None:
        raise ValueError(f"Profile '{name}' not found in .env")

    return shlex.split(value)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env from project root
env_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(env_path)

def load_profile(name):
    key = name.upper()  # FULL, SILENT, FAST, etc.
    value = os.getenv(key)

    if value is None:
        raise ValueError(f"Profile '{name}' not found in .env")

    return shlex.split(value)

# -------------------------------------------------
# DEPENDENCY FILE LOCATIONS (new logic)
# -------------------------------------------------

# utils/ directory (where this file lives)
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))

# utils/dependency/ folder
DEPENDENCY_DIR = os.path.join(UTILS_DIR, "dependency")

# Fully resolved absolute file paths
OUI_FILE = os.path.join(DEPENDENCY_DIR, "ieee-oui.txt")
MAC_FILE = os.path.join(DEPENDENCY_DIR, "mac-vendor.txt")

def get_dependency_paths():
    """Return absolute paths to OUI and MAC database files."""
    return OUI_FILE, MAC_FILE