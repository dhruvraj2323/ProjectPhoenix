"""
=================================================
Project Phoenix
Reporting Engine Test
=================================================
"""

from reporting.reporting_engine import ReportingEngine


def run_test():

    engine = ReportingEngine()

    result = engine.run()

    print()

    print("===== Reporting Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved
    assert result.status.generated
    assert result.status.analytics_completed

    print()

    print("Reporting Engine Test Passed")


if __name__ == "__main__":

    run_test()