# Working with ASA using Python

Tutorial:
* https://developer.algorand.org/tutorials/asa-python/

Requirements:
* Have 3 accounts, and make sure they are funded with testnet funds.
* Have a testnet node running

## Steps

Step 1: `create_asa.py`
* Connects to a node
* Signs a transaction to create an ASA token
* Sets account 2 as the manager, reserve, freeze, and clawback address.

Asset created: https://testnet.algoexplorer.io/asset/21219685

Step 2: `change_manager_role.py`
* Reconfiguring an asset - we will change the manager from account 2 to account 1

Step 3: `optin.py`
* To opt into an asset

## Notes

* The code is not the best I've seen so I made a `new/` version.

* To view the asset info:
```python
print(json.dumps(algod_client.asset_info(21219685), indent=4))
```

* To view the account info:
```python
print(json.dumps(algod_client.account_info("3SDHBADFGPL33DZYWITBQMTZYB7G7GXNWGSVUV6HYYKQFUTVZHUGIZ3MGI"), indent=4))
print(json.dumps(algod_client.account_info("TBPSXBIA4FIEKPO4WVJGZ2SUGMFRC24DUKOQFBPLOE7JU4TNR7D7K5YRB"), indent=4))
print(json.dumps(algod_client.account_info("4NSO56TVP7KNKH5ICE46QRA6FYWJ2JZ7WJOXY6H6FF5BRU7AF3Y2PVO4YY"), indent=4))
```