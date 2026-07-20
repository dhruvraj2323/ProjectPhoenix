"""
=================================================
Project Phoenix
Reporting Models Test
=================================================
"""

from reporting.reporting_models import (
    EquityCurve,
    MonthlyStatistics,
    PerformanceAnalytics,
    ReportingResult,
    ReportingStatus,
    ReportSummary,
    TradeStatistics,
)


def run_test():

    summary = ReportSummary(
        report_name="Monthly Report",
        generated_at="2026-01-01 10:00",
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

    equity = EquityCurve(
        starting_balance=100000.0,
        current_balance=112500.0,
        highest_balance=114000.0,
    )

    monthly = MonthlyStatistics(
        month="January",
        trades=45,
        profit=3500.0,
        win_rate=70.0,
    )

    status = ReportingStatus(
        generated=True,
        analytics_completed=True,
        report_name="Monthly Report",
    )

    result = ReportingResult(
        approved=True,
        reason="Reporting completed successfully.",
        status=status,
    )

    assert summary.total_records == 250
    assert statistics.total_trades == 100
    assert analytics.net_profit == 12500.0
    assert equity.current_balance == 112500.0
    assert monthly.month == "January"
    assert result.approved

    print("===== Reporting Models =====")
    print(f"Report Name      : {summary.report_name}")
    print(f"Total Trades     : {statistics.total_trades}")
    print(f"Net Profit       : {analytics.net_profit}")
    print(f"Current Balance  : {equity.current_balance}")
    print(f"Month            : {monthly.month}")

    print()
    print("Reporting Models Test Passed")


if __name__ == "__main__":

    run_test()