# Node Setup

(Linux - should use ~/node folder version)

## Install node code

See https://developer.algorand.org/docs/run-a-node/setup/install/#installing-with-other-linux-distros

Install the node:
```
mkdir ~/node
cd ~/node
wget https://raw.githubusercontent.com/algorand/go-algorand-doc/master/downloads/installers/update.sh
chmod 544 update.sh
./update.sh -i -c stable -p ~/node -d ~/node/data -n
```

## Configure System

See https://developer.algorand.org/docs/run-a-node/setup/install/#overview

Configure `.bashrc` by adding environment variables and add path:
```bash
# ...
export ALGORAND_DATA="$HOME/node/data"
export PATH="$HOME/node:$PATH"
```
This will add the algorand-devtools commands and the data environment variable to PATH.

## Switch networks

See https://developer.algorand.org/docs/run-a-node/operations/switch_networks/#mac-os-or-other-linux-distros

Switch networks by creating a new directory (`testnetdata`) containing the genesis file.

```bash
cd ~/node
./goal node stop -d data
mkdir testnetdata
cp ~/node/genesisfiles/testnet/genesis.json ~/node/testnetdata
```

## Fast catchup

See https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup

We can now start our node...
```bash
goal node start
goal node status
```

The Sync Time will be 0.0s when it is caught up with the network.

To fast-catchup, obtain the latest catchpoint value:
* Testnet: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint
* i.e. 4420000#Q7T2RRTDIRTYESIXKAAFJYFQWG4A3WRA3JIUZVCJ3F4AQ2G2HZRA

Then run the commands:
```bash
goal node catchup <catchpoint>
goal node status -w 1000 # watch
```

The downloaded blocks should increase until caught up.

## View logs

See https://developer.algorand.org/docs/reference/node/artifacts/#carpenter

```bash
carpenter -D
# and/or
goal node status -w 100
```