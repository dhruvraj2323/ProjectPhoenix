"""
Project Phoenix

Unit Test
Configuration Logger
"""

from config.config_loader import (
    ConfigurationLoader,
)

from config.config_logger import (
    ConfigurationLogger,
)

from config.config_models import (
    ConfigurationContext,
    ConfigurationDecision,
    ConfigurationStatus,
)

from config.config_validator import (
    ConfigurationValidator,
)


def test_config_logger():

    context = ConfigurationContext(

        application_name="Project Phoenix",

        version="1.0",

        environment="DEVELOPMENT",

    )

    items = ConfigurationLoader().load(
        context
    )

    validation = (
        ConfigurationValidator()
        .validate(items)
    )

    decision = ConfigurationDecision(

        status=(
            ConfigurationStatus.APPROVED
            if validation.valid
            else ConfigurationStatus.REJECTED
        ),

        items=items,

        approved=validation.valid,

        reason=validation.reason,

    )

    logger = ConfigurationLogger()

    logger.log(
        context,
        decision,
    )

    print("\nConfiguration Logger Test Passed")


if __name__ == "__main__":

    test_config_logger()