"""
Test for execution_validator.py
"""

from execution.execution_models import (
    OrderRequest,
    OrderSide,
    OrderType,
)
from execution.execution_validator import ExecutionValidator

order = OrderRequest(
    symbol="XAUUSD",
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    volume=0.10,
    entry_price=3350.0,
    stop_loss=3345.0,
    take_profit=3360.0,
)

validator = ExecutionValidator()

result = validator.validate(order)

print("===== Execution Validator Test =====")
print(f"Valid  : {result.valid}")
print(f"Reason : {result.reason}")