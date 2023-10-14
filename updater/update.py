#!/usr/bin/env python3

'''
A docstring for the updater module.
'''

from typing import List
import logging
import threading
import subprocess
import time
import os
from pathlib import Path
import requests
import toml
from pydantic import BaseModel

class AuthDetails(BaseModel):
    '''
    A class for storing the authentication details for a domain.
    '''
    username: str
    password: str
    subdomain: str
    domain: str

class DNSUpdaterConfig(BaseModel):
    '''
    A class for storing the configuration for the DNSUpdater.
    '''
    ttl: int
    auth_details: List[AuthDetails]

class DNSUpdater:
    '''
    A class for handling DNS updates.
    
    Attributes:
        config (DNSUpdaterConfig): The configuration for the DNSUpdater.
        { 
            ttl, 
            [ 
                auth_details { username, password, subdomain, domain } 
            ] 
        }
    '''

    def __init__(self):
        '''
        Initialises the config and logger for the DNSUpdater class.
        
        The config is loaded from the auth_details.toml file. This is
        achieved through the use of Pydantic.
        '''

        toml_file = Path("auth_details.toml")
        with open(toml_file, "r", encoding = "utf-8") as f:
            toml_data = toml.load(f)

        self.config = DNSUpdaterConfig(**toml_data)
        self.load_logger()

    def load_logger(self):
        '''
        Writes to a log file in the logs directory. The log file name is
        based on the current date in the format YYYY_MM_DD. If there already
        exists a log file, the oldest log file is deleted.
        '''

        cur_time = time.strftime("%Y_%m_%d")
        log_name = f"logs/{cur_time}"

        if not os.path.exists("logs"):
            os.makedirs("logs")
        if not os.path.exists(log_name):
            open(log_name, "w", encoding = "utf-8").close()

        if len(os.listdir("logs")) > 1:
            oldest_file = min(os.listdir("logs"))
            os.remove(f"logs/{oldest_file}")

        logging.basicConfig(
            format = '%(asctime)s | %(levelname)s: %(message)s', 
            filemode = 'a',
            filename = log_name,
            level = logging.INFO
        )

    def check_ip_requires_update(self, subdomain: str, domain: str) -> bool:
        '''
        Returns if subdomain.domain requires an update. This is done by 
        checking if the ip of subdomain.domain matches the ip of the host.
        
        Arguments:
            subdomain (str): The subdomain of the domain to check.
            domain (str): The domain to check.
        
        Returns:
            bool: Whether the ip of subdomain.domain matches the ip of the host.
        '''

        target_ip = subprocess.check_output(
            ["dig", "+short", f"{subdomain}.{domain}"]
        ).decode("utf-8").strip()

        my_ip = requests.get("https://domains.google.com/checkip", timeout = 10).text

        logging.info("Domain name is %s.%s with IP %s", subdomain, domain, target_ip)
        logging.info("Host machine ip is %s", my_ip)

        if target_ip != my_ip:
            logging.info("IPs do not match, updating...")
            return True 
        else:
            logging.info("IPs match, no update needed")
            return False

    def update_ip(self, username: str, password: str, domain: str, subdomain: str):
        '''
        Sends a request to Google Domains to update the ip of subdomain.domain.
        The request is formatted as follows:
            https://domains.google.com/nic/update?hostname=subdomain.domain&myip=ip
        
        Arguments:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            domain (str): The domain to update.
            subdomain (str): The subdomain of the domain to update.
        '''

        resp = requests.get(
            "https://domains.google.com/nic/update",
            params = {
                "hostname": f"{subdomain}.{domain}",
                "myip": requests.get("https://domains.google.com/checkip", timeout = 10).text,
            },
            auth = (
                username,
                password,
            ),
            timeout = 10,
        )

        if resp.status_code == 200:
            logging.info("Request success with message: %s", resp.content)
        else:
            logging.error("Request failed with error %s", resp.content)
            exit(1)

    def run_update(self):
        '''
        For each auth_details stored in the config, checks if the subdomain.domain
        requires an update. If it does, the ip of subdomain.domain is updated.
        
        After the update, the function sleeps for ttl seconds before running again.
        '''

        self.load_logger()

        for auth_details in self.config.auth_details:
            if self.check_ip_requires_update(auth_details.subdomain, auth_details.domain):
                self.update_ip(
                    auth_details.username,
                    auth_details.password,
                    auth_details.domain,
                    auth_details.subdomain,
                )

        logging.info('Sleeping for %s seconds', self.config.ttl)
        threading.Timer(self.config.ttl, self.run_update).start()


def main():
    '''
    The main function for the updater. Creates a DNSUpdater and runs the update.
    '''
    updater = DNSUpdater()
    updater.run_update()

if __name__ == "__main__":
    main()
