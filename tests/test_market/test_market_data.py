"""
=================================================
Project Phoenix
Market Data Manager Test
=================================================

Tests:
- Historical Data
- Current Tick
- Current Price
- Symbol Information
"""

from dataclasses import dataclass


# -------------------------------------------------
# Mock Market Data Manager
# -------------------------------------------------


@dataclass
class MarketData:

    def historical_data(self):

        return [
            {
                "time": "2026-07-20 09:15",
                "open": 100.00,
                "high": 101.50,
                "low": 99.80,
                "close": 101.20,
                "volume": 1250,
            },
            {
                "time": "2026-07-20 09:30",
                "open": 101.20,
                "high": 102.10,
                "low": 100.90,
                "close": 101.80,
                "volume": 1430,
            },
        ]

    def current_tick(self):

        return {
            "bid": 101.75,
            "ask": 101.80,
            "last": 101.78,
        }

    def current_price(self):

        return 101.78

    def symbol_info(self):

        return {
            "symbol": "EURUSD",
            "digits": 5,
            "point": 0.00001,
            "spread": 12,
        }


# -------------------------------------------------
# Test
# -------------------------------------------------


def run_test():

    market = MarketData()

    history = market.historical_data()
    tick = market.current_tick()
    price = market.current_price()
    symbol = market.symbol_info()

    print("===== Market Data =====")

    print(f"Historical Bars : {len(history)}")
    print(f"Current Bid     : {tick['bid']}")
    print(f"Current Ask     : {tick['ask']}")
    print(f"Last Price      : {tick['last']}")
    print(f"Current Price   : {price}")
    print(f"Symbol          : {symbol['symbol']}")
    print(f"Digits          : {symbol['digits']}")
    print(f"Spread          : {symbol['spread']}")

    assert len(history) > 0
    assert tick["bid"] > 0
    assert tick["ask"] > 0
    assert price > 0
    assert symbol["digits"] > 0

    print()
    print("Market Data Manager Test Passed")


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    run_test()