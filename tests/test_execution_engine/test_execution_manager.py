"""
=================================================
Project Phoenix
Test Execution Manager
M37
=================================================
"""

from unittest.mock import patch


class DummySymbolInfo:
    name = "XAUUSD"
    visible = True
    trade_mode = 0
    trade_exemode = 0
    filling_mode = 1
    trade_stops_level = 0
    trade_freeze_level = 0


class DummyResult:
    retcode = 10009
    order = 123456
    price = 3350.0
    volume = 0.10
    comment = "Executed"


from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_manager import (
    ExecutionManager,
)

from strategy.strategy_models import (
    StrategyResult,
    StrategySignal,
    StrategyType,
    TradeDirection,
)

from risk_engine.risk_models import (
    RiskMetrics,
    RiskResult,
)


@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.order_send",
)
def test_execution_manager(
    mock_order_send,
    mock_symbol_info,
):

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    manager = ExecutionManager()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    signal = StrategySignal(
        strategy_id="S01",
        strategy_name=StrategyType.S01_EMA_TREND,
        direction=TradeDirection.BUY,
        confidence=90,
        entry_price=3350,
        stop_loss=3340,
        take_profit=3370,
        risk_percent=1,
        reason="BUY",
    )

    result = StrategyResult()

    result.signals.append(
        signal,
    )

    context.strategy_result = result

    context.signal_result = object()

    risk = RiskResult()

    risk.metrics = RiskMetrics(
        position_size=0.10,
        stop_loss=3340,
        take_profit=3370,
    )

    context.risk_result = risk

    context.ai_result = object()

    output = manager.execute(
        context,
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert output.completed is True

    assert output.order is not None

    assert (
        output.execution_result.accepted
        is True
    )

    assert (
        output.execution_result.order_id
        == "123456"
    )

    # --------------------------------------------------
    # MT5 Boundary Verification
    # --------------------------------------------------

    mock_symbol_info.assert_called_once_with(
        "XAUUSD",
    )

    mock_order_send.assert_called_once()