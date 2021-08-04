from pyteal import Seq, compileTeal, Return, Int, Mode, App, Txn, Bytes, If, Gtxn, Or, OnComplete, Cond


def approval():

    # Constructor
    on_init = Seq([
        App.globalPut(Bytes("george"), Txn.sender()),  # set george (player) to creators address
        App.globalPut(Bytes("health"), Int(5)),  # set health to 5
        Return(Int(1)),
    ])

    # check if 2nd tx amount is correct and that george receives the payment
    correct_amt_for_george = If(
        Or(
            Gtxn[1].amount() < Int(100),  # Check for at least 100 microalgos
            Gtxn[1].receiver() != App.globalGet(Bytes("george"))
        ),
        Return(Int(0))
    )

    # check if npc is dead or fully replenished
    alive_or_dead = If(Or(App.globalGet(Bytes("health")) >= Int(10),
                          App.globalGet(Bytes("health")) <= Int(0)), Return(Int(0)))

    # check if fully alive/dead, george gets payment, and remove health
    on_injure = Seq([
        alive_or_dead,
        correct_amt_for_george,
        App.globalPut(Bytes("health"), App.globalGet(
            Bytes("health")) - Int(1)),
        Return(Int(1)),
    ])

    # check if fully alive/dead, george gets payment, and remove health
    on_heal = Seq([
        alive_or_dead,
        correct_amt_for_george,
        App.globalPut(Bytes("health"), App.globalGet(
            Bytes("health")) + Int(1)),
        Return(Int(1)),
    ])

    # Is creator
    is_creator = Txn.sender() == App.globalGet(Bytes("george"))

    # Program
    program = Cond(
        # init
        [Txn.application_id() == Int(0), on_init],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],  # delete
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],  # update
        [Txn.application_args[0] == Bytes("heal"), on_heal],                        # heal
        [Txn.application_args[0] == Bytes("damage"), on_injure],                    # injure
    )
    return program


def clear_state():
    program = Seq([Return(Int(1))])
    return program


if __name__ == "__main__":
    with open('approval.teal', 'w') as f:
        compiled = compileTeal(approval(), mode=Mode.Application, version=2)
        f.write(compiled)

    with open('clear_state.teal', 'w') as f:
        compiled = compileTeal(clear_state(), mode=Mode.Application, version=2)
        f.write(compiled)
