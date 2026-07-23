"""
=================================================
Project Phoenix
Unit Test
Indicator Calculator
=================================================
"""

from indicator_engine.indicator_calculator import IndicatorCalculator


def test_indicator_calculator():

    calculator = IndicatorCalculator()

    candles = []

    results = calculator.calculate_all(candles)

    assert "EMA_20" in results
    assert "SMA_20" in results
    assert "RSI_14" in results
    assert "ATR_14" in results
    assert "MACD" in results
    assert "BOLLINGER_BANDS" in results
    assert "VWAP" in results
    assert "SUPERTREND" in results

    print("\n===== Indicator Calculator =====")

    for key, value in results.items():
        print(f"{key:<20}: {value}")

    print("\nIndicator Calculator Test Passed")


if __name__ == "__main__":
    test_indicator_calculator()