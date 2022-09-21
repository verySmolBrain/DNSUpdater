#!/usr/bin/env python3
import logging 
import threading 
import subprocess
import requests
import time 
import os 

def setupEnvironment():
    REQUIRED_ENV_VARS = [
        "TTL", 
        "USERNAME",
        "PASSWORD",
        "DOMAIN", 
        "SUBDOMAIN",
    ]

    for env_var in REQUIRED_ENV_VARS:
        if not os.environ.get(env_var):
            logging.critical(f"Please set the {env_var} environment variable")
            exit(1)


    if int(os.environ.get("TTL")) < 900:
        logging.critical(
            f"Please set TTL to at least 900 seconds, currently set to {os.environ.get('TTL')}")
    if not os.path.exists("logs"):
        os.makedirs("logs")

    curTime = time.strftime("%Y_%m_%d-%I_%M_%S_%p")
    logName = f"logs/{curTime}"
    logging.basicConfig(
        format = '%(asctime)s | %(levelname)s: %(message)s', 
        filemode = 'a',
        filename = logName,
        level = logging.INFO
    )

def IPRequireUpdate():
    SUBDOMAIN = os.environ.get("SUBDOMAIN")
    DOMAIN = os.environ.get("DOMAIN")

    targetIP = subprocess.check_output(
        ["dig", "+short", f"{SUBDOMAIN}.{DOMAIN}"]
    ).decode("utf-8").strip()
    
    myIP = requests.get("https://domains.google.com/checkip").text

    logging.info(f"Domain name is {SUBDOMAIN}.{DOMAIN} with IP {targetIP}")
    logging.info(f"Host machine ip is {myIP}")

    if targetIP != myIP:
        logging.info("IPs do not match, updating...")
        return True 
    else:
        logging.info("IPs match, no update needed")
        return False

def updateIP():
    resp = requests.get(
        "https://domains.google.com/nic/update",
        params = {
            "hostname": f"{os.environ.get('SUBDOMAIN')}.{os.environ.get('DOMAIN')}",
            "myip": requests.get("https://domains.google.com/checkip").text,
        },
        auth = (
            os.environ.get("USERNAME"),
            os.environ.get("PASSWORD"),
        ),
    )

    if resp.status_code == 200:
        logging.info("Request successful")
    else:
        logging.error(f"Request failed with error {resp.content}")
        exit(1)

def main():
    setupEnvironment()
    if IPRequireUpdate():
        updateIP()

    TTL = int(os.environ.get("TTL"))
    logging.info(f"Sleeping for {TTL} seconds")

    threading.Timer(TTL, main).start()

if __name__ == "__main__":
    main()



