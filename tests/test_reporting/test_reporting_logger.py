"""
=================================================
Project Phoenix
Reporting Logger Test
=================================================
"""

from reporting.reporting_logger import ReportingLogger
from reporting.reporting_models import (
    ReportingResult,
    ReportingStatus,
)


def run_test():

    status = ReportingStatus(
        generated=True,
        analytics_completed=True,
        report_name="Monthly Report",
    )

    result = ReportingResult(

        approved=True,

        reason="Reporting completed successfully.",

        status=status,

        report={
            "total_trades": 100,
            "win_rate": 68.0,
            "net_profit": 12500.0,
            "profit_factor": 3.27,
        },

    )

    ReportingLogger.log(result)

    assert result.approved

    print()
    print("Reporting Logger Test Passed")


if __name__ == "__main__":

    run_test()