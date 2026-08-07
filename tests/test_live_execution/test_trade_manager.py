"""
=================================================
Project Phoenix
Test Trade Manager
M59.1.9
=================================================
"""

from unittest.mock import patch

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_manager import (
    TradeManager,
)


class DummyRisk:

    position_size = 0.10


class DummyStrategy:

    entry_price = 1.1000

    stop_loss = 1.0950

    take_profit = 1.1100


class DummySignal:

    pass


class DummyAI:

    pass


class DummyResult:

    retcode = 10009

    order = 123456

    price = 1.1000

    volume = 0.10

    comment = "Executed"


@patch(
    "MetaTrader5.order_send",
)
def test_trade_manager(
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

    context.strategy_result = (
        DummyStrategy()
    )

    context.signal_result = (
        DummySignal()
    )

    context.risk_result = (
        DummyRisk()
    )

    context.ai_result = (
        DummyAI()
    )

    manager = TradeManager()

    result = manager.execute(
        context,
    )

    assert result.completed is True

    assert result.trade_response is not None

    assert result.trade_response.ticket == 123456