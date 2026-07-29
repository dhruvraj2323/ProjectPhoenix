"""
=================================================
Project Phoenix
Integration Logger Test
=================================================
"""

from trading_system.integration_logger import (
    IntegrationLogger,
)


def test_integration_logger():

    logger = IntegrationLogger()

    logger.info(

        "TradingCoordinator",

        "Trading started.",

    )

    logger.warning(

        "RiskEngine",

        "High exposure detected.",

    )

    logger.error(

        "ExecutionEngine",

        "Order rejected.",

    )

    assert logger.count() == 3

    latest = logger.latest()

    assert latest is not None

    assert latest.level == "ERROR"

    assert latest.component == "ExecutionEngine"

    logger.clear()

    assert logger.count() == 0

    print()

    print("Integration Logger Test Passed")


if __name__ == "__main__":

    test_integration_logger()