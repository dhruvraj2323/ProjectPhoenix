"""
Test Trade Engine
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

from live_execution.trade_engine import (
    TradeEngine,
)


class DummySignal:
    pass


class DummyAI:
    pass


class DummySymbolInfo:
    name = "EURUSD"
    visible = True
    trade_mode = 0
    trade_exemode = 0
    filling_mode = 1
    trade_stops_level = 0
    trade_freeze_level = 0
    digits = 5


class DummyTick:
    bid = 1.0998
    ask = 1.1002


class DummyResult:
    retcode = 10009
    order = 123456
    price = 1.1002
    volume = 0.10
    comment = "Executed"


class DummyOrderCheckResult:
    retcode = 0
    comment = "Done"


@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.symbol_info_tick",
)
@patch(
    "MetaTrader5.order_check",
)
@patch(
    "MetaTrader5.order_send",
)
def test_trade_engine(
    mock_order_send,
    mock_order_check,
    mock_symbol_info_tick,
    mock_symbol_info,
):

    # --------------------------------------------------
    # MT5 Mocks
    # --------------------------------------------------

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_symbol_info_tick.return_value = (
        DummyTick()
    )

    mock_order_check.return_value = (
        DummyOrderCheckResult()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    # --------------------------------------------------
    # Trade Context
    # --------------------------------------------------

    context = TradeContext(
        execution_id="EXEC-001",
        symbol="EURUSD",
        timeframe="M15",
    )

    # --------------------------------------------------
    # Strategy Result
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Signal Engine Output
    # --------------------------------------------------

    context.signal_result = (
        DummySignal()
    )

    # --------------------------------------------------
    # Risk Engine Output
    # --------------------------------------------------

    risk = RiskResult()

    risk.metrics = RiskMetrics(
        position_size=0.10,
        stop_loss=1.0950,
        take_profit=1.1100,
    )

    context.risk_result = risk

    # --------------------------------------------------
    # AI Output
    # --------------------------------------------------

    context.ai_result = (
        DummyAI()
    )

    # --------------------------------------------------
    # Execute Trade Engine
    # --------------------------------------------------

    engine = TradeEngine()

    result = engine.run(
        context,
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert result.completed is True

    assert result.trade_response is not None

    assert (
        result.trade_response.ticket
        == 123456
    )

    # --------------------------------------------------
    # MT5 Boundary Verification
    # --------------------------------------------------

    mock_symbol_info_tick.assert_called_once_with(
        "EURUSD",
    )

    mock_symbol_info.assert_called_with(
        "EURUSD",
    )

    mock_order_check.assert_called_once()

    mock_order_send.assert_called_once()