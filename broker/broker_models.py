"""
=================================================
Project Phoenix
Broker Models
=================================================

Data models for broker abstraction.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Broker Account
# -------------------------------------------------


@dataclass(slots=True)
class BrokerAccount:
    """
    Broker account information.
    """

    account_id: int
    broker_name: str
    balance: float
    equity: float
    margin: float
    free_margin: float


# -------------------------------------------------
# Broker Order
# -------------------------------------------------


@dataclass(slots=True)
class BrokerOrder:
    """
    Order model.
    """

    ticket: int
    symbol: str
    order_type: str
    volume: float
    price: float
    status: str


# -------------------------------------------------
# Broker Position
# -------------------------------------------------


@dataclass(slots=True)
class BrokerPosition:
    """
    Position model.
    """

    ticket: int
    symbol: str
    direction: str
    volume: float
    open_price: float
    current_price: float
    profit: float


# -------------------------------------------------
# Broker Balance
# -------------------------------------------------


@dataclass(slots=True)
class BrokerBalance:
    """
    Account balance.
    """

    balance: float
    equity: float
    margin: float
    free_margin: float


# -------------------------------------------------
# Broker Symbol
# -------------------------------------------------


@dataclass(slots=True)
class BrokerSymbol:
    """
    Trading symbol.
    """

    symbol: str
    digits: int
    spread: int
    trade_allowed: bool


# -------------------------------------------------
# Broker Status
# -------------------------------------------------


@dataclass(slots=True)
class BrokerStatus:
    """
    Broker connection status.
    """

    connected: bool
    logged_in: bool
    broker_name: str


# -------------------------------------------------
# Broker Result
# -------------------------------------------------


@dataclass(slots=True)
class BrokerResult:
    """
    Final broker operation result.
    """

    approved: bool
    reason: str
    status: BrokerStatus