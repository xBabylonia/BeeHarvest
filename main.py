import asyncio
import json
from datetime import datetime
import aiohttp
from colorama import Fore, Style, init
from loguru import logger

# Initialize colorama
init(autoreset=True)

# Bot Configuration
CONFIG = {
    "enable_spin": True,
    "enable_stake": False,
    "enable_mining_upgrade": True,
}

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "beeharvest.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)
logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <white>{message}</white>",
    level="INFO"
)

class BeeHarvestBot:
    def __init__(self):
        self.base_url = "https://api.beeharvest.life"
        self.session = None
        self.default_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://beeharvest.life",
            "Referer": "https://beeharvest.life/",
            "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        }

    def print_banner(self):
        """Print the bot banner"""
        banner = f"""{Fore.CYAN}
    ┏━━━━┳┓╋╋╋╋╋┏━━━┓╋╋╋┏┓╋╋╋╋╋┏━━━┓╋╋┏┓╋╋╋╋╋┏━┓    Auto BeeHarvest Bot
    ┃┏┓┏┓┃┃╋╋╋╋╋┃┏━┓┃╋╋╋┃┃╋╋╋╋╋┃┏━┓┃╋╋┃┃╋╋╋╋╋┃┏┛    Modified by @yogschannel
    ┗┛┃┃┗┫┗━┳━━┓┃┃╋┃┣━┳━┛┣━━┳━┓┃┃╋┃┣━━┫┗━┳━━┳┛┗┓
    ╋╋┃┃╋┃┏┓┃┃━┫┃┃╋┃┃┏┫┏┓┃┃━┫┏┛┃┗━┛┃━━┫┏┓┃┏┓┣┓┏┛
    ╋╋┃┃╋┃┃┃┃┃━┫┃┗━┛┃┃┃┗┛┃┃━┫┃╋┃┏━┓┣━━┃┃┃┃┏┓┃┃┃
    ╋╋┗┛╋┗┛┗┻━━┛┗━━━┻┛┗━━┻━━┻┛╋┗┛╋┗┻━━┻┛┗┻┛┗┛┗┛
    {Style.RESET_ALL}
    """
        print(banner)
        logger.info("Starting BeeHarvest Bot...")

    # Authentication Methods
    async def get_token(self, user_data):
        """Get authentication token"""
        try:
            headers = {**self.default_headers, "Content-Type": "application/json"}
            async with self.session.post("/auth/validate", headers=headers, json={"hash": user_data}, timeout=30) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        token = data.get("data", {}).get("token")
                        if token:
                            print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] Token received successfully{Style.RESET_ALL}")
                            return token
                        else:
                            token = data.get("data", {}).get("user", {}).get("token")
                            if token:
                                print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] Token received successfully from alternate path{Style.RESET_ALL}")
                                return token
                            print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] Token not found in response structure{Style.RESET_ALL}")
                    except json.JSONDecodeError:
                        print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] Failed to parse JSON response{Style.RESET_ALL}")
                return None
        except Exception as e:
            print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] Error during token request: {str(e)}{Style.RESET_ALL}")
            return None

    # Task Processing Methods
    async def process_task(self, task, auth_headers):
        """Process a single task"""
        try:
            task_id = task.get("id")
            title = task.get("title", "Unknown Task")
            task_type = task.get("type", "unknown")
            criterions = task.get("criterions", [])
            
            if task.get("ended", False):
                print(f"{Fore.YELLOW}[Task] ⚠ {title} - Task has ended{Style.RESET_ALL}")
                return

            if task_type == "other" and criterions:
                for criterion in criterions:
                    if criterion.get("type") == "transfer":
                        try:
                            description = criterion.get("description")
                            if description:
                                transfer_data = json.loads(description)
                                print(f"{Fore.CYAN}[Task] ℹ {title} - Transfer task detected{Style.RESET_ALL}")
                                await self.verify_task(task_id, auth_headers)
                        except json.JSONDecodeError:
                            print(f"{Fore.RED}[Task] ✗ {title} - Invalid transfer data format{Style.RESET_ALL}")
            else:
                await self.verify_task(task_id, auth_headers)
                
        except Exception as e:
            print(f"{Fore.RED}[Task] ✗ Error processing {title}: {str(e)}{Style.RESET_ALL}")

    async def verify_task(self, task_id, auth_headers):
        """Verify task completion"""
        try:
            async with self.session.post(f"/tasks/check_tg_task/{task_id}", headers=auth_headers) as task_response:
                if task_response.status == 200:
                    response_data = await task_response.json()
                    msg = response_data.get("message", "Task completed")
                    print(f"{Fore.GREEN}[Task] ✓ {msg}{Style.RESET_ALL}")
                else:
                    response_data = await task_response.json()
                    msg = response_data.get("message", "Unknown error")
                    print(f"{Fore.YELLOW}[Task] ⚠ {msg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[Task] ✗ Verification error: {str(e)}{Style.RESET_ALL}")

    async def process_tasks(self, session, auth_headers):
        """Process all available tasks"""
        async with session.get("/tasks/user", headers=auth_headers) as response:
            if response.status == 200:
                tasks = (await response.json()).get('data', [])
                if tasks:
                    logger.info(f"Found {len(tasks)} tasks")
                    for task in tasks:
                        if not task.get("ended", False):
                            task_id = task.get("id")
                            async with session.post(f"/tasks/check_tg_task/{task_id}", headers=auth_headers) as task_response:
                                if task_response.status == 200:
                                    logger.success(f"Task {task_id} completed")

    # Spin Processing Methods
    async def get_spin_info(self, session, auth_headers):
        """Get spin information"""
        try:
            async with session.get("/spinner/spin", headers=auth_headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {})
                return None
        except Exception as e:
            logger.error(f"{Fore.RED}Error getting spin info: {str(e)}{Style.RESET_ALL}")
            return None

    async def perform_spin(self, session, auth_headers, spin_count):
        """Perform spin with specified count"""
        try:
            payload = {"spin_count": spin_count}
            headers = {**auth_headers, "Content-Type": "application/json"}
            async with session.post("/spinner/spin", headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    rewards = data.get("data", [])
                    if rewards:
                        for reward in rewards:
                            reward_type = reward.get("type", "unknown")
                            reward_value = reward.get("value", 0)
                            reward_count = reward.get("count", 0)
                            logger.info(f"{Fore.GREEN}Spin Reward: {reward_count}x {reward_type} (value: {reward_value}){Style.RESET_ALL}")
                    return True
                return False
        except Exception as e:
            logger.error(f"{Fore.RED}Error performing spin: {str(e)}{Style.RESET_ALL}")
            return False

    async def process_spins(self, session, auth_headers):
        """Process all available spins"""
        if not CONFIG["enable_spin"]:
            logger.info(f"{Fore.YELLOW}Spin feature is disabled in config{Style.RESET_ALL}")
            return

        spin_info = await self.get_spin_info(session, auth_headers)
        if not spin_info:
            return

        spin_count = spin_info.get("spin_count", 0)
        logger.info(f"{Fore.CYAN}Available spins: {spin_count}{Style.RESET_ALL}")

        while spin_count >= 5:
            logger.info(f"{Fore.CYAN}Performing 5x spin{Style.RESET_ALL}")
            if await self.perform_spin(session, auth_headers, 5):
                spin_count -= 5
            else:
                break
            await asyncio.sleep(1)

        while spin_count >= 3:
            logger.info(f"{Fore.CYAN}Performing 3x spin{Style.RESET_ALL}")
            if await self.perform_spin(session, auth_headers, 3):
                spin_count -= 3
            else:
                break
            await asyncio.sleep(1)

        while spin_count >= 1:
            logger.info(f"{Fore.CYAN}Performing 1x spin{Style.RESET_ALL}")
            if await self.perform_spin(session, auth_headers, 1):
                spin_count -= 1
            else:
                break
            await asyncio.sleep(1)

    # Squad Methods
    async def check_squad_status(self, session, auth_headers):
        """Check if user is in a squad"""
        try:
            async with session.get("/user/profile", headers=auth_headers) as response:
                if response.status == 200:
                    user_info = await response.json()
                    squad_id = user_info.get("data", {}).get("squad_id")
                    return squad_id is not None and squad_id > 0
                return False
        except Exception as e:
            logger.error(f"Error checking squad status: {str(e)}")
            return False

    # Account Processing Methods
    async def process_account(self, user_data):
        """Process a single account"""
        async with aiohttp.ClientSession(base_url=self.base_url) as session:
            try:
                # Get token
                headers = {**self.default_headers, "Content-Type": "application/json"}
                async with session.post("/auth/validate", headers=headers, json={"hash": user_data}) as response:
                    if response.status != 200:
                        logger.error(f"{Fore.RED}Failed to get token - skipping account{Style.RESET_ALL}")
                        return
                    token = (await response.json()).get("data", {}).get("token")
                    if not token:
                        logger.error(f"{Fore.RED}No token received - skipping account{Style.RESET_ALL}")
                        return

                auth_headers = {**self.default_headers, "Authorization": f"Bearer {token}"}

                # Get User Info
                async with session.get("/user/profile", headers=auth_headers) as response:
                    if response.status == 200:
                        user_info = await response.json()
                        username = user_info.get("data", {}).get("tg_username")
                        balance = user_info.get("data", {}).get("balance")
                        logger.info(f"{Fore.CYAN}Account: {username} | Balance: {balance}{Style.RESET_ALL}")


                # Login Daily
                async with session.post("/user/streak/claim", headers=auth_headers) as response:
                    msg = (await response.json()).get("message", "Unknown response")
                    logger.info(f"{Fore.GREEN}Daily Login: {msg}{Style.RESET_ALL}")

                # Process Spins
                await self.process_spins(session, auth_headers)

                # Upgrade Mining if enabled
                if CONFIG["enable_mining_upgrade"]:
                    async with session.post("/user/boost/honey/next_level", headers=auth_headers) as response:
                        msg = (await response.json()).get("message", "Unknown response")
                        logger.info(f"{Fore.GREEN}Mining Upgrade: {msg}{Style.RESET_ALL}")

                # Join Squad
                async with session.post("/user/join_squad/2637", headers=auth_headers) as response:
                    msg = (await response.json()).get("message", "Unknown response")
                    logger.info(f"{Fore.GREEN}Join Squad: {msg}{Style.RESET_ALL}")

                # Process Tasks
                await self.process_tasks(session, auth_headers)

                # Check squad status before staking
                is_in_squad = await self.check_squad_status(session, auth_headers)

                # Get Final Balance and Stake if enabled
                if CONFIG["enable_stake"]:
                    async with session.get("/user/profile", headers=auth_headers) as response:
                        if response.status == 200:
                            user_info = await response.json()
                            balance = float(user_info.get("data", {}).get("balance", 0))
                            logger.info(f"{Fore.CYAN}Balance: {balance:.5f}{Style.RESET_ALL}")

                            if balance > 0:
                                if is_in_squad:
                                    stake_payload = {"amount": balance}
                                    headers = {**auth_headers, "Content-Type": "application/json"}
                                    async with session.post("/token_pool/", headers=headers, json=stake_payload) as response:
                                        status = "✓" if response.status == 200 else "✗"
                                        logger.info(f"{Fore.GREEN}Staked {balance:.5f} tokens - Status: {status}{Style.RESET_ALL}")
                                else:
                                    logger.warning(f"{Fore.YELLOW}Skipping stake for {balance:.5f} tokens - Account not in squad{Style.RESET_ALL}")

            except Exception as e:
                logger.error(f"{Fore.RED}Account Error: {str(e)}{Style.RESET_ALL}")

    async def process_all_accounts(self):
        """Process all accounts from data.txt"""
        try:
            # Check if data.txt exists
            try:
                with open("data.txt", "r") as file:
                    accounts = file.readlines()
                    if not accounts:
                        print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] data.txt is empty{Style.RESET_ALL}")
                        return
                    print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] Found {len(accounts)} accounts in data.txt{Style.RESET_ALL}")
            except FileNotFoundError:
                print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] data.txt not found{Style.RESET_ALL}")
                return

            for i, account_data in enumerate(accounts):
                account_data = account_data.strip()
                if account_data:
                    print(f"\n{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] Processing account {i+1}/{len(accounts)}{Style.RESET_ALL}")
                    await self.process_account(account_data)
                    if i < len(accounts) - 1:
                        print(f"\n{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] Waiting 3 seconds before next account...{Style.RESET_ALL}\n")
                        await asyncio.sleep(3)
                else:
                    print(f"{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] Skipping empty line in data.txt{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] Error in process_all_accounts: {str(e)}{Style.RESET_ALL}")

    async def run(self):
        """Main run method"""
        self.print_banner()
        cycle_count = 1
        
        while True:
            try:
                logger.info(f"Starting Cycle #{cycle_count}")

                try:
                    with open("data.txt", "r") as file:
                        accounts = [line.strip() for line in file if line.strip()]
                    
                    if not accounts:
                        logger.error("data.txt is empty")
                        return

                    logger.info(f"Found {len(accounts)} accounts")

                    for i, account_data in enumerate(accounts, 1):
                        logger.info(f"Processing account {i}/{len(accounts)}")
                        await self.process_account(account_data)
                        if i < len(accounts):
                            await asyncio.sleep(3)

                except FileNotFoundError:
                    logger.error("data.txt not found")
                    return

                logger.info(f"Cycle #{cycle_count} completed. Waiting 10 minutes...")
                
                for remaining in range(600, 0, -1):
                    minutes = remaining // 60
                    seconds = remaining % 60
                    print(f"Next cycle in: {minutes:02d}:{seconds:02d}", end='\r')
                    await asyncio.sleep(1)
                
                cycle_count += 1

            except Exception as e:
                logger.error(f"Error: {str(e)}")
                logger.warning("Waiting 60 seconds before retry...")
                await asyncio.sleep(60)

# Main entry point
if __name__ == "__main__":
    try:
        bot = BeeHarvestBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user")