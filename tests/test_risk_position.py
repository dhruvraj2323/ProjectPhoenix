"""
Test for risk_position.py
"""

from risk.risk_position import PositionSizer


sizer = PositionSizer()

position = sizer.calculate(
    account_balance=100000,
    risk_percent=1.0,
)

print("===== Position Size Test =====")
print(f"Quantity          : {position.quantity}")
print(f"Capital Allocated : {position.capital_allocated}")
print(f"Risk %            : {position.risk_percent}")