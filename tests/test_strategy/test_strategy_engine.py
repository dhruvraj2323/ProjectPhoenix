"""
=================================================
Project Phoenix
Test Strategy Engine
M38
=================================================
"""

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_engine import (
    StrategyEngine,
)

from strategy.strategy_models import (
    StrategyStatus,
    StrategyType,
)


def test_strategy_engine():

    engine = StrategyEngine()

    context = StrategyContext(
        engine_id="STRATEGY-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    context.indicators = {
        "EMA9": 2455.0,
        "EMA21": 2450.0,
        "EMA200": 2435.0,
        "RSI14": 60.0,
    }

    context.market_data = {
        "price": 2458.0,
    }

    context.patterns = [
        {
            "name": "DOJI",
        }
    ]

    result = engine.run(
        context,
    )

    assert result.completed is True

    assert result.failed is False

    assert (
        result.strategy_result.status
        == StrategyStatus.APPROVED
    )

    assert (
        result.strategy_result.selected_strategy
        == StrategyType.S01_EMA_TREND
    )

    assert (
        len(
            result.strategy_result.signals
        )
        == 1
    )