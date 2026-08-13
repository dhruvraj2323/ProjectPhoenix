"""
=================================================
Project Phoenix
Deployment Engine Tests
M61.7.1 - Deployment Approval Gate
=================================================
"""

from unittest.mock import MagicMock

from deployment.deployment_engine import (
    DeploymentEngine,
)


# =========================================================
# Helper
# =========================================================

def _create_engine(
    runtime_started: bool,
    runtime_running: bool,
    healthy: bool,
) -> DeploymentEngine:

    engine = DeploymentEngine()

    engine.runtime = MagicMock()

    engine.runtime.start.return_value = (
        runtime_started
    )

    engine.runtime.status.return_value = (
        runtime_running
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

    engine.runtime.start.assert_called_once()

    engine.runtime.status.assert_called_once()

    engine.monitor.health_report.assert_called_once()


# =========================================================
# Test B
# Runtime Startup Failed
# =========================================================

def test_deployment_engine_runtime_start_failed():

    engine = _create_engine(
        runtime_started=False,
        runtime_running=False,
        healthy=True,
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


# =========================================================
# Test C
# Runtime Not Running
# =========================================================

def test_deployment_engine_runtime_not_running():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=False,
        healthy=True,
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


# =========================================================
# Test D
# Health Check Failed
# =========================================================

def test_deployment_engine_health_failed():

    engine = _create_engine(
        runtime_started=True,
        runtime_running=True,
        healthy=False,
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


# =========================================================
# Test E
# Runtime Failed + Health Failed
# =========================================================

def test_deployment_engine_runtime_and_health_failed():

    engine = _create_engine(
        runtime_started=False,
        runtime_running=False,
        healthy=False,
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