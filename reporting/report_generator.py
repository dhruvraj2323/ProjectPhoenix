"""
=================================================
Project Phoenix
Report Generator
=================================================

Generates structured trading reports.
"""

from reporting.reporting_models import (
    PerformanceAnalytics,
    ReportSummary,
    TradeStatistics,
)


class ReportGenerator:
    """
    Generates reporting summaries.
    """

    def generate(
        self,
        summary: ReportSummary,
        statistics: TradeStatistics,
        analytics: PerformanceAnalytics,
    ):

        return {
            "report_name": summary.report_name,
            "generated_at": summary.generated_at,
            "total_records": summary.total_records,
            "total_trades": statistics.total_trades,
            "winning_trades": statistics.winning_trades,
            "losing_trades": statistics.losing_trades,
            "win_rate": statistics.win_rate,
            "net_profit": analytics.net_profit,
            "profit_factor": analytics.profit_factor,
            "drawdown": analytics.drawdown,
        }