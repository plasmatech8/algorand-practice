# Explore Features

https://developer.algorand.org/docs/features/

Contents:
- [Explore Features](#explore-features)
  - [Accounts](#accounts)
  - [Transactions](#transactions)
  - [Assets](#assets)
  - [Atomic Transfers](#atomic-transfers)

## Accounts

Overview:

* Keys/Addresses
  * Use Ed25519 high-speed, high-security elliptic-curve signatures
  * Transformation: Public Key to Address
    * 4 byte checksum encoded in base32 is added to public key (?)
  * Transformation: Private Key to base64 private key
    * Concatenation of public and private key
  * Transformation: Private key to 25-word mnemonic
    * Convert private key into 11-bit integers (2048)
    * This makes 24 words using the bip-0039 English word list (2048)
    * The final word is a checksum of the first tow bytes of the hash of the private key and converting into 11-bit integer

* Wallets
  * All information needed can be derived from the passphrase (address, private key, etc)

* Accounts
  * Every account has a minimum balance of 100,000 microAlgos (0.1 Algo)
  * Minimum increases with every asset owned
  * By default an account is **offline**, meaning that it does not participate in consensus
  * Other account types
    * Mulisig accounts
    * Smart contract accounts
  * Special accounts
    * FeeSink
      * Where all fees from transactions are sent
      * Can only spend to the RewardsPool
    * RewardsPool
      * Holds Algos that are distributed as rewards defined by the protocol
    * Zero addresss
      * (AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ)

Creation Methods / Types:

* Wallet-derived (kmd)
  * Intro:
    * The **Key Management Daemon** is a process that runs on nodes.
    * If you are using a third-party service, this is likely not available.
    * It is the underlying key storage mechanism used with `goal`
  * Why use?:
    * ????
    * We can create a wallet with mulitple addresses
  * Why not use?:
    * Using kmd requires running a process and storing keys on disk.
    * Standalone accounts may be better option for lightweight solutions
  * How to use:
    * Start the process
    * Retrieve teh kmd IP address & access token
    * `goal wallet new testwallet`, `goal account new`
  * ...

* Standalone
  * An address & private key (mnemonic) that is not stored on disk
  * Why use?:
    * Only need the 25-word mnemonic
  * Why not use?:
    * kmd will store keys encrypted on-disk
  * How to generate:
    * `goal account new`, `goal account export -a address<PLACEHOLDER>`

* Multisignature
  * Intro:
    * Essentially a hash of the ordered list of accounts, threshold, and version
    * Threshold determines how many account signatures are needed to process a transaction

Rekeying:

* Intro:
  * A protocol feature that enables an account holder to maintain a static public address, while rotating private keys.
  * This is done by issuing a 'rekey-to transaction' which sets the authorised address in the account object.

* Authorized addresses
  * The balance record of every account includes the "auth-addr" field
  * A rekeyed account points to a standard account (spending key) using this field

...

## Transactions

Transaction types:
* Payment
* Key Registration
* Asset Configuration
* Asset Freeze
* Asset Transfer

Fees:
* Suggested fee
  * (suggested fee per byte `fee`)
  * Can be obtained via SDK
  * If suggested fee is less than the 'minimum fee', minimum fee will be used instead
* ...

## Assets

Overview
* A single account can create up to 1000 assets
* For each asset created/owned, the minimum balance is increased by 0.1 Algos

Immutable Asset Parameters:
* Creator (required)
* AssetName (optional, but recommended)
* UnitName (optional, but recommended)
* Total (required)
* Decimals (required)
* DefaultFrozen (required)
* URL (optional)
* MetaDataHash (optional)

Mutable Asset Parameters:
* Manager address
  * re-configure or destroy an asset
* Reserve address
  * non-minted assets will reside in that account instead of the default creator account
* Freeze address
  * freeze or unfreeze the asset holdings for a specific account.
* Clawback address
  * transfer assets from and to any asset holder

Asset Functions:
* Creating an asset
* Modifying an asset
* Recieving an asset
* Transferring an asset
* Freezing an asset
* Revoking an asset
* Destroying an asset

Retrieving asset info:
```bash
goal asset info --creator <creator-address> --asset unitname  -d ~/node/data -w testwall
# Asset ID:         <created-asset-id>
# Creator:          <creator-address>
# Asset name:       testtoken
# Unit name:        unitname
# Maximum issue:    12 unitname
# Reserve amount:   12 unitname
# Issued:           0 unitname
# Decimals:         0
# Default frozen:   false
# Manager address:  <creator-address>
# Reserve address:  <reserve-address>
# Freeze address:   <freeze-address>
# Clawback address: <clawback-address>
```

## Atomic Transfers

All transactions in a transfer either all succeed or fail.

Irreducable batch operations.

Also eliminates need for complex solutions like 'hashed timelock contracts'
* i.e. Requires the reciever to acknowledge payment before a deadline

Use cases:
* Circular trades (> Alice > Bob > Alice)
* Group payments (everyone pays, or no one)
* Decentralised exchanges
* Distributed payments
* Pooled transaction fees (one transaction pays fees of others)

Process:
* N unsigned transactions are combined/grouped
* All transactions are given a group ID
* Each account then signs the transaction sequencially

Up to 16 unsigned transactions of any type can be grouped.

Example: Sending transactions individually:
```bash
goal clerk send --from=my-account-a<PLACEHOLDER> --to=my-account-c<PLACEHOLDER> --fee=1000 --amount=1000000 --out=unsginedtransaction1.txn
goal clerk send --from=my-account-b<PLACEHOLDER> --to=my-account-a<PLACEHOLDER> --fee=1000 --amount=2000000 --out=unsginedtransaction2.txn
```

Example: Sending transactions combined:
* Combine transaction files using `cat`
```bash
cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx
```
* Group the transactions (hash of transactions set as group ID)
```bash
goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx -d data -w yourwallet
```
* Split the grouped transactions so each wallet can sign
* Assemble transaction grop
* Send transaction group

> This feels a bit tedious - (?)



