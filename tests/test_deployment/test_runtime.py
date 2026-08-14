"""
=================================================
Project Phoenix
Runtime Tests
M61.6.2 - Deployment Readiness Gate
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime import (
    Runtime,
)


# =========================================================
# Test A
# Healthy Runtime Starts
# =========================================================

def test_runtime_start():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is True

    assert (
        runtime.health_monitor.is_healthy.call_count
        == 1
    )

    runtime.continuous_runner.start.assert_called_once_with(
        cycles=1,
    )

    assert runtime.running is True


# =========================================================
# Test B
# Unhealthy Runtime Is Blocked
# =========================================================

def test_runtime_start_blocked_when_unhealthy():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    assert (
        runtime.health_monitor.is_healthy.call_count
        == 1
    )

    runtime.continuous_runner.start.assert_not_called()

    assert runtime.running is False


# =========================================================
# Test C
# Readiness Helper
# =========================================================

def test_runtime_is_ready():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    assert (
        runtime.is_ready()
        is True
    )

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    assert (
        runtime.is_ready()
        is False
    )


# =========================================================
# Test D
# Stop Runtime
# =========================================================

def test_runtime_stop():

    runtime = Runtime(
        interval=0,
    )

    runtime.running = True

    runtime.continuous_runner = (
        MagicMock()
    )

    runtime.stop()

    assert runtime.running is False

    runtime.continuous_runner.stop.assert_called_once()


# =========================================================
# Test E
# Runner Exception Still Resets Runtime State
# =========================================================

def test_runtime_runner_exception_resets_state():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = (
        MagicMock()
    )

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = (
        MagicMock()
    )

    runtime.continuous_runner.start.side_effect = (
        RuntimeError(
            "Simulated runner failure."
        )
    )

    try:

        runtime.start(
            cycles=1,
        )

    except RuntimeError:

        pass

    assert runtime.running is False

# =========================================================
# M61.8.5
# Test F
# Runtime Passes Trading Protection
# =========================================================

def test_runtime_passes_trading_protection():

    from deployment.trading_protection import (
        TradingProtection,
    )

    protection = TradingProtection()

    runtime = Runtime(
        interval=0,
        trading_protection=protection,
    )

    assert (
        runtime.trading_protection
        is protection
    )

    assert (
        runtime.continuous_runner.trading_protection
        is protection
    )

# =========================================================
# M62.3.2
# Test G
# Configuration Readiness Allows Startup
# =========================================================

def test_runtime_start_when_configuration_is_ready():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            ConfigurationReadinessResult(
                ready=True,
                environment_ready=True,
                mt5_ready=True,
                runtime_ready=True,
                secrets_safe=True,
            )
        ),
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = MagicMock()

    result = runtime.start(
        cycles=1,
    )

    assert result is True

    runtime.health_monitor.is_healthy.assert_called_once()

    runtime.continuous_runner.start.assert_called_once_with(
        cycles=1,
    )

    assert runtime.running is True


# =========================================================
# M62.3.2
# Test H
# Configuration Readiness Blocks Startup
# =========================================================

def test_runtime_start_blocked_when_configuration_is_not_ready():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            ConfigurationReadinessResult(
                ready=False,
                environment_ready=False,
                mt5_ready=True,
                runtime_ready=True,
                secrets_safe=True,
                errors=(
                    "Environment configuration is not ready.",
                ),
            )
        ),
    )

    runtime.health_monitor = MagicMock()
    runtime.continuous_runner = MagicMock()

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    runtime.health_monitor.is_healthy.assert_not_called()

    runtime.continuous_runner.start.assert_not_called()

    assert runtime.running is False


# =========================================================
# M62.3.2
# Test I
# Configuration Ready But Health Unhealthy
# =========================================================

def test_runtime_start_blocked_when_health_is_unhealthy():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=(
            ConfigurationReadinessResult(
                ready=True,
                environment_ready=True,
                mt5_ready=True,
                runtime_ready=True,
                secrets_safe=True,
            )
        ),
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        False
    )

    runtime.continuous_runner = MagicMock()

    result = runtime.start(
        cycles=1,
    )

    assert result is False

    runtime.health_monitor.is_healthy.assert_called_once()

    runtime.continuous_runner.start.assert_not_called()

    assert runtime.running is False


# =========================================================
# M62.3.2
# Test J
# Both Readiness Gates Must Pass
# =========================================================

def test_runtime_requires_configuration_and_health():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    runtime.continuous_runner = MagicMock()

    assert (
        runtime.is_ready()
        is True
    )

    result = runtime.start(
        cycles=1,
    )

    assert result is True


# =========================================================
# M62.3.2
# Test K
# Missing Configuration Result Preserves Existing Contract
# =========================================================

def test_runtime_without_configuration_result_preserves_health_gate():

    runtime = Runtime(
        interval=0,
    )

    runtime.health_monitor = MagicMock()

    runtime.health_monitor.is_healthy.return_value = (
        True
    )

    assert (
        runtime.configuration_is_ready()
        is True
    )

    assert (
        runtime.is_ready()
        is True
    )


# =========================================================
# M62.3.2
# Test L
# Configuration Readiness Does Not Grant Live Approval
# =========================================================

def test_configuration_readiness_does_not_grant_live_approval():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    assert not hasattr(
        runtime,
        "live_approved",
    )

    assert not hasattr(
        configuration,
        "live_approved",
    )

# =========================================================
# M62.3.3.3
# Runtime Operational State Integration
# =========================================================

def test_runtime_initial_state_is_stopped():

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    runtime = Runtime(
        interval=0,
    )

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


def test_runtime_enters_running_state_after_start():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = True

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is True

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.RUNNING
    )


def test_configuration_failure_sets_failed_state():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=False,
            environment_ready=False,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )


def test_health_failure_sets_failed_state():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = False

    runtime.continuous_runner = MagicMock()

    assert runtime.start(cycles=1) is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )


def test_runner_failure_sets_failed_state():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = True

    runtime.continuous_runner = MagicMock()

    runtime.continuous_runner.start.side_effect = (
        RuntimeError("Simulated runner failure.")
    )

    assert runtime.start(cycles=1) is False

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.FAILED
    )


def test_runtime_stop_reaches_stopped_state():

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    runtime = Runtime(
        interval=0,
    )

    runtime.running = True
    runtime.continuous_runner = MagicMock()

    runtime.stop()

    assert (
        runtime.operational_state().state
        == RuntimeOperationalState.STOPPED
    )


def test_ready_state_is_observable_before_runner_start():

    from config.configuration_readiness_models import (
        ConfigurationReadinessResult,
    )

    from deployment.runtime_operational_state import (
        RuntimeOperationalState,
    )

    configuration = (
        ConfigurationReadinessResult(
            ready=True,
            environment_ready=True,
            mt5_ready=True,
            runtime_ready=True,
            secrets_safe=True,
        )
    )

    runtime = Runtime(
        interval=0,
        configuration_readiness=configuration,
    )

    runtime.health_monitor = MagicMock()
    runtime.health_monitor.is_healthy.return_value = True

    runtime.continuous_runner = MagicMock()

    original_start = (
        runtime.continuous_runner.start
    )

    def inspect_before_start(*args, **kwargs):
        assert (
            runtime.operational_state().state
            == RuntimeOperationalState.READY
        )

    runtime.continuous_runner.start.side_effect = (
        inspect_before_start
    )

    assert runtime.start(cycles=1) is True