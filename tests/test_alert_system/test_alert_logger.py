"""
=================================================
Project Phoenix
Alert Logger Test
=================================================
"""

from alert_system.alert_logger import AlertLogger
from alert_system.alert_models import (
    AlertStatus,
    AlertResult,
)


def run_test():

    status = AlertStatus(
        running=True,
        alerts_sent=5,
        connected_channels=2,
    )

    result = AlertResult(
        approved=True,
        reason="Alert system initialized successfully.",
        status=status,
    )

    AlertLogger.log(result)

    assert result.approved

    print()
    print("Alert Logger Test Passed")


if __name__ == "__main__":

    run_test()