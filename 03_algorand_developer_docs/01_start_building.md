# Start Building

Contents:
- [Start Building](#start-building)
  - [1. Workspace Setup](#1-workspace-setup)
    - [Available tools](#available-tools)
    - [Choosing a network](#choosing-a-network)
    - [How to obtain an algod address and token?](#how-to-obtain-an-algod-address-and-token)
  - [2. Connect to Node](#2-connect-to-node)
    - [Create an algod client](#create-an-algod-client)
    - [Check node status](#check-node-status)
    - [Check suggested params](#check-suggested-params)
  - [03. Your First Transaction](#03-your-first-transaction)
  - [04. Building Applications](#04-building-applications)
    - [Tokenizing assets or your own coin](#tokenizing-assets-or-your-own-coin)
    - [Applications that require guaranteed exchange of assets](#applications-that-require-guaranteed-exchange-of-assets)
    - [Applications that require historical data](#applications-that-require-historical-data)
    - [Transaction-level metadata](#transaction-level-metadata)
    - [Excrow account-based applications](#excrow-account-based-applications)
    - [Applications that delegate spending authority](#applications-that-delegate-spending-authority)

## 1. Workspace Setup

An application connects to the Algorand blockchain through an algod client.

The algod client requires a valid **algod REST endpoint IP address** and **algod token** from an
Algorand node that is connected to the network you plan to interact with.

### Available tools

Algorand SDKs (see https://developer.algorand.org/docs/reference/sdks/):
* `pip3 install py-algorand-sdk`
* `npm install algosdk`

Algorand CLIs:
* [goal](https://developer.algorand.org/docs/reference/cli/goal/goal/)
  * used for operating a node
  * an essential tool for developers
  * manage keys
  * sign & send transactions
  * create assets
  * perform actions available in SDKs (though not required for building an application)
* [kmd](https://developer.algorand.org/docs/reference/cli/kmd/)
  * CLI for the Algorand Key Management daemon
* [algokey](https://developer.algorand.org/docs/reference/cli/algokey/algokey/)
  * Standalone utility for generating Algorand accounts and signing transactions
  * Often used as lightweight offline client

Indexer:
* A standalone daemon that reads blocks from the blockchain and maintains a local database of transactions and accounts.
* Provides a REST API

### Choosing a network

* [Mainnet](https://developer.algorand.org/docs/reference/algorand-networks/mainnet/)
* [Testnet](https://developer.algorand.org/docs/reference/algorand-networks/testnet/) where Algo can be dispensed via a [faucet](https://bank.testnet.algorand.network/)
* [Betanet](https://developer.algorand.org/docs/reference/algorand-networks/betanet/) where new functionality is tested

If your application depends on features available on the MainNet, use the TestNet for your public
testing.

It is recommended to use private networks for greater control and isolation of your environment.

See https://developer.algorand.org/docs/reference/algorand-networks/

### How to obtain an algod address and token?

Options:
1. Use a third-party service
2. Use Docker Sandbox
3. Run your own node

Third party services like `https://testnet.algoexplorerapi.io` seems to provide
`IndexError: Required an index` when doing transfers. (?)

## 2. Connect to Node

### Create an algod client

You should have obtained an **algoIP address** and **access token**.

You can connect using one of the SDKs.

```python
from algosdk.v2client import algod

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

algod_client = algod.AlgodClient(algod_token, algod_address)
```

Note: some third-party services might require a different API header such as:
```py
headers = {
    "X-API-Key": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)
```

e.g.
```py
from algosdk.v2client import algod
algod_address = "https://testnet.algoexplorerapi.io"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

client = algod.AlgodClient(algod_token, algod_address, headers={'User-Agent': 'DoYouLoveMe?'})
```

### Check node status

Use `client.status()`

```py
import json
status = client.status()
print(json.dumps(status, indent=4))
# {
#     "catchpoint": "",
#     "catchpoint-acquired-blocks": 0,
#     "catchpoint-processed-accounts": 0,
#     "catchpoint-total-accounts": 0,
#     "catchpoint-total-blocks": 0,
#     "catchpoint-verified-accounts": 0,
#     "catchup-time": 0,
#     "last-catchpoint": "15560000#Q6HQED2HRUKODD34NUDLEHWLXSZPLS6DQRH5QLYXHWP4E5WXFFOA",
#     "last-round": 15561337,
#     "last-version": "https://github.com/algorandfoundation/specs/tree/65b4ab3266c52c56a0fa7d591754887d68faad0a",
#     "next-version": "https://github.com/algorandfoundation/specs/tree/65b4ab3266c52c56a0fa7d591754887d68faad0a",
#     "next-version-round": 15561338,
#     "next-version-supported": true,
#     "stopped-at-unsupported-round": false,
#     "time-since-last-round": 1548105149
# }
```

### Check suggested params

Returns information about:
* identity of the network
* parameters for constructing a new transaction.

```py
try:
    params = client.suggested_params()
    print(json.dumps(vars(params), indent=4))
except Exception as e:
    print(e)
# {
#     "first": 15561365,
#     "last": 15562365,
#     "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#     "gen": "testnet-v1.0",
#     "fee": 0,
#     "flat_fee": false,
#     "consensus_version": "https://github.com/algorandfoundation/specs/tree/65b4ab3266c52c56a0fa7d591754887d68faad0a",
#     "min_fee": 1000
# }
```

## 03. Your First Transaction

To create and submit a transaction:
```py
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn

# 1. Create an account

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    print("My address: {}".format(address))
    print("My passphrase: {}".format(passphrase))
    return address, passphrase
address, passphrase = generate_algorand_keypair()

# 2. Add funds
"Go to https://bank.testnet.algorand.network/"

# 3. Connect client

algod_address = "https://testnet.algoexplorerapi.io"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
client = algod.AlgodClient(algod_token, algod_address, headers={'User-Agent': 'DoYouLoveMe?'})

# 4. Check balance

account_info = client.account_info(address)
print("Account balance: {} microAlgos".format(account_info.get('amount')))

# 5. Contruct the transaction (send 1 Algo to the testnet faucent address)

params = client.suggested_params()
# comment out the next two (2) lines to use suggested fees
params.flat_fee = True
params.fee = 1000
receiver = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
note = "Hello World".encode()
unsigned_txn = PaymentTxn(address, params, receiver, 1000000, None, note)

# 6. Sign the transaction

signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))

# 7. Submit the transaction
txid = client.send_transaction(signed_txn)
print("Successfully sent transaction with txID: {}".format(txid))
```

We will see that 1000000 microAlgo was sent (1 Algo) with a fee of 1000 microAlgo (0.001 Algo)

There is example code for waiting for a transaction complete in the docs.

We can wait for  the transaction to complete and view blockchain info using:
```py
import base64

# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round
    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception('pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


# wait for confirmation
try:
    confirmed_txn = wait_for_confirmation(client, txid, 4)
except Exception as err:
    print(err)

print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))
```

## 04. Building Applications

### Tokenizing assets or your own coin

**Algorand Standard Assets (ASAs)** can be created with a single transaction (no contract code).

They are also highly configurable, providing minting, freezing, revoking, etc.

### Applications that require guaranteed exchange of assets

**Atomic transfers** can be used to guarantee transfer.

Up to 16 transactions can be grouped, and if one fails, all fail.

These transactions can include payments, asset transfer, smart contract calls, etc.

### Applications that require historical data

An **indexor node** was created with the purpose of providing fast/efficient access to search
capabilities of the blockchain.

### Transaction-level metadata

The optional `note` field can be used to add arbitrary data, up to 1 KB.

An indexor can use this field to access historical records.

### Excrow account-based applications

In traditional finance, an escrow account is one in which funds are kept locked up until some
predetermined event.

**Stateless smart contracts** can be used to specify conditions and only allow the claim
transaction when the conditions are met. These contracts do not live on the blockchain, only
executed when the transaction is submitted.

For TEAL docs see:
* https://developer.algorand.org/docs/features/asc1/stateless/
* https://developer.algorand.org/docs/reference/teal/specification/

### Applications that delegate spending authority

Allowing third-parties to withdraw funds if conditions are fulfilled.
This can be done with stateless smart contracts.

...blah