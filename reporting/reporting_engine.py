"""
=================================================
Project Phoenix
Reporting Engine
=================================================

Master controller for the Reporting Layer.
"""

from reporting.analytics_engine import AnalyticsEngine
from reporting.report_generator import ReportGenerator
from reporting.reporting_logger import ReportingLogger
from reporting.reporting_models import (
    PerformanceAnalytics,
    ReportingResult,
    ReportingStatus,
    ReportSummary,
    TradeStatistics,
)


class ReportingEngine:
    """
    Executes the complete reporting workflow.
    """

    def __init__(self):

        self.analytics = AnalyticsEngine()

        self.generator = ReportGenerator()

    # -------------------------------------------------

    def run(self) -> ReportingResult:

        analytics_data = self.analytics.calculate(
            winning_trades=68,
            losing_trades=32,
            gross_profit=18000.0,
            gross_loss=5500.0,
        )

        summary = ReportSummary(
            report_name="Monthly Report",
            generated_at="2026-01-01",
            total_records=250,
        )

        statistics = TradeStatistics(
            total_trades=analytics_data["total_trades"],
            winning_trades=analytics_data["winning_trades"],
            losing_trades=analytics_data["losing_trades"],
            win_rate=analytics_data["win_rate"],
            loss_rate=analytics_data["loss_rate"],
        )

        performance = PerformanceAnalytics(
            net_profit=analytics_data["net_profit"],
            gross_profit=analytics_data["gross_profit"],
            gross_loss=analytics_data["gross_loss"],
            profit_factor=analytics_data["profit_factor"],
            expectancy=125.0,
            drawdown=4.5,
        )

        self.generator.generate(
            summary,
            statistics,
            performance,
        )

        status = ReportingStatus(
            generated=True,
            analytics_completed=True,
            report_name=summary.report_name,
        )

        result = ReportingResult(
            approved=True,
            reason="Reporting completed successfully.",
            status=status,
        )

        ReportingLogger.log(result)

        return result