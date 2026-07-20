"""
=================================================
Project Phoenix
Dashboard Engine Test
=================================================
"""

from dashboard.dashboard_engine import DashboardEngine


def run_test():

    engine = DashboardEngine()

    result = engine.initialize()

    print()
    print("===== Dashboard Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Dashboard Engine Test Passed")


if __name__ == "__main__":

    run_test()