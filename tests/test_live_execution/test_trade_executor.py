"""
=================================================
Project Phoenix
Test Trade Executor
M59.1.7
=================================================
"""

from unittest.mock import patch

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_executor import (
    TradeExecutor,
)

from live_execution.trade_models import (
    ExecutionStatus,
    ExecutionType,
    OrderSide,
    TradeRequest,
)


class DummyResult:

    retcode = 10009

    order = 123456

    price = 1.1000

    volume = 0.10

    comment = "Executed"


@patch(
    "MetaTrader5.order_send",
)
def test_trade_executor(
    mock_order_send,
):

    mock_order_send.return_value = (
        DummyResult()
    )

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    context.trade_request = TradeRequest(

        symbol="EURUSD",

        volume=0.10,

        side=OrderSide.BUY,

        execution_type=ExecutionType.MARKET,

        price=1.1000,

        stop_loss=1.0950,

        take_profit=1.1100,

    )

    executor = TradeExecutor()

    response = executor.execute(
        context,
    )

    assert (
        response.status
        == ExecutionStatus.EXECUTED
    )

    assert response.ticket == 123456