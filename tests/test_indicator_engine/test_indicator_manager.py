"""
=================================================
Project Phoenix
Unit Test
Indicator Manager
=================================================
"""

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_manager import IndicatorManager


def test_indicator_manager():

    manager = IndicatorManager()

    context = IndicatorContext(
        engine_id="IND-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = [
        {"close": 100},
        {"close": 101},
        {"close": 102},
    ]

    result = manager.run(context)

    assert result is context
    assert isinstance(result.indicators, dict)

    print("\n===== Indicator Manager =====")
    print("Indicators Generated :", len(result.indicators))

    for indicator in result.indicators:
        print(indicator)

    print("\nIndicator Manager Test Passed")


if __name__ == "__main__":
    test_indicator_manager()