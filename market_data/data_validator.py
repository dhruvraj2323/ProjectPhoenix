"""
Project Phoenix
Historical Market Data Validator
Version: 1.0

Purpose:
    Validate parsed OHLCV historical market data.

Checks:
    1. Duplicate timestamps
    2. Missing candles
    3. Invalid OHLC structure
"""

from datetime import timedelta


class DataValidator:
    """
    Historical candle validation engine.
    """

    def __init__(self):

        self.report = {
            "total_candles": 0,
            "duplicate_timestamps": 0,
            "missing_candles": 0,
            "invalid_ohlc": 0,
            "status": "UNKNOWN",
        }

    def validate_duplicates(self, candles):
        """
        Check duplicate datetime entries.
        """

        timestamps = set()
        duplicates = 0

        for candle in candles:

            dt = candle["datetime"]

            if dt in timestamps:
                duplicates += 1
            else:
                timestamps.add(dt)

        return duplicates

    def validate_ohlc(self, candles):
        """
        Validate OHLC relationship.

        Rules:
            High >= Open
            High >= Close
            Low <= Open
            Low <= Close
        """

        invalid = 0

        for candle in candles:

            o = candle["open"]
            h = candle["high"]
            l = candle["low"]
            c = candle["close"]

            if (
                h < o
                or h < c
                or l > o
                or l > c
            ):
                invalid += 1

        return invalid

    def validate_missing_minutes(self, candles):
        """
        Detect missing M1 candles.
        """

        if len(candles) < 2:
            return 0

        missing = 0

        sorted_candles = sorted(
            candles,
            key=lambda x: x["datetime"],
        )

        for i in range(len(sorted_candles) - 1):

            current_time = sorted_candles[i]["datetime"]
            next_time = sorted_candles[i + 1]["datetime"]

            difference = next_time - current_time

            if difference > timedelta(minutes=1):

                missing += (
                    int(difference.total_seconds() / 60) - 1
                )

        return missing

    def validate(self, candles):
        """
        Run complete validation.
        """

        self.report = {
            "total_candles": len(candles),
            "duplicate_timestamps": self.validate_duplicates(candles),
            "missing_candles": self.validate_missing_minutes(candles),
            "invalid_ohlc": self.validate_ohlc(candles),
            "status": "UNKNOWN",
        }

        if (
            self.report["duplicate_timestamps"] == 0
            and self.report["missing_candles"] == 0
            and self.report["invalid_ohlc"] == 0
        ):
            self.report["status"] = "PASS"
        else:
            self.report["status"] = "FAIL"

        return self.report


if __name__ == "__main__":

    print(
        "Data Validator Module Loaded Successfully"
    )