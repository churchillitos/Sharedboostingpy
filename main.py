

import requests
import re
import time
import random
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔════════════════════════════════════════════╗
║     🚀 SHARE BOOSTING TOOL BY CHILLI       ║
╚════════════════════════════════════════════╝
    """)

class ShareBoost:
    def __init__(self, cookie, link, amount):
        self.cookie = cookie
        self.link = link
        self.amount = amount
        self.headers = {
            'user-agent': 'Mozilla/5.0',
            'cookie': cookie
        }
        self.log_path = f"logs/shares-{datetime.now().strftime('%Y%m%d')}.txt"
        os.makedirs("logs", exist_ok=True)

    def get_token(self):
        url = 'https://business.facebook.com/content_management'
        res = requests.get(url, headers=self.headers)
        match = re.search(r'EAAG(.*?)\\"', res.text)
        if not match:
            raise Exception("Access token not found")
        return 'EAAG' + match.group(1)

    def share_post(self, token, count):
        share_url = f"https://b-graph.facebook.com/me/feed?link={self.link}&published=0&access_token={token}"
        for attempt in range(1, 4):  # up to 3 attempts
            try:
                res = requests.post(share_url, headers=self.headers)
                data = res.json()
                if 'id' not in data:
                    raise Exception("Share failed or blocked")
                print(Fore.GREEN + f"[{count}] ✅ Shared (Try {attempt})")
                self.write_log(f"[{count}] ✅ Shared successfully (Try {attempt})")
                return
            except Exception as e:
                print(Fore.RED + f"[{count}] ❌ Attempt {attempt} failed: {e}")
                time.sleep(2 * attempt)

        self.write_log(f"[{count}] ❌ Failed after 3 attempts")

    def write_log(self, text):
        with open(self.log_path, "a") as log:
            log.write(f"{datetime.now().strftime('%H:%M:%S')} {text}\n")

    def run(self):
        print_banner()
        print(Fore.YELLOW + f"Target Link: {self.link}\nShares: {self.amount}\n")
        token = self.get_token()

        for i in range(1, self.amount + 1):
            self.share_post(token, i)
            delay = random.randint(3, 6)
            time.sleep(delay)

        print(Fore.CYAN + f"\n✅ Done boosting {self.amount} shares!")

if __name__ == '__main__':
    try:
        print_banner()
        fb_cookie = input(Fore.YELLOW + "[🔒] Enter Facebook Cookie: ").strip()
        post_link = input(Fore.YELLOW + "[🔗] Enter Facebook Post Link: ").strip()
        amount = int(input(Fore.YELLOW + "[#️⃣] Enter Share Amount: ").strip())

        if not fb_cookie or not post_link.startswith("http") or amount <= 0:
            raise ValueError("Invalid input provided.")

        booster = ShareBoost(fb_cookie, post_link, amount)
        booster.run()

    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)}")
