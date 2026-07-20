"""
=================================================
Project Phoenix
Alert Formatter Test
=================================================
"""

from alert_system.alert_formatter import AlertFormatter


def run_test():

    trade = AlertFormatter.trade_alert(
        symbol="EURUSD",
        direction="BUY",
        price=1.1065,
    )

    risk = AlertFormatter.risk_alert(
        "Maximum daily loss reached."
    )

    system = AlertFormatter.system_alert(
        "Dashboard initialized."
    )

    print("===== Alert Formatter =====")

    print(f"Trade Alert   : {trade.message}")
    print(f"Risk Alert    : {risk.message}")
    print(f"System Alert  : {system.message}")

    assert trade.alert_type == "TRADE"
    assert risk.alert_type == "RISK"
    assert system.alert_type == "SYSTEM"

    print()
    print("Alert Formatter Test Passed")


if __name__ == "__main__":

    run_test()