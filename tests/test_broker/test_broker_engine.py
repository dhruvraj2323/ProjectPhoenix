"""
=================================================
Project Phoenix
Broker Engine Test
=================================================
"""

from broker.broker_engine import BrokerEngine


def run_test():

    engine = BrokerEngine("MT5")

    result = engine.initialize()

    print()
    print("===== Broker Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Broker Engine Test Passed")


if __name__ == "__main__":

    run_test()