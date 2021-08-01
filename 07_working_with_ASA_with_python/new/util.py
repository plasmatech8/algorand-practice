import json

from config import algod_client, accounts


def wait_for_confirmation(txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = algod_client.status().get('last-round')
    txinfo = algod_client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation...")
        last_round += 1
        algod_client.status_after_block(last_round)
        txinfo = algod_client.pending_transaction_info(txid)
    print(f"Transaction {txid} confirmed in round {txinfo.get('confirmed-round')}.")
    return txinfo


def print_asset_info(asset_id):
    asset_info = algod_client.asset_info(asset_id)
    print(f'Asset information for ID {asset_id}:')
    print(json.dumps(asset_info, indent=4))


def print_account_info(address):
    account_info = algod_client.account_info(address)
    print(f'Account information for address {address}:')
    print(json.dumps(account_info, indent=4))


def print_accounts_list():
    for i, acc in enumerate(accounts):
        print(f"Account {i} address: {acc['pubkey']}")
