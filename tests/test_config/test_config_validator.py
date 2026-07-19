"""
Project Phoenix

Unit Test
Configuration Validator
"""

from config.config_loader import (
    ConfigurationLoader,
)

from config.config_models import (
    ConfigurationContext,
)

from config.config_validator import (
    ConfigurationValidator,
)


def test_config_validator():

    context = ConfigurationContext(

        application_name="Project Phoenix",

        version="1.0",

        environment="DEVELOPMENT",

    )

    items = ConfigurationLoader().load(
        context
    )

    result = ConfigurationValidator().validate(
        items
    )

    print("===== Configuration Validator =====")

    print(
        f"Valid  : {result.valid}"
    )

    print(
        f"Reason : {result.reason}"
    )

    assert result.valid is True

    print("\nConfiguration Validator Test Passed")


if __name__ == "__main__":

    test_config_validator()