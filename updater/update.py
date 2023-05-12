#!/usr/bin/env python3
from typing import List
from pydantic import BaseModel
import logging 
import threading 
import subprocess
import requests
import time 
import os 
import toml
from pathlib import Path

class AuthDetails(BaseModel):
    username: str
    password: str
    subdomain: str
    domain: str

class DNSUpdaterConfig(BaseModel):
    ttl: int
    auth_details: List[AuthDetails]

class DNSUpdater:
    '''
    A class for handling DNS updates.
    '''
    
    def __init__(self):
        toml_file = Path("auth_details.toml")
        with open(toml_file, "r") as f:
            toml_data = toml.load(f)
        
        self.config = DNSUpdaterConfig(**toml_data)
        self.load_logger()
    
    def load_logger(self):
        cur_time = time.strftime("%Y_%m_%d")
        log_name = f"logs/{cur_time}"
        
        if not os.path.exists("logs"):
            os.makedirs("logs")
        if not os.path.exists(log_name):
            open(log_name, "w").close()
        
        if len(os.listdir("logs")) > 1:
            oldest_file = min(os.listdir("logs"))
            os.remove(f"logs/{oldest_file}")
        
        logging.basicConfig(
            format = '%(asctime)s | %(levelname)s: %(message)s', 
            filemode = 'a',
            filename = log_name,
            level = logging.INFO
        )
    
    def check_ip_requires_update(self, subdomain, domain):
        target_ip = subprocess.check_output(
            ["dig", "+short", f"{subdomain}.{domain}"]
        ).decode("utf-8").strip()
        
        my_ip = requests.get("https://domains.google.com/checkip").text

        logging.info(f"Domain name is {subdomain}.{domain} with IP {target_ip}")
        logging.info(f"Host machine ip is {my_ip}")

        if target_ip != my_ip:
            logging.info("IPs do not match, updating...")
            return True 
        else:
            logging.info("IPs match, no update needed")
            return False
    
    def update_ip(self, username, password, domain, subdomain):
        resp = requests.get(
            "https://domains.google.com/nic/update",
            params = {
                "hostname": f"{subdomain}.{domain}",
                "myip": requests.get("https://domains.google.com/checkip").text,
            },
            auth = (
                username,
                password,
            ),
        )

        if resp.status_code == 200:
            logging.info(f"Request success with message: {resp.content}")
        else:
            logging.error(f"Request failed with error {resp.content}")
            exit(1)
    
    def run_update(self):
        self.load_logger()
        
        for (username, password, domain, subdomain) in self.config.auth_details:
            if self.check_ip_requires_update(subdomain, domain):
                self.update_ip(username, password, domain, subdomain)
        
        logging.info(f"Sleeping for {self.config.ttl} seconds")
        threading.Timer(self.config.ttl, self.run_update).start()


def main():
    updater = DNSUpdater()
    updater.run_update()

if __name__ == "__main__":
    main()



