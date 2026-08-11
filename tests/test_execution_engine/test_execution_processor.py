"""
Execution Processor Test
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


class DummyOrderCheckResult:
    retcode = 0
    comment = "Done"


from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_processor import (
    ExecutionProcessor,
)

from strategy.strategy_models import (
    StrategySignal,
    StrategyType,
    StrategyResult,
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
    "MetaTrader5.order_check",
)
@patch(
    "MetaTrader5.order_send",
)
def test_execution_processor(
    mock_order_send,
    mock_order_check,
    mock_symbol_info,
):
    # --------------------------------------------------
    # MT5 Mocks
    # --------------------------------------------------

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_order_check.return_value = (
        DummyOrderCheckResult()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    # --------------------------------------------------
    # Processor
    # --------------------------------------------------

    processor = ExecutionProcessor()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    # --------------------------------------------------
    # Strategy Signal
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Signal Result
    # --------------------------------------------------

    context.signal_result = object()

    # --------------------------------------------------
    # Risk Result
    # --------------------------------------------------

    risk = RiskResult()

    risk.metrics = RiskMetrics(
        position_size=0.10,
        stop_loss=3340,
        take_profit=3370,
    )

    context.risk_result = risk

    # --------------------------------------------------
    # AI Result
    # --------------------------------------------------

    context.ai_result = object()

    # --------------------------------------------------
    # Process
    # --------------------------------------------------

    output = processor.process(
        context,
    )

    # --------------------------------------------------
    # Order Assertions
    # --------------------------------------------------

    assert output.order is not None

    assert (
        output.order.symbol
        == "XAUUSD"
    )

    assert (
        output.order.side
        == "BUY"
    )

    # --------------------------------------------------
    # Execution Assertions
    # --------------------------------------------------

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

    mock_order_check.assert_called_once()

    mock_order_send.assert_called_once()