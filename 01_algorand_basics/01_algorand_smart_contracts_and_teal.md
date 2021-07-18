https://www.youtube.com/watch?v=OWFRP9McBmk

# TEAL

## What it is

Transaction Execution Approval Language

Can analyze and approve/reject a transaction but cannot change or create a transaction.

A transaction approved by TEAL is signed by an account key in one of two conditions:
* TEAL code is signed by an account key - so the account approves the transaction
* Signed by a contract account (hash of the TEAL code) - contract approves the transaction

## Working

TEAL is a stack language (like a calculator).

## Shortest program

An integer 1, which returns true.
```
int 1
```

The contract is valid / approves the transaction if it ends with a
non-zero value on the stack.

## More complicated program

What it does:
1. Define limit for the Fee - to avoid people making bad contracts
2. We can either send a specific amount, or the remainder that the account owns. (???)
3. Specify receiver
4. Check that the lease so they can only have the Algo between two times. The lease is only valid for 999 rounds.

This contract gives away up to 5 Algos to the recipient every 1000 rounds.

```teal
txn Fee
int 10000
<=

txn CloseRemainderTo
global zeroAddress
==
&&

txn Receiver
addr DFP...
==
&&

txn Lease
byte btv2...

txn LastValid
txn FirstValid
-
int 999
>-
&&

txn Amount
int 5000000
<=
&&>
```

These are all `&&` because all of the statements need to be truthy.

## Math Example

(int(arg[0]) == 0) or ((9999999 / int(arg[0])) > 500)

```teal
int 9999999     // Add 9999999 to stack     > 9999999
arg 0           // Load arg 0               > "42", 9999999
btoi            // Convert to integer       > 42, 9999999
dup             // Duplicate integer        > 42, 42, 9999999
int 0           // Add 0 to stack           > 0, 42, 42, 9999999
>               // Pop 2 items on stack and compare (0 > 42), returns 1 they are same (both 0) > 42, 9999999
bnz ok          // Branch if Not Zero - GOTO 'ok' label, else go to the code below (first condition is true)

pop             // Pop last item in stack > 0, 42, 42, 9999999
int 1           // Add 1 to stack
bnz done        // GOTO 'done' label

ok:           // When first condition is true           > 42, 9999999
/             // Pop 2 items and divide (9999999 / 42)  > 238095.214286
500           // Define 500 (int?)                      > 500, 238095.214286
>             // Compare (238095.214286 > 500) and continues to the code below

done:
// other code here. The code above implements the expression.
// A non-zero int is left of the stack if the expression is true.
```

## two transaction group

Txn[0].Amount * A == Txn[1].Amount * B (AKA txn0/txn1 == B/A)

Check that the ratio of the two transactions are the same as A:B

But if we did this in the simplest way (?), it could cause overflow which will break the contract.

```teal
gtxn 0 Amount               // Get transaction amount               > txn0amt
int 1311693406324658740     // Define int                           > 1311693406324658740, txn0amt
mulw                        // Multiply wide (two 64 bit integers) and
                            // keeps all 124 bits as two separate integers > lower_half_1, higher_half_1
store 2                     // Store the lower half value into position 2 > higher_half_1

gtxn 0 Amount               // Get transaction amount
int 14627357396862417851    // Define int
mulw                        // Wide multiply
store 4                     // Store the lower half into position 4 > higher_half_2, higher_half_1

==                  // Pop and compare higher halves > 1

load 2              // Load                        > lower_half_1
load 4              // Load                        > lower_half_2

==                  // Pop and compare lower halves > 1, 1

&&                   // Pop and return AND > 1
```

## What TEAL cannot do

* Cannot **create** or **change** a transaction, only approve/reject
* Cannot **lookup balances** of Algos or other assets
* Cannot **access information** in previous blocks/transactions
* Cannot know what **round** the transaction will commit in
  * (but it can know whether it is between LastValid or FirstValid)
* Cannot know what the **time** its transaction is committed
* Cannot do **loops** using BNZ - can only be used to skip forward
* Cannot do **recursion**

## What TEAL can do

* Cross chain swaps (via hashed-time-locked-contract)
* Automatic payment splitting
* Recurring payments
* Limit order trades

???