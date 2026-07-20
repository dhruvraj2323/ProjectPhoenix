"""
=================================================
Project Phoenix
Market Adapter Models Test
=================================================
"""

from datetime import datetime

from market_adapter.market_adapter_models import (
    MarketCandle,
    TickData,
    SymbolInformation,
    MarketStatus,
    MarketDataResult,
)


def run_test():

    candle = MarketCandle(
        symbol="EURUSD",
        timeframe="M15",
        timestamp=datetime.now(),
        open=1.1050,
        high=1.1070,
        low=1.1040,
        close=1.1065,
        volume=2500,
    )

    tick = TickData(
        symbol="EURUSD",
        bid=1.1064,
        ask=1.1066,
        last=1.1065,
        timestamp=datetime.now(),
    )

    symbol = SymbolInformation(
        symbol="EURUSD",
        digits=5,
        spread=12,
        trade_allowed=True,
    )

    status = MarketStatus(
        connected=True,
        market_open=True,
        provider_name="MT5",
    )

    result = MarketDataResult(
        approved=True,
        reason="Market adapter initialized successfully.",
        status=status,
    )

    print("===== Market Adapter Models =====")

    print(f"Symbol        : {candle.symbol}")
    print(f"Close Price   : {candle.close}")
    print(f"Bid           : {tick.bid}")
    print(f"Spread        : {symbol.spread}")
    print(f"Provider      : {status.provider_name}")

    assert result.approved

    print()
    print("Market Adapter Models Test Passed")


if __name__ == "__main__":
    run_test()