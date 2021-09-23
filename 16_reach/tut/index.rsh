'reach 0.1';

const Player = {
  getHand: Fun([], UInt),
  seeOutcome: Fun([UInt], Null),
};

export const main = Reach.App(() => {
  const Alice = Participant('Alice', {
    ...Player
  });
  const Bob   = Participant('Bob', {
   ...Player
  });
  deploy();

  // write your program here

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
});