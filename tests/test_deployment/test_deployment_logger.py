"""
=================================================
Project Phoenix
Deployment Logger Tests
M61.10.4 - Trading Protection Observability
=================================================
"""

from deployment.deployment_logger import (
    DeploymentLogger,
)

from deployment.deployment_models import (
    DeploymentStatus,
    DeploymentResult,
)

from deployment.deployment_health import (
    DeploymentHealthState,
)

from deployment.trading_protection import (
    TradingProtectionState,
)


# =========================================================
# Existing Logger Test
# =========================================================

def run_test():

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

    DeploymentLogger.log(
        result,
    )

    assert result.approved

    print()

    print(
        "Deployment Logger Test Passed"
    )


if __name__ == "__main__":

    run_test()


# =========================================================
# M61.10.1
# Test A
# Healthy State Logging
# =========================================================

def test_deployment_logger_logs_health_state(
    capsys,
):

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

    DeploymentLogger.log(
        result,
    )

    captured = capsys.readouterr()

    assert (
        "Health State    : HEALTHY"
        in captured.out
    )


# =========================================================
# M61.10.1
# Test B
# Unhealthy State Logging
# =========================================================

def test_deployment_logger_logs_unhealthy_state(
    capsys,
):

    status = DeploymentStatus(
        running=True,
        healthy=False,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=False,
        reason=(
            "Deployment rejected: "
            "health check failed."
        ),
        status=status,
        health_state=(
            DeploymentHealthState.UNHEALTHY
        ),
    )

    DeploymentLogger.log(
        result,
    )

    captured = capsys.readouterr()

    assert (
        "Health State    : UNHEALTHY"
        in captured.out
    )


# =========================================================
# M61.10.4
# Test C
# Active Protection State Logging
# =========================================================

def test_deployment_logger_logs_active_protection(
    capsys,
):

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

    DeploymentLogger.log(
        result,
    )

    captured = capsys.readouterr()

    assert (
        "Protection      : ACTIVE"
        in captured.out
    )


# =========================================================
# M61.10.4
# Test D
# Paused Protection State Logging
# =========================================================

def test_deployment_logger_logs_paused_protection(
    capsys,
):

    status = DeploymentStatus(
        running=True,
        healthy=False,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=False,
        reason=(
            "Deployment rejected: "
            "health check failed."
        ),
        status=status,
        health_state=(
            DeploymentHealthState.UNHEALTHY
        ),
        trading_protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    DeploymentLogger.log(
        result,
    )

    captured = capsys.readouterr()

    assert (
        "Protection      : PAUSED"
        in captured.out
    )