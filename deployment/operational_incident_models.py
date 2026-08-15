"""
=================================================
Project Phoenix
Operational Incident Models
M62.6.1 - Operational Incident Models
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# -------------------------------------------------
# Operational Incident Event Type
# -------------------------------------------------


class OperationalIncidentEventType(
    Enum
):
    """
    Standard operational incident event types.
    """

    CONFIGURATION_FAILURE = (
        "CONFIGURATION_FAILURE"
    )

    DEPLOYMENT_HEALTH_FAILURE = (
        "DEPLOYMENT_HEALTH_FAILURE"
    )

    RUNTIME_FAILURE = (
        "RUNTIME_FAILURE"
    )

    HEALTH_DEGRADED = (
        "HEALTH_DEGRADED"
    )

    HEALTH_RECOVERED = (
        "HEALTH_RECOVERED"
    )

    TRADING_PROTECTION_PAUSED = (
        "TRADING_PROTECTION_PAUSED"
    )

    TRADING_PROTECTION_RECOVERED = (
        "TRADING_PROTECTION_RECOVERED"
    )

    RUNTIME_SHUTDOWN = (
        "RUNTIME_SHUTDOWN"
    )


# -------------------------------------------------
# Operational Incident Severity
# -------------------------------------------------


class OperationalIncidentSeverity(
    Enum
):
    """
    Operational incident severity levels.
    """

    INFO = "INFO"

    WARNING = "WARNING"

    CRITICAL = "CRITICAL"


# -------------------------------------------------
# Operational Incident
# -------------------------------------------------


@dataclass(frozen=True, slots=True)
class OperationalIncident:
    """
    Immutable representation of one operational
    incident.

    This model represents the operational event
    itself. It does not send alerts and does not
    control runtime behavior.
    """

    incident_id: str

    event_type: (
        OperationalIncidentEventType
    )

    severity: (
        OperationalIncidentSeverity
    )

    message: str

    timestamp: datetime

    processing_cycle_id: str = ""

    def __post_init__(self) -> None:
        """
        Validate mandatory incident fields.
        """

        if not self.incident_id:
            raise ValueError(
                "incident_id must not be empty."
            )

        if not isinstance(
            self.event_type,
            OperationalIncidentEventType,
        ):
            raise TypeError(
                "event_type must be an "
                "OperationalIncidentEventType."
            )

        if not isinstance(
            self.severity,
            OperationalIncidentSeverity,
        ):
            raise TypeError(
                "severity must be an "
                "OperationalIncidentSeverity."
            )

        if not self.message:
            raise ValueError(
                "message must not be empty."
            )

        if not isinstance(
            self.timestamp,
            datetime,
        ):
            raise TypeError(
                "timestamp must be a datetime."
            )

        if not isinstance(
            self.processing_cycle_id,
            str,
        ):
            raise TypeError(
                "processing_cycle_id must be a string."
            )