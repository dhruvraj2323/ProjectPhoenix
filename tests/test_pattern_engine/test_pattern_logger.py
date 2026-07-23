"""
=================================================
Project Phoenix
Test Pattern Logger
M33
=================================================
"""

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_logger import (
    PatternLogger,
)


def test_pattern_logger():

    logger = PatternLogger()

    context = PatternContext(
        engine_id="PATTERN-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.patterns.append("DOJI")

    logger.log_start(context)

    logger.log_complete(context)

    assert True