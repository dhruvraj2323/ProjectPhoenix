"""
=================================================
Project Phoenix
Operational Alert Adapter
M62.6.3 - Operational Alert Adapter
=================================================
"""

from __future__ import annotations

from deployment.operational_incident_models import (
    OperationalIncident,
)

from alert_system.alert_models import (
    AlertMessage,
)


class OperationalAlertAdapter:
    """
    Convert Project Phoenix operational incidents
    into the existing AlertMessage contract.

    Responsibilities:
    - Translate incident information into AlertMessage
    - Preserve incident severity
    - Preserve incident timestamp
    - Preserve operational event type

    This class does not:
    - send alerts
    - log alerts
    - modify Runtime
    - modify TradingProtection
    - execute trades
    """

    @staticmethod
    def to_alert_message(
        incident: OperationalIncident,
    ) -> AlertMessage:
        """
        Convert one OperationalIncident into an
        AlertMessage understood by the existing
        Alert System.
        """

        return AlertMessage(
            title=(
                OperationalAlertAdapter
                ._build_title(incident)
            ),
            message=incident.message,
            alert_type=(
                incident.event_type.value
            ),
            timestamp=(
                incident.timestamp.isoformat()
            ),
        )

    @staticmethod
    def _build_title(
        incident: OperationalIncident,
    ) -> str:
        """
        Build a stable operational alert title.

        Severity is included so the alert remains
        immediately understandable without exposing
        implementation details.
        """

        return (
            "Project Phoenix | "
            f"{incident.severity.value} | "
            f"{incident.event_type.value}"
        )