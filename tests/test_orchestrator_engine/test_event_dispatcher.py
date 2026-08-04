"""
=================================================
Project Phoenix
Event Dispatcher Test
M56
=================================================
"""

from live_trading.live_context import LiveContext
from orchestrator_engine.event_dispatcher import EventDispatcher
from paper_trading.paper_context import PaperContext


def test_event_dispatcher():

    dispatcher = EventDispatcher()

    # -----------------------------------------
    # Paper Trading
    # -----------------------------------------

    paper = PaperContext(
        paper_id="PAPER-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    paper.execution_result = object()

    paper_result = dispatcher.dispatch(
        paper,
        live_mode=False,
    )

    assert paper_result.completed

    # -----------------------------------------
    # Live Trading
    # -----------------------------------------

    live = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    live.execution_result = object()

    live.market_price = 1.1050

    live_result = dispatcher.dispatch(
        live,
        live_mode=True,
    )

    assert live_result.completed