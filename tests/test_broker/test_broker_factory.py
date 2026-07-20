"""
=================================================
Project Phoenix
Broker Factory Test
=================================================
"""

from broker.broker_factory import BrokerFactory


def run_test():

    broker = BrokerFactory.create("MT5")

    print("===== Broker Factory =====")

    print(f"Broker       : MT5")
    print(f"Connected    : {broker.connect()}")
    print(f"Login        : {broker.login()}")
    print(f"Balance      : {broker.balance()}")
    print(f"Symbols      : {broker.symbols()}")

    assert broker.connect()
    assert broker.login()
    assert broker.is_connected()

    print()
    print("Broker Factory Test Passed")


if __name__ == "__main__":

    run_test()