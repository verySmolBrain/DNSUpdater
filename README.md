# DNS Updater

A very simple DNS updater for Google Domains.

### Setup

1. Fill in the variables under environment in the docker-compose.yml file. 

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

