"""
=================================================
Project Phoenix
Operational Alert Adapter Tests
M62.6.3
=================================================
"""

from datetime import datetime, timezone

from alert_system.alert_models import (
    AlertMessage,
)

from deployment.operational_alert_adapter import (
    OperationalAlertAdapter,
)

from deployment.operational_incident_models import (
    OperationalIncident,
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


def _incident(
    event_type,
    severity,
    message="Operational event.",
):
    return OperationalIncident(
        incident_id="INC-200",
        event_type=event_type,
        severity=severity,
        message=message,
        timestamp=datetime(
            2026,
            8,
            15,
            12,
            30,
            0,
            tzinfo=timezone.utc,
        ),
        processing_cycle_id="CYCLE-200",
    )


# =================================================
# Basic Conversion
# =================================================


def test_incident_is_converted_to_alert_message():

    incident = _incident(
        OperationalIncidentEventType
        .HEALTH_DEGRADED,
        OperationalIncidentSeverity.WARNING,
        "Runtime health degraded.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert isinstance(
        alert,
        AlertMessage,
    )

    assert (
        alert.message
        == "Runtime health degraded."
    )

    assert (
        alert.alert_type
        == "HEALTH_DEGRADED"
    )


# =================================================
# Timestamp Preservation
# =================================================


def test_incident_timestamp_is_preserved():

    incident = _incident(
        OperationalIncidentEventType
        .RUNTIME_FAILURE,
        OperationalIncidentSeverity.CRITICAL,
        "Runtime execution failed.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.timestamp
        == "2026-08-15T12:30:00+00:00"
    )


# =================================================
# Severity in Title
# =================================================


def test_critical_incident_title_contains_severity():

    incident = _incident(
        OperationalIncidentEventType
        .RUNTIME_FAILURE,
        OperationalIncidentSeverity.CRITICAL,
        "Runtime execution failed.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "CRITICAL | "
            "RUNTIME_FAILURE"
        )
    )


def test_warning_incident_title_contains_severity():

    incident = _incident(
        OperationalIncidentEventType
        .HEALTH_DEGRADED,
        OperationalIncidentSeverity.WARNING,
        "Runtime health degraded.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "WARNING | "
            "HEALTH_DEGRADED"
        )
    )


def test_info_incident_title_contains_severity():

    incident = _incident(
        OperationalIncidentEventType
        .HEALTH_RECOVERED,
        OperationalIncidentSeverity.INFO,
        "Runtime health recovered.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "INFO | "
            "HEALTH_RECOVERED"
        )
    )


# =================================================
# Event Type Preservation
# =================================================


def test_configuration_failure_event_is_preserved():

    incident = _incident(
        OperationalIncidentEventType
        .CONFIGURATION_FAILURE,
        OperationalIncidentSeverity.CRITICAL,
        "Configuration readiness failed.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.alert_type
        == "CONFIGURATION_FAILURE"
    )


def test_protection_pause_event_is_preserved():

    incident = _incident(
        OperationalIncidentEventType
        .TRADING_PROTECTION_PAUSED,
        OperationalIncidentSeverity.WARNING,
        "Trading protection paused.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.alert_type
        == "TRADING_PROTECTION_PAUSED"
    )


def test_protection_recovery_event_is_preserved():

    incident = _incident(
        OperationalIncidentEventType
        .TRADING_PROTECTION_RECOVERED,
        OperationalIncidentSeverity.INFO,
        "Trading protection recovered.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.alert_type
        == "TRADING_PROTECTION_RECOVERED"
    )


# =================================================
# Message Preservation
# =================================================


def test_original_incident_message_is_not_modified():

    message = (
        "Runtime health recovered "
        "after watchdog transition."
    )

    incident = _incident(
        OperationalIncidentEventType
        .HEALTH_RECOVERED,
        OperationalIncidentSeverity.INFO,
        message,
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert (
        alert.message
        == message
    )


# =================================================
# Adapter Does Not Send
# =================================================


def test_adapter_only_creates_alert_message():

    incident = _incident(
        OperationalIncidentEventType
        .RUNTIME_SHUTDOWN,
        OperationalIncidentSeverity.INFO,
        "Runtime stopped.",
    )

    alert = (
        OperationalAlertAdapter
        .to_alert_message(
            incident
        )
    )

    assert isinstance(
        alert,
        AlertMessage,
    )

    assert (
        alert.alert_type
        == "RUNTIME_SHUTDOWN"
    )