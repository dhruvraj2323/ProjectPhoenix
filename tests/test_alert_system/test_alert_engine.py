"""
=================================================
Project Phoenix
Alert Engine Test
=================================================
"""

from alert_system.alert_engine import AlertEngine


def run_test():

    engine = AlertEngine()

    result = engine.initialize()

    print()
    print("===== Alert Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Alert Engine Test Passed")


if __name__ == "__main__":

    run_test()