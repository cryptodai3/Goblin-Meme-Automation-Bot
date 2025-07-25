from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, re, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Goblin:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://www.goblin.meme",
            "Referer": "https://www.goblin.meme/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://www.goblin.meme/api"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n" + "═" * 90)
        print(Fore.GREEN + Style.BRIGHT + "    ⚡ Goblin Meme Automation BOT ⚡")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.YELLOW + Style.BRIGHT + "    🧠 Project    : Goblin Meme - Automation Bot")
        print(Fore.YELLOW + Style.BRIGHT + "    🧑‍💻 Author     : YetiDAO")
        print(Fore.YELLOW + Style.BRIGHT + "    🌐 Status     : Running & Mining...")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.MAGENTA + Style.BRIGHT + "    🧬 Powered by Cryptodai3 × YetiDAO | Buddy v1.1 🚀")
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "═" * 90 + "\n")

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
        
        return None
    
    async def auth_session(self, cookie: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/auth/session"
        headers = {
            **self.headers,
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def box_lists(self, cookie: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/box"
        headers = {
            **self.headers,
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def box_data(self, cookie: str, box_id: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/box/{box_id}"
        headers = {
            **self.headers,
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def start_mining(self, cookie: str, box_id: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/box/{box_id}/start"
        headers = {
            **self.headers,
            "Content-Length": "2",
            "Content-Type": "application/json",
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
                        if response.status == 400:
                            return None
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def open_box(self, cookie: str, box_id: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/box/{box_id}/claim"
        headers = {
            **self.headers,
            "Content-Length": "2",
            "Content-Type": "application/json",
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def complete_mission(self, cookie: str, box_id: str, mission_url: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/box/{box_id}/mission"
        data = json.dumps({"url":mission_url})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Cookie": cookie
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None

    async def process_check_connection(self, cookie: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(cookie) if use_proxy else None
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if is_valid:
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(cookie)
                continue

            return False
        
    async def process_accounts(self, cookie: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(cookie, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(cookie) if use_proxy else None
            
            username = "N/A"
            balance = "N/A"

            session = await self.auth_session(cookie, proxy)
            if session:
                username = session.get("user", {}).get("xUsername", "N/A")
                balance = session.get("user", {}).get("goblinPoints", 0)

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Handler:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {username} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Balance:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {balance} PTS {Style.RESET_ALL}"
            )
            
            box_lists = await self.box_lists(cookie, proxy)
            if not box_lists:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Boxes  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} GET Available Box Failed {Style.RESET_ALL}"
                )
                return
            
            boxes = box_lists["boxes"]
            
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Boxes  :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Available {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(boxes)}{Style.RESET_ALL}"
            )

            for box in boxes:
                if box:
                    box_id = box["_id"]
                    box_name = box["name"]
                    is_active = box["active"]

                    if not is_active:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}   ●{Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT} {box_name} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Inactive{Style.RESET_ALL}"
                        )
                        continue

                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}   ●{Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT} {box_name} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Active{Style.RESET_ALL}"
                    )

                    data = await self.box_data(cookie, box_id, proxy)
                    if not data:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} GET Status Box Failed {Style.RESET_ALL}"
                        )
                        continue

                    mission_url = data["missionUrl"]
                    mission_desc = data["missionDesc"]
                    is_completed = data["missionCompleted"]
                    is_hasbox = data["hasBox"]
                    is_ready = data["isReady"]
                    is_opened = data["opened"]

                    if not is_hasbox:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Has Box : {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}False{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Starting Mining...{Style.RESET_ALL}"
                        )

                        start = await self.start_mining(cookie, box_id, proxy)
                        if start and start.get("message") == "Box mining started":
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Failed or Already Have an Active Box Mining{Style.RESET_ALL}"
                            )
                        continue

                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Has Box : {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}True{Style.RESET_ALL}"
                    )

                    if not is_ready:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Is Ready: {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Not Yet{Style.RESET_ALL}"
                        )
                        continue

                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Is Ready: {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}True{Style.RESET_ALL}"
                    )

                    if not is_completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Mission : {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{mission_desc}{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Uncomplete {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Completing Mission... {Style.RESET_ALL}"
                        )

                        complete = await self.complete_mission(cookie, box_id, mission_url, proxy)
                        if complete:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Completed{Style.RESET_ALL}"
                            )

                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} Opening Box... {Style.RESET_ALL}"
                            )

                            open = await self.open_box(cookie, box_id, proxy)
                            if open and open.get("message") == "Box opened! Prize credited.":
                                reward = open["prizeAmount"]

                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Reward  : {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{reward} PTS{Style.RESET_ALL}"
                                )

                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT} Starting Mining... {Style.RESET_ALL}"
                                )

                                start = await self.start_mining(cookie, box_id, proxy)
                                if start and start.get("message") == "Box mining started":
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                        f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                        f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Failed or Already Have an Active Box Mining{Style.RESET_ALL}"
                                    )

                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
                                )

                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Not Complete{Style.RESET_ALL}"
                            )
                        continue

                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Mission : {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{mission_desc}{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Completed {Style.RESET_ALL}"
                    )

                    if not is_opened:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Opened  : {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}False{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Opening Box...{Style.RESET_ALL}"
                        )

                        open = await self.open_box(cookie, box_id, proxy)
                        if open and open.get("message") == "Box opened! Prize credited.":
                            reward = open["prizeAmount"]

                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                            )
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Reward  : {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{reward} PTS{Style.RESET_ALL}"
                            )

                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} Starting Mining... {Style.RESET_ALL}"
                            )

                            start = await self.start_mining(cookie, box_id, proxy)
                            if start and start.get("message") == "Box mining started":
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
                                )

                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}     >{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
                            )

    async def main(self):
        try:
            with open('cookies.txt', 'r') as file:
                cookies = [line.strip() for line in file if line.strip()]

            use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(cookies)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)

                separator = "=" * 25
                for idx, cookie in enumerate(cookies, start=1):
                    if cookie:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Of{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {len(cookies)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )
                        
                        await self.process_accounts(cookie, use_proxy, rotate_proxy)
                        await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*60)
                
                delay = 24 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise

if __name__ == "__main__":
    try:
        bot = Goblin()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Goblin Meme - BOT{Style.RESET_ALL}                                       "                              
        )
