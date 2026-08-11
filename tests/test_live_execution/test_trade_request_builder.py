"""
Test Trade Request Builder
"""

from strategy.strategy_models import (
    StrategySignal,
    StrategyResult,
    StrategyType,
    TradeDirection,
)

from risk_engine.risk_models import (
    RiskMetrics,
    RiskResult,
)

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


def test_trade_request_builder():

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    context.signal_result = DummySignal()

    # ----------------------------------------
    # Strategy Result
    # ----------------------------------------

    signal = StrategySignal(

        strategy_id="S01",

        strategy_name=StrategyType.S01_EMA_TREND,

        direction=TradeDirection.BUY,

        confidence=90,

        entry_price=1.1000,

        stop_loss=0.0,

        take_profit=0.0,

        risk_percent=1,

        reason="BUY",

    )

    strategy = StrategyResult()

    strategy.signals.append(
        signal,
    )

    context.strategy_result = strategy

    # ----------------------------------------
    # Risk Result
    # ----------------------------------------

    risk = RiskResult()

    risk.metrics = RiskMetrics(

        position_size=0.10,

        stop_loss=1.0950,

        take_profit=1.1100,

    )

    context.risk_result = risk

    # ----------------------------------------

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