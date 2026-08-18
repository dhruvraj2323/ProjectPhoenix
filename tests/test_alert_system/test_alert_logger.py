"""
=================================================
Project Phoenix
Alert Logger Tests
=================================================
"""

from alert_system.alert_logger import (
    AlertLogger,
)

from alert_system.alert_models import (
    AlertStatus,
    AlertResult,
)


def test_alert_logger(
    capsys,
):

    status = AlertStatus(
        running=True,
        alerts_sent=5,
        connected_channels=2,
    )

    result = AlertResult(
        approved=True,
        reason=(
            "Alert system initialized successfully."
        ),
        status=status,
        delivered_channels=[
            "Telegram",
            "Email",
        ],
    )

    AlertLogger.log(
        result
    )

    captured = capsys.readouterr()

    assert (
        "Alert System"
        in captured.out
    )

    assert (
        "Approved          : True"
        in captured.out
    )

    assert (
        "Alerts Sent       : 5"
        in captured.out
    )

    assert (
        "Connected Channels: 2"
        in captured.out
    )