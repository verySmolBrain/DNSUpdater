# DNS Updater

A very simple DNS updater for Google Domains.

### Setup

1.  In updater/auth_details.toml, fill in the details for each domain you want to update.
    If there are multiple domains, add another `[[auth_details]]` section.
    The resulting file should look like this:

```
# TTL for DNS record in seconds
ttl = 900

[[auth_details]]
# Username for Google DDNS
username = "" 
# Password for Google DDNS
password = "" 
# Subdomain to update
subdomain = "" 
# Domain to update
domain = "" 

[[auth_details]]
# Username for Google DDNS
username = ""
# Password for Google DDNS
password = ""
# Subdomain to update
subdomain = ""
# Domain to update
domain = ""
```

2. Run the container with 

``` bash 
docker compose build 
docker compose up -d 
```

### Logs 

To specify an alternate location to save 
the logs, in the docker-compose.yml file, edit

```
volumes:
    - ./logs:/data/logs
```

to

```
volumes:
    - .{Your desired location}:/data/logs
```

