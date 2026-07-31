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