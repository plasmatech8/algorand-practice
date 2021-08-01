from config import accounts, algod_client, wait_for_confirmation, print_created_asset
from algosdk.future.transaction import AssetConfigTxn

# ============================== 01 - Create a transaction

# The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

asset_id = 21219685         # !!! Asset ID from create_asa.py

txn = AssetConfigTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id,
    manager=accounts[1]['pk'],      # Set manager to account 1 (instead of account 2)
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'])

# ========================= 02 - sign transaction

# sign by the current manager - Account 2
stxn = txn.sign(accounts[2]['sk'])

# ========================= 03 - send transaction

txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)

# ========================= 04 - print asset info

# Check asset info to view change in management. manager should now be account 1
print_created_asset(algod_client, accounts[1]['pk'], asset_id)