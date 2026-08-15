"""
=================================================
Project Phoenix
Operational Incident Classifier Tests
M62.6.2
=================================================
"""

from datetime import datetime, timezone

import pytest

from deployment.operational_incident_classifier import (
    OperationalIncidentClassifier,
)

from deployment.operational_incident_models import (
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


def _timestamp():
    return datetime.now(
        timezone.utc
    )


# =================================================
# Critical Event Classification
# =================================================


@pytest.mark.parametrize(
    "event_type",
    [
        OperationalIncidentEventType
        .CONFIGURATION_FAILURE,

        OperationalIncidentEventType
        .DEPLOYMENT_HEALTH_FAILURE,

        OperationalIncidentEventType
        .RUNTIME_FAILURE,
    ],
)
def test_critical_events_receive_critical_severity(
    event_type,
):

    severity = (
        OperationalIncidentClassifier
        .severity_for(event_type)
    )

    assert (
        severity
        == OperationalIncidentSeverity.CRITICAL
    )


# =================================================
# Warning Event Classification
# =================================================


@pytest.mark.parametrize(
    "event_type",
    [
        OperationalIncidentEventType
        .HEALTH_DEGRADED,

        OperationalIncidentEventType
        .TRADING_PROTECTION_PAUSED,
    ],
)
def test_warning_events_receive_warning_severity(
    event_type,
):

    severity = (
        OperationalIncidentClassifier
        .severity_for(event_type)
    )

    assert (
        severity
        == OperationalIncidentSeverity.WARNING
    )


# =================================================
# Informational Event Classification
# =================================================


@pytest.mark.parametrize(
    "event_type",
    [
        OperationalIncidentEventType
        .HEALTH_RECOVERED,

        OperationalIncidentEventType
        .TRADING_PROTECTION_RECOVERED,

        OperationalIncidentEventType
        .RUNTIME_SHUTDOWN,
    ],
)
def test_info_events_receive_info_severity(
    event_type,
):

    severity = (
        OperationalIncidentClassifier
        .severity_for(event_type)
    )

    assert (
        severity
        == OperationalIncidentSeverity.INFO
    )


# =================================================
# Incident Creation
# =================================================


def test_classifier_creates_operational_incident():

    timestamp = _timestamp()

    incident = (
        OperationalIncidentClassifier.classify(
            event_type=(
                OperationalIncidentEventType
                .HEALTH_DEGRADED
            ),
            message=(
                "Runtime health degraded."
            ),
            timestamp=timestamp,
            incident_id="INC-100",
            processing_cycle_id="CYCLE-100",
        )
    )

    assert (
        incident.incident_id
        == "INC-100"
    )

    assert (
        incident.event_type
        == OperationalIncidentEventType
        .HEALTH_DEGRADED
    )

    assert (
        incident.severity
        == OperationalIncidentSeverity.WARNING
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
        == "CYCLE-100"
    )


def test_classifier_preserves_critical_event():

    incident = (
        OperationalIncidentClassifier.classify(
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_FAILURE
            ),
            message=(
                "Runtime execution failed."
            ),
            timestamp=_timestamp(),
            incident_id="INC-101",
        )
    )

    assert (
        incident.severity
        == OperationalIncidentSeverity.CRITICAL
    )


def test_classifier_preserves_recovery_event():

    incident = (
        OperationalIncidentClassifier.classify(
            event_type=(
                OperationalIncidentEventType
                .HEALTH_RECOVERED
            ),
            message=(
                "Runtime health recovered."
            ),
            timestamp=_timestamp(),
            incident_id="INC-102",
        )
    )

    assert (
        incident.severity
        == OperationalIncidentSeverity.INFO
    )


# =================================================
# Processing Cycle
# =================================================


def test_processing_cycle_id_defaults_to_empty():

    incident = (
        OperationalIncidentClassifier.classify(
            event_type=(
                OperationalIncidentEventType
                .RUNTIME_SHUTDOWN
            ),
            message=(
                "Runtime stopped."
            ),
            timestamp=_timestamp(),
            incident_id="INC-103",
        )
    )

    assert (
        incident.processing_cycle_id
        == ""
    )


# =================================================
# Invalid Event Type
# =================================================


def test_invalid_event_type_is_rejected():

    with pytest.raises(
        ValueError,
        match="Unsupported",
    ):

        OperationalIncidentClassifier.severity_for(
            "INVALID_EVENT"
        )