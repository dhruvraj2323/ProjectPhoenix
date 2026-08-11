"""
Test Trade Request Builder
"""

from unittest.mock import patch

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


class DummySymbolInfo:
    digits = 5


class DummyTick:
    bid = 1.0998
    ask = 1.1002


@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.symbol_info_tick",
)
def test_trade_request_builder(
    mock_symbol_info_tick,
    mock_symbol_info,
):

    # ----------------------------------------
    # MT5 Symbol
    # ----------------------------------------

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    # ----------------------------------------
    # MT5 Current Tick
    # ----------------------------------------

    mock_symbol_info_tick.return_value = (
        DummyTick()
    )

    # ----------------------------------------
    # Context
    # ----------------------------------------

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    context.signal_result = (
        DummySignal()
    )

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
    # Build Request
    # ----------------------------------------

    builder = TradeRequestBuilder()

    request = builder.build(
        context,
    )

    # ----------------------------------------
    # Assertions
    # ----------------------------------------

    assert request.symbol == "EURUSD"

    assert request.volume == 0.10

    assert (
        request.execution_type
        == ExecutionType.MARKET
    )

    # BUY must use current MT5 ASK,
    # not the historical strategy entry price.

    assert request.price == 1.1002

    assert request.stop_loss == 1.0950

    assert request.take_profit == 1.1100

    assert (
        context.trade_request
        is request
    )

    # ----------------------------------------
    # MT5 Boundary Verification
    # ----------------------------------------

    mock_symbol_info_tick.assert_called_once_with(
        "EURUSD",
    )

    mock_symbol_info.assert_called_once_with(
        "EURUSD",
    )