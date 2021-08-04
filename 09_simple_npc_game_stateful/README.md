# Simple NPC game interactions using a stateful contract and atomic transfers

See: https://developer.algorand.org/tutorials/simple-npc-game-interactions-using-a-stateful-contract-and-atomic-transfers/

Using stateful contracts and atomic transfers, we will keep track of a health variable and
decide whether to help or deceive an NPC. The game ends when health is max or zero.

## 01. Contract in PYTEAL

We will create contract `contract.py`

## 02. Deploying the contract

We can actually use a helper from algo-builder to create a private network:
```bash
git clone https://github.com/scale-it/algo-builder
cd algo-builder/infrastructure
make create-private-net
export ALGO_PVTNET_DATA=$(pwd)/node_data/PrimaryNodecd
```

```bash
goal node start -d $ALGO_PVTNET_DATA
goal node status -d $ALGO_PVTNET_DATA -w 100

goal wallet list -d $ALGO_PVTNET_DATA
goal account list -d $ALGO_PVTNET_DATA
```

We can use a makefile to easily run commands like `make deploy`, etc.

```bash
make deploy -d $ALGO_PVTNET_DATA

export APP_ID=<INSERT_ID>
```

TODO: figure out private net stuff.