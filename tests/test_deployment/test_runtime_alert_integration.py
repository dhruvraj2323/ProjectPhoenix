"""
=================================================
Project Phoenix
Runtime Alert Integration Tests
M62.6.5
=================================================
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.runtime import Runtime

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)

from deployment.trading_protection import (
    TradingProtection,
)


def _ready_configuration():

    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
    )


def _create_runtime():

    protection = TradingProtection()

    dispatcher = MagicMock()

    dispatcher.dispatch.return_value = [
        "Telegram",
    ]

    runtime = Runtime(
        interval=0,
        trading_protection=protection,
        configuration_readiness=(
            _ready_configuration()
        ),
        alert_dispatcher=dispatcher,
    )

    return (
        runtime,
        dispatcher,
        protection,
    )


# =================================================
# Dependency Injection
# =================================================


def test_runtime_accepts_alert_dispatcher():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert (
        runtime.alert_dispatcher
        is dispatcher
    )


# =================================================
# Configuration Failure
# =================================================


def test_configuration_failure_generates_alert():

    protection = TradingProtection()

    dispatcher = MagicMock()

    configuration = (
        ConfigurationReadinessResult(
            ready=False,
            environment_ready=False,
            mt5_ready=True,
            runtime_ready=False,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        trading_protection=protection,
        configuration_readiness=configuration,
        alert_dispatcher=dispatcher,
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "CONFIGURATION_FAILURE"
    )


# =================================================
# Deployment Health Failure
# =================================================


def test_deployment_health_failure_generates_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "DEPLOYMENT_HEALTH_FAILURE"
    )


# =================================================
# Runtime Failure
# =================================================


def test_runtime_execution_failure_generates_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    runtime.continuous_runner.start = (
        MagicMock(
            side_effect=RuntimeError(
                "Runner failure."
            )
        )
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "RUNTIME_FAILURE"
    )


# =================================================
# Watchdog Degradation
# =================================================


def test_watchdog_degradation_generates_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "HEALTH_DEGRADED"
    )


# =================================================
# Watchdog Recovery
# =================================================


def test_watchdog_recovery_generates_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=True
        )
    )

    runtime.check_watchdog()

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "HEALTH_RECOVERED"
    )


# =================================================
# Exactly One Degradation Alert
# =================================================


def test_repeated_unhealthy_state_generates_one_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()
    runtime.check_watchdog()
    runtime.check_watchdog()

    assert (
        dispatcher.dispatch.call_count
        == 1
    )


# =================================================
# Exactly One Recovery Alert
# =================================================


def test_repeated_healthy_state_generates_one_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=True
        )
    )

    runtime.check_watchdog()
    runtime.check_watchdog()
    runtime.check_watchdog()

    assert (
        dispatcher.dispatch.call_count
        == 1
    )


# =================================================
# Shutdown
# =================================================


def test_runtime_shutdown_generates_alert():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    dispatcher.dispatch.reset_mock()

    runtime.stop()

    dispatcher.dispatch.assert_called_once()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert (
        incident.event_type.value
        == "RUNTIME_SHUTDOWN"
    )


# =================================================
# Alert Failure Must Not Break Runtime
# =================================================


def test_alert_dispatch_failure_does_not_break_runtime():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    dispatcher.dispatch.side_effect = (
        RuntimeError(
            "Alert delivery failed."
        )
    )

    assert runtime.start(
        cycles=1,
    ) is True

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    result = runtime.check_watchdog()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )


# =================================================
# Incident Contains Timestamp
# =================================================


def test_runtime_alert_incident_contains_timestamp():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert isinstance(
        incident.timestamp,
        datetime,
    )


# =================================================
# Incident Contains Processing Context
# =================================================


def test_runtime_alert_incident_has_processing_cycle_field():

    runtime, dispatcher, protection = (
        _create_runtime()
    )

    assert runtime.start(
        cycles=1,
    ) is True

    dispatcher.dispatch.reset_mock()

    runtime.health_monitor.is_healthy = (
        MagicMock(
            return_value=False
        )
    )

    runtime.check_watchdog()

    incident = (
        dispatcher.dispatch.call_args.args[0]
    )

    assert isinstance(
        incident.processing_cycle_id,
        str,
    )