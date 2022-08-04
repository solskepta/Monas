import json
from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
import names
import random
import threading
import os
import csv

from src.utils.utils import Useragents, log_message, read_file, notify_entry, load_proxies

init(autoreset=True)

class Whooopty:

    def __init__(self):
        self.read_files()
        self.setup()
        if os.path.exists("./data/proxies.txt"):
            self.proxies = load_proxies("./data/proxies.txt")
        else:
            log_message("Error", "Proxy file not found.")
            exit()

    def read_files(self):

        self.config = read_file("./data/config.json")

        self.webhook: str = self.config["settings"]["webhook"]
        self.catchall: str = self.config["settings"]["catchall"]
        self.task_number: int = int(self.config["settings"]["tasks_per_profile"])

        with open(r'./data/profiles.csv', 'r') as file:
            reader = csv.reader(file)
            firstline = True
            for row in reader:
                if firstline:  # skip first line
                    firstline = False
                    continue
                self.PROFILE = row

                self.line1: str = self.PROFILE[0]
                self.line2: str = self.PROFILE[1]
                self.city: str = self.PROFILE[2]
                self.postcode: str = self.PROFILE[3]
                
        if '@' in self.catchall:
            self.catchall = self.catchall.replace('@', '')

    def setup(self):
        self.site_options = {1: "GiffGaff",
                            2: "SOON",
                            3: "SOON",
                            4: "SOON"}
        for key, val in self.site_options.items():
            print(Fore.CYAN + f"{key}. - {val}")
        self.site = str(input("What site would you like to run?\n"))
        while '1' not in self.site.lower().strip() and '2' not in self.site.lower().strip() and '3' not in self.site.lower().strip() and '4' not in self.site.lower().strip():
            self.site = str(input("Please choose a valid option...\n"))
        if self.site == '1':
            self.site_string = 'GiffGaff'
            print(Fore.CYAN + Style.BRIGHT + self.site_string + ' Mode Initialized')
            self.site_url = 'https://www.giffgaff.com/free-sim-cards'
    
    def jig_info(self):
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name()
        
        self.buildingNum = self.line1.split(' ', 1)[0]
        self.street = self.line1.split(' ', 1)[1]

    def create_payload(self, useragent: str) -> dict:
        #self.email = f"{self.first_name}.{self.last_name}{random.randint(1, 999)}@{self.catchall}"
        self.email = 'oliver.pleasance@hotmail.com'
        return {
                'preselect_gb_sku': '', 
                'simorder_security_token': self.token,
                'non-submission-elements': '',
                'firstname': self.first_name,
                'lastname': self.last_name,
                'email': self.email,
                'alternative_phone': '', 
                'postcode': self.postcode,
                'buildingNum': self.buildingNum,
                'locality': '',
                'buildingName': '',
                'abodeNumber': '',
                'street': self.street,
                'line1': self.line1,
                'line2': '',
                'city': self.city,
                'state': '',
                'notify': '1',
                'submitButton': 'Order your free SIM',
            }
    
    def checkout(self):
        print(self.PROFILE)
        headers = {
                "authority": "www.giffgaff.com",
                "method": "POST",
                "path": "/ajax-helper/sim-order",
                "scheme": "https",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "content-length": "377",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://www.giffgaff.com",   
                "referer": "https://www.giffgaff.com/free-sim-cards",
                "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "user-agent": Useragents().get_random_useragent(),
        }

        s = requests.Session()
        if self.proxies:
            s.proxies.update(random.choice(self.proxies))
        s.headers.update(headers)

        try:
            r = s.get(self.site_url, headers={
            "authority": "www.giffgaff.com",
            "method": "GET",
            "path": "/free-sim-cards",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "referer": "https://www.giffgaff.com/",
            "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": Useragents().get_random_useragent(),
            })

            soup = BeautifulSoup(r.text, 'html.parser')
            self.token = soup.find_all('input')[1]['value']
            log_message('Security Token Successfully Parsed As', f'[{self.token}]')
            
        except ConnectionError:
            log_message("ERROR", "Connection error. Try again later.")
            exit()

        if r.status_code not in range(200, 210):
            log_message("Error", f"[{r.status_code}] - Failed to retrieve the raffle URL.")
            exit()

        else:
            while self.site != '1':
                self.site = str(input("Please choose a valid option... (Only GiffGaff is live as of now)\n"))
        self.jig_info()

        useragent = Useragents().get_random_useragent()
        payload = self.create_payload(useragent)

        ###esponse = s.post('https://www.giffgaff.com/ajax-helper/sim-order', json=payload)
        ##if response.status_code in range(200, 210):
            #log_message("Success", f"[{response.status_code}] - Successfully ordered sim.")
        if self.webhook.strip():
            notify_entry(self.webhook,
                        f"{self.first_name} {self.last_name}",
                        self.email, self.line1, self.site_string)
        else:
            log_message("Error", f"[{response.status_code}] - Failed to enter. {respo.reason}")

    def run(self):

        more = True

        while more:
            threads = []
            for i in range(len(self.PROFILE)):
                i = threads
                t = threading.Thread(target=self.checkout())
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            again = input("Would you like to run more? (Yes/No)\n")
            if again.lower().startswith('y'):
                continue
            else:
                more = False


