# Writing a Simple Smart Contract

We will create a TEAL contract and place it in our node under: `~/node/teal/passphrase.teal`

We will check a passphrase.

## Value Checks

Length check:
```bash
echo -n "weather comfort erupt verb pet range endorse exhibit tree brush crane man" | wc
```

Base64 hash check:
```python
import hashlib
import base64
print(
    base64.b64encode(
        hashlib.sha256(
            str(
                'weather comfort erupt verb pet range endorse exhibit tree brush crane man'
            ).encode('utf-8')
        ).digest()
    ).decode('utf-8')
)
# 30AT2gOReDBdJmLBO/DgvjC6hIXgACecTpFDcP1bJHU=
```

## CloseRemainderTo Check

When set, the sender account is closed and remaining funds are transfered to this address.

We want to make sure that it is not set (meaning the value is same as the sender).

## Compile TEAL

```bash
goal clerk compile passphrase.teal
```

This will generate a `.teal.tok` file, and diplay an Algorand address: RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI

Now lets go to https://bank.testnet.algorand.network/ and give this address some ALGO.

Check balance:
```bash
goal account balance -a  RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI
```

## Use a non-submitted transaction to debug TEAL

Convert our passphrase parameter into base64:
```bash
echo -n "weather comfort erupt verb pet range endorse exhibit tree brush crane man" | base64
# d2VhdGhlciBjb21mb3J0IGVydXB0IHZlcmIgcGV0IHJhbmdlIGVuZG9yc2UgZXhoaWJpdCB0cmVlIGJydXNoIGNyYW5lIG1hbg==
```

Create test transaction, creating a txn file:
```bash
goal clerk send \
    -a 30000 \
    --from-program passphrase.teal  \
    -c STF6TH6PKINM4CDIQHNSC7QEA4DM5OJKKSACAPWGTG776NWSQOMAYVGOQE \
    --argb64 d2VhdGhlciBjb21mb3J0IGVydXB0IHZlcmIgcGV0IHJhbmdlIGVuZG9yc2UgZXhoaWJpdCB0cmVlIGJydXNoIGNyYW5lIG1hbg==  \
    -t STF6TH6PKINM4CDIQHNSC7QEA4DM5OJKKSACAPWGTG776NWSQOMAYVGOQE \
    -o out.txn
    #-d ~/node/testnetdata
```

Now lets test the contract with a test transaction:
```bash
goal clerk dryrun -t out.txn
# tx[0] trace:
#   1 intcblock 10000 73 => <empty stack>
#   6 bytecblock 0xdf4013da039178305d2662c13bf0e0be30ba8485e000279c4e914370fd5b2475 => <empty stack>
#  41 txn Fee => (1000 0x3e8)
#  43 intc_0 // 10000 => (10000 0x2710)
#  44 <= => (1 0x1)
#  45 arg_0 => (7765617468657220636f6d666f72742065727570742076657262207065742072616e676520656e646f72736520657868696269742074726565206272757368206372616e65206d616e)
#  46 len => (73 0x49)
#  47 intc_1 // 73 => (73 0x49)
#  48 == => (1 0x1)
#  49 && => (1 0x1)
#  50 arg_0 => (7765617468657220636f6d666f72742065727570742076657262207065742072616e676520656e646f72736520657868696269742074726565206272757368206372616e65206d616e)
#  51 sha256 => (df4013da039178305d2662c13bf0e0be30ba8485e000279c4e914370fd5b2475)
#  52 bytec_0 // addr 35ABHWQDSF4DAXJGMLATX4HAXYYLVBEF4AACPHCOSFBXB7K3ER2SPJXOSA => (df4013da039178305d2662c13bf0e0be30ba8485e000279c4e914370fd5b2475)
#  53 == => (1 0x1)
#  54 && => (1 0x1)
#  55 txn CloseRemainderTo => (94cbe99fcf521ace086881db217e040706ceb92a5480203ec699bfff36d28398)
#  57 txn Receiver => (94cbe99fcf521ace086881db217e040706ceb92a5480203ec699bfff36d28398)
#  59 == => (1 0x1)
#  60 && => (1 0x1)

#  - pass -
```

pass == success :) Yay

## Submit transaction to the network

```bash
goal clerk rawsend -f out.txn #-d ~/node/testnetdata
```

## Examine

View the contract:
https://testnet.algoexplorer.io/address/RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI

Definitely should try making a different contract, so it is not the same as an existing one.

On rejection: we get a .txn.rej file and it says REJECTED.