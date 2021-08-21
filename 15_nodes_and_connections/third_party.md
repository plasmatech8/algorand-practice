# Third party

Third party nodes are convenient and cheap if you stick to free tier.

Notes:
* Free tier, but has API limits


## REST API

You need to include the `x-api-key` key for the provider.

Example:
```bash
curl -X GET "http://<HOST-AND-PATH>/v2/status" \
    -H "x-api-key:<PURESTAKE-TOKEN>"
```