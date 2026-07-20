"""
Project Phoenix
Historical Parser Test
Version: 1.0
"""

from market_data.historical_parser import HistoricalParser


TEST_FILE = (
    r"data\raw\historical\test_sample.txt"
)


parser = HistoricalParser()


candles = parser.parse_file(TEST_FILE)


print("\nTotal Candles:")
print(len(candles))


if candles:

    print("\nFirst Candle:")
    print(candles[0])


    print("\nLast Candle:")
    print(candles[-1])

else:

    print("No candles found")