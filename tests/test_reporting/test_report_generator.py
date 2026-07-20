"""
=================================================
Project Phoenix
Report Generator Test
=================================================
"""

from reporting.report_generator import ReportGenerator
from reporting.reporting_models import (
    PerformanceAnalytics,
    ReportSummary,
    TradeStatistics,
)


def run_test():

    summary = ReportSummary(
        report_name="Monthly Report",
        generated_at="2026-01-01",
        total_records=250,
    )

    statistics = TradeStatistics(
        total_trades=100,
        winning_trades=68,
        losing_trades=32,
        win_rate=68.0,
        loss_rate=32.0,
    )

    analytics = PerformanceAnalytics(
        net_profit=12500.0,
        gross_profit=18000.0,
        gross_loss=5500.0,
        profit_factor=3.27,
        expectancy=125.0,
        drawdown=4.5,
    )

    generator = ReportGenerator()

    report = generator.generate(
        summary,
        statistics,
        analytics,
    )

    print("===== Report Generator =====")

    print(f"Report Name   : {report['report_name']}")
    print(f"Trades        : {report['total_trades']}")
    print(f"Win Rate      : {report['win_rate']}")
    print(f"Net Profit    : {report['net_profit']}")
    print(f"Profit Factor : {report['profit_factor']}")

    assert report["report_name"] == "Monthly Report"
    assert report["total_trades"] == 100
    assert report["net_profit"] == 12500.0

    print()
    print("Report Generator Test Passed")


if __name__ == "__main__":

    run_test()