"""
=================================================
Project Phoenix
Broker Logger
=================================================

Broker logging utilities.
"""

from broker.broker_models import BrokerResult


class BrokerLogger:
    """
    Logs broker operations.
    """

    @staticmethod
    def log(result: BrokerResult):

        print("===== Broker =====")

        print(f"Approved      : {result.approved}")
        print(f"Reason        : {result.reason}")
        print()

        print(f"Broker        : {result.status.broker_name}")
        print(f"Connected     : {result.status.connected}")
        print(f"Logged In     : {result.status.logged_in}")