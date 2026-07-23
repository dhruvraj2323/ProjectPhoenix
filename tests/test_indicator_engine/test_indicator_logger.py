"""
=================================================
Project Phoenix
Unit Test
Indicator Logger
=================================================
"""

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_logger import IndicatorLogger


def test_indicator_logger():

    logger = IndicatorLogger()

    context = IndicatorContext(
        engine_id="IND-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.indicators = {
        "EMA_20": None,
        "RSI_14": None,
    }

    logger.log_start(context)
    logger.log_indicator("EMA_20")
    logger.log_indicator("RSI_14")
    logger.log_finish(context)

    print("\n===== Indicator Logger =====")
    print("Logger executed successfully.")
    print("Indicator Logger Test Passed")


if __name__ == "__main__":
    test_indicator_logger()