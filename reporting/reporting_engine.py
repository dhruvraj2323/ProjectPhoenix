"""
=================================================
Project Phoenix
Reporting Engine
M57
=================================================
"""

from __future__ import annotations

from reporting.analytics_engine import (
    AnalyticsEngine,
)
from reporting.report_generator import (
    ReportGenerator,
)
from reporting.reporting_logger import (
    ReportingLogger,
)
from reporting.reporting_models import (
    DailyReport,
    TradeRecord,
)


class ReportingEngine:
    """
    Executes the complete
    Reporting workflow.
    """

    def __init__(
        self,
    ) -> None:

        self.analytics = (
            AnalyticsEngine()
        )

        self.generator = (
            ReportGenerator()
        )

        self.logger = (
            ReportingLogger()
        )

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    def run(
        self,
        trades: list[TradeRecord],
    ) -> DailyReport:
        """
        Execute complete
        reporting workflow.
        """

        # Create temporary report
        report = DailyReport()

        self.logger.log_start(
            report,
        )

        summary = (
            self.analytics.calculate(
                trades,
            )
        )

        report = (
            self.generator.generate(
                trades,
                summary,
            )
        )

        self.logger.log_finish(
            report,
        )

        return report