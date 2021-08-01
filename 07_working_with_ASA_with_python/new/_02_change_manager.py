from algosdk.future.transaction import AssetConfigTxn

from config import accounts, algod_client
from util import print_asset_info, wait_for_confirmation


def change_manager(asset_id):
    # Define transaction
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True
    txn = AssetConfigTxn(
        sender=accounts[1]['pubkey'],
        sp=params,
        index=asset_id,
        manager=accounts[0]['pubkey'],
        reserve=accounts[1]['pubkey'],
        freeze=accounts[1]['pubkey'],
        clawback=accounts[1]['pubkey']
    )

    # Sign transaction
    txn_signed = txn.sign(accounts[1]['privkey'])

    # Send transaction
    txn_id = algod_client.send_transaction(txn_signed)
    print(f'Transaction ID: {txn_id}')

    # Wait for the transaction to be confirmed
    wait_for_confirmation(txn_id)

    # Check asset info to view change in management. manager should now be account 1
    print_asset_info(asset_id)
    print('Asset manager has now changed to account 1. See above.')