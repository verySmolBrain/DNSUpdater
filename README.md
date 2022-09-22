# DNS Updater

A very simple DNS updater for Google Domains.

### Setup

1. Create a .env file in the base folder then copy and fill this in:

```
# Interval between checks (Default 15 minutes)
TTL = "900" 

USERNAME = "" 
PASSWORD = "" 

SUBDOMAIN = "" 
DOMAIN = "" 
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

