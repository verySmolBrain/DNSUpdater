import dns
from getpass import getpass
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Flag to update env easily
# Threading to check for update in background (Implement in Tauri)

load_dotenv(join(dirname(__file__), '.env')) # Gets env file in current directory

if os.getenv('CONFIG_VERSION') != dns.config_version():
    if os.path.isfile('.env'):
        print("Invalid environment configuration. Please delete .env and run dns_update.py again")
        exit()
    print("Setting up environment...")
    dns.setup.__init__() # Runs setup.py
    
print(""" 
█▀▄ █▄░█ █▀   █░█ █▀█ █▀▄ ▄▀█ ▀█▀ █▀▀ █▀█
█▄▀ █░▀█ ▄█   █▄█ █▀▀ █▄▀ █▀█ ░█░ ██▄ █▀▄
""")

username = dns.config.username()
subdomain = dns.config.subdomain()
domain = dns.config.domain()
if dns.config.is_save_password():
    password = dns.config.password()
else:
    password = getpass("Enter password for {}.{}: ".format(subdomain, domain))

dns.domain_request.create_request(username, password, subdomain, domain) # Runs domain_request.py
