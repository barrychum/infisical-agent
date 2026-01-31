# infisical-agent

![GitHub License](https://img.shields.io/github/license/barrychum/infisical-agent) ![Custom Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/barrychum/6210ce668e923bd7b478ff9f965debee/raw/docker-openssh-build-date-badge.json) 

![Custom Badge](https://ghcr-badge.egpl.dev/barrychum/infisical-agent/tags?color=%2344cc11&ignore=&n=1&label=ghcr+tag&trim=) ![Custom Badge](https://ghcr-badge.egpl.dev/barrychum/infisical-agent/size?color=%2344cc11&tag=latest&label=image+size&trim=)

Create a docker volume, infisical_shared_secrets, to store shared secrets.
Deploy a container using the following docker compose.  Attach it to the same network of the inficial container.

```
services:
  infisical-fetcher:
    image: barrychum/infisical:0.1.0
    networks:
      - proxy
    environment:
      # Path to the mounted agent-config.yaml inside the container
      - AGENT_CONFIG=/config/agent-config.yaml
    volumes:
      # Mount host folder containing agent-config.yaml
      - /mnt/disk2/docker/infisical:/config:ro
      # Shared volume where .env files will be written
      - infisical_shared_secrets:/secrets

volumes:
  infisical_shared_secrets:
    external: true

networks:
  proxy:
    external: true
```

