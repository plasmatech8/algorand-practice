# Nodes & Connections


Algorand Sandbox:
* Best for:
  * development - can develop locally

Third party:
* Best for:
  * Services (if an indexer is required)

Running your own node:
* Best for:
  * Services (if there is no indexer)
  * Staking


## REST APIs

> Note: to connect to both 3rd party or self-hosted nodes, you can add headers for both:
> ```bash
> curl -X GET "http://<IP>:<PORT>/v2/status" \
>     -H "x-algo-api-token:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
>     -H "x-api-key:<PROVIDER-TOKEN>"
> ```

### Algod v2 REST API

Algod v2 REST API spec: https://developer.algorand.org/docs/reference/rest-apis/algod/v2/

Examples:
```bash
export ALGO_HEADER="x-algo-api-token:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
curl "localhost:4001/health"
curl "localhost:4001/versions" | jq
curl "localhost:4001/swagger.json" | jq
curl "localhost:4001/v2/status" -H $ALGO_HEADER | jq
curl "localhost:4001/v2/ledger/supply" -H $ALGO_HEADER | jq
curl "localhost:4001/v2/status/wait-for-block-after/223" -H $ALGO_HEADER | jq
```
Also check out:
```
POST /v2/teal/compile
POST /v2/teal/dryrun
GET /v2/transactions/pending
GET /v2/transactions/pending/{txid}
```

### Indexer REST API

Indexer REST API Spec: https://developer.algorand.org/docs/reference/rest-apis/indexer

Examples:
```bash
curl "localhost:8980/v2/transactions?pretty"
curl "localhost:8980/v2/accounts" | jq
```
Also check out:
```
GET /v2/accounts
GET /v2/accounts/{account-id}
GET /v2/applications
GET /v2/applications/{application-id}
+ more
```