"""
=================================================
Project Phoenix
Test Live Trade Models
M59.1.1
=================================================
"""

from live_execution.trade_models import (
    ExecutionStatus,
    ExecutionType,
    OrderSide,
    TradeRequest,
    TradeResponse,
)


def test_trade_models():

    request = TradeRequest(

        symbol="EURUSD",

        volume=0.10,

        side=OrderSide.BUY,

        execution_type=ExecutionType.MARKET,

        price=1.1000,

        stop_loss=1.0950,

        take_profit=1.1100,

    )

    assert request.symbol == "EURUSD"

    assert request.volume == 0.10

    assert request.side == OrderSide.BUY

    response = TradeResponse(

        status=ExecutionStatus.EXECUTED,

        ticket=123456,

        executed_price=1.1002,

        executed_volume=0.10,

        broker_message="Order Executed",

    )

    assert (
        response.status
        == ExecutionStatus.EXECUTED
    )

    assert response.ticket == 123456

    assert response.executed_volume == 0.10