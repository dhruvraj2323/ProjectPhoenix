"""
=================================================
Project Phoenix
Reporting Logger
M57
=================================================
"""

from __future__ import annotations

import logging

from reporting.reporting_models import DailyReport


class ReportingLogger:
    """
    Logger for Reporting Engine.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "ReportingEngine",
        )

        if not self.logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
            )

            handler.setFormatter(
                formatter,
            )

            self.logger.addHandler(
                handler,
            )

            self.logger.setLevel(
                logging.INFO,
            )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def log_start(
        self,
        report: DailyReport,
    ) -> None:
        """
        Log report generation start.
        """

        self.logger.info(
            "Report generation started | Date=%s",
            report.report_date.strftime(
                "%Y-%m-%d",
            ),
        )

    # --------------------------------------------------
    # Finish
    # --------------------------------------------------

    def log_finish(
        self,
        report: DailyReport,
    ) -> None:
        """
        Log successful report generation.
        """

        self.logger.info(
            "Report generated successfully | Trades=%d | Net Profit=%.2f",
            report.summary.total_trades,
            report.summary.net_profit,
        )

    # --------------------------------------------------
    # Failure
    # --------------------------------------------------

    def log_failure(
        self,
        reason: str,
    ) -> None:
        """
        Log report generation failure.
        """

        self.logger.error(
            "Report generation failed | Reason=%s",
            reason,
        )