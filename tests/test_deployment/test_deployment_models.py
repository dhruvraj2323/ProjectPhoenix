"""
=================================================
Project Phoenix
Deployment Models Test
=================================================
"""

from deployment.deployment_models import (
    DeploymentStatus,
    RuntimeStatus,
    DeploymentResult,
)


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
        reason="Deployment initialized successfully.",
        status=status,
    )

    print("===== Deployment Models =====")

    print(f"Version          : {status.version}")
    print(f"Environment      : {status.environment}")
    print(f"CPU Usage        : {runtime.cpu_usage}%")
    print(f"Memory Usage     : {runtime.memory_usage} MB")
    print(f"Threads          : {runtime.active_threads}")

    assert result.approved

    print()
    print("Deployment Models Test Passed")


if __name__ == "__main__":

    run_test()