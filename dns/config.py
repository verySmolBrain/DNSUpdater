import os

def username():
    return os.getenv('DNS_USERNAME')

def password():
    return os.getenv('DNS_PASSWORD')

def is_save_password():
    is_save = os.getenv('DNS_SAVE_PASSWORD')
    return True if is_save == 'y' else False

def subdomain():
    return os.getenv('DNS_SUBDOMAIN')

def domain():
    return os.getenv('DNS_DOMAIN')

def freq():
    return os.getenv('UPDATE_FREQUENCY')