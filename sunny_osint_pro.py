#!/usr/bin/env python3
# sunny_osint_pro.py

import requests
import time
import sys
import json
import threading
from colorama import init, Fore, Style

init(autoreset=True)

# ================== CONFIG ==================
API_LIST = [
    "https://ayaanmods.site/number.php?key=annonymous&number=",
    # future APIs yaha add kar sakte ho
]
# ===========================================

_fetch_container = {"done": False, "results": [], "error": None}

# ================== BANNER ==================
def banner():
    ascii_art = f"""
{Fore.CYAN}
   ███████╗██╗   ██╗███╗   ██╗███╗   ██╗██╗   ██╗
   ██╔════╝██║   ██║████╗  ██║████╗  ██║╚██╗ ██╔╝
   ███████╗██║   ██║██╔██╗ ██║██╔██╗ ██║ ╚████╔╝ 
   ╚════██║██║   ██║██║╚██╗██║██║╚██╗██║  ╚██╔╝  
   ███████║╚██████╔╝██║ ╚████║██║ ╚████║   ██║   
   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝   ╚═╝   

        ☠️  SUNNY OSINT PRO ☠️
"""
    print(ascii_art)
    print(Fore.YELLOW + "        Advanced Mobile Intelligence Tool\n")

# ================= API CALL =================
def call_api(api_url, number):
    try:
        resp = requests.get(api_url + str(number), timeout=8)
        if resp.status_code != 200:
            return []

        data = resp.json()

        if "result" in data and isinstance(data["result"], list):
            return data["result"]

    except:
        return []

    return []

# ============================================

def fetch_thread(number):
    all_results = []

    for api in API_LIST:
        results = call_api(api, number)
        if results:
            all_results.extend(results)

    _fetch_container["results"] = all_results
    _fetch_container["done"] = True

def get_number():
    number = input(Fore.GREEN + "📱 Enter mobile number: " + Style.BRIGHT).strip()

    if not number.isdigit() or len(number) != 10:
        print(Fore.RED + "[!] Invalid number!")
        return None
    return number

# ================= LOADER ===================
def progress_bar():
    spinner = "|/-\\"
    i = 0

    while not _fetch_container["done"]:
        sys.stdout.write(
            f"\r{Fore.CYAN}Scanning {spinner[i % 4]} "
        )
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    print(f"\r{Fore.GREEN}✔ Scan Complete!          ")

# ============================================

def print_result(entry, idx):
    print(Fore.CYAN + Style.BRIGHT + f"\n══════ RESULT {idx} ══════")

    print(Fore.GREEN + f"👤 Name       : {entry.get('name', 'N/A')}")
    print(Fore.GREEN + f"👨 Father     : {entry.get('father_name', 'N/A')}")
    print(Fore.GREEN + f"📱 Mobile     : {entry.get('mobile', 'N/A')}")
    print(Fore.GREEN + f"📞 Alt Mobile : {entry.get('alternate', 'N/A')}")
    print(Fore.GREEN + f"📧 Email      : {entry.get('email', 'N/A')}")
    print(Fore.GREEN + f"🆔 ID         : {entry.get('id', 'N/A')}")
    print(Fore.GREEN + f"📍 Circle     : {entry.get('circle', 'N/A')}")
    print(Fore.GREEN + f"🏠 Address    : {entry.get('address', 'N/A')}")

# ================= MAIN =====================
def main():
    banner()

    number = get_number()
    if not number:
        return

    _fetch_container["done"] = False

    t = threading.Thread(target=fetch_thread, args=(number,), daemon=True)
    t.start()

    progress_bar()

    results = _fetch_container["results"]

    if not results:
        print(Fore.RED + "\n❌ No data found.")
        return

    print(Fore.GREEN + f"\n🔥 Total Results: {len(results)}")

    for idx, entry in enumerate(results, 1):
        print_result(entry, idx)

# ============================================

if __name__ == "__main__":
    main()
