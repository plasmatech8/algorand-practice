from pyteal import (App, Assert, Bytes, Global, Int, Mode, Txn,
                    Btoi, Return, And, If, Seq, Cond, OnComplete, compileTeal)

def approval_program():

    # Initialize program data
    on_creation = Seq([
        App.globalPut(Bytes("Creator"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(4)),
        App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[3])),
        Return(Int(1))
    ])

    # If sender is creator - is_creator
    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    # Get what the vote of the sender is - has_voted (0 or 'voted')
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

    # Remove a vote (when an account opts-out)
    on_closeout = Seq([
        # Check voter has 'voted' in their local state
        get_vote_of_sender,
        If(And(Global.round() <= App.globalGet(Bytes("VoteEnd")), get_vote_of_sender.hasValue()),
            App.globalPut(get_vote_of_sender.value(), App.globalGet(get_vote_of_sender.value()) - Int(1))
        ),
        Return(Int(1))
    ])

    # If user registers between the begin round and ending round - can_register
    on_register = Return(And(
        Global.round() >= App.globalGet(Bytes("RegBegin")),
        Global.round() <= App.globalGet(Bytes("RegEnd"))
    ))

    # Do voting
    choice = Txn.application_args[1]
    choice_tally = App.globalGet(choice)
    on_vote = Seq([
        # Valid voting period
        Assert(And(
            Global.round() >= App.globalGet(Bytes("VoteBegin")),
            Global.round() <= App.globalGet(Bytes("VoteEnd"))
        )),
        # Check that voter has 'voted' in their local state
        get_vote_of_sender,
        # Fail if account has already voted
        If(get_vote_of_sender.hasValue(),
            Return(Int(0))
        ),
        # Increment the global tally variable for 'choice'
        App.globalPut(choice, choice_tally + Int(1)),
        # Set the account 'voted' to 'choice'
        App.localPut(Int(0), Bytes("voted"), choice),
        Return(Int(1))
    ])

    # Switch condition, else terminate with error.
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        [Txn.application_args[0] == Bytes("vote"), on_vote]
    )

    return program


def clear_state_program():
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))
    program = Seq([
        # Check that voter has 'voted' key in local state
        get_vote_of_sender,
        # If the vote has not finished and the voter has voted, remove the vote from tally counter for the 'choice'
        If(And(Global.round() <= App.globalGet(Bytes("VoteEnd")), get_vote_of_sender.hasValue()),
            App.globalPut(get_vote_of_sender.value(), App.globalGet(get_vote_of_sender.value()) - Int(1))
        ),
        Return(Int(1))
    ])
    return program


def compile_all():
    with open('vote_approval.teal', 'w') as f:
        compiled = compileTeal(approval_program(), Mode.Application)
        f.write(compiled)
    with open('vote_clear_state.teal', 'w') as f:
        compiled = compileTeal(clear_state_program(), Mode.Application)
        f.write(compiled)
