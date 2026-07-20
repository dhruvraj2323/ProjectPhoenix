"""
Project Phoenix
Historical Data Validation Test
Version: 1.0
"""

from market_data.historical_parser import HistoricalParser
from market_data.data_validator import DataValidator


TEST_FILE = (
    r"data\raw\historical\test_sample.txt"
)


parser = HistoricalParser()

validator = DataValidator()


# Parse data

candles = parser.parse_file(TEST_FILE)


print("\nParsed Candles:")
print(len(candles))


# Validate data

report = validator.validate(candles)


print("\nValidation Report:")

for key, value in report.items():

    print(
        f"{key}: {value}"
    )