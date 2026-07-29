from market_data.historical_parser import HistoricalParser
from market_data.timeframe_converter import TimeframeConverter


def test_timeframe_converter():

    parser = HistoricalParser()

    candles = parser.parse_file(
        "data/raw/historical/test_sample.txt"
    )

    converter = TimeframeConverter()

    result = converter.convert(
        candles,
        "M5",
    )

    assert len(candles) > 0
    assert len(result) > 0

    first = result[0]

    assert "datetime" in first
    assert "open" in first
    assert "high" in first
    assert "low" in first
    assert "close" in first
    assert "volume" in first