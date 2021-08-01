from algosdk.future.transaction import AssetTransferTxn

from config import accounts, algod_client
from util import print_account_info, wait_for_confirmation


def opt_in(asset_id):
    # Check if account 3 is opted into the token
    account_info = algod_client.account_info(accounts[2]['pubkey'])
    holding = any(asset['asset-id'] == asset_id for asset in account_info['assets'])
    if not holding:

        # Define transaction
        params = algod_client.suggested_params()
        params.fee = 1000
        params.flat_fee = True
        txn = AssetTransferTxn( # Use the AssetTransferTxn to transfer assets and opt-in
            sender=accounts[2]['pubkey'],
            sp=params,
            receiver=accounts[2]["pubkey"],
            amt=0,
            index=asset_id
        )

        # Sign transaction
        txn_signed = txn.sign(accounts[2]['privkey'])

        # Send transaction
        txn_id = algod_client.send_transaction(txn_signed)
        print(f'Transaction ID: {txn_id}')

        wait_for_confirmation(txn_id)
        print_account_info(accounts[2]['pubkey'])
        print('Account 3 is now Opted-In. See above.')

    else:
        print('Account 3 has already opted into the token.')
        print(f"Account 3 address: {accounts[2]['pubkey']}")
        print(f"Asset ID: {asset_id}")

