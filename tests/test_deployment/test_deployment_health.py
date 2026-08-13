"""
=================================================
Project Phoenix
Deployment Health Contract Tests
M61.9.1 - Deployment Health State Contract
=================================================
"""

from deployment.deployment_health import (
    DeploymentHealthState,
    health_state_from_report,
)


# =========================================================
# Test A
# Healthy Report
# =========================================================

def test_health_state_from_healthy_report():

    report = {
        "cpu": 12.5,
        "memory": 245.7,
        "database": True,
        "broker": True,
        "scheduler": True,
        "healthy": True,
    }

    result = (
        health_state_from_report(
            report,
        )
    )

    assert (
        result
        == DeploymentHealthState.HEALTHY
    )


# =========================================================
# Test B
# Unhealthy Report
# =========================================================

def test_health_state_from_unhealthy_report():

    report = {
        "cpu": 12.5,
        "memory": 245.7,
        "database": True,
        "broker": False,
        "scheduler": True,
        "healthy": False,
    }

    result = (
        health_state_from_report(
            report,
        )
    )

    assert (
        result
        == DeploymentHealthState.UNHEALTHY
    )


# =========================================================
# Test C
# Missing Health Field
# =========================================================

def test_health_state_from_missing_health_field():

    report = {
        "cpu": 12.5,
        "memory": 245.7,
        "database": True,
        "broker": True,
        "scheduler": True,
    }

    result = (
        health_state_from_report(
            report,
        )
    )

    assert (
        result
        == DeploymentHealthState.UNHEALTHY
    )


# =========================================================
# Test D
# Explicit False
# =========================================================

def test_health_state_from_false_health_field():

    report = {
        "healthy": False,
    }

    result = (
        health_state_from_report(
            report,
        )
    )

    assert (
        result
        == DeploymentHealthState.UNHEALTHY
    )