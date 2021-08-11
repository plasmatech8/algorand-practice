import sys
from pyteal import Global, Txn, Gtxn, Int, TxnType, And, Seq, Assert, Cond, Bytes, Mode, compileTeal


def contract_account(app_id):
    """
    A stateless contract acting as an escrow account.
    """
    # normally this would check that the user is not closing their account and moving funds to a new one
    # !!! Here we are making sure that no-one steals the escrow account funds !!!
    asset_close_to_check = Txn.asset_close_to() == Global.zero_address()

    # check that the transaction does not set a new spending key / auth address
    rekey_check = Txn.rekey_to() == Global.zero_address()

    # check that first transaction is a call to the application
    linked_with_app_call = And(
        Gtxn[0].type_enum() == TxnType.ApplicationCall,
        Gtxn[0].application_id() == Int(app_id)
    )

    # Check that fee is not too big
    fee_check = Txn.fee() <= Int(1000)

    # create asa from escrow
    on_create_asa = Txn.type_enum() == TxnType.AssetConfig

    # fund 1 asa that has been created by escrow
    on_fund_asa = Seq([
        Assert(Txn.type_enum() == TxnType.AssetTransfer),
        Assert(Txn.asset_sender() == Global.zero_address()),  # To Stop Clawback (see notes)
        Assert(asset_close_to_check),
        Assert(Txn.asset_amount() == Int(1)),
        Int(1)
    ])

    return Seq([
        Assert(Txn.group_index() == Int(1)),
        Assert(linked_with_app_call),
        Assert(rekey_check),
        Assert(fee_check),
        Cond(
            [Gtxn[0].application_args[0] == Bytes("create_asa"), on_create_asa],
            [Gtxn[0].application_args[0] == Bytes("fund_asa"), on_fund_asa]
        )
    ])


if __name__ == "__main__":
    arg = int(sys.argv[1])
    print(compileTeal(contract_account(arg), Mode.Signature, version=3))
