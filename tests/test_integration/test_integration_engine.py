"""
=================================================
Project Phoenix
Integration Engine Test
=================================================
"""

from integration.integration_engine import (
    IntegrationEngine,
)


def run_test():

    engine = IntegrationEngine()

    result = engine.run()

    print()

    print("===== Integration Engine =====")

    print(f"Status   : {result.status}")
    print(f"Approved : {result.approved}")
    print(
        f"Reason   : {result.validation.reason}"
    )

    assert result.approved

    print()

    print("Integration Engine Test Passed")


if __name__ == "__main__":

    run_test()