"""
=================================================
Project Phoenix
Dashboard Engine
=================================================

Master controller for Dashboard.
"""

from dashboard.dashboard_logger import DashboardLogger
from dashboard.dashboard_models import (
    DashboardStatus,
    DashboardResult,
)
from dashboard.dashboard_renderer import DashboardRenderer


class DashboardEngine:
    """
    Master Dashboard Controller.
    """

    def __init__(self):

        self.renderer = DashboardRenderer()

    def initialize(self):

        self.renderer.render()

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

        return result