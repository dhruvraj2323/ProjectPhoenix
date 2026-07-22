"""
=================================================
Project Phoenix
Alert Engine
=================================================

Master controller for Alert System.
"""

from alert_system.alert_formatter import AlertFormatter
from alert_system.alert_logger import AlertLogger
from alert_system.alert_models import (
    AlertStatus,
    AlertResult,
)
from alert_system.alert_sender import AlertSender


class AlertEngine:
    """
    Master controller for Alert System.
    """

    def __init__(self):

        self.sender = AlertSender()

    def initialize(self):

        alert = AlertFormatter.system_alert(
            "Project Phoenix Alert System Initialized."
        )

        delivered = self.sender.send(alert)

        status = AlertStatus(
            running=True,
            alerts_sent=1,
            connected_channels=len(delivered),
        )

        result = AlertResult(
            approved=True,
            reason="Alert system initialized successfully.",
            status=status,
            delivered_channels=delivered,
        )

        AlertLogger.log(result)

        return result

    def shutdown(self):
        """
        Shutdown Alert System.
        """

        return True