"""
=================================================
Project Phoenix
Health Monitor Test
=================================================
"""

from deployment.health_monitor import HealthMonitor


def run_test():

    monitor = HealthMonitor()

    report = monitor.health_report()

    print("===== Health Monitor =====")

    print(f"CPU Usage       : {report['cpu']}%")
    print(f"Memory Usage    : {report['memory']} MB")
    print(f"Database        : {report['database']}")
    print(f"Broker          : {report['broker']}")
    print(f"Scheduler       : {report['scheduler']}")
    print(f"Healthy         : {report['healthy']}")

    assert report["healthy"]

    print()
    print("Health Monitor Test Passed")


if __name__ == "__main__":

    run_test()