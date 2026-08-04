"""
=================================================
Project Phoenix
Session Controller Test
M56
=================================================
"""

from live_trading.live_context import (
    LiveContext,
)
from orchestrator_engine.session_controller import (
    SessionController,
)
from paper_trading.paper_context import (
    PaperContext,
)


def test_session_controller():

    controller = SessionController()

    # ---------------------------------------
    # Paper Session
    # ---------------------------------------

    paper = PaperContext(
        paper_id="PAPER-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    paper.execution_result = object()

    paper_result = controller.execute(
        paper,
        live_mode=False,
    )

    assert paper_result.completed

    assert paper_result.metadata[
        "session_started"
    ]

    assert paper_result.metadata[
        "session_completed"
    ]

    # ---------------------------------------
    # Live Session
    # ---------------------------------------

    live = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    live.execution_result = object()

    live.market_price = 1.1050

    live_result = controller.execute(
        live,
        live_mode=True,
    )

    assert live_result.completed

    assert live_result.metadata[
        "session_started"
    ]

    assert live_result.metadata[
        "session_completed"
    ]