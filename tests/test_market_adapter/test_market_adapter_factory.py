"""
=================================================
Project Phoenix
Market Adapter Factory Test
=================================================
"""

from market_adapter.market_adapter_factory import MarketAdapterFactory


def run_test():

    provider = MarketAdapterFactory.create("MT5")

    print("===== Market Adapter Factory =====")

    print(f"Provider       : MT5")
    print(f"Connected      : {provider.connect()}")
    print(f"Latest Price   : {provider.latest_price()}")
    print(f"Latest Tick    : {provider.latest_tick()}")
    print(f"Symbols        : {provider.symbols()}")

    assert provider.connect()
    assert provider.is_connected()

    print()
    print("Market Adapter Factory Test Passed")


if __name__ == "__main__":

    run_test()