"""
=================================================
Project Phoenix
Deployment Logger
=================================================

Logs deployment events.
"""

from deployment.deployment_models import DeploymentResult


class DeploymentLogger:
    """
    Deployment logging.
    """

    @staticmethod
    def log(result: DeploymentResult):

        print("===== Deployment =====")

        print(f"Approved        : {result.approved}")
        print(f"Reason          : {result.reason}")
        print()

        print(f"Running         : {result.status.running}")
        print(f"Healthy         : {result.status.healthy}")
        print(f"Version         : {result.status.version}")
        print(f"Environment     : {result.status.environment}")