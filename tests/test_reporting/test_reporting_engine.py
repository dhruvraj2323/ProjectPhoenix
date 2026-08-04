"""
=================================================
Project Phoenix
Reporting Engine Test
M57
=================================================
"""

from reporting.reporting_engine import (
    ReportingEngine,
)
from reporting.reporting_models import (
    TradeRecord,
)


def test_reporting_engine():

    trades = [

        TradeRecord(
            trade_id="TRD-001",
            symbol="EURUSD",
            direction="BUY",
            strategy="Breakout",
            pattern="Bull Flag",
            profit_loss=150.0,
            status="CLOSED",
        ),

        TradeRecord(
            trade_id="TRD-002",
            symbol="EURUSD",
            direction="SELL",
            strategy="Reversal",
            pattern="Double Top",
            profit_loss=-50.0,
            status="CLOSED",
        ),

    ]

    engine = ReportingEngine()

    report = engine.run(
        trades,
    )

    assert report.summary.total_trades == 2

    assert report.summary.winning_trades == 1

    assert report.summary.losing_trades == 1

    assert report.summary.net_profit == 100.0

    assert len(report.trades) == 2

    assert report.output_file.endswith(
        ".xlsx"
    )