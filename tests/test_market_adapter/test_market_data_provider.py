"""
=================================================
Project Phoenix
Market Data Provider Test
=================================================
"""

from market_adapter.market_data_provider import MarketDataProvider


class DummyProvider(MarketDataProvider):

    def connect(self):
        return True

    def disconnect(self):
        return True

    def symbols(self):
        return ["EURUSD", "GBPUSD"]

    def latest_tick(self):
        return {"bid": 1.1064, "ask": 1.1066}

    def latest_price(self):
        return 1.1065

    def historical_data(self):
        return []

    def current_candle(self):
        return {}

    def market_status(self):
        return "OPEN"

    def is_connected(self):
        return True


def run_test():

    provider = DummyProvider()

    print("===== Market Data Provider =====")

    print(f"Connect        : {provider.connect()}")
    print(f"Connected      : {provider.is_connected()}")
    print(f"Latest Price   : {provider.latest_price()}")
    print(f"Latest Tick    : {provider.latest_tick()}")
    print(f"Symbols        : {provider.symbols()}")

    assert provider.connect()
    assert provider.is_connected()

    print()
    print("Market Data Provider Test Passed")


if __name__ == "__main__":

    run_test()