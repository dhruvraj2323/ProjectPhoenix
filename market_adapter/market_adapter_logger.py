"""
=================================================
Project Phoenix
Market Adapter Logger
=================================================
"""

from market_adapter.market_adapter_models import MarketDataResult


class MarketAdapterLogger:
    """
    Logs market adapter operations.
    """

    @staticmethod
    def log(result: MarketDataResult):

        print("===== Market Adapter =====")

        print(f"Approved      : {result.approved}")
        print(f"Reason        : {result.reason}")
        print()

        print(f"Provider      : {result.status.provider_name}")
        print(f"Connected     : {result.status.connected}")
        print(f"Market Open   : {result.status.market_open}")