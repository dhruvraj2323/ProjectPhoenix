from market_data.historical_parser import HistoricalParser
from market_data.timeframe_converter import TimeframeConverter


def main():

    parser = HistoricalParser()

    candles = parser.parse_file(
        "data/raw/historical/test_sample.txt"
    )

    print("\nInput M1 Candles:")
    print(len(candles))


    converter = TimeframeConverter()

    result = converter.convert(
        candles,
        "M5"
    )


    print("\nM5 Candles:")
    print(len(result))


    if result:
        print("\nFirst M5 Candle:")
        print(result[0])


    print("\nStatus: PASS")


if __name__ == "__main__":
    main()