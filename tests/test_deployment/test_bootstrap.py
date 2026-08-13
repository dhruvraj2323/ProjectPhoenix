"""
=================================================
Project Phoenix
Bootstrap Tests
M61.7.2 - Deployment Approval Integration
=================================================
"""

from unittest.mock import MagicMock

from deployment.bootstrap import (
    Bootstrap,
)

from deployment.deployment_models import (
    DeploymentResult,
    DeploymentStatus,
)


# =========================================================
# Helpers
# =========================================================

def _create_result(
    approved: bool,
    running: bool,
    healthy: bool,
    reason: str,
) -> DeploymentResult:

    status = DeploymentStatus(
        running=running,
        healthy=healthy,
        version="1.0",
        environment="Production",
    )

    return DeploymentResult(
        approved=approved,
        reason=reason,
        status=status,
        health_report={
            "healthy": healthy,
        },
    )


# =========================================================
# Test A
# Approved Deployment Starts Bootstrap
# =========================================================

def test_bootstrap_start_approved():

    engine = MagicMock()

    engine.initialize.return_value = (
        _create_result(
            approved=True,
            running=True,
            healthy=True,
            reason=(
                "Deployment initialized "
                "successfully."
            ),
        )
    )

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    assert bootstrap.started is False

    result = bootstrap.start()

    assert result is True

    assert bootstrap.started is True

    assert (
        bootstrap.deployment_result.approved
        is True
    )

    engine.initialize.assert_called_once()


# =========================================================
# Test B
# Rejected Deployment Blocks Bootstrap
# =========================================================

def test_bootstrap_start_rejected():

    engine = MagicMock()

    engine.initialize.return_value = (
        _create_result(
            approved=False,
            running=False,
            healthy=False,
            reason=(
                "Deployment rejected: "
                "health check failed."
            ),
        )
    )

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    result = bootstrap.start()

    assert result is False

    assert bootstrap.started is False

    assert (
        bootstrap.deployment_result.approved
        is False
    )

    engine.initialize.assert_called_once()


# =========================================================
# Test C
# Stop Approved Deployment
# =========================================================

def test_bootstrap_stop():

    engine = MagicMock()

    engine.initialize.return_value = (
        _create_result(
            approved=True,
            running=True,
            healthy=True,
            reason=(
                "Deployment initialized "
                "successfully."
            ),
        )
    )

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    bootstrap.start()

    result = bootstrap.stop()

    assert result is True

    assert bootstrap.started is False

    engine.shutdown.assert_called_once()


# =========================================================
# Test D
# Stop Before Successful Start
# =========================================================

def test_bootstrap_stop_before_start():

    engine = MagicMock()

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    result = bootstrap.stop()

    assert result is False

    engine.shutdown.assert_not_called()

    assert bootstrap.started is False


# =========================================================
# Test E
# Rejected Deployment Must Not Shutdown
# =========================================================

def test_bootstrap_rejected_deployment_no_shutdown():

    engine = MagicMock()

    engine.initialize.return_value = (
        _create_result(
            approved=False,
            running=False,
            healthy=False,
            reason=(
                "Deployment rejected: "
                "runtime startup failed."
            ),
        )
    )

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    assert (
        bootstrap.start()
        is False
    )

    assert (
        bootstrap.stop()
        is False
    )

    engine.shutdown.assert_not_called()


# =========================================================
# Test F
# Deployment Result Is Preserved
# =========================================================

def test_bootstrap_preserves_deployment_result():

    engine = MagicMock()

    result = _create_result(
        approved=True,
        running=True,
        healthy=True,
        reason=(
            "Deployment initialized "
            "successfully."
        ),
    )

    engine.initialize.return_value = result

    bootstrap = Bootstrap(
        deployment_engine=engine,
    )

    bootstrap.start()

    assert (
        bootstrap.deployment_result
        is result
    )