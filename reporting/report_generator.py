"""
=================================================
Project Phoenix
Report Generator
M57
=================================================
"""

from __future__ import annotations

from datetime import datetime

from reporting.reporting_models import (
    DailyReport,
    PerformanceSummary,
    TradeRecord,
)


class ReportGenerator:
    """
    Builds Daily Trading Reports.
    """

    def generate(
        self,
        trades: list[TradeRecord],
        summary: PerformanceSummary,
    ) -> DailyReport:
        """
        Generate complete daily report.
        """

        report = DailyReport()

        report.trades = trades

        report.summary = summary

        report.report_date = (
            datetime.utcnow()
        )

        report.generated_at = (
            datetime.utcnow()
        )

        report.report_name = (
            report.report_date.strftime(
                "%Y-%m-%d"
            )
            + "_Trading_Report"
        )

        report.output_file = (
            "reports/Daily/"
            + report.report_name
            + ".xlsx"
        )

        return report