from config import accounts, algod_client, wait_for_confirmation, print_asset_holding, print_created_asset
from algosdk.future.transaction import AssetConfigTxn

# =========================== 03 - Create a transaction object
# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()

# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction

txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=accounts[2]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'],
    url="https://path/to/my/asset/details",
    decimals=0)

# =========================== 04 - sign the transaction

# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# =========================== 05 - send the transaction

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print(txid)

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client,txid)

try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
except Exception as e:
    print(e)


# See the asset at: https://testnet.algoexplorer.io/asset/<asset-id>
# acc2 is the  manager, reserve, freeze, and clawback address.