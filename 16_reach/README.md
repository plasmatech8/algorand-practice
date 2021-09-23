# Reach

See:
* https://docs.reach.sh/overview.html

Contents:
- [Reach](#reach)
  - [1. Overview](#1-overview)
  - [2. Tutorial](#2-tutorial)
    - [2.1 Install and initialize](#21-install-and-initialize)
    - [2.2 Scaffolding and setup](#22-scaffolding-and-setup)
    - [2.3 Rock, paper, scissors](#23-rock-paper-scissors)

Thoughts:
* It looks okay. Feels a little weird.

## 1. Overview

## 2. Tutorial

### 2.1 Install and initialize

Needs:
* make
* Docker
* Docker Compose

Create project folder and download reach.
```bash
mkdir tut
cd tut
curl https://docs.reach.sh/reach -o reach ; chmod +x reach
```

Try (will download docker images if not exists):
```bash
./reach version
./reach compile --help
```

### 2.2 Scaffolding and setup

We will make rock-paper-scissors.

In `index.rsh` we will define our backend contract code.
```js
'reach 0.1';

export const main = Reach.App(() => {
  const Alice = Participant('Alice', {
    // Specify Alice's interact interface here
  });
  const Bob   = Participant('Bob', {
   // Specify Bob's interact interface here
  });
  deploy();
  // write your program here

});
```

We can compile this using `./reach compile`.

In `index.mjh` we will define our frontend code. (???) This looks more like a testing script.
```js
import { loadStdlib } from '@reach-sh/stdlib';
import * as backend from './build/index.main.mjs';
const stdlib = loadStdlib(process.env);

(async () => {
  const startingBalance = stdlib.parseCurrency(10);
  const accAlice = await stdlib.newTestAccount(startingBalance);
  const accBob = await stdlib.newTestAccount(startingBalance);

  const ctcAlice = accAlice.deploy(backend);
  const ctcBob = accBob.attach(backend, ctcAlice.getInfo());

  await Promise.all([
    backend.Alice(ctcAlice, {
      // implement Alice's interact object here
    }),
    backend.Bob(ctcBob, {
      // implement Bob's interact object here
    }),
  ]);
})(); // <-- Don't forget these!
```

We can run this using `./reach run`.

This will build and run a new Docker container for the application.

### 2.3 Rock, paper, scissors

In `index.rsh` we will create a Player 'interact interface' for the players.
* getHand returns a number for the hand
* seeOutcome recieves a number for win/lose/draw

This interface will be added to the participants.

```js
'reach 0.1';

const Player = {
  getHand: Fun([], UInt),
  seeOutcome: Fun([UInt], Null),
};

export const main = Reach.App(() => {
  const Alice = Participant('Alice', {
    ...Player,
  });
  const Bob   = Participant('Bob', {
    ...Player,
  });
  deploy();

  Alice.only(() => {
```

In `index.mjs` frontend, we will implement the methods in the frontend amd add them to the participants:
```js
const HAND = ['Rock', 'Paper', 'Scissors'];
const OUTCOME = ['Bob wins', 'Draw', 'Alice wins'];
const Player = (Who) => ({
    getHand: () => {
        const hand = Math.floor(Math.random() * 3);
        console.log(`${Who} played ${HAND[hand]}`);
        return hand;
    },
    seeOutcome: (outcome) => {
        console.log(`${Who} saw outcome ${OUTCOME[outcome]}`);
    },
});

await Promise.all([
    backend.Alice(ctcAlice, {
        ...Player('Alice'),
    }),
    backend.Bob(ctcBob, {
        ...Player('Bob'),
    }),
]);
```

This contains the logic to choose what your hand is and viewing the outcome.

Then we can add backend logic to ask for alice, then bob, then show outcomes.

```js
  // 1. Ask Alice for hand
  Alice.only(() => {
    const handAlice = declassify(interact.getHand());
  });
  Alice.publish(handAlice);
  commit();

  // 2. Ask Bob for hand
  Bob.only(() => {
    const handBob = declassify(interact.getHand());
  });
  Bob.publish(handBob);

  // 3. Calculate the outcome
  const outcome = (handAlice + (4 - handBob)) % 3;
  commit();

  // 4. Allow Alice and Bob to view the outcome
  each([Alice, Bob], () => {
    interact.seeOutcome(outcome);
  });
```

