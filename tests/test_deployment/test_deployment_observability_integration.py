"""
=================================================
Project Phoenix
Deployment Observability Integration Tests
M61.10.5 - End-to-End Deployment Observability
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
    healthy: bool,
    protection_state: TradingProtectionState,
):

    engine = DeploymentEngine()

    engine.runtime = MagicMock()

    engine.runtime.start.return_value = True

    engine.runtime.status.return_value = True

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
# Healthy Deployment Full State
# =========================================================

def test_healthy_deployment_full_observability():

    engine = _create_engine(
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
        result.health_state
        == DeploymentHealthState.HEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.ACTIVE
    )

    assert result.status.running is True

    assert result.status.healthy is True

    assert (
        result.health_report["healthy"]
        is True
    )

    engine.runtime.stop.assert_not_called()


# =========================================================
# Test B
# Unhealthy Deployment Full State
# =========================================================

def test_unhealthy_deployment_full_observability():

    engine = _create_engine(
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
        result.health_state
        == DeploymentHealthState.UNHEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    assert result.status.running is True

    assert result.status.healthy is False

    assert (
        result.health_report["healthy"]
        is False
    )

    engine.runtime.stop.assert_called_once()


# =========================================================
# Test C
# Healthy State and Protection State Are Independent
# =========================================================

def test_health_and_protection_states_are_explicit():

    engine = _create_engine(
        healthy=True,
        protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = (
        engine.initialize()
    )

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    assert result.approved is True

    engine.runtime.stop.assert_not_called()