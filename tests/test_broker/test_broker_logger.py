"""
=================================================
Project Phoenix
Broker Logger Test
=================================================
"""

from broker.broker_logger import BrokerLogger
from broker.broker_models import (
    BrokerStatus,
    BrokerResult,
)


def run_test():

    status = BrokerStatus(
        connected=True,
        logged_in=True,
        broker_name="MT5",
    )

    result = BrokerResult(
        approved=True,
        reason="Broker initialized successfully.",
        status=status,
    )

    BrokerLogger.log(result)

    assert result.approved

    print()
    print("Broker Logger Test Passed")


if __name__ == "__main__":

    run_test()