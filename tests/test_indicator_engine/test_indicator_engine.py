"""
=================================================
Project Phoenix
Unit Test
Indicator Engine
=================================================
"""

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_engine import IndicatorEngine


def test_indicator_engine():

    engine = IndicatorEngine()
    
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

    result = engine.run(context)

    assert result is context
    assert isinstance(result.indicators, dict)

    print("\n===== Indicator Engine =====")
    print("Indicators Generated :", len(result.indicators))

    for key in result.indicators:
        print(key)

    print("\nIndicator Engine Test Passed")


if __name__ == "__main__":
    test_indicator_engine()