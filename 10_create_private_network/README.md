# Create A Private Network

https://developer.algorand.org/tutorials/create-private-network/

## Overview

Before creating a private net, a template needs to be created
specifying wallets and configuration.

Note: online account = staking and participating in consensus

Wallets can be configured with:
* Name
* Stake
* Online

Nodes can be configured with:
* Name (also the directory name)
* IsRelay
* Wallets

## Node types

Participation nodes:
* Holds keys for accounts participating in consensus.

(Archival mode):
* Non-relay nodes hold approximately the last 1000 blocks locally.
* Archival mode will store the entire ledger.

Relay nodes:
* Relay nodes allow other nodes to connect to each other.
* There must be at least one relay in a network.
* They must be reasonably powerful so that can control data flow and connections.
* Relay nodes are always in archival mode.
* Can technically participate in concensus, but not recommended.

## 01. Create Network Template

`Primary` will be a relay node. (perhaps we should call it 'RelayNode'?)

`Node` will be a regular participation node. (perhaps we should call it 'ParticipationNode'?)

Create: `my_network_template.json`
```json
{
    "Genesis": {
        "NetworkName": "",
        "Wallets": [
            {
                "Name": "Wallet1",
                "Stake": 50,
                "Online": true
            },
            {
                "Name": "Wallet2",
                "Stake": 40,
                "Online": true
            },
            {
                "Name": "Wallet3",
                "Stake": 10,
                "Online": false
            }
        ]
    },
    "Nodes": [
        {
            "Name": "Primary",
            "IsRelay": true,
            "Wallets": [
                {
                    "Name": "Wallet1",
                    "ParticipationOnly": false
                }
            ]
        },
        {
            "Name": "Node",
            "Wallets": [
                {
                    "Name": "Wallet2",
                    "ParticipationOnly": false
                },
                {
                    "Name": "Wallet3",
                    "ParticipationOnly": false
                }
            ]
        }
    ]
}
```
## 02. Create a new network

Run commands:
```bash
# Create the network
goal network create -r ~/net1 -n private -t my_network_template.json

# Start the network
goal network start -r ~/net1
goal network status -r ~/net1

# View the node (do not touch the node - managed automatically by network)
goal node status -d ~/net1/Node -w 100

# View wallets
goal account list -d ~/net1/Primary
goal account list -d ~/net1/Node

# Stop and delete the network
goal network stop -r ~/net1
goal network delete -r ~/net1
# (Deletes the ~/net1 directory)
```

Note: `-r` is root directory. `-d` is data directory.

Note: Stopping and starting the node will break it. use network start/stop only.
