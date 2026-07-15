"""
=================================================
Project Phoenix
Market Data Manager
=================================================

Responsible for:
- Historical OHLC data
- Live Tick data
- Bid / Ask prices
- Data conversion
- Data validation
"""

import pandas as pd
import MetaTrader5 as mt5

from core.logger import logger
from core.config import config

# -------------------------------------------------
# Logger Instance
# -------------------------------------------------

app_logger = logger.initialize()

# -------------------------------------------------
# Market Data Manager
# -------------------------------------------------


class MarketData:
    """
    Handles all market data operations.
    """

    def __init__(self):
        """
        Initialize Market Data Manager.
        """

        self.symbol = config.settings["market"]["symbol"]
        self.timeframe = config.settings["market"]["timeframe"]

        app_logger.info(
            "Market Data Manager initialized."
        )

    def get_historical_data(
        self,
        candle_count=500
    ):
        """
        Retrieve historical OHLC data from MT5.
        """

        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
        }

        timeframe = timeframe_map.get(
            self.timeframe
        )

        if timeframe is None:

            app_logger.error(
                f"Unsupported timeframe: {self.timeframe}"
            )

            return None

        rates = mt5.copy_rates_from_pos(
            self.symbol,
            timeframe,
            0,
            candle_count
        )

        if rates is None:

            app_logger.error(
                "Unable to retrieve historical data."
            )

            app_logger.error(
                f"MT5 Error: {mt5.last_error()}"
            )

            return None

        app_logger.info(
            f"{len(rates)} candles received."
        )

        return rates

    def get_dataframe(
        self,
        candle_count=500
    ):
        """
        Return historical data as a Pandas DataFrame.
        """

        rates = self.get_historical_data(
            candle_count
        )

        if rates is None:
            return None

        dataframe = pd.DataFrame(rates)

        dataframe["time"] = pd.to_datetime(
            dataframe["time"],
            unit="s"
        )

        app_logger.info(
            f"DataFrame created with {len(dataframe)} rows."
        )

        return dataframe

    def get_tick(self):
        """
        Retrieve latest market tick.
        """

        tick = mt5.symbol_info_tick(self.symbol)

        if tick is None:

            app_logger.error(
                f"Unable to retrieve tick data."
            )

            app_logger.error(
                f"MT5 Error: {mt5.last_error()}"
            )

            return None

        app_logger.info(
            "Live tick data received."
        )

        return tick

    def get_symbol_info(self):
        """
        Retrieve symbol information.
        """

        symbol_info = mt5.symbol_info(
            self.symbol
        )

        if symbol_info is None:

            app_logger.error(
                "Unable to retrieve symbol information."
            )

            app_logger.error(
                f"MT5 Error: {mt5.last_error()}"
            )

            return None

        app_logger.info(
            "Symbol information received."
        )

        return symbol_info

    def get_current_price(self):
        """
        Return current Bid and Ask prices.
        """

        tick = self.get_tick()

        if tick is None:
            return None

        return {
            "bid": tick.bid,
            "ask": tick.ask
        }        