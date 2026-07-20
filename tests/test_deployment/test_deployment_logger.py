"""
=================================================
Project Phoenix
Deployment Logger Test
=================================================
"""

from deployment.deployment_logger import DeploymentLogger
from deployment.deployment_models import (
    DeploymentStatus,
    DeploymentResult,
)


def run_test():

    status = DeploymentStatus(
        running=True,
        healthy=True,
        version="1.0",
        environment="Production",
    )

    result = DeploymentResult(
        approved=True,
        reason="Deployment initialized successfully.",
        status=status,
    )

    DeploymentLogger.log(result)

    assert result.approved

    print()
    print("Deployment Logger Test Passed")


if __name__ == "__main__":

    run_test()