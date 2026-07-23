"""
=================================================
Project Phoenix
Test Pattern Detector
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_detector import (
    PatternDetector,
)


def test_pattern_detector():

    detector = PatternDetector()

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = [

        {
            "open": 100,
            "high": 105,
            "low": 95,
            "close": 100.2,
        },

        {
            "open": 101,
            "high": 106,
            "low": 100,
            "close": 105,
        },

    ]

    result = detector.detect(
        context
    )

    assert len(
        result.patterns
    ) == 1

    assert (
        result.patterns[0]["name"]
        == "DOJI"
    )