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