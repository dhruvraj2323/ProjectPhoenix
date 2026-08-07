"""
=================================================
Project Phoenix
Test Trade Request Builder
M59.1.4
=================================================
"""

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_models import (
    ExecutionType,
)

from live_execution.trade_request_builder import (
    TradeRequestBuilder,
)


class DummySignal:

    pass


class DummyRisk:

    position_size = 0.10


class DummyStrategy:

    entry_price = 1.1000

    stop_loss = 1.0950

    take_profit = 1.1100


def test_trade_request_builder():

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    context.signal_result = DummySignal()

    context.risk_result = DummyRisk()

    context.strategy_result = DummyStrategy()

    builder = TradeRequestBuilder()

    request = builder.build(
        context,
    )

    assert request.symbol == "EURUSD"

    assert request.volume == 0.10

    assert (
        request.execution_type
        == ExecutionType.MARKET
    )

    assert request.price == 1.1000

    assert request.stop_loss == 1.0950

    assert request.take_profit == 1.1100

    assert (
        context.trade_request
        is request
    )