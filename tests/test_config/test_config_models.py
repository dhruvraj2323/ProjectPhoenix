"""
Project Phoenix

Unit Test
Configuration Models
"""

from config.config_models import (
    ConfigurationContext,
    ConfigurationDecision,
    ConfigurationItem,
    ConfigurationStatus,
)


def test_config_models():

    item = ConfigurationItem(

        key="risk_percent",

        value=1.0,

        category="Risk",

        description="Maximum risk per trade.",

    )

    context = ConfigurationContext(

        application_name="Project Phoenix",

        version="1.0",

        environment="DEVELOPMENT",

        configuration={

            "risk_percent": 1.0,

        },

    )

    decision = ConfigurationDecision(

        status=ConfigurationStatus.APPROVED,

        items=[item],

        approved=True,

        reason="Configuration loaded successfully.",

    )

    assert item.key == "risk_percent"

    assert context.environment == "DEVELOPMENT"

    assert decision.approved is True

    print("Configuration Models Test Passed")


if __name__ == "__main__":

    test_config_models()