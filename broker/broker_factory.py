"""
=================================================
Project Phoenix
Broker Factory
=================================================

Creates broker instances.
"""

from broker.broker_interface import BrokerInterface


class MT5Broker(BrokerInterface):
    """
    Dummy MT5 broker implementation.
    """

    def connect(self):
        return True

    def disconnect(self):
        return True

    def login(self):
        return True

    def logout(self):
        return True

    def account_info(self):
        return {}

    def positions(self):
        return []

    def orders(self):
        return []

    def place_order(self):
        return True

    def modify_order(self):
        return True

    def close_order(self):
        return True

    def cancel_order(self):
        return True

    def symbols(self):
        return ["EURUSD", "GBPUSD"]

    def balance(self):
        return 10000.0

    def is_connected(self):
        return True


class BrokerFactory:
    """
    Creates broker implementations.
    """

    @staticmethod
    def create(broker_name: str) -> BrokerInterface:

        broker_name = broker_name.upper()

        if broker_name == "MT5":
            return MT5Broker()

        raise ValueError(
            f"Unsupported broker: {broker_name}"
        )