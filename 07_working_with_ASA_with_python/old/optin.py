from config import accounts, algod_client, wait_for_confirmation, print_asset_holding
from algosdk.future.transaction import AssetTransferTxn

asset_id = 21219685         # !!! Asset ID from create_asa.py

# ================================== 01 - define transaction

# OPT-IN

# Check if asset_id is in account 3's asset holdings prior
# to opt-in
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

account_info = algod_client.account_info(accounts[3]['pk'])
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=accounts[3]['pk'],
        sp=params,
        receiver=accounts[3]["pk"],
        amt=0,
        index=asset_id)

# ================================== 02 - sign transaction

stxn = txn.sign(accounts[3]['sk'])

# ================================== 03 - send transaction


txid = algod_client.send_transaction(stxn)
print(txid)
# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)
# Now check the asset holding for that account.
# This should now show a holding with a balance of 0.
print_asset_holding(algod_client, accounts[3]['pk'], asset_id)
