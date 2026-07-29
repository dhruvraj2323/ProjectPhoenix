"""
=================================================
Project Phoenix
Test Execution Manager
M37
=================================================
"""

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


def test_execution_manager():

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

    result.signals.append(signal)

    context.strategy_result = result

    context.signal_result = object()

    context.risk_result = object()

    context.ai_result = object()

    output = manager.execute(
        context,
    )

    assert output.completed is True

    assert output.order is not None

    assert output.execution_result.accepted is True