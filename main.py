

import requests
import re
import time
import random
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

info = {
    "owner": "chilli",
    "facebook": "N/A",
    "tool": "Spamshare",
    "version": "1.0"
}

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + Style.BRIGHT + f"  TOOL: {info['tool']}   |   VERSION: {info['version']}")
    print(Fore.YELLOW + Style.BRIGHT + f"  OWNER: {info['owner']}   |   FACEBOOK: {info['facebook']}")
    print(Fore.CYAN + "=" * 60)

class Share:
    def __init__(self, cookie, post, share_count):
        self.cookie = cookie
        self.post = post
        self.share_count = share_count
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'cookie': cookie
        }

    def get_token(self):
        url = "https://business.facebook.com/content_management"
        res = requests.get(url, headers=self.headers)
        match = re.search(r'EAAG(.*?)","', res.text)
        if not match:
            raise Exception("Token not found. Check your cookie.")
        return "EAAG" + match.group(1)

    def share(self, token):
        self.headers['accept-encoding'] = 'gzip, deflate'
        self.headers['host'] = 'b-graph.facebook.com'

        for count in range(1, self.share_count + 1):
            try:
                url = f"https://b-graph.facebook.com/me/feed?link={self.post}&published=0&access_token={token}"
                res = requests.post(url, headers=self.headers)
                if 'id' in res.json():
                    print(Fore.GREEN + f"[+] {count}/{self.share_count} shared successfully.")
                else:
                    print(Fore.RED + "[!] Cookie may be invalid or blocked. Exiting...")
                    break
            except Exception as e:
                print(Fore.RED + f"[!] Request failed: {e}")
                break

        print(Fore.GREEN + Style.BRIGHT + "[*] Sharing process completed.")

def run():
    clear_console()
    banner()

    print()
    cookie = input(Fore.BLUE + Style.BRIGHT + "[?] Enter Facebook Cookie: ").strip()

    print()
    post = input(Fore.BLUE + Style.BRIGHT + "[?] Enter Post Link: ").strip()

    print()
    try:
        share_count = int(input(Fore.BLUE + Style.BRIGHT + "[?] Number of Shares: ").strip())
    except ValueError:
        print(Fore.RED + "[!] Invalid number for shares.")
        return

    if not post.startswith("http") or share_count <= 0:
        print(Fore.RED + "[!] Invalid post link or share count.")
        return

    clear_console()
    banner()
    print(Fore.YELLOW + "[*] Starting sharing process...")

    tool = Share(cookie, post, share_count)
    try:
        token = tool.get_token()
        tool.share(token)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

if __name__ == "__main__":
    run()
