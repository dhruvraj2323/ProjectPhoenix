"""
=================================================
Project Phoenix
Deployment Engine Tests
M61.10.3 - Runtime Protection Observability
=================================================
"""

from unittest.mock import MagicMock

from deployment.deployment_engine import (
    DeploymentEngine,
)

from deployment.deployment_health import (
    DeploymentHealthState,
)

from deployment.trading_protection import (
    TradingProtectionState,
)


# =========================================================
# Helper
# =========================================================

def _create_engine(
    runtime_started: bool,
    runtime_running: bool,
    healthy: bool,
    protection_state=(
        TradingProtectionState.ACTIVE
    ),
) -> DeploymentEngine:

    engine = DeploymentEngine()

    engine.runtime = MagicMock()

    engine.runtime.start.return_value = (
        runtime_started
    )

    engine.runtime.status.return_value = (
        runtime_running
    )

    engine.runtime.trading_protection_state.return_value = (
        protection_state
    )

    engine.monitor = MagicMock()

    engine.monitor.health_report.return_value = {
        "cpu": 12.5,
        "memory": 245.7,
        "database": True,
        "broker": True,
        "scheduler": True,
        "healthy": healthy,
    }

    return engine


# =========================================================
# Test A
# Runtime Started + Healthy
# =========================================================

def test_deployment_engine_approved():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=True,
        protection_state=(
            TradingProtectionState.ACTIVE
        ),
    )

    result = (
        engine.initialize()
    )

    assert result.approved is True

    assert (
        result.reason
        == "Deployment initialized successfully."
    )

    assert result.status.running is True

    assert result.status.healthy is True

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.ACTIVE
    )

    engine.runtime.start.assert_called_once()

    engine.runtime.status.assert_called_once()

    engine.runtime.trading_protection_state.assert_called_once()

    engine.monitor.health_report.assert_called_once()

    engine.runtime.stop.assert_not_called()


# =========================================================
# Test B
# Runtime Startup Failed
# =========================================================

def test_deployment_engine_runtime_start_failed():

    engine = _create_engine(
        runtime_started=False,
        runtime_running=False,
        healthy=True,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert result.approved is False

    assert (
        result.reason
        == "Deployment rejected: "
        "runtime startup failed."
    )

    assert result.status.running is False

    assert result.status.healthy is True

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    engine.runtime.stop.assert_not_called()


# =========================================================
# Test C
# Runtime Not Running
# =========================================================

def test_deployment_engine_runtime_not_running():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=False,
        healthy=True,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert result.approved is False

    assert (
        result.reason
        == "Deployment rejected: "
        "runtime is not running."
    )

    assert result.status.running is False

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    engine.runtime.stop.assert_not_called()


# =========================================================
# Test D
# Health Check Failed
# =========================================================

def test_deployment_engine_health_failed():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=False,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert result.approved is False

    assert (
        result.reason
        == "Deployment rejected: "
        "health check failed."
    )

    assert result.status.running is True

    assert result.status.healthy is False

    assert (
        result.health_state
        == DeploymentHealthState.UNHEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    engine.runtime.trading_protection_state.assert_called_once()

    engine.runtime.stop.assert_called_once()


# =========================================================
# Test E
# Runtime Failed + Health Failed
# =========================================================

def test_deployment_engine_runtime_and_health_failed():

    engine = _create_engine(
        runtime_started=False,
        runtime_running=False,
        healthy=False,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert result.approved is False

    assert (
        result.reason
        == "Deployment rejected: "
        "runtime startup failed."
    )

    assert result.status.running is False

    assert result.status.healthy is False

    assert (
        result.health_state
        == DeploymentHealthState.UNHEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    engine.runtime.stop.assert_not_called()


# =========================================================
# Test F
# Shutdown
# =========================================================

def test_deployment_engine_shutdown():

    engine = DeploymentEngine()

    engine.runtime = MagicMock()

    result = (
        engine.shutdown()
    )

    assert result is True

    engine.runtime.stop.assert_called_once()


# =========================================================
# M61.9.2
# Test G
# Healthy Deployment Health State
# =========================================================

def test_deployment_engine_health_state_healthy():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=True,
    )

    result = (
        engine.health_state()
    )

    assert (
        result
        == DeploymentHealthState.HEALTHY
    )

    engine.monitor.health_report.assert_called_once()


# =========================================================
# M61.9.2
# Test H
# Unhealthy Deployment Health State
# =========================================================

def test_deployment_engine_health_state_unhealthy():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=False,
    )

    result = (
        engine.health_state()
    )

    assert (
        result
        == DeploymentHealthState.UNHEALTHY
    )

    engine.monitor.health_report.assert_called_once()


# =========================================================
# M61.9.4
# Test I
# Approved Deployment Carries Healthy State
# =========================================================

def test_deployment_engine_result_health_state_healthy():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=True,
    )

    result = (
        engine.initialize()
    )

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )


# =========================================================
# M61.9.4
# Test J
# Rejected Deployment Carries Unhealthy State
# =========================================================

def test_deployment_engine_result_health_state_unhealthy():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=False,
    )

    result = (
        engine.initialize()
    )

    assert (
        result.health_state
        == DeploymentHealthState.UNHEALTHY
    )


# =========================================================
# M61.10.3
# Test K
# Active Protection State Is Captured
# =========================================================

def test_deployment_engine_result_active_protection_state():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=True,
        protection_state=(
            TradingProtectionState.ACTIVE
        ),
    )

    result = (
        engine.initialize()
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# M61.10.3
# Test L
# Paused Protection State Is Captured
# =========================================================

def test_deployment_engine_result_paused_protection_state():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=False,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )