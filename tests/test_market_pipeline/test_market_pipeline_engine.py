"""
=================================================
Project Phoenix
Market Pipeline Engine Test
=================================================
"""

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)


def test_market_pipeline_engine():

    engine = MarketPipelineEngine()

    result = engine.run(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    assert result.approved is True
    assert result.status.completed is True
    assert result.validation.passed is True

    print()
    print("===== Market Pipeline Engine =====")
    print("Approved :", result.approved)
    print("Stage    :", result.status.stage)
    print("Reason   :", result.reason)
    print()

    print("Market Pipeline Engine Test Passed")


if __name__ == "__main__":
    test_market_pipeline_engine()