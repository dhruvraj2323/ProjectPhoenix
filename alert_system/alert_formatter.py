"""
=================================================
Project Phoenix
Alert Formatter
=================================================

Formats alert messages.
"""

from alert_system.alert_models import AlertMessage


class AlertFormatter:
    """
    Creates standardized alert messages.
    """

    @staticmethod
    def trade_alert(
        symbol: str,
        direction: str,
        price: float,
    ):

        return AlertMessage(
            title=f"{direction} Signal",
            message=f"{symbol} {direction} @ {price}",
            alert_type="TRADE",
            timestamp="2026-07-20 10:30:00",
        )

    @staticmethod
    def risk_alert(message: str):

        return AlertMessage(
            title="Risk Alert",
            message=message,
            alert_type="RISK",
            timestamp="2026-07-20 10:30:00",
        )

    @staticmethod
    def system_alert(message: str):

        return AlertMessage(
            title="System Alert",
            message=message,
            alert_type="SYSTEM",
            timestamp="2026-07-20 10:30:00",
        )