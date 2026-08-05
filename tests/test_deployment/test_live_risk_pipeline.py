"""
=================================================
Project Phoenix
Live Risk Pipeline Test
M58.12.7
=================================================
"""

from deployment.live_risk_pipeline import (
    LiveRiskPipeline,
)


def test_live_risk_pipeline():

    pipeline = LiveRiskPipeline()

    result = pipeline.execute(

        symbol="EURUSD",

        timeframe="M15",

        bars=200,

    )

    assert result is not None

    assert result.completed is True

    assert result.failed is False

    assert result.risk_result is not None

    assert result.risk_result.reason != ""

    print()

    print("===== Live Risk Pipeline =====")

    print("Account :", result.account_id)

    print("Balance :", result.balance)

    print("Equity  :", result.equity)

    print("Reason  :", result.risk_result.reason)

    print()