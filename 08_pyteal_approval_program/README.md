# Creating Stateful Algorand Smart Contracts in Python with PyTeal

See https://developer.algorand.org/articles/creating-stateful-algorand-smart-contracts-python-pyteal/

> PyTeal v0.6.0 improves programmers’ ability to manage control flow on a granular level, adding:
> * `Seq`, a new expression for creating a sequence of expressions.
> * `Assert`, a new expression for asserting that a condition is true.
> * `Return`, a new expression that immediately exits the program with a return code.
> * Single branch `If` statements.
>
> Additionally, programmers can manipulate state with new PyTeal operations:
> * Reading and writing to application global state with `App.globalPut`, `App.globalGet`, `App.globalDel`.
> * Reading and writing to account local state with `App.localPut`, `App.localGet`, `App.localDel`.
> * Performing extended reads with App.localGetEx and App.globalGetEx.
> * Reading and writing to temporary scratch slots with ScratchLoad and ScratchStore
>
> We’ve also added new features to make writing TEAL v2 applications easier and more powerful:
> * Bitwise arithmetic expressions: `&`, `|`, `^`, `~`.
> * The ability to create byte strings from UTF-8 strings with `Bytes`.
> * Defining what type of smart contract you are writing with `Mode.Signature` and `Mode.Application`.
> * A new way to compile PyTeal programs, `compileTeal(program, mode)`

Stateful smart contract functionality can allow us to perform complex tasks like running auctions,
managing crowdfunding, hosting polls, etc.

## Stateful Example

`approval_program` - responsible for application calls and opting into a contract

There are two ways for an account to opt-out of a contract: `closing_out` and `clearing_state`

`clearing_state_program` - clears account state.

I do not know how to deploy this.


## Cont.

Compiling and deploying to a private network (see 10_create_private_network)

```bash
# Compile to teal
python approval_program.py

# Compile to teal.tok
goal clerk compile vote_approval.teal -d ~/net1/Node
goal clerk compile vote_clear_state.teal -d ~/net1/Node
# vote_approval address: JXT7N56YFSSUV2MQCJU4MVFRB2QKEIHA2FKCYZXXDSIVWV3LOQO7TGTYT4
# vote_clear_state address: 7BF7UDFEXCBEQJRMELOWO5DL3W3KLDZCVQ7EIYAWJ7PIRRCCEKVSUWDDWY

# Find an account to send the transaction
goal account list -d ~/net1/Node

#TODO: goal app create

# Send txn
# goal app send \
#     -a 30000 \
#     --from-program vote_approval.teal  \
#     -c GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -t GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -o vote_approval.out.txn \
#     -d ~/net1/Node
# goal clerk send \
#     -a 30000 \
#     --from-program vote_clear_state.teal  \
#     -c GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -t GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -o vote_clear_state.out.txn \
#     -d ~/net1/Node
# vote_approval ID: ???????
# vote_clear_state ID: ????????

# goal clerk send \
#     -a 30000 \
#     -f GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -t JXT7N56YFSSUV2MQCJU4MVFRB2QKEIHA2FKCYZXXDSIVWV3LOQO7TGTYT4 \
#     -o out1.txn \
#     -d ~/net1/Node
# goal clerk send \
#     -a 30000 \
#     -f GOGVMSAC37IP5HD3LUTVHHC5WGAS5MMGPGNKNDHQB25OZN7AP4FPKIP3DE \
#     -t 7BF7UDFEXCBEQJRMELOWO5DL3W3KLDZCVQ7EIYAWJ7PIRRCCEKVSUWDDWY \
#     -o out2.txn \
#     -d ~/net1/Node
#
# View app
# goal app info <ID>
```


