"""
=================================================
Project Phoenix
Operational Alert Lifecycle Tests
M62.6.6 - End-to-End Operational Alert Lifecycle
=================================================
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from alert_system.alert_models import (
    AlertMessage,
)

from deployment.operational_alert_dispatcher import (
    OperationalAlertDispatcher,
)

from deployment.operational_alert_adapter import (
    OperationalAlertAdapter,
)

from deployment.operational_incident_classifier import (
    OperationalIncidentClassifier,
)

from deployment.operational_incident_models import (
    OperationalIncident,
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


def _timestamp():
    return datetime(
        2026,
        8,
        15,
        12,
        30,
        0,
        tzinfo=timezone.utc,
    )


def _create_incident(
    event_type,
    message,
    incident_id="INC-600",
    processing_cycle_id="CYCLE-600",
):
    return (
        OperationalIncidentClassifier.classify(
            event_type=event_type,
            message=message,
            timestamp=_timestamp(),
            incident_id=incident_id,
            processing_cycle_id=(
                processing_cycle_id
            ),
        )
    )


def _create_dispatcher():
    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
    ]

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    return (
        dispatcher,
        sender,
    )


# =================================================
# Complete Lifecycle
# =================================================


def test_critical_incident_completes_full_alert_lifecycle():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .RUNTIME_FAILURE,
        "Runtime execution failed.",
    )

    result = dispatcher.dispatch(
        incident
    )

    assert (
        result
        == ["Telegram"]
    )

    sender.send.assert_called_once()

    alert = (
        sender.send.call_args.args[0]
    )

    assert isinstance(
        alert,
        AlertMessage,
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "CRITICAL | "
            "RUNTIME_FAILURE"
        )
    )

    assert (
        alert.message
        == "Runtime execution failed."
    )

    assert (
        alert.alert_type
        == "RUNTIME_FAILURE"
    )

    assert (
        alert.timestamp
        == "2026-08-15T12:30:00+00:00"
    )


def test_warning_incident_completes_full_alert_lifecycle():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .HEALTH_DEGRADED,
        "Runtime health degraded.",
    )

    result = dispatcher.dispatch(
        incident
    )

    assert (
        result
        == ["Telegram"]
    )

    sender.send.assert_called_once()

    alert = (
        sender.send.call_args.args[0]
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "WARNING | "
            "HEALTH_DEGRADED"
        )
    )

    assert (
        alert.message
        == "Runtime health degraded."
    )

    assert (
        alert.alert_type
        == "HEALTH_DEGRADED"
    )


def test_recovery_incident_completes_full_alert_lifecycle():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .HEALTH_RECOVERED,
        "Runtime health recovered.",
    )

    result = dispatcher.dispatch(
        incident
    )

    assert (
        result
        == ["Telegram"]
    )

    sender.send.assert_called_once()

    alert = (
        sender.send.call_args.args[0]
    )

    assert (
        alert.title
        == (
            "Project Phoenix | "
            "INFO | "
            "HEALTH_RECOVERED"
        )
    )

    assert (
        alert.message
        == "Runtime health recovered."
    )

    assert (
        alert.alert_type
        == "HEALTH_RECOVERED"
    )


# =================================================
# Incident Metadata Preservation
# =================================================


def test_full_lifecycle_preserves_incident_metadata():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .DEPLOYMENT_HEALTH_FAILURE,
        "Deployment health check failed.",
        incident_id="INC-601",
        processing_cycle_id="CYCLE-601",
    )

    dispatcher.dispatch(
        incident
    )

    alert = (
        sender.send.call_args.args[0]
    )

    assert (
        incident.incident_id
        == "INC-601"
    )

    assert (
        incident.processing_cycle_id
        == "CYCLE-601"
    )

    assert (
        alert.alert_type
        == "DEPLOYMENT_HEALTH_FAILURE"
    )

    assert (
        alert.message
        == "Deployment health check failed."
    )

    assert (
        alert.timestamp
        == "2026-08-15T12:30:00+00:00"
    )


# =================================================
# Adapter + Dispatcher Boundary
# =================================================


def test_adapter_output_can_be_sent_directly_by_dispatcher():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .CONFIGURATION_FAILURE,
        "Configuration readiness failed.",
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

    result = dispatcher.send_alert(
        alert
    )

    assert (
        result
        == ["Telegram"]
    )

    sender.send.assert_called_once_with(
        alert
    )


# =================================================
# Multiple Independent Incidents
# =================================================


def test_multiple_incidents_generate_independent_alerts():

    dispatcher, sender = (
        _create_dispatcher()
    )

    first_incident = _create_incident(
        OperationalIncidentEventType
        .HEALTH_DEGRADED,
        "Runtime health degraded.",
        incident_id="INC-602",
        processing_cycle_id="CYCLE-602",
    )

    second_incident = _create_incident(
        OperationalIncidentEventType
        .HEALTH_RECOVERED,
        "Runtime health recovered.",
        incident_id="INC-603",
        processing_cycle_id="CYCLE-603",
    )

    first_result = dispatcher.dispatch(
        first_incident
    )

    second_result = dispatcher.dispatch(
        second_incident
    )

    assert (
        first_result
        == ["Telegram"]
    )

    assert (
        second_result
        == ["Telegram"]
    )

    assert (
        sender.send.call_count
        == 2
    )

    first_alert = (
        sender.send.call_args_list[0]
        .args[0]
    )

    second_alert = (
        sender.send.call_args_list[1]
        .args[0]
    )

    assert (
        first_alert.alert_type
        == "HEALTH_DEGRADED"
    )

    assert (
        second_alert.alert_type
        == "HEALTH_RECOVERED"
    )

    assert (
        first_alert.message
        != second_alert.message
    )


# =================================================
# No Duplicate Delivery
# =================================================


def test_one_dispatch_produces_exactly_one_sender_call():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .RUNTIME_SHUTDOWN,
        "Runtime stopped.",
    )

    dispatcher.dispatch(
        incident
    )

    assert (
        sender.send.call_count
        == 1
    )


# =================================================
# Incident Is Not Modified
# =================================================


def test_dispatch_does_not_modify_incident():

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .TRADING_PROTECTION_PAUSED,
        "Trading protection paused.",
    )

    original_id = (
        incident.incident_id
    )

    original_event_type = (
        incident.event_type
    )

    original_severity = (
        incident.severity
    )

    original_message = (
        incident.message
    )

    original_timestamp = (
        incident.timestamp
    )

    original_cycle = (
        incident.processing_cycle_id
    )

    dispatcher.dispatch(
        incident
    )

    assert (
        incident.incident_id
        == original_id
    )

    assert (
        incident.event_type
        == original_event_type
    )

    assert (
        incident.severity
        == original_severity
    )

    assert (
        incident.message
        == original_message
    )

    assert (
        incident.timestamp
        == original_timestamp
    )

    assert (
        incident.processing_cycle_id
        == original_cycle
    )


# =================================================
# Delivery Result Preservation
# =================================================


def test_multiple_delivery_channels_are_preserved():

    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
        "Email",
    ]

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .RUNTIME_FAILURE,
        "Runtime execution failed.",
    )

    result = dispatcher.dispatch(
        incident
    )

    assert (
        result
        == [
            "Telegram",
            "Email",
        ]
    )

    sender.send.assert_called_once()


# =================================================
# Sender Failure Isolation
# =================================================


def test_sender_failure_does_not_create_false_delivery():

    sender = MagicMock()

    sender.send.return_value = []

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    incident = _create_incident(
        OperationalIncidentEventType
        .RUNTIME_FAILURE,
        "Runtime execution failed.",
    )

    result = dispatcher.dispatch(
        incident
    )

    assert result == []

    sender.send.assert_called_once()


# =================================================
# Severity Contract
# =================================================


@pytest.mark.parametrize(
    "event_type, expected_severity",
    [
        (
            OperationalIncidentEventType
            .CONFIGURATION_FAILURE,
            OperationalIncidentSeverity.CRITICAL,
        ),
        (
            OperationalIncidentEventType
            .DEPLOYMENT_HEALTH_FAILURE,
            OperationalIncidentSeverity.CRITICAL,
        ),
        (
            OperationalIncidentEventType
            .RUNTIME_FAILURE,
            OperationalIncidentSeverity.CRITICAL,
        ),
        (
            OperationalIncidentEventType
            .HEALTH_DEGRADED,
            OperationalIncidentSeverity.WARNING,
        ),
        (
            OperationalIncidentEventType
            .HEALTH_RECOVERED,
            OperationalIncidentSeverity.INFO,
        ),
        (
            OperationalIncidentEventType
            .RUNTIME_SHUTDOWN,
            OperationalIncidentSeverity.INFO,
        ),
    ],
)
def test_complete_lifecycle_preserves_standard_severity(
    event_type,
    expected_severity,
):

    dispatcher, sender = (
        _create_dispatcher()
    )

    incident = _create_incident(
        event_type,
        "Operational event.",
    )

    assert (
        incident.severity
        == expected_severity
    )

    dispatcher.dispatch(
        incident
    )

    alert = (
        sender.send.call_args.args[0]
    )

    assert (
        expected_severity.value
        in alert.title
    )