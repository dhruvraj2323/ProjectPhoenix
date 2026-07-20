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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
class BrokerResult:
    """
    Final broker operation result.
    """

    approved: bool
    reason: str
    status: BrokerStatus