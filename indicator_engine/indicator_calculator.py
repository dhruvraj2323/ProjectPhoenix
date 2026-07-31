"""
=================================================
Project Phoenix
Indicator Calculator
M32.1
Strategy Alignment
=================================================
"""

from __future__ import annotations

from typing import Any, Dict


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
    # Internal Helpers
    # ---------------------------------------------------------

    def _get_close(
        self,
        candle,
    ) -> float:
        """
        Extract close price from a candle.

        Supports dictionary candles and
        future object-based candle models.
        """

        if isinstance(candle, dict):

            return float(candle.get("close", 0.0))

        return float(getattr(candle, "close", 0.0))

    def _get_high(
        self,
        candle,
    ) -> float:
        """
        Extract high price from a candle.

        Supports dictionary candles and
        future object-based candle models.
        """

        if isinstance(candle, dict):

            return float(candle.get("high", 0.0))

        return float(getattr(candle, "high", 0.0))

    def _get_low(
        self,
        candle,
    ) -> float:
        """
        Extract low price from a candle.

        Supports dictionary candles and
        future object-based candle models.
        """

        if isinstance(candle, dict):

            return float(candle.get("low", 0.0))

        return float(getattr(candle, "low", 0.0))
        
    # ---------------------------------------------------------
    # EMA
    # ---------------------------------------------------------

    def calculate_ema(
        self,
        candles,
        period: int,
    ):

        if candles is None or len(candles) < period:

            value = 0.0

        else:

            closes = [
                self._get_close(candle)
                for candle in candles
            ]

            multiplier = 2.0 / (period + 1)

            ema = (
                sum(closes[:period])
                / period
            )

            for close in closes[period:]:

                ema = (
                    (close - ema)
                    * multiplier
                ) + ema

            value = round(
                ema,
                5,
            )

        self._results[f"EMA_{period}"] = value
        self._results[f"EMA{period}"] = value

        return value

    # ---------------------------------------------------------
    # SMA
    # ---------------------------------------------------------

    def calculate_sma(
        self,
        candles,
        period: int,
    ):

        if candles is None or len(candles) < period:

            value = 0.0

        else:

            closes = [
                self._get_close(candle)
                for candle in candles[-period:]
            ]

            value = round(
                sum(closes) / period,
                5,
            )

        self._results[f"SMA_{period}"] = value
        self._results[f"SMA{period}"] = value

        return value

    # ---------------------------------------------------------
    # RSI
    # ---------------------------------------------------------

    def calculate_rsi(
        self,
        candles,
        period: int,
    ):

        if candles is None or len(candles) < (period + 1):

            value = 0.0

        else:

            closes = [
                self._get_close(candle)
                for candle in candles
            ]

            gains = []
            losses = []

            for index in range(1, len(closes)):

                change = (
                    closes[index]
                    - closes[index - 1]
                )

                if change > 0:

                    gains.append(change)
                    losses.append(0.0)

                elif change < 0:

                    gains.append(0.0)
                    losses.append(abs(change))

                else:

                    gains.append(0.0)
                    losses.append(0.0)

            average_gain = (
                sum(gains[:period])
                / period
            )

            average_loss = (
                sum(losses[:period])
                / period
            )

            for index in range(
                period,
                len(gains),
            ):

                average_gain = (
                    (
                        average_gain
                        * (period - 1)
                    )
                    + gains[index]
                ) / period

                average_loss = (
                    (
                        average_loss
                        * (period - 1)
                    )
                    + losses[index]
                ) / period

            if (
                average_gain == 0.0
                and average_loss == 0.0
            ):

                value = 50.0

            elif average_loss == 0.0:

                value = 100.0

            else:

                relative_strength = (
                    average_gain
                    / average_loss
                )

                value = (
                    100.0
                    - (
                        100.0
                        / (
                            1.0
                            + relative_strength
                        )
                    )
                )

                value = round(
                    value,
                    5,
                )

        self._results[f"RSI_{period}"] = value
        self._results[f"RSI{period}"] = value

        return value

    # ---------------------------------------------------------
    # ATR
    # ---------------------------------------------------------

    def calculate_atr(
        self,
        candles,
        period: int,
    ):

        if candles is None or len(candles) < (period + 1):

            value = 0.0

        else:

            true_ranges = []

            for index in range(
                1,
                len(candles),
            ):

                current = candles[index]
                previous = candles[index - 1]

                high = self._get_high(current)
                low = self._get_low(current)
                previous_close = self._get_close(previous)

                true_range = max(
                    high - low,
                    abs(high - previous_close),
                    abs(low - previous_close),
                )

                true_ranges.append(true_range)

            atr = (
                sum(true_ranges[:period])
                / period
            )

            for true_range in true_ranges[period:]:

                atr = (
                    (
                        atr
                        * (period - 1)
                    )
                    + true_range
                ) / period

            value = round(
                atr,
                5,
            )

        self._results[f"ATR_{period}"] = value
        self._results[f"ATR{period}"] = value

        return value

    # ---------------------------------------------------------

    def calculate_macd(
        self,
        candles,
    ):

        if candles is None or len(candles) < 35:

            value = {
                "macd": 0.0,
                "signal": 0.0,
                "histogram": 0.0,
            }

        else:

            closes = [
                self._get_close(candle)
                for candle in candles
            ]

            def ema_series(
                values,
                period,
            ):

                multiplier = 2.0 / (
                    period + 1
                )

                ema = (
                    sum(values[:period])
                    / period
                )

                series = [ema]

                for current in values[period:]:

                    ema = (
                        (
                            current
                            - ema
                        )
                        * multiplier
                    ) + ema

                    series.append(ema)

                return series

            ema12 = ema_series(
                closes,
                12,
            )

            ema26 = ema_series(
                closes,
                26,
            )

            macd_values = []

            offset = (
                len(ema12)
                - len(ema26)
            )

            for index in range(
                len(ema26)
            ):

                macd_values.append(
                    ema12[
                        index + offset
                    ]
                    - ema26[index]
                )

            signal_values = ema_series(
                macd_values,
                9,
            )

            macd_line = round(
                macd_values[-1],
                5,
            )

            signal_line = round(
                signal_values[-1],
                5,
            )

            histogram = round(
                macd_line
                - signal_line,
                5,
            )

            value = {
                "macd": macd_line,
                "signal": signal_line,
                "histogram": histogram,
            }

        self._results["MACD"] = value

        return value

    # ---------------------------------------------------------

    def calculate_bollinger_bands(
        self,
        candles,
        period: int = 20,
    ):

        value = 0.0

        self._results["BOLLINGER_BANDS"] = value

        return value

    # ---------------------------------------------------------

    def calculate_vwap(
        self,
        candles,
    ):

        value = 0.0

        self._results["VWAP"] = value

        return value

    # ---------------------------------------------------------

    def calculate_supertrend(
        self,
        candles,
        period: int = 10,
        multiplier: float = 3.0,
    ):

        value = 0.0

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

        self._results.clear()

        # Strategy-required EMA values
        self.calculate_ema(candles, 9)
        self.calculate_ema(candles, 21)
        self.calculate_ema(candles, 200)

        # Existing EMA
        self.calculate_ema(candles, 20)

        # Existing SMA
        self.calculate_sma(candles, 20)

        # Strategy-required RSI
        self.calculate_rsi(candles, 14)

        # Existing indicators
        self.calculate_atr(candles, 14)
        self.calculate_macd(candles)
        self.calculate_bollinger_bands(candles)
        self.calculate_vwap(candles)
        self.calculate_supertrend(candles)

        return self._results

    # ---------------------------------------------------------

    @property
    def results(self) -> Dict[str, Any]:

        return self._results