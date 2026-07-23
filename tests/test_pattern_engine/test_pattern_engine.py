"""
=================================================
Project Phoenix
Test Pattern Engine
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_engine import (
    PatternEngine,
)


def test_pattern_engine():

    engine = PatternEngine()

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = [
        {"close": 100},
        {"close": 101},
        {"close": 102},
    ]

    result = engine.run(context)

    assert result is context

    assert isinstance(
        result.patterns,
        list,
    )