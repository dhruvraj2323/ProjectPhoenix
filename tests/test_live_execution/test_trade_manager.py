"""
Test Trade Manager
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

from live_execution.trade_manager import (
    TradeManager,
)


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

    manager = TradeManager()

    result = manager.execute(
        context,
    )

    assert result.completed is True

    assert result.trade_response is not None

    assert result.trade_response.ticket == 123456