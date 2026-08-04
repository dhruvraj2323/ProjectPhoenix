"""
=================================================
Project Phoenix
Reporting Logger Test
M57
=================================================
"""

from reporting.reporting_logger import (
    ReportingLogger,
)
from reporting.reporting_models import (
    DailyReport,
)


def test_reporting_logger():

    logger = ReportingLogger()

    report = DailyReport()

    report.summary.total_trades = 5

    report.summary.net_profit = 250.75

    logger.log_start(report)

    logger.log_finish(report)

    logger.log_failure(
        "Sample failure.",
    )

    assert True