"""
=================================================
Project Phoenix
Test Trade Engine
M59.1.8
=================================================
"""

from unittest.mock import patch

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_engine import (
    TradeEngine,
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
def test_trade_engine(
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

    engine = TradeEngine()

    result = engine.run(
        context,
    )

    assert result.completed is True

    assert result.trade_response is not None

    assert result.trade_response.ticket == 123456