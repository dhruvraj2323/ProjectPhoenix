"""
=================================================
Project Phoenix
Operational Incident Models Tests
M62.6.1
=================================================
"""

from datetime import datetime, timezone

import pytest

from deployment.operational_incident_models import (
    OperationalIncident,
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


def _timestamp():
    return datetime.now(
        timezone.utc
    )


# =================================================
# Event Type Tests
# =================================================


def test_event_types_are_defined():

    assert (
        OperationalIncidentEventType
        .CONFIGURATION_FAILURE.value
        == "CONFIGURATION_FAILURE"
    )

    assert (
        OperationalIncidentEventType
        .DEPLOYMENT_HEALTH_FAILURE.value
        == "DEPLOYMENT_HEALTH_FAILURE"
    )

    assert (
        OperationalIncidentEventType
        .RUNTIME_FAILURE.value
        == "RUNTIME_FAILURE"
    )

    assert (
        OperationalIncidentEventType
        .HEALTH_DEGRADED.value
        == "HEALTH_DEGRADED"
    )

    assert (
        OperationalIncidentEventType
        .HEALTH_RECOVERED.value
        == "HEALTH_RECOVERED"
    )


def test_protection_event_types_are_defined():

    assert (
        OperationalIncidentEventType
        .TRADING_PROTECTION_PAUSED.value
        == "TRADING_PROTECTION_PAUSED"
    )

    assert (
        OperationalIncidentEventType
        .TRADING_PROTECTION_RECOVERED.value
        == "TRADING_PROTECTION_RECOVERED"
    )


def test_runtime_shutdown_event_type_is_defined():

    assert (
        OperationalIncidentEventType
        .RUNTIME_SHUTDOWN.value
        == "RUNTIME_SHUTDOWN"
    )


# =================================================
# Severity Tests
# =================================================


def test_severity_levels_are_defined():

    assert (
        OperationalIncidentSeverity.INFO.value
        == "INFO"
    )

    assert (
        OperationalIncidentSeverity.WARNING.value
        == "WARNING"
    )

    assert (
        OperationalIncidentSeverity.CRITICAL.value
        == "CRITICAL"
    )


# =================================================
# Model Construction
# =================================================


def test_operational_incident_can_be_created():

    timestamp = _timestamp()

    incident = OperationalIncident(
        incident_id="INC-001",
        event_type=(
            OperationalIncidentEventType
            .HEALTH_DEGRADED
        ),
        severity=(
            OperationalIncidentSeverity.WARNING
        ),
        message=(
            "Runtime health degraded."
        ),
        timestamp=timestamp,
        processing_cycle_id="CYCLE-001",
    )

    assert (
        incident.incident_id
        == "INC-001"
    )

    assert (
        incident.event_type
        == OperationalIncidentEventType
        .HEALTH_DEGRADED
    )

    assert (
        incident.severity
        == OperationalIncidentSeverity
        .WARNING
    )

    assert (
        incident.message
        == "Runtime health degraded."
    )

    assert (
        incident.timestamp
        == timestamp
    )

    assert (
        incident.processing_cycle_id
        == "CYCLE-001"
    )


# =================================================
# Immutable Model
# =================================================


def test_operational_incident_is_immutable():

    incident = OperationalIncident(
        incident_id="INC-002",
        event_type=(
            OperationalIncidentEventType
            .RUNTIME_FAILURE
        ),
        severity=(
            OperationalIncidentSeverity.CRITICAL
        ),
        message="Runtime failed.",
        timestamp=_timestamp(),
    )

    with pytest.raises(
        AttributeError
    ):

        incident.message = (
            "Changed message."
        )


# =================================================
# Validation Tests
# =================================================


def test_empty_incident_id_is_rejected():

    with pytest.raises(
        ValueError,
        match="incident_id",
    ):

        OperationalIncident(
            incident_id="",
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_FAILURE
            ),
            severity=(
                OperationalIncidentSeverity.CRITICAL
            ),
            message="Runtime failed.",
            timestamp=_timestamp(),
        )


def test_empty_message_is_rejected():

    with pytest.raises(
        ValueError,
        match="message",
    ):

        OperationalIncident(
            incident_id="INC-003",
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_FAILURE
            ),
            severity=(
                OperationalIncidentSeverity.CRITICAL
            ),
            message="",
            timestamp=_timestamp(),
        )


def test_invalid_event_type_is_rejected():

    with pytest.raises(
        TypeError,
        match="event_type",
    ):

        OperationalIncident(
            incident_id="INC-004",
            event_type="RUNTIME_FAILURE",
            severity=(
                OperationalIncidentSeverity.CRITICAL
            ),
            message="Runtime failed.",
            timestamp=_timestamp(),
        )


def test_invalid_severity_is_rejected():

    with pytest.raises(
        TypeError,
        match="severity",
    ):

        OperationalIncident(
            incident_id="INC-005",
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_FAILURE
            ),
            severity="CRITICAL",
            message="Runtime failed.",
            timestamp=_timestamp(),
        )


def test_invalid_timestamp_is_rejected():

    with pytest.raises(
        TypeError,
        match="timestamp",
    ):

        OperationalIncident(
            incident_id="INC-006",
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_FAILURE
            ),
            severity=(
                OperationalIncidentSeverity.CRITICAL
            ),
            message="Runtime failed.",
            timestamp="2026-08-15",
        )


def test_processing_cycle_id_defaults_to_empty():

    incident = OperationalIncident(
        incident_id="INC-007",
        event_type=(
            OperationalIncidentEventType
            .HEALTH_RECOVERED
        ),
        severity=(
            OperationalIncidentSeverity.INFO
        ),
        message=(
            "Runtime health recovered."
        ),
        timestamp=_timestamp(),
    )

    assert (
        incident.processing_cycle_id
        == ""
    )