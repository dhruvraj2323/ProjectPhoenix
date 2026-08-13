"""
=================================================
Project Phoenix
Reporting Engine
M61.4 - Consolidated Cycle Reporting
=================================================
"""

from __future__ import annotations

from deployment.execution_summary import (
    CycleExecutionSummary,
)

from reporting.analytics_engine import (
    AnalyticsEngine,
)

from reporting.report_generator import (
    ReportGenerator,
)

from reporting.reporting_models import (
    DailyReport,
    TradeRecord,
)


class ReportingEngine:
    """
    Coordinates trading report generation.

    M61.4 responsibilities:
    - Calculate trading performance
    - Generate daily trading report
    - Pass cycle execution summary to
      the report generator
    - Preserve backward compatibility with
      ReportingEngine.run(trades)
    """

    def __init__(self) -> None:

        self.analytics = (
            AnalyticsEngine()
        )

        self.generator = (
            ReportGenerator()
        )

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    def run(
        self,
        trades: list[TradeRecord],
        execution_summary: (
            CycleExecutionSummary | None
        ) = None,
    ) -> DailyReport:
        """
        Generate a complete trading report.

        Parameters
        ----------
        trades:
            Individual executed trade records.

        execution_summary:
            Optional cycle-level execution summary.

        Returns
        -------
        DailyReport
            Generated trading report.
        """

        # --------------------------------------------------
        # Performance Analytics
        # --------------------------------------------------

        summary = (
            self.analytics.calculate(
                trades,
            )
        )

        # --------------------------------------------------
        # Report Generation
        # --------------------------------------------------

        report = (
            self.generator.generate(
                trades=trades,
                summary=summary,
                execution_summary=execution_summary,
            )
        )

        # --------------------------------------------------
        # Preserve Summary On Report
        # --------------------------------------------------

        report.execution_summary = (
            execution_summary
        )

        return report