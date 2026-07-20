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
    )

    ReportingLogger.log(result)

    assert result.approved

    print()
    print("Reporting Logger Test Passed")


if __name__ == "__main__":

    run_test()