# Algo Wallet Integration

Check out:
* https://github.com/lucasvanmol/algobets

To sign transactions, you will still need a algod connection via one of the Algorand SDK.

## Algosigner

Tutorial:
* [Adding Transaction Capabilities to a dApp Using AlgoSigner](https://developer.algorand.org/tutorials/adding-transaction-capabilities-dapp-using-algosigner/)
  * Not really following it. It is basically a rundown of the demo.

JavaScript code examples:
* [algosigner-dapp-example](https://purestake.github.io/algosigner-dapp-example/)
  * (Zoom out to see the top-bar)
* [documentation](https://github.com/PureStake/algosigner/tree/develop/docs)
  * https://github.com/PureStake/algosigner/blob/develop/docs/dApp-integration.md)

Install:
* Don't need to install. `window.AlgoSigner` will be injected onto the page.

Check wallet presence:
```js
setTimeout(() => {
  if (window.AlgoSigner) {
    this.algosignerStatus = "AlgoSigner is installed.";
  } else {
    this.algosignerStatus = "AlgoSigner is NOT installed.";
  }
}, 5);
```

## MyAlgo Connect

Tutorial:
* [Introducing MyAlgo Connect for DApp Developers](https://developer.algorand.org/articles/introducing-myalgo-connect/)

Examples:
* [Readme API usage examples / docs](https://github.com/randlabs/myalgo-connect)

Install:
```bash
npm install @randlabs/myalgo-connect
```

Connect:
```js
try{
  this.connect();
} catch(e){
  console.error(e);
}
```

We cannot check wallet presence, we can only connect.

It is a little annoying that it is a website that requires service availability, has slow loading
time, and asks us to type a password every single time.