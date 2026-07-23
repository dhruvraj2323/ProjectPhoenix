"""
=================================================
Project Phoenix
Unit Test
Indicator Validator
=================================================
"""

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_validator import IndicatorValidator


def test_indicator_validator():

    validator = IndicatorValidator()

    context = IndicatorContext(
        engine_id="IND-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.candles = [1, 2, 3, 4, 5]

    assert validator.validate(context) is True

    assert validator.validate_indicator("EMA") is True
    assert validator.validate_indicator("RSI") is True
    assert validator.validate_indicator("ATR") is True
    assert validator.validate_indicator("MACD") is True
    assert validator.validate_indicator("VWAP") is True

    assert validator.validate_indicator("UNKNOWN") is False

    print("\n===== Indicator Validator =====")
    print("Context Validation :", validator.validate(context))
    print("EMA Supported      :", validator.validate_indicator("EMA"))
    print("RSI Supported      :", validator.validate_indicator("RSI"))
    print("UNKNOWN Supported  :", validator.validate_indicator("UNKNOWN"))
    print("\nIndicator Validator Test Passed")


if __name__ == "__main__":
    test_indicator_validator()