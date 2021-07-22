# Create your Own Coin on TestNet (LaylaCoin Series)

Following tutorial:
* https://developer.algorand.org/tutorials/create-laylacoin/

Files:
* `main.py` contains the main functions to create, opt-in, and send the asset.
* `config.py` This will contain all of our configurable parameters. This is the file you will need to update as you run through this tutorial.
* `util.py` various utility functions.
* `LaylaGyoza.jpg` This is an image of Layla the puppy that we will reference when we create our coin.

## 01. Generate the LaylaCoin creator and reciever accounts

Using the `util.generate_new_account()` function, we will create two accounts to put into
`config.py`.

We will write the address and passphrase into `creator_address`, `creator_passphrase`,
`receiver_address`, `receiver_passphrase`.

Then we can go to https://bank.testnet.algorand.network/ faucet to fund the wallets.

## Define Coin parameters

We will set:
* manager
* reserve manager (reconfigure the asset)
* freeze manager (freeze specific accounts)
* clawback manager (revoke assets from accounts)
* We will also set the total number of base units to 888,888,888 with 2 decimal places, meaning that there is 8,888,888.88 total coins.
* `"default_frozen": False` means that holders do not need to be whitelisted by the freeze manager before being able to send transactions.
* `asset_url` filename of the dog image (just some additional first-order asset details)
* `metadata_hash` a hash of the file created using `hash_file_data(filename, return_type="bytes")` (just some additional first-order asset details)

`config.py`
```py
# Details of the asset creation transaction
asset_details = {
	"asset_name": "DoggyCoin",
	"unit_name": "Bork",

	"manager": creator_address,
	"reserve": creator_address,
	"freeze": creator_address,
	"clawback": creator_address,

	"total": 888888888,
	"decimals": 2,
	"default_frozen": False,

	"url": "LaylaGyoza.jpg",
	"metadata_hash": b'O\x88\xfd\xf2\xd1\xfe\xee\x96+\xf9\xf0\xb6\xb2\x8d\r\xb5\xced)#\x9bV\xce\xa4\x81\xa6\xb9\xbd\x0e\xf7al'
}
```

Learn more about asset parameters (and parameters for other things) here:
* https://developer.algorand.org/docs/reference/transactions/#asset-parameters


## 03 Create the coin

We will need to run an AlgoD client connected to a testnet node.

We will use `main.py` to run actions in relation to our coin.
* `create(passphrase=None)` create an asset using the asset details configuration
  * If passphraise is supplied, it will create the transaction, else just creates a txn file

Util:
* `sign_and_send(txn, passphrase, client)` used to send a transaction
* `wait_for_confirmation(client, transaction_id, timeout)` used to wait for the transaction

Now we can create our asset:
```python
from main import create
from config import creator_passphrase
create(creator_passphrase)
```

TODO: Need to connect to an AlgoD node somehow

...


```py
import config
import main

main.create(config.creator_passphrase)
# Confirmed TXID: LBMIHUDE6VH5VOG73FVCEAPYWB5ULNRARXMFGWQ4K6ZDUCHDO46Q
# Asset ID: 20158270

main.check_holdings(20158270, "BOFH7UOCKFDBJY56R3IJCEFPQUIL34XTXDPARL4YBZOLAITY75UH5DYEEI")
# Account BOFH7UOCKFDBJY56R3IJCEFPQUIL34XTXDPARL4YBZOLAITY75UH5DYEEI has 8888888.88 Bork.

main.check_holdings(20158270, "Q7B33FEJ522NQFF5EXO4ESC5ABVX6ZIYFJFZZUC5TBVW24V63KTAIL4ETI")
# Account Q7B33FEJ522NQFF5EXO4ESC5ABVX6ZIYFJFZZUC5TBVW24V63KTAIL4ETI must opt-in to Asset ID 20158270.

main.transfer("bad passphrase")
main.transfer("spirit start collect visual life post nest must tube before tuition parade armor raccoon example bicycle diagram genuine fatal flock dinosaur bubble slogan abstract wide")
main.optin("spirit start collect visual life post nest must tube before tuition parade armor raccoon example bicycle diagram genuine fatal flock dinosaur bubble slogan abstract wide")
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/home/mark/Code/algorand-practice/02_create_laylacoin_on_testnet/create-layla-coin/main.py", line 47, in transfer
#     txn = AssetTransferTxn(sender=creator_address, sp=params, receiver=receiver_address, amt=amount, index=asset_id)
#   File "/home/mark/anaconda3/lib/python3.7/site-packages/algosdk/future/transaction.py", line 960, in __init__
#     self.index = self.creatable_index(index, required=True)
#   File "/home/mark/anaconda3/lib/python3.7/site-packages/algosdk/future/transaction.py", line 270, in creatable_index
#     raise IndexError("Required an index")
# IndexError: Required an index
```