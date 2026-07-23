"""
=================================================
Project Phoenix
Indicator Calculator
M32
=================================================
"""

from __future__ import annotations

from typing import Dict, Any


class IndicatorCalculator:
    """
    Performs all indicator calculations.

    Actual mathematical implementations
    will be connected during later
    implementation phases.
    """

    def __init__(self) -> None:

        self._results: Dict[str, Any] = {}

    # ---------------------------------------------------------

    def calculate_ema(
        self,
        candles,
        period: int = 20,
    ):

        value = None

        self._results[f"EMA_{period}"] = value

        return value

    # ---------------------------------------------------------

    def calculate_sma(
        self,
        candles,
        period: int = 20,
    ):

        value = None

        self._results[f"SMA_{period}"] = value

        return value

    # ---------------------------------------------------------

    def calculate_rsi(
        self,
        candles,
        period: int = 14,
    ):

        value = None

        self._results[f"RSI_{period}"] = value

        return value

    # ---------------------------------------------------------

    def calculate_atr(
        self,
        candles,
        period: int = 14,
    ):

        value = None

        self._results[f"ATR_{period}"] = value

        return value

    # ---------------------------------------------------------

    def calculate_macd(
        self,
        candles,
    ):

        value = None

        self._results["MACD"] = value

        return value

    # ---------------------------------------------------------

    def calculate_bollinger_bands(
        self,
        candles,
        period: int = 20,
    ):

        value = None

        self._results["BOLLINGER_BANDS"] = value

        return value

    # ---------------------------------------------------------

    def calculate_vwap(
        self,
        candles,
    ):

        value = None

        self._results["VWAP"] = value

        return value

    # ---------------------------------------------------------

    def calculate_supertrend(
        self,
        candles,
        period: int = 10,
        multiplier: float = 3.0,
    ):

        value = None

        self._results["SUPERTREND"] = value

        return value

    # ---------------------------------------------------------

    def calculate_all(
        self,
        candles,
    ) -> Dict[str, Any]:
        """
        Execute every supported indicator.
        """

        self.calculate_ema(candles)
        self.calculate_sma(candles)
        self.calculate_rsi(candles)
        self.calculate_atr(candles)
        self.calculate_macd(candles)
        self.calculate_bollinger_bands(candles)
        self.calculate_vwap(candles)
        self.calculate_supertrend(candles)

        return self._results

    # ---------------------------------------------------------

    @property
    def results(self) -> Dict[str, Any]:

        return self._results