from algosdk.v2client import algod
from algosdk import mnemonic

# Accounts
mnemonics = [
    # acc1: 3SDHBADFGPL33DZYWITBQMTZYB7G7GXNWGSVUV6HYYKQFUTVZHUGIZ3MGI
    # acc2: TBPSXBIA4FIEKPO4WVJGZ2SUGMFRC24DUKOQFBPLOE7JU4TNR7D7K5YRBU
    # acc3: 4NSO56TVP7KNKH5ICE46QRA6FYWJ2JZ7WJOXY6H6FF5BRU7AF3Y2PVO4YY
    "spring talent join journey ramp initial plate guilt blood train merit smooth host mechanic stuff only decide staff half venue detail push flip absent liquid",
    "runway ostrich proof profit giant public fat dizzy extend odor rude demise old enter private scissors faith crew company blue athlete august phrase above egg",
    "conduct pottery wrestle sibling great canoe vacuum share stereo attack govern pool place bring secret asthma casual candy cabin ribbon kitten common wasp ability spot",
]
accounts = [
    {
        'phrase': m,
        'pubkey': mnemonic.to_public_key(m),
        'privkey':  mnemonic.to_private_key(m),
    } for m in mnemonics
]

# Initialize an algod client
algod_address = "http://localhost:8080"
algod_token = "bafe33dc865d8bded216e662727196765dfaaf63ec0d828a93392715c9e1013c"#"INSERT_HERE"
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)


