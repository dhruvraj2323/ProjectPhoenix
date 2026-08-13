"""
=================================================
Project Phoenix
Deployment Health Contract
M61.9.1 - Deployment Health State Contract
=================================================
"""

from __future__ import annotations

from enum import Enum


class DeploymentHealthState(Enum):
    """
    Deployment-level health state.

    HEALTHY
        Deployment health permits normal operation.

    UNHEALTHY
        Deployment health does not permit normal
        operation.
    """

    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


def health_state_from_report(
    report: dict,
) -> DeploymentHealthState:
    """
    Convert a deployment health report into the
    explicit DeploymentHealthState contract.
    """

    if report.get("healthy") is True:

        return DeploymentHealthState.HEALTHY

    return DeploymentHealthState.UNHEALTHY