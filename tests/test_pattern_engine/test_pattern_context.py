"""
=================================================
Project Phoenix
Test Pattern Context
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)


def test_pattern_context():

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.add_pattern(
        {
            "name": "DOJI",
            "strength": 0.82,
        }
    )

    assert len(
        context.get_patterns()
    ) == 1

    context.set_metadata(
        "version",
        "2.0",
    )

    assert (
        context.get_metadata(
            "version"
        )
        == "2.0"
    )

    context.mark_completed()

    assert context.completed is True

    context.reset()

    assert (
        len(
            context.patterns
        )
        == 0
    )

    assert context.completed is False