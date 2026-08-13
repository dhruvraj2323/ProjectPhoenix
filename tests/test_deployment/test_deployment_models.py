"""
=================================================
Project Phoenix
Deployment Models Tests
M61.10.2 - Runtime Protection Observability
=================================================
"""

from deployment.deployment_models import (
    DeploymentStatus,
    RuntimeStatus,
    DeploymentResult,
)

from deployment.deployment_health import (
    DeploymentHealthState,
)

from deployment.trading_protection import (
    TradingProtectionState,
)


# =========================================================
# Existing Model Test
# =========================================================

def run_test():

    status = DeploymentStatus(
        running=True,
        healthy=True,
        version="1.0",
        environment="Production",
    )

    runtime = RuntimeStatus(
        uptime="00:10:15",
        cpu_usage=12.5,
        memory_usage=245.7,
        active_threads=8,
    )

    result = DeploymentResult(
        approved=True,
        reason=(
            "Deployment initialized successfully."
        ),
        status=status,
    )

    assert (
        result.health_state
        == DeploymentHealthState.UNHEALTHY
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )

    print(
        "===== Deployment Models ====="
    )

    print(
        f"Version          : "
        f"{status.version}"
    )

    print(
        f"Environment      : "
        f"{status.environment}"
    )

    print(
        f"CPU Usage        : "
        f"{runtime.cpu_usage}%"
    )

    print(
        f"Memory Usage     : "
        f"{runtime.memory_usage} MB"
    )

    print(
        f"Threads          : "
        f"{runtime.active_threads}"
    )

    assert result.approved

    print()

    print(
        "Deployment Models Test Passed"
    )


if __name__ == "__main__":

    run_test()


# =========================================================
# M61.9.3
# Test A
# Explicit Healthy State
# =========================================================

def test_deployment_result_health_state():

    status = DeploymentStatus(
        running=True,
        healthy=True,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=True,
        reason=(
            "Deployment initialized successfully."
        ),
        status=status,
        health_state=(
            DeploymentHealthState.HEALTHY
        ),
    )

    assert (
        result.health_state
        == DeploymentHealthState.HEALTHY
    )


# =========================================================
# M61.10.2
# Test B
# Default Protection State Is Paused
# =========================================================

def test_deployment_result_default_protection_state():

    status = DeploymentStatus(
        running=True,
        healthy=True,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=True,
        reason=(
            "Deployment initialized successfully."
        ),
        status=status,
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.PAUSED
    )


# =========================================================
# M61.10.2
# Test C
# Explicit Active Protection State
# =========================================================

def test_deployment_result_active_protection_state():

    status = DeploymentStatus(
        running=True,
        healthy=True,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=True,
        reason=(
            "Deployment initialized successfully."
        ),
        status=status,
        health_state=(
            DeploymentHealthState.HEALTHY
        ),
        trading_protection_state=(
            TradingProtectionState.ACTIVE
        ),
    )

    assert (
        result.trading_protection_state
        == TradingProtectionState.ACTIVE
    )