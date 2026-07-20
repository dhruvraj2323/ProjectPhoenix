"""
=================================================
Project Phoenix
Broker Engine
=================================================

Master controller of Broker Layer.
"""

from broker.broker_factory import BrokerFactory
from broker.broker_logger import BrokerLogger
from broker.broker_models import (
    BrokerStatus,
    BrokerResult,
)


class BrokerEngine:
    """
    Master Broker Controller.
    """

    def __init__(self, broker_name: str):

        self.broker = BrokerFactory.create(broker_name)

    def initialize(self):

        connected = self.broker.connect()

        if connected:
            self.broker.login()

        status = BrokerStatus(
            connected=self.broker.is_connected(),
            logged_in=True,
            broker_name="MT5",
        )

        result = BrokerResult(
            approved=True,
            reason="Broker initialization completed successfully.",
            status=status,
        )

        BrokerLogger.log(result)

        return result