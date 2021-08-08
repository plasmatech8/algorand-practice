# Permissionless Voting Stateful Application

See: https://developer.algorand.org/solutions/example-permissionless-voting-stateful-smart-contract-application/

A smart contracts which allows an any address to vote once.

> For voting, it is probably a good idea to somehow read balances (???) to ensure empty spam
> accounts aren't used.

Steps:
1. Create voting smart contract
    * Creator address used to delete or update the contract
    * Time period in rounds must be configured
    * Contruction params (`goal app create`)
      * set registration rounds
      * set voting rounds
      * set creator
    * Data
      * global state
      * registration begin round
      * registration end round
      * vote begin round
      * vote end round
      * candidate A votes
      * candidate B votes
      * vote creator
2. Register to vote
    * Opt-into the contract to vote (`goal app optin`)
    * Must be between registration rounds
3. Vote
    * Double voting is prevented
    * (TBA about solution for empty spam accounts)
4. Close out
    * Voters can close our their participation and their vote is nullified
    * Contract checks if vote is over

## 01.Voting Smart Contract

See [vote.teal](vote.teal)

```bash
goal app create \
    --creator BOBKQDRGOJWPIAHDEPKBJZLQ6O6NQ5TTQUALJA7JHVG6S543BSQ4UO4FVU \
    --approval-prog ./vote.teal \
    --global-byteslices 1 \
    --global-ints 6 \
    --local-byteslices 1 \
    --local-ints 0 \
    --app-arg "int:1" \
    --app-arg "int:20" \
    --app-arg "int:20" \
    --app-arg "int:100" \
    --clear-prog ./vote_opt_out.teal \
    -d ~/net1/Node
```

........

TODO: finish fixing and commenting on `vote.teal`.

## Commands

```bash
goal app create \
    --creator {CentralAccount}   \
    --approval-prog ./vote.teal \
    --global-byteslices 1 \
    --global-ints 6 \
    --local-byteslices 1 \
    --local-ints 0 \
    --app-arg "int:1" \
    --app-arg "int:20" \
    --app-arg "int:20" \
    --app-arg "int:100" \
    --clear-prog ./vote_opt_out.teal \
    -d ~/node/data

goal app optin  \
    --app-id {APPID} \
    --from {ACCOUNT} \
    -d ~/node/data

goal app call \
    --app-id {APPID}  \
    --app-arg "str:vote" \
    --app-arg "str:candidatea" \
    --from {ACCOUNT}  \
    -d ~/node/data

goal app closeout \
    --app-id {APPID}  \
    --from {ACCOUNT}  \
    -d ~/node/data
```