"""
=================================================
Project Phoenix
Market Adapter Engine Test
=================================================
"""

from market_adapter.market_adapter_engine import MarketAdapterEngine


def run_test():

    engine = MarketAdapterEngine("MT5")

    result = engine.initialize()

    print()
    print("===== Market Adapter Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Market Adapter Engine Test Passed")


if __name__ == "__main__":

    run_test()