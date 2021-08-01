# ========================== 01 - Initialise variables

import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics

# acc1: 3SDHBADFGPL33DZYWITBQMTZYB7G7GXNWGSVUV6HYYKQFUTVZHUGIZ3MGI
mnemonic1 = "spring talent join journey ramp initial plate guilt blood train merit smooth host mechanic stuff only decide staff half venue detail push flip absent liquid"
# acc2: TBPSXBIA4FIEKPO4WVJGZ2SUGMFRC24DUKOQFBPLOE7JU4TNR7D7K5YRBU
mnemonic2 = "runway ostrich proof profit giant public fat dizzy extend odor rude demise old enter private scissors faith crew company blue athlete august phrase above egg"
# acc3: 4NSO56TVP7KNKH5ICE46QRA6FYWJ2JZ7WJOXY6H6FF5BRU7AF3Y2PVO4YY
mnemonic3 = "conduct pottery wrestle sibling great canoe vacuum share stereo attack govern pool place bring secret asthma casual candy cabin ribbon kitten common wasp ability spot"


# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Specify your node address and token. This must be updated.

algod_address = "http://localhost:8080"
algod_token = "INSERT_HERE"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

# ========================== 02 - utility functions, including to get the asset

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


print("Account 1 address: {}".format(accounts[1]['pk']), )
print("Account 2 address: {}".format(accounts[2]['pk']), )
print("Account 3 address: {}".format(accounts[3]['pk']), )