"""
=================================================
Project Phoenix
Operational Incident Classifier
M62.6.2 - Operational Incident Classifier
=================================================
"""

from __future__ import annotations

from datetime import datetime

from deployment.operational_incident_models import (
    OperationalIncident,
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


class OperationalIncidentClassifier:
    """
    Classifies runtime operational conditions into
    immutable OperationalIncident objects.

    Responsibilities:
    - Map operational events to standard event types
    - Assign standard severity
    - Create incident identifiers
    - Preserve timestamp and processing-cycle context

    This class does not:
    - send alerts
    - log alerts
    - modify Runtime state
    - modify TradingProtection
    - execute trades
    """

    @staticmethod
    def classify(
        event_type: OperationalIncidentEventType,
        message: str,
        timestamp: datetime,
        incident_id: str,
        processing_cycle_id: str = "",
    ) -> OperationalIncident:
        """
        Create an OperationalIncident using the
        standard severity associated with the event.
        """

        severity = (
            OperationalIncidentClassifier
            .severity_for(event_type)
        )

        return OperationalIncident(
            incident_id=incident_id,
            event_type=event_type,
            severity=severity,
            message=message,
            timestamp=timestamp,
            processing_cycle_id=(
                processing_cycle_id
            ),
        )

    @staticmethod
    def severity_for(
        event_type: OperationalIncidentEventType,
    ) -> OperationalIncidentSeverity:
        """
        Return the standard severity for an
        operational incident event.
        """

        if event_type in (
            OperationalIncidentEventType
            .CONFIGURATION_FAILURE,

            OperationalIncidentEventType
            .DEPLOYMENT_HEALTH_FAILURE,

            OperationalIncidentEventType
            .RUNTIME_FAILURE,
        ):
            return (
                OperationalIncidentSeverity.CRITICAL
            )

        if event_type in (
            OperationalIncidentEventType
            .HEALTH_DEGRADED,

            OperationalIncidentEventType
            .TRADING_PROTECTION_PAUSED,
        ):
            return (
                OperationalIncidentSeverity.WARNING
            )

        if event_type in (
            OperationalIncidentEventType
            .HEALTH_RECOVERED,

            OperationalIncidentEventType
            .TRADING_PROTECTION_RECOVERED,

            OperationalIncidentEventType
            .RUNTIME_SHUTDOWN,
        ):
            return (
                OperationalIncidentSeverity.INFO
            )

        raise ValueError(
            "Unsupported operational incident "
            "event type."
        )