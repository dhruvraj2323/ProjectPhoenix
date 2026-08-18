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
from reporting.daily_trade_ledger import (
    DailyTradeLedger,
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
    Post-M63 reporting reliability:
    - Persist executed trade records across repeated
      live/demo cycles for the same day.
    - De-duplicate trades by trade identity.
    - Calculate daily analytics from the complete
      accumulated trade set.
    """
    def __init__(self) -> None:
        self.analytics = (
            AnalyticsEngine()
        )
        self.generator = (
            ReportGenerator()
        )
        self.daily_trade_ledger = (
            DailyTradeLedger(
                self.generator.REPORT_DIRECTORY,
            )
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
            When supplied by the live/demo trading cycle,
            the current trades are merged into the persistent
            daily ledger before analytics/report generation.
            When omitted, the original in-memory behavior is
            preserved for compatibility with existing callers.
        Returns
        -------
        DailyReport
            Generated trading report.
        """
        # --------------------------------------------------
        # Persistent Daily Trade Collection
        # --------------------------------------------------
        #
        # Continuous/demo operation runs many cycles per day.
        # TradingCycle intentionally resets its in-memory
        # trade_records list at the start of every cycle.
        #
        # Persist the executed records here so later cycles
        # cannot replace earlier daily trades in the Excel
        # report.
        #
        if execution_summary is not None:
            # Keep the ledger synchronized with the
            # generator's current report directory.
            #
            # This also supports tests and controlled
            # deployments that redirect reporting.
            #
            self.daily_trade_ledger = (
                DailyTradeLedger(
                    self.generator.REPORT_DIRECTORY,
                )
            )
            trades = (
                self.daily_trade_ledger.merge(
                    trades=trades,
                )
            )
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
