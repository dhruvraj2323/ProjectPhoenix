"""
=================================================
Project Phoenix
Alert Engine
M62.1.5 - Telegram-only Alert Integration
=================================================

Master controller for Alert System.
"""

from __future__ import annotations

from alert_system.alert_formatter import (
    AlertFormatter,
)

from alert_system.alert_logger import (
    AlertLogger,
)

from alert_system.alert_models import (
    AlertStatus,
    AlertResult,
)

from alert_system.alert_sender import (
    AlertSender,
)


class AlertEngine:
    """
    Master controller for Alert System.

    Telegram is the only supported alert channel.
    """

    def __init__(
        self,
        sender: AlertSender | None = None,
    ):
        """
        Initialize Alert Engine.

        An AlertSender can be injected for testing
        and controlled integration.
        """

        self.sender = (
            sender
            if sender is not None
            else AlertSender()
        )

    def initialize(self):
        """
        Initialize the Alert System.

        Sends the system initialization alert
        through the configured Telegram channel.
        """

        alert = AlertFormatter.system_alert(
            "Project Phoenix Alert System Initialized."
        )

        delivered = self.sender.send(
            alert
        )

        status = AlertStatus(
            running=True,
            alerts_sent=1,
            connected_channels=len(
                delivered
            ),
        )

        result = AlertResult(
            approved=True,
            reason=(
                "Alert system initialized "
                "successfully."
            ),
            status=status,
            delivered_channels=delivered,
        )

        AlertLogger.log(
            result
        )

        return result

    def shutdown(self):
        """
        Shutdown Alert System.
        """

        return True