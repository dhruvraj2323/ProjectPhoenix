"""
=================================================
Project Phoenix
Pattern Detector
M33
=================================================
"""

from __future__ import annotations

from pattern_engine.pattern_context import (
    PatternContext,
)


class PatternDetector:
    """
    Detects candlestick patterns.
    """

    def detect(
        self,
        context: PatternContext,
    ) -> PatternContext:
        """
        Detect candlestick patterns.

        M50.X.1
        Enhanced Doji Detection
        """

        DOJI_THRESHOLD = 0.10

        for index, candle in enumerate(context.candles):

            open_price = candle.get("open", 0.0)
            close_price = candle.get("close", 0.0)
            high = candle.get("high", 0.0)
            low = candle.get("low", 0.0)

            candle_range = high - low

            if candle_range <= 0:

                continue

            body = abs(close_price - open_price)

            body_ratio = body / candle_range

            if body_ratio <= DOJI_THRESHOLD:

                strength = round(
                    1.0 - (body_ratio / DOJI_THRESHOLD),
                    3,
                )

                context.add_pattern(
                    {
                        "name": "DOJI",
                        "index": index,
                        "strength": strength,
                        "body_ratio": round(body_ratio, 5),
                    }
                )

        return context

            # ---------------------------------------------
        # Hammer Detection
        # ---------------------------------------------

        upper_shadow = (
            high
            - max(
                open_price,
                close_price,
            )
        )

        lower_shadow = (
            min(
                open_price,
                close_price,
            )
            - low
        )

        body = abs(
            close_price
            - open_price
        )

        if candle_range > 0:

            body_ratio = (
                body
                / candle_range
            )

            lower_ratio = (
                lower_shadow
                / candle_range
            )

            upper_ratio = (
                upper_shadow
                / candle_range
            )

            if (

                body_ratio <= 0.35

                and

                lower_ratio >= 0.50

                and

                upper_ratio <= 0.20

            ):

                strength = round(

                    (
                        lower_ratio
                        * (
                            1.0
                            - body_ratio
                        )
                    ),

                    3,

                )

                context.add_pattern(

                    {

                        "name": "HAMMER",

                        "index": index,

                        "strength": strength,

                        "body_ratio": round(
                            body_ratio,
                            5,
                        ),

                        "lower_shadow": round(
                            lower_ratio,
                            5,
                        ),

                        "upper_shadow": round(
                            upper_ratio,
                            5,
                        ),

                    }

                )        

        # ---------------------------------------------
        # Shooting Star Detection
        # ---------------------------------------------

        if candle_range > 0:

            body_ratio = (
                body
                / candle_range
            )

            lower_ratio = (
                lower_shadow
                / candle_range
            )

            upper_ratio = (
                upper_shadow
                / candle_range
            )

            if (

                body_ratio <= 0.35

                and

                upper_ratio >= 0.50

                and

                lower_ratio <= 0.20

            ):

                strength = round(

                    (
                        upper_ratio
                        * (
                            1.0
                            - body_ratio
                        )
                    ),

                    3,

                )

                context.add_pattern(

                    {

                        "name": "SHOOTING_STAR",

                        "index": index,

                        "strength": strength,

                        "body_ratio": round(
                            body_ratio,
                            5,
                        ),

                        "upper_shadow": round(
                            upper_ratio,
                            5,
                        ),

                        "lower_shadow": round(
                            lower_ratio,
                            5,
                        ),

                    }

                )      

        # ---------------------------------------------
        # Bullish Engulfing Detection
        # ---------------------------------------------

        if index > 0:

            previous = context.candles[index - 1]

            previous_open = previous.get(
                "open",
                0.0,
            )

            previous_close = previous.get(
                "close",
                0.0,
            )

            previous_bearish = (
                previous_close
                < previous_open
            )

            current_bullish = (
                close_price
                > open_price
            )

            body_engulfs = (

                open_price
                <= previous_close

                and

                close_price
                >= previous_open

            )

            if (

                previous_bearish

                and

                current_bullish

                and

                body_engulfs

            ):

                previous_body = abs(
                    previous_open
                    - previous_close
                )

                current_body = abs(
                    close_price
                    - open_price
                )

                if previous_body > 0:

                    strength = round(
                        current_body
                        / previous_body,
                        3,
                    )

                else:

                    strength = 1.0

                context.add_pattern(

                    {

                        "name": "BULLISH_ENGULFING",

                        "index": index,

                        "strength": strength,

                        "previous_body": round(
                            previous_body,
                            5,
                        ),

                        "current_body": round(
                            current_body,
                            5,
                        ),

                    }

                )

        # ---------------------------------------------
        # Bearish Engulfing Detection
        # ---------------------------------------------

        if index > 0:

            previous = context.candles[index - 1]

            previous_open = previous.get(
                "open",
                0.0,
            )

            previous_close = previous.get(
                "close",
                0.0,
            )

            previous_bullish = (
                previous_close
                > previous_open
            )

            current_bearish = (
                close_price
                < open_price
            )

            body_engulfs = (

                open_price
                >= previous_close

                and

                close_price
                <= previous_open

            )

            if (

                previous_bullish

                and

                current_bearish

                and

                body_engulfs

            ):

                previous_body = abs(
                    previous_close
                    - previous_open
                )

                current_body = abs(
                    open_price
                    - close_price
                )

                if previous_body > 0:

                    strength = round(
                        current_body
                        / previous_body,
                        3,
                    )

                else:

                    strength = 1.0

                context.add_pattern(

                    {

                        "name": "BEARISH_ENGULFING",

                        "index": index,

                        "strength": strength,

                        "previous_body": round(
                            previous_body,
                            5,
                        ),

                        "current_body": round(
                            current_body,
                            5,
                        ),

                    }

                )

        # ---------------------------------------------
        # Pin Bar Detection
        # ---------------------------------------------

        if candle_range > 0:

            body_ratio = (
                body
                / candle_range
            )

            lower_ratio = (
                lower_shadow
                / candle_range
            )

            upper_ratio = (
                upper_shadow
                / candle_range
            )

            if (

                body_ratio <= 0.30

                and

                (

                    lower_ratio >= 0.60

                    or

                    upper_ratio >= 0.60

                )

            ):

                if lower_ratio > upper_ratio:

                    direction = "BULLISH"

                    dominant_shadow = lower_ratio

                else:

                    direction = "BEARISH"

                    dominant_shadow = upper_ratio

                strength = round(

                    dominant_shadow
                    * (
                        1.0
                        - body_ratio
                    ),

                    3,

                )

                context.add_pattern(

                    {

                        "name": "PIN_BAR",

                        "direction": direction,

                        "index": index,

                        "strength": strength,

                        "body_ratio": round(
                            body_ratio,
                            5,
                        ),

                        "upper_shadow": round(
                            upper_ratio,
                            5,
                        ),

                        "lower_shadow": round(
                            lower_ratio,
                            5,
                        ),

                    }

                )

        # ---------------------------------------------
        # Higher High / Higher Low Detection
        # ---------------------------------------------

        if index > 0:

            previous = context.candles[index - 1]

            previous_high = previous.get(
                "high",
                0.0,
            )

            previous_low = previous.get(
                "low",
                0.0,
            )

            current_high = high

            current_low = low

            if (

                current_high > previous_high

                and

                current_low > previous_low

            ):

                high_strength = (
                    current_high
                    - previous_high
                )

                low_strength = (
                    current_low
                    - previous_low
                )

                strength = round(

                    (
                        high_strength
                        + low_strength
                    )
                    / 2.0,

                    5,

                )

                context.add_pattern(

                    {

                        "name": "HIGHER_HIGH_HIGHER_LOW",

                        "index": index,

                        "strength": strength,

                        "previous_high": previous_high,

                        "previous_low": previous_low,

                        "current_high": current_high,

                        "current_low": current_low,

                    }

                )

        # ---------------------------------------------
        # Higher High / Higher Low Detection
        # ---------------------------------------------

        if index > 0:

            previous = context.candles[index - 1]

            previous_high = previous.get(
                "high",
                0.0,
            )

            previous_low = previous.get(
                "low",
                0.0,
            )

            current_high = high

            current_low = low

            if (

                current_high > previous_high

                and

                current_low > previous_low

            ):

                high_strength = (
                    current_high
                    - previous_high
                )

                low_strength = (
                    current_low
                    - previous_low
                )

                strength = round(

                    (
                        high_strength
                        + low_strength
                    )
                    / 2.0,

                    5,

                )

                context.add_pattern(

                    {

                        "name": "HIGHER_HIGH_HIGHER_LOW",

                        "index": index,

                        "strength": strength,

                        "previous_high": previous_high,

                        "previous_low": previous_low,

                        "current_high": current_high,

                        "current_low": current_low,

                    }

                )

        # ---------------------------------------------
        # Lower High / Lower Low Detection
        # ---------------------------------------------

        if index > 0:

            previous = context.candles[index - 1]

            previous_high = previous.get(
                "high",
                0.0,
            )

            previous_low = previous.get(
                "low",
                0.0,
            )

            current_high = high

            current_low = low

            if (

                current_high < previous_high

                and

                current_low < previous_low

            ):

                high_strength = (
                    previous_high
                    - current_high
                )

                low_strength = (
                    previous_low
                    - current_low
                )

                strength = round(

                    (
                        high_strength
                        + low_strength
                    )
                    / 2.0,

                    5,

                )

                context.add_pattern(

                    {

                        "name": "LOWER_HIGH_LOWER_LOW",

                        "index": index,

                        "strength": strength,

                        "previous_high": previous_high,

                        "previous_low": previous_low,

                        "current_high": current_high,

                        "current_low": current_low,

                    }

                )

        # ---------------------------------------------
        # Breakout Detection
        # ---------------------------------------------

        LOOKBACK = 5

        if index >= LOOKBACK:

            previous_candles = (
                context.candles[
                    index - LOOKBACK:index
                ]
            )

            highest_high = max(

                candle.get(
                    "high",
                    0.0,
                )

                for candle in previous_candles

            )

            if high > highest_high:

                breakout_size = round(

                    high - highest_high,

                    5,

                )

                strength = round(

                    breakout_size
                    / max(
                        highest_high,
                        1.0,
                    ),

                    5,

                )

                context.add_pattern(

                    {

                        "name": "BREAKOUT",

                        "index": index,

                        "strength": strength,

                        "breakout_size": breakout_size,

                        "highest_high": highest_high,

                        "current_high": high,

                        "lookback": LOOKBACK,

                    }

                )

        # ---------------------------------------------
        # Breakdown Detection
        # ---------------------------------------------

        LOOKBACK = 5

        if index >= LOOKBACK:

            previous_candles = (
                context.candles[
                    index - LOOKBACK:index
                ]
            )

            lowest_low = min(

                candle.get(
                    "low",
                    0.0,
                )

                for candle in previous_candles

            )

            if low < lowest_low:

                breakdown_size = round(

                    lowest_low - low,

                    5,

                )

                strength = round(

                    breakdown_size
                    / max(
                        lowest_low,
                        1.0,
                    ),

                    5,

                )

                context.add_pattern(

                    {

                        "name": "BREAKDOWN",

                        "index": index,

                        "strength": strength,

                        "breakdown_size": breakdown_size,

                        "lowest_low": lowest_low,

                        "current_low": low,

                        "lookback": LOOKBACK,

                    }

                )

        # ---------------------------------------------
        # Retest Detection
        # ---------------------------------------------

        RETEST_TOLERANCE = 0.002

        if index >= 1:

            previous = context.candles[index - 1]

            previous_high = previous.get(
                "high",
                0.0,
            )

            previous_low = previous.get(
                "low",
                0.0,
            )

            bullish_retest = (

                low
                <= previous_high

                and

                low
                >= previous_high
                * (
                    1.0
                    - RETEST_TOLERANCE
                )

            )

            bearish_retest = (

                high
                >= previous_low

                and

                high
                <= previous_low
                * (
                    1.0
                    + RETEST_TOLERANCE
                )

            )

            if bullish_retest:

                distance = abs(
                    low
                    - previous_high
                )

                strength = round(

                    1.0
                    - (
                        distance
                        / max(
                            previous_high,
                            1.0,
                        )
                    ),

                    5,

                )

                context.add_pattern(

                    {

                        "name": "BULLISH_RETEST",

                        "index": index,

                        "strength": strength,

                        "reference_level": previous_high,

                        "price": low,

                    }

                )

            elif bearish_retest:

                distance = abs(
                    high
                    - previous_low
                )

                strength = round(

                    1.0
                    - (
                        distance
                        / max(
                            previous_low,
                            1.0,
                        )
                    ),

                    5,

                )

                context.add_pattern(

                    {

                        "name": "BEARISH_RETEST",

                        "index": index,

                        "strength": strength,

                        "reference_level": previous_low,

                        "price": high,

                    }

                )

        # ---------------------------------------------
        # Indicator-Based Pattern Confirmation
        # ---------------------------------------------

        indicators = context.get_metadata(
            "indicators",
            {},
        )

        if (

            indicators

            and

            context.patterns

        ):

            ema20 = indicators.get(
                "EMA_20",
                0.0,
            )

            ema200 = indicators.get(
                "EMA_200",
                indicators.get(
                    "EMA200",
                    0.0,
                ),
            )

            rsi = indicators.get(
                "RSI_14",
                50.0,
            )

            supertrend = indicators.get(
                "SUPERTREND",
                0.0,
            )

            for pattern in context.patterns:

                confirmation = 0

                if ema20 > ema200:

                    confirmation += 1

                if 40 <= rsi <= 70:

                    confirmation += 1

                if close_price >= supertrend:

                    confirmation += 1

                pattern[
                    "indicator_confirmation"
                ] = confirmation

                pattern[
                    "confirmed"
                ] = (
                    confirmation >= 2
                )

                pattern[
                    "confirmation_score"
                ] = round(
                    confirmation / 3.0,
                    3,
                )                                                                                                                                                                             