# Using Stateful Smart Contract To Create Algorand Standard Asset

See https://developer.algorand.org/solutions/using-stateful-smart-contract-to-create-algorand-standard-asset/

Steps:
* startnet.sh: Sets up private network
* createapp.sh: Compiles the PyTeal files to TEAL and deploys the stateful smart contract
* fundescrow.sh: Send Algos to escrow account
* linkapptoescrow.sh: Adds the escrow address to the application's global state
* createasa.sh: Creates a new ASA from the escrow account
* fundasa.sh: Receive 1 ASA that was created by the escrow account
* stopnet.sh: Delete private network

Inspection:
```bash
APP_ID=1
ESCROW_ADDRESS=5DXB4ICSPZBJEW6A3OTWGVFE5IMDTM5DC6B3KASVDNJ7RE322NCJP4FBSU
PERSONAL_ADDRESS=MQ4E6V4OIJKLFQMYGDVADDG6DI4Y7DWQJBVBZ62BDOSCC5URFRELVQ2M2I
ALGORAND_DATA=../net1/Primary
ASA_NAME=AppASA-0
ASA_ID=8

goal account info -a $ESCROW_ADDRESS
goal account balance -a $ESCROW_ADDRESS

goal account info -a $PERSONAL_ADDRESS
goal account balance -a $PERSONAL_ADDRESS

# The escrow address is the full manager of the asset!
goal asset info --assetid $ASA_ID

goal app info --app-id $APP_ID
goal app read --global --app-id $APP_ID
goal app read --local --app-id $APP_ID --from $PERSONAL_ADDRESS
```

## Introduction

ASAs are usually created by a user account, but here we will do so using a stateful smart contract
linked to an excrow account.

Escrow: ***a legal arrangement in which a third party temporarily holds large sums money or property until a particular condition has been met***

This way, we can use on-chain data to determine ASA parameters.

The stateful contract stores state that is used to verify the ASA creation parameters.

To create an ASA, you group the application call with ASA creation transaction using an atomic
transfer.

Transaction:
* Transaction Group: [ Application Call Txn, ASA Creation Txn ]
* Verifies the ASA parametrs

Similarly to send the ASA from contract account, you group an application call transaction with an
asset tranfer transaction.

## Scope

Application allows you to create assets with name: `AppASA-X`

Allows anyone to get 1 ASA from the escrow account.

## Notes


To perform an action on behalf of a escrow contract, a transaction needs to be signed by
passing in the contract program as the signer.
* i.e. `goal clerk sign -i split-1.tx -p ${TEAL_ESCROW} -o signout-1.tx`

We need to make sure our escrow contract checks that the user is not trying to steal funds using
the `asset_close_to` address! - Which will remove the contract and migrate funds to a new address.
* i.e. `asset_close_to_check = Txn.asset_close_to() == Global.zero_address()`


We also need to make sure that the asset sender is the zero address (so it is not a clawback
transaction). It must be empty to ensure that assets cannot be revoked.
* i.e. `Txn.asset_sender() == Global.zero_address()`
* AssetTransferTx can be used for transferring assets and for clawback
  * **sender** == Where funds are witdrawn and fees are paid by.
  * **assetSender** == if present, the address where funds are withdrawn. Replaces sender, and makes sender a clawback address,
  * FOR REGULAR TRANSFERS, KEEP `assetSender` EMPTY

We also need to make sure that the rekey addres is the zero address, so the user is not changing
the auth address / spending key of the contract.
* i.e. `rekey_check = Txn.rekey_to() == Global.zero_address()`