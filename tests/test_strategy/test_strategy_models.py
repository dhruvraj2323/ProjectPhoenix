"""
=================================================
Project Phoenix
Test Strategy Models
M38
=================================================
"""

from strategy.strategy_models import (
    StrategyType,
    TradeDirection,
    StrategyStatus,
    StrategySignal,
    StrategyStatistics,
    StrategyResult,
)


def test_strategy_models():

    signal = StrategySignal(
        strategy_id="S01",
        strategy_name=StrategyType.S01_EMA_TREND,
        direction=TradeDirection.BUY,
        confidence=92.5,
        entry_price=2450.50,
        stop_loss=2445.00,
        take_profit=2461.50,
        risk_percent=1.0,
        reason="EMA Trend Confirmed",
    )

    assert signal.strategy_id == "S01"

    assert (
        signal.strategy_name
        == StrategyType.S01_EMA_TREND
    )

    assert (
        signal.direction
        == TradeDirection.BUY
    )

    assert signal.confidence == 92.5

    statistics = StrategyStatistics(
        total_evaluated=4,
        approved=1,
        rejected=3,
    )

    result = StrategyResult(
        status=StrategyStatus.APPROVED,
        selected_strategy=StrategyType.S01_EMA_TREND,
        signals=[signal],
        statistics=statistics,
        message="Strategy Approved",
    )

    assert (
        result.status
        == StrategyStatus.APPROVED
    )

    assert (
        result.selected_strategy
        == StrategyType.S01_EMA_TREND
    )

    assert len(result.signals) == 1

    assert (
        result.statistics.total_evaluated
        == 4
    )

    assert (
        result.statistics.approved
        == 1
    )

    assert (
        result.statistics.rejected
        == 3
    )

    assert (
        result.message
        == "Strategy Approved"
    )