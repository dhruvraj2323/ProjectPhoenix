"""
=================================================
Project Phoenix
Candlestick Recognition Engine
=================================================

Responsible for:
- Candle Body
- Upper Wick
- Lower Wick
- Candle Range
- Bullish / Bearish Candle
"""

from core.logger import logger

app_logger = logger.initialize()


class CandlestickEngine:
    """
    Handles candlestick calculations.
    """

    def __init__(self):
        app_logger.info(
            "Candlestick Engine initialized."
        )

    def prepare_candles(
        self,
        dataframe
    ):
        """
        Prepare candle anatomy for pattern recognition.
        """

        dataframe = dataframe.copy()

        # -----------------------------------------
        # Candle Body
        # -----------------------------------------

        dataframe["BODY"] = (
            dataframe["close"] -
            dataframe["open"]
        ).abs()

        # -----------------------------------------
        # Upper Wick
        # -----------------------------------------

        dataframe["UPPER_WICK"] = (
            dataframe[["open", "close"]].max(axis=1)
        )

        dataframe["UPPER_WICK"] = (
            dataframe["high"] -
            dataframe["UPPER_WICK"]
        )

        # -----------------------------------------
        # Lower Wick
        # -----------------------------------------

        dataframe["LOWER_WICK"] = (
            dataframe[["open", "close"]].min(axis=1)
        )

        dataframe["LOWER_WICK"] = (
            dataframe["LOWER_WICK"] -
            dataframe["low"]
        )

        # -----------------------------------------
        # Candle Range
        # -----------------------------------------

        dataframe["RANGE"] = (
            dataframe["high"] -
            dataframe["low"]
        )

        # -----------------------------------------
        # Bullish Candle
        # -----------------------------------------

        dataframe["BULLISH"] = (
            dataframe["close"] >
            dataframe["open"]
        )

        # -----------------------------------------
        # Bearish Candle
        # -----------------------------------------

        dataframe["BEARISH"] = (
            dataframe["close"] <
            dataframe["open"]
        )

        app_logger.info(
            "Candlestick preparation completed."
        )

        return dataframe

    def detect_doji(
        self,
        dataframe,
        body_percentage=0.10
    ):
        """
        Detect Doji candlestick pattern.

        A candle is considered a Doji when its body
        is less than or equal to 10% of its total range.
        """

        dataframe = dataframe.copy()

        dataframe["DOJI"] = (
            dataframe["BODY"]
            <=
            (dataframe["RANGE"] * body_percentage)
        )

        app_logger.info(
            "Doji detection completed."
        )

        return dataframe

    def detect_hammer(
        self,
        dataframe
    ):
        """
        Detect Hammer candlestick pattern.

        Rules:
        - Lower wick >= 2 × body
        - Upper wick <= body
        """

        dataframe = dataframe.copy()

        dataframe["HAMMER"] = (
            (dataframe["LOWER_WICK"] >= (dataframe["BODY"] * 2))
            &
            (dataframe["UPPER_WICK"] <= dataframe["BODY"])
        )

        app_logger.info(
            "Hammer detection completed."
        )

        return dataframe

    def detect_inverted_hammer(
        self,
        dataframe
    ):
        """
        Detect Inverted Hammer candlestick pattern.

        Rules:
        - Upper wick >= 2 × Body
        - Lower wick <= Body
        """

        dataframe = dataframe.copy()

        dataframe["INVERTED_HAMMER"] = (
            (
                dataframe["UPPER_WICK"]
                >=
                (dataframe["BODY"] * 2)
            )
            &
            (
                dataframe["LOWER_WICK"]
                <=
                dataframe["BODY"]
            )
        )

        app_logger.info(
            "Inverted Hammer detection completed."
        )

        return dataframe


    def detect_shooting_star(
        self,
        dataframe
    ):
        """
        Detect Shooting Star candlestick pattern.

        Rules:
        - Upper wick >= 2 × Body
        - Lower wick <= Body
        - Bearish candle
        """

        dataframe = dataframe.copy()

        dataframe["SHOOTING_STAR"] = (
            (
                dataframe["UPPER_WICK"]
                >=
                (dataframe["BODY"] * 2)
            )
            &
            (
                dataframe["LOWER_WICK"]
                <=
                dataframe["BODY"]
            )
            &
            (
                dataframe["BEARISH"]
            )
        )

        app_logger.info(
            "Shooting Star detection completed."
        )

        return dataframe       
                  
    def detect_hanging_man(
        self,
        dataframe
    ):
        """
        Detect Hanging Man candlestick pattern.

        Rules:
        - Lower wick >= 2 × Body
        - Upper wick <= Body
        - Bearish candle
        """

        dataframe = dataframe.copy()

        dataframe["HANGING_MAN"] = (
            (
                dataframe["LOWER_WICK"]
                >=
                (dataframe["BODY"] * 2)
            )
            &
            (
                dataframe["UPPER_WICK"]
                <=
                dataframe["BODY"]
            )
            &
            (
                dataframe["BEARISH"]
            )
        )

        app_logger.info(
            "Hanging Man detection completed."
        )

        return dataframe  

    def detect_spinning_top(
        self,
        dataframe,
        body_percentage=0.30
    ):
        """
        Detect Spinning Top candlestick pattern.

        Rules:
        - Small body (<= 30% of total range)
        - Upper wick >= Body
        - Lower wick >= Body
        """

        dataframe = dataframe.copy()

        dataframe["SPINNING_TOP"] = (
            (
                dataframe["BODY"]
                <=
                (dataframe["RANGE"] * body_percentage)
            )
            &
            (
                dataframe["UPPER_WICK"]
                >=
                dataframe["BODY"]
            )
            &
            (
                dataframe["LOWER_WICK"]
                >=
                dataframe["BODY"]
            )
        )

        app_logger.info(
            "Spinning Top detection completed."
        )

        return dataframe     

    def detect_marubozu(
        self,
        dataframe
    ):
        """
        Detect Marubozu candlestick pattern.

        Rules:
        - Very small upper wick
        - Very small lower wick
        - Strong candle body
        """

        dataframe = dataframe.copy()

        dataframe["MARUBOZU"] = (
            (
                dataframe["UPPER_WICK"]
                <=
                (dataframe["BODY"] * 0.10)
            )
            &
            (
                dataframe["LOWER_WICK"]
                <=
                (dataframe["BODY"] * 0.10)
            )
        )

        app_logger.info(
            "Marubozu detection completed."
        )

        return dataframe

    def detect_bullish_engulfing(
        self,
        dataframe
    ):
        """
        Detect Bullish Engulfing pattern.

        Rules:
        - Previous candle is Bearish
        - Current candle is Bullish
        - Current Open < Previous Close
        - Current Close > Previous Open
        """

        dataframe = dataframe.copy()

        dataframe["BULLISH_ENGULFING"] = (
            (
                dataframe["BEARISH"].shift(1)
            )
            &
            (
                dataframe["BULLISH"]
            )
            &
            (
                dataframe["open"]
                <
                dataframe["close"].shift(1)
            )
            &
            (
                dataframe["close"]
                >
                dataframe["open"].shift(1)
            )
        )

        app_logger.info(
            "Bullish Engulfing detection completed."
        )

        return dataframe  

    def detect_bearish_engulfing(
        self,
        dataframe
    ):
        """
        Detect Bearish Engulfing pattern.

        Rules:
        - Previous candle is Bullish
        - Current candle is Bearish
        - Current Open > Previous Close
        - Current Close < Previous Open
        """

        dataframe = dataframe.copy()

        dataframe["BEARISH_ENGULFING"] = (
            (
                dataframe["BULLISH"].shift(1)
            )
            &
            (
                dataframe["BEARISH"]
            )
            &
            (
                dataframe["open"]
                >
                dataframe["close"].shift(1)
            )
            &
            (
                dataframe["close"]
                <
                dataframe["open"].shift(1)
            )
        )

        app_logger.info(
            "Bearish Engulfing detection completed."
        )

        return dataframe         

    def detect_piercing_pattern(
        self,
        dataframe
    ):
        """
        Detect Piercing Pattern.

        Rules:
        - Previous candle is Bearish
        - Current candle is Bullish
        - Current Open < Previous Close
        - Current Close > Midpoint of Previous Body
        """

        dataframe = dataframe.copy()

        previous_midpoint = (
            dataframe["open"].shift(1)
            +
            dataframe["close"].shift(1)
        ) / 2

        dataframe["PIERCING_PATTERN"] = (
            (
                dataframe["BEARISH"].shift(1)
            )
            &
            (
                dataframe["BULLISH"]
            )
            &
            (
                dataframe["open"]
                <
                dataframe["close"].shift(1)
            )
            &
            (
                dataframe["close"]
                >
                previous_midpoint
            )
        )

        app_logger.info(
            "Piercing Pattern detection completed."
        )

        return dataframe    

    def detect_dark_cloud_cover(
        self,
        dataframe
    ):
        """
        Detect Dark Cloud Cover pattern.

        Rules:
        - Previous candle is Bullish
        - Current candle is Bearish
        - Current Open > Previous Close
        - Current Close < Previous Body Midpoint
        """

        dataframe = dataframe.copy()

        previous_open = dataframe["open"].shift(1)
        previous_close = dataframe["close"].shift(1)

        previous_body_midpoint = (
            previous_open + previous_close
        ) / 2

        dataframe["DARK_CLOUD_COVER"] = (
            (
                dataframe["BEARISH"]
            )
            &
            (
                dataframe["BULLISH"].shift(1)
            )
            &
            (
                dataframe["open"]
                >
                previous_close
            )
            &
            (
                dataframe["close"]
                <
                previous_body_midpoint
            )
        )

        app_logger.info(
            "Dark Cloud Cover detection completed."
        )

        return dataframe

    def detect_harami(
        self,
        dataframe
    ):
        """
        Detect Bullish Harami and Bearish Harami patterns.

        Bullish Harami:
        - Previous candle is Bearish
        - Current candle is Bullish
        - Current body completely inside previous body

        Bearish Harami:
        - Previous candle is Bullish
        - Current candle is Bearish
        - Current body completely inside previous body
        """

        dataframe = dataframe.copy()

        dataframe["BULLISH_HARAMI"] = False
        dataframe["BEARISH_HARAMI"] = False

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            previous_body_high = max(
                previous["open"],
                previous["close"]
            )

            previous_body_low = min(
                previous["open"],
                previous["close"]
            )

            current_body_high = max(
                current["open"],
                current["close"]
            )

            current_body_low = min(
                current["open"],
                current["close"]
            )

            # -----------------------------
            # Bullish Harami
            # -----------------------------
            if (
                previous["BEARISH"]
                and current["BULLISH"]
                and current_body_high < previous_body_high
                and current_body_low > previous_body_low
            ):
                dataframe.loc[
                    dataframe.index[i],
                    "BULLISH_HARAMI"
                ] = True

            # -----------------------------
            # Bearish Harami
            # -----------------------------
            if (
                previous["BULLISH"]
                and current["BEARISH"]
                and current_body_high < previous_body_high
                and current_body_low > previous_body_low
            ):
                dataframe.loc[
                    dataframe.index[i],
                    "BEARISH_HARAMI"
                ] = True

        app_logger.info(
            "Harami detection completed."
        )

        return dataframe      

    def detect_morning_star(
        self,
        dataframe
    ):
        """
        Detect Morning Star pattern.

        Rules

        Candle 1
        - Bearish

        Candle 2
        - Small body (<=30% of range)

        Candle 3
        - Bullish
        - Close above midpoint of Candle 1
        """

        dataframe = dataframe.copy()

        dataframe["MORNING_STAR"] = False

        for i in range(2, len(dataframe)):

            candle1 = dataframe.iloc[i - 2]
            candle2 = dataframe.iloc[i - 1]
            candle3 = dataframe.iloc[i]

            midpoint = (
                candle1["open"] +
                candle1["close"]
            ) / 2

            if (

                candle1["BEARISH"]

                and

                (
                    candle2["BODY"]
                    <=
                    candle2["RANGE"] * 0.30
                )

                and

                candle3["BULLISH"]

                and

                (
                    candle3["close"]
                    >
                    midpoint
                )

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "MORNING_STAR"
                ] = True

        app_logger.info(
            "Morning Star detection completed."
        )

        return dataframe 

    def detect_evening_star(
        self,
        dataframe
    ):
        """
        Detect Evening Star pattern.

        Rules:
        Candle 1:
            Strong Bullish

        Candle 2:
            Small body

        Candle 3:
            Strong Bearish
            Close below midpoint of Candle 1
        """

        dataframe = dataframe.copy()

        dataframe["EVENING_STAR"] = False

        for i in range(2, len(dataframe)):

            first = dataframe.iloc[i - 2]
            second = dataframe.iloc[i - 1]
            third = dataframe.iloc[i]

            midpoint = (
                first["open"] +
                first["close"]
            ) / 2

            if (

                first["BULLISH"]

                and

                second["BODY"]
                <=
                (
                    second["RANGE"] * 0.30
                )

                and

                third["BEARISH"]

                and

                third["close"] < midpoint

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "EVENING_STAR"
                ] = True

        app_logger.info(
            "Evening Star detection completed."
        )

        return dataframe  

    def detect_three_white_soldiers(
        self,
        dataframe
    ):
        """
        Detect Three White Soldiers pattern.

        Rules:
        - Three consecutive Bullish candles
        - Each candle opens inside previous body
        - Each candle closes higher than previous close
        """

        dataframe = dataframe.copy()

        dataframe["THREE_WHITE_SOLDIERS"] = False

        for i in range(2, len(dataframe)):

            c1 = dataframe.iloc[i - 2]
            c2 = dataframe.iloc[i - 1]
            c3 = dataframe.iloc[i]

            if (

                c1["BULLISH"]
                and
                c2["BULLISH"]
                and
                c3["BULLISH"]

                and

                c2["open"] > c1["open"]
                and
                c2["open"] < c1["close"]

                and

                c3["open"] > c2["open"]
                and
                c3["open"] < c2["close"]

                and

                c2["close"] > c1["close"]
                and
                c3["close"] > c2["close"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "THREE_WHITE_SOLDIERS"
                ] = True

        app_logger.info(
            "Three White Soldiers detection completed."
        )

        return dataframe  

    def detect_three_black_crows(
        self,
        dataframe
    ):
        """
        Detect Three Black Crows pattern.

        Rules:
        - Three consecutive bearish candles
        - Each close lower than previous close
        - Each open inside previous candle body
        """

        dataframe = dataframe.copy()

        dataframe["THREE_BLACK_CROWS"] = (
            (
                dataframe["BEARISH"]
            )
            &
            (
                dataframe["BEARISH"].shift(1)
            )
            &
            (
                dataframe["BEARISH"].shift(2)
            )
            &
            (
                dataframe["close"]
                <
                dataframe["close"].shift(1)
            )
            &
            (
                dataframe["close"].shift(1)
                <
                dataframe["close"].shift(2)
            )
            &
            (
                dataframe["open"]
                <
                dataframe["open"].shift(1)
            )
            &
            (
                dataframe["open"]
                >
                dataframe["close"].shift(1)
            )
            &
            (
                dataframe["open"].shift(1)
                <
                dataframe["open"].shift(2)
            )
            &
            (
                dataframe["open"].shift(1)
                >
                dataframe["close"].shift(2)
            )
        )

        app_logger.info(
            "Three Black Crows detection completed."
        )

        return dataframe  

    def detect_tweezer_top(
        self,
        dataframe
    ):
        """
        Detect Tweezer Top pattern.

        Rules:
        - Previous candle is Bullish
        - Current candle is Bearish
        - Highs are approximately equal
        """

        dataframe = dataframe.copy()

        tolerance = 0.001

        dataframe["TWEEZER_TOP"] = (
            (
                dataframe["BULLISH"].shift(1)
            )
            &
            (
                dataframe["BEARISH"]
            )
            &
            (
                (
                    dataframe["high"]
                    -
                    dataframe["high"].shift(1)
                ).abs()
                <=
                tolerance
            )
        )

        app_logger.info(
            "Tweezer Top detection completed."
        )

        return dataframe  

    def detect_tweezer_bottom(
        self,
        dataframe,
        tolerance=0.20
    ):
        """
        Detect Tweezer Bottom pattern.

        Rules:
        - Previous candle is Bearish
        - Current candle is Bullish
        - Both candles have nearly equal lows
        """

        dataframe = dataframe.copy()

        dataframe["TWEEZER_BOTTOM"] = (
            (
                dataframe["BEARISH"].shift(1)
            )
            &
            (
                dataframe["BULLISH"]
            )
            &
            (
                (
                    dataframe["low"]
                    -
                    dataframe["low"].shift(1)
                ).abs()
                <=
                tolerance
            )
        )

        app_logger.info(
            "Tweezer Bottom detection completed."
        )

        return dataframe 

    def detect_inside_bar(
        self,
        dataframe
    ):
        """
        Detect Inside Bar pattern.

        Rules:
        - Current High < Previous High
        - Current Low > Previous Low
        """

        dataframe = dataframe.copy()

        dataframe["INSIDE_BAR"] = (
            (
                dataframe["high"]
                <
                dataframe["high"].shift(1)
            )
            &
            (
                dataframe["low"]
                >
                dataframe["low"].shift(1)
            )
        )

        app_logger.info(
            "Inside Bar detection completed."
        )

        return dataframe  

    def detect_outside_bar(
        self,
        dataframe
    ):
        """
        Detect Outside Bar.

        Rules:
        - Current High > Previous High
        - Current Low < Previous Low
        """

        dataframe = dataframe.copy()

        dataframe["OUTSIDE_BAR"] = (
            (
                dataframe["high"]
                >
                dataframe["high"].shift(1)
            )
            &
            (
                dataframe["low"]
                <
                dataframe["low"].shift(1)
            )
        )

        app_logger.info(
            "Outside Bar detection completed."
        )

        return dataframe   

    def detect_rising_three_methods(
        self,
        dataframe
    ):
        """
        Detect Rising Three Methods.

        Rules:
        - Candle 1 : Large Bullish
        - Candle 2 : Small Bearish inside Candle 1
        - Candle 3 : Small Bearish inside Candle 1
        - Candle 4 : Small Bearish inside Candle 1
        - Candle 5 : Strong Bullish closes above Candle 1 High
        """

        dataframe = dataframe.copy()

        dataframe["RISING_THREE_METHODS"] = False

        for i in range(4, len(dataframe)):

            c1 = dataframe.iloc[i - 4]
            c2 = dataframe.iloc[i - 3]
            c3 = dataframe.iloc[i - 2]
            c4 = dataframe.iloc[i - 1]
            c5 = dataframe.iloc[i]

            inside_1 = (
                c2["high"] < c1["high"]
                and
                c2["low"] > c1["low"]
            )

            inside_2 = (
                c3["high"] < c1["high"]
                and
                c3["low"] > c1["low"]
            )

            inside_3 = (
                c4["high"] < c1["high"]
                and
                c4["low"] > c1["low"]
            )

            if (

                c1["BULLISH"]

                and

                c2["BEARISH"]

                and

                c3["BEARISH"]

                and

                c4["BEARISH"]

                and

                c5["BULLISH"]

                and

                inside_1

                and

                inside_2

                and

                inside_3

                and

                c5["close"] > c1["high"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "RISING_THREE_METHODS"
                ] = True

        app_logger.info(
            "Rising Three Methods detection completed."
        )

        return dataframe   

    def detect_falling_three_methods(
        self,
        dataframe
    ):
        """
        Detect Falling Three Methods.

        Rules:
        - Candle 1 : Large Bearish
        - Candle 2 : Small Bullish inside Candle 1
        - Candle 3 : Small Bullish inside Candle 1
        - Candle 4 : Small Bullish inside Candle 1
        - Candle 5 : Strong Bearish closes below Candle 1 Low
        """

        dataframe = dataframe.copy()

        dataframe["FALLING_THREE_METHODS"] = False

        for i in range(4, len(dataframe)):

            c1 = dataframe.iloc[i - 4]
            c2 = dataframe.iloc[i - 3]
            c3 = dataframe.iloc[i - 2]
            c4 = dataframe.iloc[i - 1]
            c5 = dataframe.iloc[i]

            inside_1 = (
                c2["high"] < c1["high"]
                and
                c2["low"] > c1["low"]
            )

            inside_2 = (
                c3["high"] < c1["high"]
                and
                c3["low"] > c1["low"]
            )

            inside_3 = (
                c4["high"] < c1["high"]
                and
                c4["low"] > c1["low"]
            )

            if (

                c1["BEARISH"]

                and

                c2["BULLISH"]

                and

                c3["BULLISH"]

                and

                c4["BULLISH"]

                and

                c5["BEARISH"]

                and

                inside_1

                and

                inside_2

                and

                inside_3

                and

                c5["close"] < c1["low"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "FALLING_THREE_METHODS"
                ] = True

        app_logger.info(
            "Falling Three Methods detection completed."
        )

        return dataframe                                                                        

    def detect_bullish_marubozu(
        self,
        dataframe
    ):
        """
        Detect Bullish Marubozu candlestick pattern.

        Rules:
        - Bullish candle
        - Upper wick <= 5% of body
        - Lower wick <= 5% of body
        """

        dataframe = dataframe.copy()

        dataframe["BULLISH_MARUBOZU"] = (
            (
                dataframe["UPPER_WICK"]
                <=
                (dataframe["BODY"] * 0.05)
            )
            &
            (
                dataframe["LOWER_WICK"]
                <=
                (dataframe["BODY"] * 0.05)
            )
            &
            (
                dataframe["BULLISH"]
            )
        )

        app_logger.info(
            "Bullish Marubozu detection completed."
        )

        return dataframe        

    def detect_bearish_marubozu(
        self,
        dataframe
    ):
        """
        Detect Bearish Marubozu candlestick pattern.

        Rules:
        - Bearish candle
        - Upper wick <= 5% of body
        - Lower wick <= 5% of body
        """

        dataframe = dataframe.copy()

        dataframe["BEARISH_MARUBOZU"] = (
            (
                dataframe["UPPER_WICK"]
                <=
                (dataframe["BODY"] * 0.05)
            )
            &
            (
                dataframe["LOWER_WICK"]
                <=
                (dataframe["BODY"] * 0.05)
            )
            &
            (
                dataframe["BEARISH"]
            )
        )

        app_logger.info(
            "Bearish Marubozu detection completed."
        )

        return dataframe

    def detect_three_inside_up(
        self,
        dataframe
    ):
        """
        Detect Three Inside Up pattern.

        Rules:
        - Candle 1 : Bearish
        - Candle 2 : Bullish Harami
        - Candle 3 : Bullish
        - Candle 3 closes above Candle 1 open
        """

        dataframe = dataframe.copy()

        dataframe["THREE_INSIDE_UP"] = False

        for i in range(2, len(dataframe)):

            c1 = dataframe.iloc[i - 2]
            c2 = dataframe.iloc[i - 1]
            c3 = dataframe.iloc[i]

            c1_body_high = max(
                c1["open"],
                c1["close"]
            )

            c1_body_low = min(
                c1["open"],
                c1["close"]
            )

            c2_body_high = max(
                c2["open"],
                c2["close"]
            )

            c2_body_low = min(
                c2["open"],
                c2["close"]
            )

            if (

                c1["BEARISH"]

                and

                c2["BULLISH"]

                and

                c2_body_high < c1_body_high

                and

                c2_body_low > c1_body_low

                and

                c3["BULLISH"]

                and

                c3["close"] > c1["open"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "THREE_INSIDE_UP"
                ] = True

        app_logger.info(
            "Three Inside Up detection completed."
        )

        return dataframe

    def detect_three_inside_down(
        self,
        dataframe
    ):
        """
        Detect Three Inside Down pattern.

        Rules:
        - Candle 1 : Bullish
        - Candle 2 : Bearish body completely inside Candle 1 body
        - Candle 3 : Bearish closes below Candle 1 open
        """

        dataframe = dataframe.copy()

        dataframe["THREE_INSIDE_DOWN"] = False

        for i in range(2, len(dataframe)):

            candle1 = dataframe.iloc[i - 2]
            candle2 = dataframe.iloc[i - 1]
            candle3 = dataframe.iloc[i]

            body1_high = max(
                candle1["open"],
                candle1["close"]
            )

            body1_low = min(
                candle1["open"],
                candle1["close"]
            )

            body2_high = max(
                candle2["open"],
                candle2["close"]
            )

            body2_low = min(
                candle2["open"],
                candle2["close"]
            )

            if (

                candle1["BULLISH"]

                and

                candle2["BEARISH"]

                and

                body2_high < body1_high

                and

                body2_low > body1_low

                and

                candle3["BEARISH"]

                and

                candle3["close"] < candle1["open"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "THREE_INSIDE_DOWN"
                ] = True

        app_logger.info(
            "Three Inside Down detection completed."
        )

        return dataframe

    def detect_tasuki_gap(
        self,
        dataframe
    ):
        """
        Detect Bullish and Bearish Tasuki Gap.

        Bullish Tasuki Gap:
        - Candle 1 Bullish
        - Candle 2 Bullish with Gap Up
        - Candle 3 Bearish
        - Candle 3 closes inside the gap
        - Gap not completely filled

        Bearish Tasuki Gap:
        - Candle 1 Bearish
        - Candle 2 Bearish with Gap Down
        - Candle 3 Bullish
        - Candle 3 closes inside the gap
        - Gap not completely filled
        """

        dataframe = dataframe.copy()

        dataframe["BULLISH_TASUKI_GAP"] = False
        dataframe["BEARISH_TASUKI_GAP"] = False

        for i in range(2, len(dataframe)):

            c1 = dataframe.iloc[i - 2]
            c2 = dataframe.iloc[i - 1]
            c3 = dataframe.iloc[i]

            # ---------------------------------
            # Bullish Tasuki Gap
            # ---------------------------------

            if (

                c1["BULLISH"]

                and

                c2["BULLISH"]

                and

                c2["low"] > c1["high"]

                and

                c3["BEARISH"]

                and

                c3["close"] < c2["open"]

                and

                c3["close"] > c1["high"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "BULLISH_TASUKI_GAP"
                ] = True

            # ---------------------------------
            # Bearish Tasuki Gap
            # ---------------------------------

            if (

                c1["BEARISH"]

                and

                c2["BEARISH"]

                and

                c2["high"] < c1["low"]

                and

                c3["BULLISH"]

                and

                c3["close"] > c2["open"]

                and

                c3["close"] < c1["low"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "BEARISH_TASUKI_GAP"
                ] = True

        app_logger.info(
            "Tasuki Gap detection completed."
        )

        return dataframe

    def detect_kicking_pattern(
        self,
        dataframe
    ):
        """
        Detect Bullish and Bearish Kicking Pattern.

        Rules

        Bullish Kicking
        - Candle 1 Bearish Marubozu
        - Candle 2 Bullish Marubozu
        - Gap Up between both candles

        Bearish Kicking
        - Candle 1 Bullish Marubozu
        - Candle 2 Bearish Marubozu
        - Gap Down between both candles
        """

        dataframe = dataframe.copy()

        dataframe["BULLISH_KICKING"] = False
        dataframe["BEARISH_KICKING"] = False

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            # ---------------------------------
            # Bullish Kicking
            # ---------------------------------

            if (

                previous["BEARISH_MARUBOZU"]

                and

                current["BULLISH_MARUBOZU"]

                and

                current["low"] > previous["high"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "BULLISH_KICKING"
                ] = True

            # ---------------------------------
            # Bearish Kicking
            # ---------------------------------

            if (

                previous["BULLISH_MARUBOZU"]

                and

                current["BEARISH_MARUBOZU"]

                and

                current["high"] < previous["low"]

            ):

                dataframe.loc[
                    dataframe.index[i],
                    "BEARISH_KICKING"
                ] = True

        app_logger.info(
            "Kicking Pattern detection completed."
        )

        return dataframe
    def detect_belt_hold(
        self,
        dataframe
    ):
        """
        Detect Bullish and Bearish Belt Hold patterns.

        Bullish Belt Hold
        - Bullish candle
        - Opens at (or very near) the Low
        - Strong bullish body

        Bearish Belt Hold
        - Bearish candle
        - Opens at (or very near) the High
        - Strong bearish body
        """

        dataframe = dataframe.copy()

        tolerance = 0.001

        dataframe["BULLISH_BELT_HOLD"] = (

            dataframe["BULLISH"]

            &

            (
                (
                    dataframe["open"]
                    -
                    dataframe["low"]
                ).abs()
                <=
                tolerance
            )

            &

            (
                dataframe["BODY"]
                >=
                dataframe["RANGE"] * 0.60
            )

        )

        dataframe["BEARISH_BELT_HOLD"] = (

            dataframe["BEARISH"]

            &

            (
                (
                    dataframe["high"]
                    -
                    dataframe["open"]
                ).abs()
                <=
                tolerance
            )

            &

            (
                dataframe["BODY"]
                >=
                dataframe["RANGE"] * 0.60
            )

        )

        app_logger.info(
            "Belt Hold detection completed."
        )

        return dataframe                                       