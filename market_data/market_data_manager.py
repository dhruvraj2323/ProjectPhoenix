"""
=================================================
Project Phoenix
Market Data Manager
M40.X.1
=================================================
"""

from __future__ import annotations

from market_data.data_validator import DataValidator
from market_data.historical_loader import HistoricalLoader
from market_data.market_data_models import MarketDataResult
from market_data.timeframe_converter import TimeframeConverter


class MarketDataManager:
    """
    Project Phoenix Market Data Manager.

    Responsibilities
    ----------------
    1. Load historical market data.
    2. Validate loaded candles.
    3. Convert timeframe if requested.
    4. Return a standardized MarketDataResult.
    """

    def __init__(self) -> None:

        self.loader = HistoricalLoader()
        self.validator = DataValidator()
        self.converter = TimeframeConverter()

    # ---------------------------------------------------------

    def process(
        self,
        market_data_source: str,
        timeframe: str = "M1",
    ) -> MarketDataResult:
        """
        Execute the complete Market Data workflow.
        """

        result = MarketDataResult()

        try:

            # Load historical data
            candles = self.loader.load_zip(market_data_source)

            # Validate loaded candles
            validation_report = self.validator.validate(candles)

            # Convert timeframe if required
            if timeframe != "M1":
                candles = self.converter.convert(
                    candles,
                    timeframe,
                )

            result.success = True
            result.candles = candles
            result.validation_report = validation_report
            result.timeframe = timeframe
            result.candle_count = len(candles)

        except Exception as ex:

            result.success = False
            result.add_error(str(ex))

        return result


if __name__ == "__main__":

    print("Market Data Manager Module Loaded Successfully")