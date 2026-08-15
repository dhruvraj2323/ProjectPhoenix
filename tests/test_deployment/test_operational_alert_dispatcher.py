"""
=================================================
Project Phoenix
Operational Alert Dispatcher Tests
M62.6.4
=================================================
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from alert_system.alert_models import (
    AlertMessage,
)

from deployment.operational_alert_dispatcher import (
    OperationalAlertDispatcher,
)

from deployment.operational_incident_models import (
    OperationalIncident,
    OperationalIncidentEventType,
    OperationalIncidentSeverity,
)


def _incident():

    return OperationalIncident(
        incident_id="INC-300",
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
        timestamp=datetime(
            2026,
            8,
            15,
            12,
            30,
            tzinfo=timezone.utc,
        ),
    )


def test_dispatcher_accepts_injected_sender():

    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
    ]

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    assert (
        dispatcher.sender
        is sender
    )


def test_dispatch_converts_incident_to_alert():

    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
    ]

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    result = dispatcher.dispatch(
        _incident()
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
        alert.alert_type
        == "HEALTH_DEGRADED"
    )


def test_dispatch_preserves_incident_message():

    sender = MagicMock()

    sender.send.return_value = []

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    dispatcher.dispatch(
        _incident()
    )

    alert = (
        sender.send.call_args.args[0]
    )

    assert (
        alert.message
        == "Runtime health degraded."
    )


def test_dispatch_returns_sender_result():

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

    result = dispatcher.dispatch(
        _incident()
    )

    assert (
        result
        == [
            "Telegram",
            "Email",
        ]
    )


def test_send_alert_accepts_existing_alert_message():

    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
    ]

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    alert = AlertMessage(
        title="Operational Alert",
        message="Runtime issue.",
        alert_type="RUNTIME_FAILURE",
        timestamp=(
            "2026-08-15T12:30:00+00:00"
        ),
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


def test_dispatch_does_not_modify_incident():

    sender = MagicMock()

    sender.send.return_value = []

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    incident = _incident()

    dispatcher.dispatch(
        incident
    )

    assert (
        incident.message
        == "Runtime health degraded."
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


def test_sender_failure_is_not_converted_to_success():

    sender = MagicMock()

    sender.send.return_value = []

    dispatcher = (
        OperationalAlertDispatcher(
            sender=sender,
        )
    )

    result = dispatcher.dispatch(
        _incident()
    )

    assert result == []

    sender.send.assert_called_once()