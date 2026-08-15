"""
=================================================
Project Phoenix
Operational Alert Dispatcher
M62.6.4 - Operational Alert Dispatcher
=================================================
"""

from __future__ import annotations

from deployment.operational_alert_adapter import (
    OperationalAlertAdapter,
)

from deployment.operational_incident_models import (
    OperationalIncident,
)

from alert_system.alert_models import (
    AlertMessage,
)

from alert_system.alert_sender import (
    AlertSender,
)


class OperationalAlertDispatcher:
    """
    Dispatch operational incidents through the
    existing AlertSender boundary.

    Responsibilities:
    - Convert OperationalIncident to AlertMessage
    - Send the resulting AlertMessage
    - Return delivery information

    This class does not:
    - modify Runtime
    - modify TradingProtection
    - execute trades
    - create duplicate notification systems
    """

    def __init__(
        self,
        sender: AlertSender | None = None,
    ) -> None:

        self.sender = (
            sender
            if sender is not None
            else AlertSender()
        )

    def dispatch(
        self,
        incident: OperationalIncident,
    ) -> list[str]:
        """
        Convert and dispatch one operational incident.

        Returns:
            List of successfully delivered channels.
        """

        alert = (
            OperationalAlertAdapter
            .to_alert_message(
                incident
            )
        )

        return self.send_alert(
            alert
        )

    def send_alert(
        self,
        alert: AlertMessage,
    ) -> list[str]:
        """
        Send an already constructed AlertMessage
        through the existing AlertSender.
        """

        return self.sender.send(
            alert
        )