"""
Project Phoenix

Unit Test
Configuration Loader
"""

from config.config_loader import (
    ConfigurationLoader,
)

from config.config_models import (
    ConfigurationContext,
)


def test_config_loader():

    context = ConfigurationContext(

        application_name="Project Phoenix",

        version="1.0",

        environment="DEVELOPMENT",

    )

    loader = ConfigurationLoader()

    items = loader.load(
        context
    )

    print("===== Configuration Loader =====")

    for item in items:

        print(

            f"{item.category:<12}"

            f"{item.key:<20}"

            f"{item.value}"

        )

    assert len(items) == 8

    print("\nConfiguration Loader Test Passed")


if __name__ == "__main__":

    test_config_loader()