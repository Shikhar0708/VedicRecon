import random
from colorama import Fore, Style, init
init(autoreset=True)

# --- BANNERS (using raw f-strings so no escape warnings) ---
BANNERS = [

rf"""{Fore.GREEN}
   .--.
  |o_o |    
  |:_/ |    {Fore.YELLOW}VedicRecon Scanner
 //   \ \  
(|     | ) 
/'\_   _/`\
\___)=(___/ 
{Style.RESET_ALL}
""",
rf"""{Fore.RED}
      .----.
    _/      \_
   (  ◉    ◉  )   {Fore.YELLOW}VedicRecon SCANNER
    \   __   /
     '-.__.-'
        ||
     ___||___
    /   ||   \\
{Style.RESET_ALL}
""",
rf"""{Fore.YELLOW}
 __     __          _ _      ____                      
 \ \   / /__ _ _ __(_) | ___|  _ \ ___  ___ ___  _ __  
  \ \ / / _ \ '__/ _` |/ _ \ |_) / _ \/ __/ _ \| '_ \ 
   \ V /  __/ | | (_| |  __/  _ <  __/ (_| (_) | | | | {Fore.YELLOW}VedicRecon Scanner
    \_/ \___|_|  \__,_|\___|_| \_\___|\___\___/|_| |_|
              V E D I C R E C O N
{Style.RESET_ALL}
"""
]

# --- prevent repeating the same banner ---
_last_banner = None

def banner(author="DEVIC/VEDIC", version="1.0.a"):
    global _last_banner

    # choose random banner that is NOT the last one
    b = random.choice(BANNERS)
    while b == _last_banner and len(BANNERS) > 1:
        b = random.choice(BANNERS)

    _last_banner = b  # remember last banner used

    print(b)
    print(Fore.BLUE + f" Author  : {author}")
    print(Fore.BLUE + f" Version : {version}\n" + Style.RESET_ALL)
