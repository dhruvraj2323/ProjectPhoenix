"""
=================================================
Project Phoenix
Dashboard Logger Test
=================================================
"""

from dashboard.dashboard_logger import DashboardLogger
from dashboard.dashboard_models import (
    DashboardStatus,
    DashboardResult,
)


def run_test():

    status = DashboardStatus(
        running=True,
        connected=True,
        refresh_rate=5,
    )

    result = DashboardResult(
        approved=True,
        reason="Dashboard initialized successfully.",
        status=status,
    )

    DashboardLogger.log(result)

    assert result.approved

    print()
    print("Dashboard Logger Test Passed")


if __name__ == "__main__":

    run_test()