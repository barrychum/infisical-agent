import os
import yaml
from infisical_sdk import InfisicalSDKClient
import time

REFRESH_INTERVAL = 60  # seconds
INDEFINITE_LOOP = True

while INDEFINITE_LOOP:
    try:
        # Path to mounted agent-config.yaml
        CONFIG_FILE = os.environ.get("AGENT_CONFIG", "/config/agent-config.yaml")

        # Load config
        with open(CONFIG_FILE) as f:
            cfg = yaml.safe_load(f)

        infisical_cfg = cfg["infisical"]
        auth_cfg = cfg["auth"]
        templates = cfg.get("templates", [])

        host = infisical_cfg["address"]
        client_id = auth_cfg["config"]["clientId"]
        client_secret = auth_cfg["config"]["clientSecret"]
        project_id = infisical_cfg["projectId"]
        environment = infisical_cfg["environment"]

        # Init client with host
        client = InfisicalSDKClient(host=host)

        # Login using Universal Auth
        client.auth.universal_auth.login(
            client_id=client_id,
            client_secret=client_secret
        )

        # Fetch secrets
        response = client.secrets.list_secrets(
            project_id=project_id,
            environment_slug=environment,
            secret_path="/",
            view_secret_value=True
        )

        # response.secrets contains the actual secret objects
        secret_map = {s.secretKey: s.secretValue for s in response.secrets}

        lines_out = []
        # Render templates
        for tpl in templates:
            src = tpl["source"]
            dst_path = tpl["destination"]
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            for line in src.splitlines():
                if "secret" in line:
                    key = line.split('"')[1]
                    value = secret_map.get(key, "")
                    lines_out.append(f'{key}="{value}"')

        with open(dst_path, "w") as f:
            f.write("\n".join(lines_out))

        print(f"Wrote secrets to {dst_path}")

    except Exception as e:
        print(f"Error fetching secrets: {e}")
        exit(1)

    INDEFINITE_LOOP = False
    time.sleep(5)
    # time.sleep(REFRESH_INTERVAL)



