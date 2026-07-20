"""
=================================================
Project Phoenix
Deployment Engine Test
=================================================
"""

from deployment.deployment_engine import DeploymentEngine


def run_test():

    engine = DeploymentEngine()

    result = engine.initialize()

    print()
    print("===== Deployment Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Deployment Engine Test Passed")


if __name__ == "__main__":

    run_test()