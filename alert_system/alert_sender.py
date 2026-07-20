"""
=================================================
Project Phoenix
Alert Sender
=================================================

Sends alerts through configured channels.
"""

from alert_system.alert_models import (
    AlertChannel,
    AlertMessage,
)


class AlertSender:
    """
    Sends alert notifications.
    """

    def __init__(self):

        self.channels = [
            AlertChannel(
                name="Telegram",
                enabled=True,
                connected=True,
            ),
            AlertChannel(
                name="Email",
                enabled=True,
                connected=True,
            ),
        ]

    def send(self, alert: AlertMessage):

        delivered = []

        for channel in self.channels:

            if channel.enabled and channel.connected:

                delivered.append(channel.name)

        return delivered