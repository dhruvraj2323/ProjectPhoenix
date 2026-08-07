"""
=================================================
Project Phoenix
Test Trade Result
M59.1.5
=================================================
"""

from live_execution.trade_models import (
    ExecutionStatus,
)

from live_execution.trade_result import (
    TradeResultBuilder,
)


def test_trade_result():

    builder = TradeResultBuilder()

    success = builder.success(

        ticket=123456,

        price=1.1005,

        volume=0.10,

        message="Order Executed",

    )

    assert (
        success.status
        == ExecutionStatus.EXECUTED
    )

    assert success.ticket == 123456

    assert success.executed_price == 1.1005

    assert success.executed_volume == 0.10

    failed = builder.failure(

        message="Trade Rejected",

    )

    assert (
        failed.status
        == ExecutionStatus.FAILED
    )

    assert (
        failed.broker_message
        == "Trade Rejected"
    )