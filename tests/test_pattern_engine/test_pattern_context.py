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

    # -------------------------------------------------
    # Pattern Management
    # -------------------------------------------------

    context.add_pattern(
        {
            "name": "DOJI",
            "strength": 0.82,
        }
    )

    assert len(
        context.get_patterns()
    ) == 1

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Approval
    # -------------------------------------------------

    context.approve(
        decision="PATTERNS_DETECTED",
        reason="Pattern detection completed successfully.",
    )

    assert context.approved is True
    assert context.completed is True
    assert context.failed is False

    assert (
        context.decision
        == "PATTERNS_DETECTED"
    )

    assert (
        context.reason
        == "Pattern detection completed successfully."
    )

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    context.reset()

    assert len(
        context.patterns
    ) == 0

    assert context.approved is False
    assert context.completed is False
    assert context.failed is False

    assert context.decision == ""
    assert context.reason == ""