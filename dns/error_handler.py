def translate(resp):
    if resp == 'nohost':
        print("\n[!] The hostname doesn't exist, or doesn't have Dynamic DNS enabled.")
        return False
    elif resp == 'badauth':
        print("\n[!] The username/password combination isn't valid for the specified host.")
        return False
    elif resp == 'notfqdn':
        print("\n[!] The hostname specified is not a fully-qualified domain name.")
        return False
    elif resp == 'badagent':
        print("\n[!] Your Dynamic DNS client makes bad requests. Ensure the user agent is set in the request.")
        return False
    elif resp == 'abuse':
        print("\n[!] The hostname is blocked due to abuse. Did you make too many requests?")
        return False
    elif resp == '911':
        print("\n[!] The hostname is blocked due to a system error. Please try again later.")
    elif resp == 'conflict A' or resp == 'conflict AAAA':
        print("\n[!] A custom A or AAAA resource record conflicts with the update. Delete the indicated resource record within the DNS settings page and try the update again.")
        return False

    return True