import datetime
import json
import os
import random
import site
import requests
from colorama import Fore, init
from discord_webhook import DiscordWebhook, DiscordEmbed
from typing import Union

class Icons:
    def __init__(self):
        self.PFP = "https://cdn.discordapp.com/attachments/993642384686596188/1004784274018414662/imgonline-com-ua-resize-yOEFrCHaTB5d5Y.jpg"
        self.SOLSKEPTA = "https://cdn.discordapp.com/attachments/993642384686596188/1004784449663287296/artworks-000652310233-i1b8gr-t500x500.jpg"

class Colors:
    def __init__(self):
        self.YELLOW = 0xFFFF00
        self.RED = 0xFF0000
        self.PURPLE = 0xAB79F2
        self.BONZAY = 0xAB79F2

class Useragents:

    def __init__(self):
        self.desktop = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.62",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edge/44.18363.8131",
        ]

    def get_random_useragent(self) -> str:
            return random.choice(self.desktop)

def get_time() -> str:
    now = str(datetime.datetime.now().time())
    # now = now[:-3] #[14:49:05.525]
    now = now[:-7]  # only want 3 decimal places
    return f"[{now}]"
    
def log_message(status: str, message: str, location: str = None, ) -> None:
    if location:
        status = f"[{status.upper()}] ({location.upper()})"
    else:
        status = f"[{status.upper()}]"
    if status.lower().strip() == 'success':
        print(Fore.GREEN + f"{get_time()} {status} -> {message}")
    elif status.lower().strip() == 'error':
        print(Fore.RED + f"{get_time()} {status} -> {message}")
    else:
        print(f"{get_time()} {status} -> {message}")

def read_file(filename: str) -> Union[str, dict, None]:
    
    try:
        file_type = filename.split(".")[-1]
        if file_type == "json":
            if os.stat(filename).st_size == 0:
                return {}
            with open(filename, "r") as f:
                j = json.load(f)
            return j

    except Exception as e:
        raise e

def notify_entry(webhook_url: str, name: str, email: str, line1: str, site_string: str) -> None:
    i = Icons()
    c = Colors()
    now = str(datetime.datetime.utcnow().time())[:-5]
    hook = DiscordWebhook(url=webhook_url, username="Whoopty Sim Bot", avatar_url=i.PFP, )
    embed = DiscordEmbed(
        title="Successfully ordered sim from " + site_string,
        url="https://www.giffgaff.com/free-sim-cards",
        color=c.BONZAY,
    )
    embed.add_embed_field(name="Name", value=name)
    embed.add_embed_field(name="Email", value=f"||{email}||", inline=False)
    embed.add_embed_field(name="Address", value=f"||{line1}||", inline=False)
    embed.set_footer(text="@solskepta on Twitter", icon_url=i.SOLSKEPTA)

    hook.add_embed(embed)
    return hook.execute()

def load_proxies(filename: str) -> Union[list, None]:
    with open(filename, "r") as f:
        file_contents = f.read()
        file_contents = file_contents.split("\n")
    formatted_proxy_list = []
    try:
        try:
            for i in range(0, len(file_contents)):
                if ":" in file_contents[i]:
                    tmp = file_contents[i]
                    tmp = tmp.split(":")
                    proxies = {
                        "http": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                        "https": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                    }
                    formatted_proxy_list.append(proxies)
        except:
            # IP auth
            for n in range(0, len(file_contents)):
                if ":" in file_contents[n]:
                    temp = file_contents[n]
                    proxies = {"http": "http://" + temp, "https": "http://" + temp}
                    formatted_proxy_list.append(proxies)
    except:
        return None
    return formatted_proxy_list