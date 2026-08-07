"""
=================================================
Project Phoenix
Test Pre Trade Safety Manager
M59.4.6
=================================================
"""

from unittest.mock import patch

from live_execution.pre_trade_safety_manager import (
    PreTradeSafetyManager,
)


@patch(
    "live_execution.connection_health_checker.ConnectionHealthChecker.validate",
)
@patch(
    "live_execution.demo_account_guard.DemoAccountGuard.validate",
)
@patch(
    "live_execution.market_status_validator.MarketStatusValidator.validate",
)
@patch(
    "live_execution.volume_validator.VolumeValidator.validate",
)
@patch(
    "live_execution.price_validator.PriceValidator.validate",
)
def test_pre_trade_safety_manager(
    mock_price,
    mock_volume,
    mock_market,
    mock_demo,
    mock_connection,
):

    mock_connection.return_value = True

    mock_demo.return_value = True

    mock_market.return_value = True

    mock_volume.return_value = True

    mock_price.return_value = True

    manager = PreTradeSafetyManager()

    assert manager.validate(

        symbol="EURUSD",

        volume=0.10,

        price=1.10000,

        stop_loss=1.09500,

        take_profit=1.11000,

    ) is True