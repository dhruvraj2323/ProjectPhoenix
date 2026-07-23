"""
=================================================
Project Phoenix
Test Pattern Validator
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_validator import (
    PatternValidator,
)


def test_pattern_validator():

    validator = PatternValidator()

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = []

    assert (
        validator.validate(context)
        is True
    )

    context.symbol = ""

    assert (
        validator.validate(context)
        is False
    )