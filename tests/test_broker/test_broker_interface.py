"""
=================================================
Project Phoenix
Broker Interface Test
=================================================
"""

from broker.broker_interface import BrokerInterface


class DummyBroker(BrokerInterface):

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
        return ["EURUSD"]

    def balance(self):
        return 10000.0

    def is_connected(self):
        return True


def run_test():

    broker = DummyBroker()

    print("===== Broker Interface =====")

    print(f"Connect        : {broker.connect()}")
    print(f"Login          : {broker.login()}")
    print(f"Connected      : {broker.is_connected()}")
    print(f"Balance        : {broker.balance()}")
    print(f"Symbols        : {broker.symbols()}")

    assert broker.connect()
    assert broker.login()
    assert broker.is_connected()

    print()
    print("Broker Interface Test Passed")


if __name__ == "__main__":

    run_test()