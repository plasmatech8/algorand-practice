from algosdk.future.transaction import AssetConfigTxn

from config import accounts, algod_client
from util import accounts, wait_for_confirmation, print_asset_info, print_account_info


def create_asset():
    # Define transaction
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True
    txn = AssetConfigTxn(
        sender=accounts[0]['pubkey'],
        sp=params,
        total=1000,
        default_frozen=False,
        unit_name="LATINUM",
        asset_name="latinum",
        manager=accounts[1]['pubkey'],
        reserve=accounts[1]['pubkey'],
        freeze=accounts[1]['pubkey'],
        clawback=accounts[1]['pubkey'],
        url="https://path/to/my/asset/details",
        decimals=0
    )

    # Sign the transaction
    txn_signed = txn.sign(accounts[0]['privkey'])

    # Send the transaction
    txn_id = algod_client.send_transaction(txn_signed)
    print(f'Transaction ID: {txn_id}')

    # Wait for the transaction to be confirmed
    wait_for_confirmation(txn_id)
    txn_pending = algod_client.pending_transaction_info(txn_id)
    asset_id = txn_pending["asset-index"]

    print_asset_info(asset_id)
    print('Asset has now been created. See above.')

    return asset_id
