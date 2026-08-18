"""
=================================================
Project Phoenix
M62.8 - End-to-End Runtime / Trading Integration
=================================================

Purpose:
    Prove the operational runtime chain end-to-end without
    recreating existing modules.

Validated boundaries:
    Configuration -> Readiness -> Deployment -> Runtime
    -> TradingProtection -> TradingCycle -> Reporting
    -> Alerts / Degradation / Recovery -> Shutdown

This file intentionally uses controlled mocks at external
system boundaries. It does not connect to a live MT5 account.
"""

from unittest.mock import MagicMock

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.continuous_runner import ContinuousRunner
from deployment.execution_summary import (
    CycleExecutionStatus,
)
from deployment.runtime import Runtime
from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)
from deployment.runtime_watchdog import WatchdogHealthState
from deployment.trading_cycle import TradingCycle
from deployment.operational_incident_models import OperationalIncidentEventType


def _ready_configuration():
    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
    )


def _failed_configuration():
    return ConfigurationReadinessResult(
        ready=False,
        environment_ready=False,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        errors=("Environment configuration is not ready.",),
    )


def _runtime(
    configuration=None,
    healthy=True,
):
    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            configuration
            if configuration is not None
            else _ready_configuration()
        ),
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = healthy

    return runtime


def test_m62_8_startup_gate_blocks_trading_when_configuration_is_not_ready():
    runtime = _runtime(
        configuration=_failed_configuration(),
        healthy=True,
    )

    runtime.continuous_runner = MagicMock()

    result = runtime.start(cycles=1)

    assert result is False
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )
    runtime.continuous_runner.start.assert_not_called()


def test_m62_8_startup_gate_blocks_trading_when_deployment_health_fails():
    runtime = _runtime(
        configuration=_ready_configuration(),
        healthy=False,
    )

    runtime.continuous_runner = MagicMock()

    result = runtime.start(cycles=1)

    assert result is False
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )
    runtime.continuous_runner.start.assert_not_called()


def test_m62_8_runtime_to_runner_to_trading_cycle_chain():
    runtime = _runtime()

    runner = ContinuousRunner(
        interval=0,
        trading_protection=runtime.trading_protection,
    )

    cycle = MagicMock()
    cycle.execute.return_value = True
    cycle.execution_summary = MagicMock(
        status=CycleExecutionStatus.PARTIAL_SUCCESS,
    )

    runner.trading_cycle = cycle
    runtime.continuous_runner = runner

    result = runtime.start(cycles=1)

    assert result is True
    assert cycle.execute.call_count == 1
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_m62_8_trading_protection_pauses_new_trading():
    runtime = _runtime()

    runner = ContinuousRunner(
        interval=0,
        trading_protection=runtime.trading_protection,
    )

    cycle = MagicMock()
    cycle.execute.return_value = True
    cycle.execution_summary = MagicMock(
        status=CycleExecutionStatus.ALL_EXECUTED,
    )

    runner.trading_cycle = cycle

    runtime.trading_protection.can_trade = MagicMock(
        return_value=False
    )

    result = runner.run_once()

    assert result is True
    cycle.execute.assert_not_called()


def test_m62_8_all_failed_cycle_propagates_failure_to_runner():
    runtime = _runtime()

    runner = ContinuousRunner(
        interval=0,
        trading_protection=runtime.trading_protection,
    )

    cycle = MagicMock()
    cycle.execute.return_value = True
    cycle.execution_summary = MagicMock(
        status=CycleExecutionStatus.ALL_FAILED,
    )

    runner.trading_cycle = cycle

    result = runner.run_once()

    assert result is False
    cycle.execute.assert_called_once()


def test_m62_8_health_degradation_pauses_trading_and_changes_runtime_state():
    runtime = _runtime()

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is True
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    assert result is True
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.DEGRADED
    )


def test_m62_8_health_recovery_restores_runtime_operation():
    runtime = _runtime()

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is True

    runtime.apply_health_state(
        WatchdogHealthState.UNHEALTHY
    )

    result = runtime.apply_health_state(
        WatchdogHealthState.HEALTHY
    )

    assert result is True
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_m62_8_alert_dispatch_isolated_from_runtime_operation():
    dispatcher = MagicMock()
    dispatcher.dispatch.side_effect = RuntimeError(
        "simulated alert delivery failure"
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=_ready_configuration(),
        alert_dispatcher=dispatcher,
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = True
    runtime.continuous_runner = MagicMock()

    # Alert failure must not make the runtime startup call itself
    # fail; the dispatcher boundary is intentionally isolated.
    assert runtime.start(cycles=1) is True
    assert dispatcher.dispatch.call_count == 0

    runtime._emit_operational_alert(
        event_type=OperationalIncidentEventType.RUNTIME_FAILURE,
        message="M62.8 alert isolation test",
    )

    assert dispatcher.dispatch.call_count == 1
    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_m62_8_trading_cycle_reporting_boundary():
    cycle = TradingCycle()

    context = MagicMock()
    context.execution_result = MagicMock(
        accepted=True,
    )
    context.symbol = "XAUUSDm"

    trade_record = MagicMock()
    trade_record.symbol = "XAUUSDm"
    trade_record.trade_id = "M62.8-XAU-001"

    cycle.pipeline_context = context
    cycle.trade_record_mapper = MagicMock()
    cycle.trade_record_mapper.map.return_value = trade_record

    assert cycle._collect_execution_record() is True

    assert len(cycle.trade_records) == 1
    assert cycle.trade_records[0] is trade_record

    cycle.execution_summary = MagicMock(
        total_symbols=1,
        executed_symbols=1,
        no_trade_symbols=0,
        failed_symbols=0,
    )

    cycle.reporting_engine = MagicMock()
    cycle.daily_report = MagicMock()
    cycle.reporting_engine.run.return_value = cycle.daily_report

    cycle._generate_consolidated_report()

    cycle.reporting_engine.run.assert_called_once()
    assert cycle.daily_report is not None


def test_m62_8_shutdown_boundary_always_stops_runtime():
    runtime = _runtime()

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is True

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )
    runtime.continuous_runner.stop.assert_called_once()
    assert runtime.running is False
