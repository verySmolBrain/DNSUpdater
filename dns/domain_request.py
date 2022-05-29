import requests
import logging
import os
import dns

''' Create request to Google Domains

Parameters:
    username (str): Username for Google Domains
    password (str): Password for Google Domains
    hostname (str): Hostname to update

Returns:

'''

def create_request(username, password, subdomain, domain):
    DOMAIN_UPDATE = 'https://${0}:${1}@domains.google.com/nic/update?hostname=${2}.${3}&myip=${4}'
    
    logging.basicConfig(
        filename = 'dns_update.log', 
        level = logging.INFO
    )
    
    ip = get_my_ip()
    if os.path.isfile('old_ip.txt') and ip == open('old_ip.txt', 'r').read():
        print('ip is the same. Not updating. \n(It\'s not cause I\'m lazy B-Baka 	(*/ω＼))')
    else:
        if os.path.isfile('old_ip.txt'):
            os.remove('old_ip.txt')
        open('old_ip.txt', 'w').write(ip) # Updates old_ip.txt with new ip
        logging.info('Updating ip to {}'.format(ip))
        
        print('Sending request...')
        DOMAIN_UPDATE.format(username, password, subdomain, domain, ip)

        domain_Resp = requests.get(DOMAIN_UPDATE, timeout = 5)
        logging.info("Response: " + domain_Resp.text) # Logs response
        
        if dns.error_handler.translate(domain_Resp.text):
            print("\n[*] Successfully finished request! ＼(￣▽￣)／")
        else:
            print("[!] An error occurred when creating request. (＞﹏＜)")

def get_my_ip():
    GOOGLE_CHECK_IP = 'https://domains.google.com/checkip'
    
    page_resp = requests.get(GOOGLE_CHECK_IP, timeout = 5)
    my_ip = page_resp.text
    
    return my_ip