FROM python:3.12-slim

# Define built-time variables
# Retrieved in action yaml
ARG VERSION=0.1.1

RUN pip install --no-cache-dir infisicalsdk pyyaml requests

WORKDIR /app
COPY fetch_secrets.py .

CMD ["python", "fetch_secrets.py"]

