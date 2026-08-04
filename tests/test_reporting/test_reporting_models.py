"""
=================================================
Project Phoenix
Reporting Models Test
M57
=================================================
"""

from reporting.reporting_models import (
    DailyReport,
    PerformanceSummary,
    TradeRecord,
)


def test_reporting_models():

    trade = TradeRecord(
        trade_id="TRD-001",
        symbol="EURUSD",
        direction="BUY",
        strategy="Breakout",
        pattern="Bull Flag",
        entry_price=1.1050,
        exit_price=1.1080,
        volume=0.10,
        profit_loss=30.0,
        status="CLOSED",
    )

    summary = PerformanceSummary(
        total_trades=1,
        winning_trades=1,
        gross_profit=30.0,
        net_profit=30.0,
    )

    report = DailyReport()

    report.trades.append(trade)

    report.summary = summary

    report.report_name = "Trading Report"

    assert report.trades[0].trade_id == "TRD-001"

    assert report.summary.total_trades == 1

    assert report.summary.net_profit == 30.0

    assert report.report_name == "Trading Report"