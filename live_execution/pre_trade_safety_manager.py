"""
=================================================
Project Phoenix
Pre Trade Safety Manager
M59.4.6
=================================================
"""

from __future__ import annotations

from live_execution.connection_health_checker import (
    ConnectionHealthChecker,
)

from live_execution.demo_account_guard import (
    DemoAccountGuard,
)

from live_execution.market_status_validator import (
    MarketStatusValidator,
)

from live_execution.volume_validator import (
    VolumeValidator,
)

from live_execution.price_validator import (
    PriceValidator,
)


class PreTradeSafetyManager:
    """
    Executes all pre-trade
    safety validations.
    """

    def __init__(
        self,
    ) -> None:

        self.connection = (
            ConnectionHealthChecker()
        )

        self.demo_guard = (
            DemoAccountGuard()
        )

        self.market = (
            MarketStatusValidator()
        )

        self.volume = (
            VolumeValidator()
        )

        self.price = (
            PriceValidator()
        )

    def validate(
        self,
        symbol: str,
        volume: float,
        price: float,
        stop_loss: float,
        take_profit: float,
    ) -> bool:

        self.connection.validate()

        self.demo_guard.validate()

        self.market.validate(
            symbol,
        )

        self.volume.validate(
            symbol,
            volume,
        )

        self.price.validate(
            symbol,
            price,
            stop_loss,
            take_profit,
        )

        return True