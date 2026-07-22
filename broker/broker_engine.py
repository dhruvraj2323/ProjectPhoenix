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
    BrokerResult,
    BrokerStatus,
)


class BrokerEngine:
    """
    Master Broker Controller.
    """

    def __init__(self, broker_name: str):

        self.broker = BrokerFactory.create(broker_name)

    # -------------------------------------------------

    def initialize(self) -> BrokerResult:

        connected = self.broker.connect()

        logged_in = False

        if connected:
            logged_in = self.broker.login()

        status = BrokerStatus(
            connected=self.broker.is_connected(),
            logged_in=logged_in,
            broker_name=self.broker.__class__.__name__.replace(
                "Broker",
                "",
            ),
        )

        approved = (
            status.connected
            and status.logged_in
        )

        result = BrokerResult(
            approved=approved,
            reason=(
                "Broker initialization completed successfully."
                if approved
                else "Broker initialization failed."
            ),
            status=status,
        )

        BrokerLogger.log(result)

        return result

    # -------------------------------------------------

    def shutdown(self) -> None:

        if self.broker.is_connected():

            self.broker.logout()

            self.broker.disconnect()