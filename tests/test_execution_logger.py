"""
Test for execution_logger.py
"""

from execution.execution_logger import ExecutionLogger
from execution.execution_models import (
    ExecutionDecision,
    ExecutionStatus,
    OrderRequest,
    OrderSide,
    OrderType,
)

order = OrderRequest(
    symbol="XAUUSD",
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    volume=0.10,
    entry_price=3350.0,
    stop_loss=3345.0,
    take_profit=3360.0,
)

decision = ExecutionDecision(
    status=ExecutionStatus.READY,
    order=order,
    approved=True,
    reason="Execution validation passed.",
)

logger = ExecutionLogger()

logger.log(decision)