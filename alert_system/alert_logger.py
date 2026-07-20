"""
=================================================
Project Phoenix
Alert Logger
=================================================

Logs alert operations.
"""

from alert_system.alert_models import AlertResult


class AlertLogger:
    """
    Logs alert activity.
    """

    @staticmethod
    def log(result: AlertResult):

        print("===== Alert System =====")

        print(f"Approved          : {result.approved}")
        print(f"Reason            : {result.reason}")
        print()

        print(f"Running           : {result.status.running}")
        print(f"Alerts Sent       : {result.status.alerts_sent}")
        print(f"Connected Channels: {result.status.connected_channels}")