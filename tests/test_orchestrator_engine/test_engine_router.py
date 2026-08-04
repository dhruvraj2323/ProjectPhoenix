"""
=================================================
Project Phoenix
Engine Router Test
M56.1
=================================================
"""

from orchestrator_engine.engine_router import EngineRouter

from paper_trading.paper_context import PaperContext

from live_trading.live_context import LiveContext


def test_engine_router():

    router = EngineRouter()

    paper_context = PaperContext(
        paper_id="PAPER-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    paper_context.execution_result = object()

    paper_result = router.route(
        paper_context,
        live_mode=False,
    )

    assert paper_result.completed

    live_context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    live_context.execution_result = object()
    
    live_context.market_price = 1.1050
    
    live_result = router.route(
        live_context,
        live_mode=True,
    )

    assert live_result.completed