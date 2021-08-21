# Sandbox

Sandbox is great for development.

Notes:
* Cannot use indexer for testnet/mainnet/betanet

Default Ports:
* 4001 = algod
* 4002 = kmd
* 8980 = indexer

## Install

```bash
# Install curl and git
apt-get update
apt-get install curl git

# Install Docker (convenience script)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Get Algorand Sandbox >>> and add to PATH via local bin (!!!)
git clone https://github.com/algorand/sandbox.git /usr/local/bin/algo-sandbox
```

## REST API

Example:
```bash
curl -X GET "http://<IP>:<PORT>/v2/status" \
    -H "x-algo-api-token:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
```