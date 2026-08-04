"""
=================================================
Project Phoenix
Report Generator Test
M57
=================================================
"""

from reporting.report_generator import (
    ReportGenerator,
)
from reporting.reporting_models import (
    PerformanceSummary,
    TradeRecord,
)


def test_report_generator():

    trades = [

        TradeRecord(
            trade_id="TRD-001",
            symbol="EURUSD",
            direction="BUY",
            strategy="Breakout",
            pattern="Bull Flag",
            profit_loss=125.0,
            status="CLOSED",
        )

    ]

    summary = PerformanceSummary(

        total_trades=1,

        winning_trades=1,

        gross_profit=125.0,

        net_profit=125.0,
    )

    generator = ReportGenerator()

    report = generator.generate(

        trades,

        summary,
    )

    assert len(report.trades) == 1

    assert report.summary.total_trades == 1

    assert report.summary.net_profit == 125.0

    assert report.report_name.endswith(
        "_Trading_Report"
    )

    assert report.output_file.endswith(
        ".xlsx"
    )