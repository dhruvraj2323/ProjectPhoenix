"""
=================================================
Project Phoenix
Test Pattern Manager
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_manager import (
    PatternManager,
)


def test_pattern_manager():

    manager = PatternManager()

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = [
        {
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 100,
        }
    ]

    result = manager.run(
        context
    )

    assert result is context

    assert isinstance(
        result.patterns,
        list,
    )