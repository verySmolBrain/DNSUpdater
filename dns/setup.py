from getpass import getpass
import dns

def __init__():
    print(""" 
    █▀ █▀▀ ▀█▀ █░█ █▀█
    ▄█ ██▄ ░█░ █▄█ █▀▀
    """)

    username = input("Username: ")
    password = ''
    ask_counter = 0
    while True:
        save_password = input("Save password? (y/n): ").lower()
        if save_password == 'y':
            password = getpass("Password: ")
            break
        elif save_password == 'n':
            password = '' # Save password as empty string 
            break
        else:
            if ask_counter == 0:
                print("Invalid input. This is a simple yes/no question.")
            elif ask_counter == 1:
                print("You're not doing this on purpose...are you?")
            elif ask_counter >= 2:
                print("(┛◉Д◉)┛彡┻━┻")
            ask_counter += 1
            continue
        
    subdomain = input("Subdomain: ")
    domain = input("Domain: ")

    try:
        config = f"""CONFIG_VERSION = "{dns.config_version()}"
DNS_USERNAME = "{username}"
DNS_PASSWORD = "{password}"
DNS_SAVE_PASSWORD = "{save_password}"
DNS_SUBDOMAIN = "{subdomain}"
DNS_DOMAIN = "{domain}"
"""
        open('./.env', 'w').write(config)
        print("\n[*] Successfully created .env file!")
        
    except Exception as e:
        print("\n[!] An error occurred when creating config file.\n" + str(e))
        exit()