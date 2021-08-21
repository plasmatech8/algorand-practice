# Self Hosted Nodes

Self-hosted nodes should be used for staking.

Notes:
* No API limits, but has cloud platform bills
* You can run in a container on Kubernetes for availability
* An indexer can be too expensive if self-hosted because it needs to be connected to an archival node holding the whole ledger

## Install

Setup:
```bash
# Variables
export ALGO_PATH=$HOME/node
export MAINNET_PATH=$ALGO_PATH/data
export MAINNET_PATH=$TESTNET_PATH/testnetdata
export PRIVNET_PATH=$HOME/privnet

# Install Python3
apt-get update
apt-get install python3 python3-pip -y
update-alternatives --install /usr/bin/python python /usr/bin/python3 10
```

Download and install Algo SDKs and setup the mainnet and testnet nodes:
```bash
# Install Algorand Node and SDKs
mkdir ${ALGO_PATH}
cd ${ALGO_PATH}
curl https://raw.githubusercontent.com/algorand/go-algorand-doc/master/downloads/installers/update.sh -o ./update.sh
chmod 544 update.sh
./update.sh -i -c stable -p ${ALGO_PATH} -d ${MAINNET_PATH} -n

# Catchup the MainNet
goal node start -d ${MAINNET_PATH}
goal node catchup $(curl https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint --silent) -d ${MAINNET_PATH}
goal node status -d ${MAINNET_PATH} -w 100
goal node stop -d ${MAINNET_PATH}
```

Add test network:
```bash
# Create testnet node
mkdir ${TESTNET_PATH}
cp ${ALGO_PATH}/genesisfiles/testnet/genesis.json ${TESTNET_PATH}

# Catchup the TestNet
goal node start -d ${TESTNET_PATH}
goal node catchup $(curl https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint --silent)  -d ${TESTNET_PATH}
goal node status -d ${TESTNET_PATH} -w 100
goal node stop -d ${TESTNET_PATH}
```

Create private network:
```bash
# Create private network
cd ${HOME}
goal network create -r ${PRIVNET_PATH} -n privnet -t ${HOME}/private_network_template.json

# Start a private network
goal network start -r ${PRIVNET_PATH}
goal network status -r ${PRIVNET_PATH}
goal network stop -r ${PRIVNET_PATH}
```
