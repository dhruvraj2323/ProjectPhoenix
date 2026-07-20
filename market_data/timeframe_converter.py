from datetime import datetime


class TimeframeConverter:

    SUPPORTED_TIMEFRAMES = {
        "M5": 5,
        "M15": 15,
        "M30": 30,
        "H1": 60
    }

    def __init__(self):
        pass

    def convert(self, candles, timeframe):
        """
        Convert M1 candles into higher timeframe candles
        """

        if timeframe not in self.SUPPORTED_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        interval = self.SUPPORTED_TIMEFRAMES[timeframe]

        converted = []

        if not candles:
            return converted

        bucket = []
        current_bucket = None

        for candle in candles:

            minute = candle["datetime"].minute
            hour = candle["datetime"].hour

            total_minutes = hour * 60 + minute

            bucket_start = (
                total_minutes // interval
            ) * interval

            if current_bucket is None:
                current_bucket = bucket_start

            if bucket_start != current_bucket:

                converted.append(
                    self._create_candle(bucket)
                )

                bucket = []
                current_bucket = bucket_start

            bucket.append(candle)

        if bucket:
            converted.append(
                self._create_candle(bucket)
            )

        return converted


    def _create_candle(self, candles):

        return {
            "datetime": candles[0]["datetime"],
            "open": candles[0]["open"],
            "high": max(
                c["high"] for c in candles
            ),
            "low": min(
                c["low"] for c in candles
            ),
            "close": candles[-1]["close"],
            "volume": sum(
                c["volume"] for c in candles
            )
        }


if __name__ == "__main__":
    print(
        "Timeframe Converter Module Loaded Successfully"
    )