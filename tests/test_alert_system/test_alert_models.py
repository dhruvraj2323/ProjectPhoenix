"""
=================================================
Project Phoenix
Alert Models Test
=================================================
"""

from alert_system.alert_models import (
    AlertMessage,
    AlertChannel,
    AlertStatus,
    AlertResult,
)


def run_test():

    message = AlertMessage(
        title="BUY Signal",
        message="EURUSD BUY @ 1.1065",
        alert_type="TRADE",
        timestamp="2026-07-20 10:30:00",
    )

    channel = AlertChannel(
        name="Telegram",
        enabled=True,
        connected=True,
    )

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

    print("===== Alert Models =====")

    print(f"Title              : {message.title}")
    print(f"Alert Type         : {message.alert_type}")
    print(f"Channel            : {channel.name}")
    print(f"Alerts Sent        : {status.alerts_sent}")
    print(f"Connected Channels : {status.connected_channels}")

    assert result.approved

    print()
    print("Alert Models Test Passed")


if __name__ == "__main__":

    run_test()