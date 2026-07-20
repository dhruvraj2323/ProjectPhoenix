"""
=================================================
Project Phoenix
Dashboard Logger
=================================================

Logs dashboard events.
"""

from dashboard.dashboard_models import DashboardResult


class DashboardLogger:
    """
    Dashboard logging.
    """

    @staticmethod
    def log(result: DashboardResult):

        print("===== Dashboard =====")

        print(f"Approved      : {result.approved}")
        print(f"Reason        : {result.reason}")
        print()

        print(f"Running       : {result.status.running}")
        print(f"Connected     : {result.status.connected}")
        print(f"Refresh Rate  : {result.status.refresh_rate}")