"""
=================================================
Project Phoenix
Alert Sender Test
=================================================
"""

from alert_system.alert_formatter import AlertFormatter
from alert_system.alert_sender import AlertSender


def run_test():

    sender = AlertSender()

    alert = AlertFormatter.trade_alert(
        symbol="EURUSD",
        direction="BUY",
        price=1.1065,
    )

    delivered = sender.send(alert)

    print("===== Alert Sender =====")

    print(f"Delivered To : {delivered}")

    assert len(delivered) == 2

    print()
    print("Alert Sender Test Passed")


if __name__ == "__main__":

    run_test()