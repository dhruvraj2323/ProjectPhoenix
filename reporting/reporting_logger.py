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

        print()

        print(
            f"Total Trades       : "
            f"{result.report['total_trades']}"
        )

        print(
            f"Win Rate           : "
            f"{result.report['win_rate']}%"
        )

        print(
            f"Net Profit         : "
            f"{result.report['net_profit']}"
        )

        print(
            f"Profit Factor      : "
            f"{result.report['profit_factor']}"
        )