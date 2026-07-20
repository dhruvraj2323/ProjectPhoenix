"""
=================================================
Project Phoenix
Scheduler Engine Test
=================================================
"""

from scheduler.scheduler_engine import SchedulerEngine


def run_test():

    engine = SchedulerEngine()

    result = engine.initialize()

    print()
    print("===== Scheduler Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Scheduler Engine Test Passed")


if __name__ == "__main__":

    run_test()