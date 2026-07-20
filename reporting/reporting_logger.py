"""
=================================================
Project Phoenix
Reporting Logger
=================================================

Logs reporting engine results.
"""

from reporting.reporting_models import ReportingResult


class ReportingLogger:
    """
    Logs reporting operations.
    """

    @staticmethod
    def log(result: ReportingResult) -> None:

        print("===== Reporting =====")

        print(f"Approved            : {result.approved}")
        print(f"Reason              : {result.reason}")

        print()

        print(f"Generated           : {result.status.generated}")
        print(f"Analytics Completed : {result.status.analytics_completed}")
        print(f"Report Name         : {result.status.report_name}")