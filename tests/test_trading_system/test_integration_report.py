"""
=================================================
Project Phoenix
Integration Report Test
=================================================
"""

from trading_system.integration_report import (
    IntegrationReport,
)


def test_integration_report():

    report = IntegrationReport(

        session_id="SESSION-001",

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

        strategy_name="EMA Strategy",

        ai_decision="BUY",

        risk_passed=True,

        order_id="ORDER-001",

        approved=True,

        decision="PAPER_EXECUTED",

        reason="Paper trade successful.",

    )

    report.mark_completed(
        processing_time_ms=125.75,
    )

    summary = report.summary()

    assert summary["session_id"] == "SESSION-001"

    assert summary["trading_id"] == "TRD-001"

    assert summary["symbol"] == "XAUUSD"

    assert summary["decision"] == "PAPER_EXECUTED"

    assert summary["processing_time_ms"] == 125.75

    print()

    print("Integration Report Test Passed")


if __name__ == "__main__":

    test_integration_report()