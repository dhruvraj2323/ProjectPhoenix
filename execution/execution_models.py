"""
Project Phoenix
Milestone M10 - Execution Rules Engine

Module:
    execution_models.py

Purpose:
    Defines all shared data models used by the Execution Rules Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from risk.risk_models import RiskDecision


class OrderSide(Enum):
    """
    Direction of the execution order.
    """

    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """
    Type of execution order.
    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


class ExecutionStatus(Enum):
    """
    Current execution status.
    """

    READY = "READY"
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


@dataclass
class ExecutionContext:
    """
    Context supplied to the Execution Engine.
    """

    risk_decision: RiskDecision

    symbol: str

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrderRequest:
    """
    Broker order request prepared by the Execution Engine.
    """

    symbol: str

    side: OrderSide

    order_type: OrderType

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    comment: str = ""

    magic_number: Optional[int] = None


@dataclass
class ExecutionDecision:
    """
    Final execution decision returned by the Execution Engine.
    """

    status: ExecutionStatus

    order: OrderRequest

    approved: bool

    reason: str