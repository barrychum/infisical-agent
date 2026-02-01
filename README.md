# infisical-agent

[comment]: <> (Github license is provided by shields.io using standard parameters)
[comment]: <> (customer badge requires a specific json that is generated in workflow)

![GitHub License](https://img.shields.io/github/license/barrychum/infisical-agent) ![Custom Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/barrychum/6210ce668e923bd7b478ff9f965debee/raw/docker-infisical-agent-build-date-badge.json) 

[comment]: <> (The create a badge, go to ghcr-badge.egpl.dev)
[comment]: <> (Enter the requied badge details, click apply, copy the URL)

![Custom Badge](https://ghcr-badge.egpl.dev/barrychum/infisical-agent/tags?color=%2344cc11&ignore=&n=1&label=image+tags&trim=) ![Custom Badge](https://ghcr-badge.egpl.dev/barrychum/infisical-agent/size?color=%2344cc11&tag=latest&label=image+size&trim=)

This repository demonstrates a simple Continuous Integration (CI) setup. When the Dockerfile in the main branch is updated, a GitHub Workflow is triggered to perform a series of actions, including building and pushing a Docker image.

## Features
- Uses the `VERSION` variable in the Dockerfile as the Docker image tag.
- Create the follwoing variables
  - DOCKER_USERNAME : the user ID of the target docker repository
  - IMAGE_NAME : the docker image name
  - GIST_ID : the gist to store a json file for badge
- Create the following secrets
  - DOCKER_ACCESS_TOKEN : the docker account developer token
  - GHCR_TOKEN : Github Container registry token
- Builds and pushes images to Docker Hub.
- Saves build artifacts and reports build status via badges.
- Creates a Docker image for an SSH server, suitable for secure file transfers via SCP.

## Docker Image
The Docker image is available on Docker Hub: [stellarhub/infisical-agent](https://hub.docker.com/r/stellarhub/infisical-agent).

### Steps to Use
1. **Create a Dockerfile**:
   Use the Dockerfile located at the root of this repository.

2. **Build the Docker Image**:
   ```bash
   docker build --build-arg USERNAME=myuser --build-arg PASSWORD=mypassword -t my-scp-server .
   ```
   Replace `myuser` and `mypassword` with your desired username and password.

3. **Run the Docker Container**:

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

Sample of the agent-config.yaml
```
infisical:
  address: "http://infisical-app:8080"
  projectId: "your_infisical_project_id"
  environment: "dev"        # or "prod"

auth:
  type: "client-credentials"      # this is auth type for self-hosted
  config:
    clientId: "your_client_id"
    clientSecret: "your_client_secret"

# The Agent writes secrets for different apps into subfolders
templates:
  - source: |
      {{- with secret "secret_key" -}}
      secret_key="{{ .Value }}"
      {{- end -}}
    destination: "/secrets/flask-app/.env"
```

   ```bash
   docker run -d -p 2222:22 -e USERNAME=myuser -e PASSWORD=mypassword -v /$HOME/mnt:/mnt/data --name scp-server my-scp-server
   ```
   - `-v /path/to/local/disk:/mnt/data` mounts a local directory to `/mnt/data` inside the container.
   - `-p 2222:22` maps host port 2222 to container port 22.
   - `--name scp-server` names the container `scp-server`.

4. **Access the SCP Server**:
   Use an SCP client to connect to your server:
   ```bash
   scp -P 2222 file.txt myuser@localhost:/mnt/data/destination/
   ```
   Replace `file.txt` with the file to transfer and adjust the destination path as needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

