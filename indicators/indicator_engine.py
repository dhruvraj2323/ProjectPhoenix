"""
=================================================
Project Phoenix
Indicator Engine
=================================================

Responsible for:
- EMA
- SMA
- RSI
- ATR
- MACD
- Bollinger Bands
"""

import pandas as pd

from core.logger import logger

app_logger = logger.initialize()


class IndicatorEngine:
    """
    Handles all technical indicator calculations.
    """

    def __init__(self):
        app_logger.info(
            "Indicator Engine initialized."
        )

    def calculate_ema(
        self,
        dataframe,
        period=20
    ):
        """
        Calculate Exponential Moving Average.
        """

        dataframe = dataframe.copy()

        dataframe[f"EMA_{period}"] = (
            dataframe["close"]
            .ewm(
                span=period,
                adjust=False
            )
            .mean()
        )

        app_logger.info(
            f"EMA {period} calculated."
        )

        return dataframe

    def calculate_sma(
        self,
        dataframe,
        period=20
    ):
        """
        Calculate Simple Moving Average.
        """

        dataframe = dataframe.copy()

        dataframe[f"SMA_{period}"] = (
            dataframe["close"]
            .rolling(
                window=period
            )
            .mean()
        )

        app_logger.info(
            f"SMA {period} calculated."
        )

        return dataframe

    def calculate_rsi(
        self,
        dataframe,
        period=14
    ):
        """
        Calculate RSI indicator.
        """

        dataframe = dataframe.copy()

        delta = dataframe["close"].diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        average_gain = gain.rolling(
            window=period
        ).mean()

        average_loss = loss.rolling(
            window=period
        ).mean()

        rs = average_gain / average_loss

        dataframe[f"RSI_{period}"] = (
            100 - (100 / (1 + rs))
        )

        app_logger.info(
            f"RSI {period} calculated."
        )

        return dataframe

    def calculate_atr(
        self,
        dataframe,
        period=14
    ):
        """
        Calculate Average True Range (ATR).
        """

        dataframe = dataframe.copy()

        high_low = (
            dataframe["high"] -
            dataframe["low"]
        )

        high_close = (
            dataframe["high"] -
            dataframe["close"].shift()
        ).abs()

        low_close = (
            dataframe["low"] -
            dataframe["close"].shift()
        ).abs()

        true_range = (
            dataframe[
                [
                    "high_low",
                    "high_close",
                    "low_close"
                ]
            ]
            if False else None
        )

        dataframe["TR"] = (
            pd.concat(
                [
                    high_low,
                    high_close,
                    low_close
                ],
                axis=1
            )
            .max(axis=1)
        )

        dataframe[f"ATR_{period}"] = (
            dataframe["TR"]
            .rolling(window=period)
            .mean()
        )

        dataframe.drop(
            columns=["TR"],
            inplace=True
        )

        app_logger.info(
            f"ATR {period} calculated."
        )

        return dataframe      
    def calculate_macd(
        self,
        dataframe,
        fast_period=12,
        slow_period=26,
        signal_period=9
    ):
        """
        Calculate MACD indicator.
        """

        dataframe = dataframe.copy()

        ema_fast = (
            dataframe["close"]
            .ewm(
                span=fast_period,
                adjust=False
            )
            .mean()
        )

        ema_slow = (
            dataframe["close"]
            .ewm(
                span=slow_period,
                adjust=False
            )
            .mean()
        )

        dataframe["MACD"] = (
            ema_fast - ema_slow
        )

        dataframe["MACD_SIGNAL"] = (
            dataframe["MACD"]
            .ewm(
                span=signal_period,
                adjust=False
            )
            .mean()
        )

        dataframe["MACD_HISTOGRAM"] = (
            dataframe["MACD"]
            - dataframe["MACD_SIGNAL"]
        )

        app_logger.info(
            "MACD calculated."
        )

        return dataframe
    def calculate_bollinger_bands(
        self,
        dataframe,
        period=20,
        std_dev=2
    ):
        """
        Calculate Bollinger Bands.
        """

        dataframe = dataframe.copy()

        dataframe["BB_MIDDLE"] = (
            dataframe["close"]
            .rolling(
                window=period
            )
            .mean()
        )

        rolling_std = (
            dataframe["close"]
            .rolling(
                window=period
            )
            .std()
        )

        dataframe["BB_UPPER"] = (
            dataframe["BB_MIDDLE"]
            + (rolling_std * std_dev)
        )

        dataframe["BB_LOWER"] = (
            dataframe["BB_MIDDLE"]
            - (rolling_std * std_dev)
        )

        app_logger.info(
            "Bollinger Bands calculated."
        )

        return dataframe