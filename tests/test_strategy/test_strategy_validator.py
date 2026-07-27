"""
=================================================
Project Phoenix
Test Strategy Validator
M38
=================================================
"""

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_validator import (
    StrategyValidator,
)


def test_strategy_validator():

    validator = StrategyValidator()

    context = StrategyContext(
        engine_id="STRATEGY-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    context.indicators = {
        "EMA9": 100,
        "EMA21": 99,
        "EMA200": 95,
        "RSI14": 60,
    }

    context.patterns = [
        {
            "name": "DOJI",
        }
    ]

    context.market_data = {
        "spread": 15,
        "session": "LONDON",
        "volatility": "NORMAL",
    }

    assert (
        validator.validate(
            context,
        )
        is True
    )

    invalid = StrategyContext(
        engine_id="STRATEGY-002",
        symbol="",
        timeframe="M15",
    )

    assert (
        validator.validate(
            invalid,
        )
        is False
    )

    assert invalid.failed is True

    assert (
        invalid.reason
        == "Symbol is missing."
    )