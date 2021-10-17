<template>
  <div id="app">
    <h1>Hello World!</h1>

    <h2>Connect</h2>
    <button @click="connect">Connect</button>

    <h2>Accounts</h2>
    <button @click="connect">Get Accounts</button>
    <ul>
      <li v-for="acc in accounts" :key="acc.address">{{ acc }}</li>
    </ul>


    <h2>Send Txn</h2>
    <form @submit.prevent="submitTxn">
      <p>
        <label for="account">Account</label>
        <select name="account" v-model="sendTxnForm.address">
          <option
            v-for="acc in accounts"
            :value="acc.address"
            :key="acc.address"
            >{{ acc.address }}</option
          >
        </select>
      </p>
      <p>
        <label for="to">To</label>
        <select name="to" v-model="sendTxnForm.to">
          <option
            v-for="acc in accounts"
            :value="acc.address"
            :key="acc.address"
            >{{ acc.address }}</option
          >
        </select>
      </p>
      <p>
        <label for="amount">Amount: </label>
        <input type="number" name="amount" v-model="sendTxnForm.amount" />
      </p>
      <p>
        <label for="note">Note: </label>
        <input type="text" name="note" v-model="sendTxnForm.note" />
      </p>
      <button type="submit">Submit</button>
    </form>
    <p v-if="pendingTxnId">Waiting for transaction: {{ pendingTxnId }}</p>

  </div>
</template>

<script>
import MyAlgo from '@randlabs/myalgo-connect';
import algosdk from "algosdk";

export default {
  name: 'App',
  components: {

  },
  data(){
    return {
      myAlgoWallet: new MyAlgo(),
      accounts: [],
      sendTxnForm: { address: null, to: null, amount: 0, note: "" },
      algodClient: null,
      pendingTxnId: null,
    }
  },
  async mounted(){
    // Connect with popup (will often be blocked if not triggered by user-action)
    // try{
    //   this.connect();
    // } catch(e){
    //   console.error(e);
    // }

    // Algo SDK
    const algodServer = "https://testnet-algorand.api.purestake.io/ps2";
    const token = { "X-API-Key": "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab" };
    const port = "";
    const algodClient = new algosdk.Algodv2(token, algodServer, port);
    const d = await algodClient.healthCheck().do();
    this.algodClient = algodClient;
    console.log("Health check:" + JSON.stringify(d));
  },
  methods: {
    async connect(){
      this.accounts = await this.myAlgoWallet.connect();
    },
    async submitTxn() {
      console.log(this.sendTxnForm);
      const suggestedParams = await this.algodClient.getTransactionParams().do();
      console.log(suggestedParams)

      // Method 1 (Default method: raw object, sign with myalgo, send with algod client)

      // Construct Transaction
      const txn = {
        ...suggestedParams,
        type: 'pay',
        from: this.sendTxnForm.address,
        to:  this.sendTxnForm.to,
        amount: +this.sendTxnForm.amount,
        note: utf8ToUint8Array(this.sendTxnForm.note),
      };
      console.log(txn);
      console.log('transaction constructed');
      // Sign transaction
      const signedTxn = await this.myAlgoWallet.signTransaction(txn);
      console.log(signedTxn)
      console.log('transaction signed');
      // Send transaction
      const sentTxn = await this.algodClient.sendRawTransaction(signedTxn.blob).do();
      console.log(sentTxn);
      console.log('transaction sent');

      // Method 2 (algosdk class, sign with myalgo, send with algod client)
      /*
      // Construct Transaction
      const txn = new algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        suggestedParams: suggestedParams,
        from: this.sendTxnForm.address,
        to:  this.sendTxnForm.to,
        amount: +this.sendTxnForm.amount,
        note: utf8ToUint8Array(this.sendTxnForm.note)
      });
      console.log(txn);
      console.log('transaction constructed');
      // Sign Transaction
      const signedTxn = await this.myAlgoWallet.signTransaction(txn.toByte());
      // console.log(txn.toByte())
      // console.log(txn.bytesToSign())
      // console.log(txn.get_obj_for_encoding())
      console.log(signedTxn);
      console.log('transaction signed');
      // Send Transaction
      const sentTxn = await this.algodClient.sendRawTransaction(signedTxn.blob).do();
      console.log(sentTxn);
      console.log('transaction sent');
      */

      // Wait for transaction

      this.pendingTxnId = sentTxn.txId;
      try {
        const completedTxnInfo = await waitForConfirmation(this.algodClient, this.pendingTxnId, 10)
        console.log('Transaction success!')
        console.log(completedTxnInfo)
        this.pendingTxnId = 'success';
      } catch(e) {
        console.log('Transaction failure!');
        console.error(e);
        this.pendingTxnId = e;
      }
    }
  }
}

/**
 * Wait until the transaction is confirmed or rejected, or until 'timeout'
 * number of rounds have passed.
 * @param {algosdk.Algodv2} algodClient the Algod V2 client
 * @param {string} txId the transaction ID to wait for
 * @param {number} timeout maximum number of rounds to wait
 * @return {Promise<*>} pending transaction information
 * @throws Throws an error if the transaction is not confirmed or rejected in the next timeout rounds
 */
const waitForConfirmation = async function (algodClient, txId, timeout) {
    if (algodClient == null || txId == null || timeout < 0) {
        throw new Error("Bad arguments");
    }
    const status = (await algodClient.status().do());
    if (status === undefined) {
        throw new Error("Unable to get node status");
    }
    const startround = status["last-round"] + 1;
    let currentround = startround;
    while (currentround < (startround + timeout)) {
        const pendingInfo = await algodClient.pendingTransactionInformation(txId).do();
        if (pendingInfo !== undefined) {
            if (pendingInfo["confirmed-round"] !== null && pendingInfo["confirmed-round"] > 0) {
                //Got the completed Transaction
                return pendingInfo;
            } else {
                if (pendingInfo["pool-error"] != null && pendingInfo["pool-error"].length > 0) {
                    // If there was a pool error, then the transaction has been rejected!
                    throw new Error("Transaction " + txId + " rejected - pool error: " + pendingInfo["pool-error"]);
                }
            }
        }
        await algodClient.statusAfterBlock(currentround).do();
        currentround++;
    }
    throw new Error("Transaction " + txId + " not confirmed after " + timeout + " rounds!");
};

// alt: new Uint8Array(Buffer.from('Hello World'))
/* eslint-disable no-unused-vars */
function utf8ToUint8Array (str) {
  const enc = new TextEncoder() // always utf-8
  return enc.encode(str)
}

function base64ToUint8Array (base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
