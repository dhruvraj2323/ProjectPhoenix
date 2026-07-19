"""
Project Phoenix

Unit Test
Configuration Engine
"""

from config.config_engine import (
    ConfigurationEngine,
)

from config.config_models import (
    ConfigurationContext,
)


def test_config_engine():

    context = ConfigurationContext(

        application_name="Project Phoenix",

        version="1.0",

        environment="DEVELOPMENT",

    )

    engine = ConfigurationEngine()

    decision = engine.run(
        context
    )

    print("\n===== Configuration Engine =====")

    print(
        f"Status   : {decision.status.value}"
    )

    print(
        f"Approved : {decision.approved}"
    )

    print(
        f"Reason   : {decision.reason}"
    )

    assert decision.approved is True

    print("\nConfiguration Engine Test Passed")


if __name__ == "__main__":

    test_config_engine()