"""
=================================================
Project Phoenix
Test Volume Validator
M59.4.3
=================================================
"""

from unittest.mock import patch

from live_execution.volume_validator import (
    VolumeValidator,
)


@patch(
    "live_execution.symbol_info.SymbolInfo.volume_min",
)
@patch(
    "live_execution.symbol_info.SymbolInfo.volume_max",
)
@patch(
    "live_execution.symbol_info.SymbolInfo.volume_step",
)
def test_volume_validator(
    mock_step,
    mock_max,
    mock_min,
):

    mock_min.return_value = 0.01

    mock_max.return_value = 100.0

    mock_step.return_value = 0.01

    validator = VolumeValidator()

    assert (
        validator.validate(
            "EURUSD",
            0.10,
        )
        is True
    )