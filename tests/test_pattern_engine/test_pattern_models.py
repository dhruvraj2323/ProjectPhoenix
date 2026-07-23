"""
=================================================
Project Phoenix
Test Pattern Models
M33
=================================================
"""

from pattern_engine.pattern_models import (
    PatternStatus,
    PatternSignal,
    PatternStatistics,
    PatternResult,
)


def test_pattern_models():

    signal = PatternSignal(
        name="DOJI",
        index=10,
        bullish=False,
        bearish=False,
        strength=0.85,
    )

    stats = PatternStatistics(
        total_patterns=1,
        bullish_patterns=0,
        bearish_patterns=0,
    )

    result = PatternResult(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
        status=PatternStatus.CREATED,
        patterns=[signal],
        statistics=stats,
    )

    assert result.engine_id == "PATTERN-001"

    assert result.symbol == "XAUUSD"

    assert result.patterns[0].name == "DOJI"

    assert result.statistics.total_patterns == 1

    assert result.status == PatternStatus.CREATED