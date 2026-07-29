"""
=================================================
Project Phoenix
Engine Contracts
M39
=================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from trading_system.trading_context import TradingContext


class EngineContract(ABC):
    """
    Base contract for every trading engine.
    """

    @abstractmethod
    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute engine logic.

        Every engine receives the same
        TradingContext and returns the
        updated TradingContext.
        """
        raise NotImplementedError


class MarketPipelineContract(
    EngineContract,
):
    """
    Market Pipeline interface.
    """

    pass


class StrategyEngineContract(
    EngineContract,
):
    """
    Strategy Engine interface.
    """

    pass


class RiskEngineContract(
    EngineContract,
):
    """
    Risk Engine interface.
    """

    pass


class AIDecisionContract(
    EngineContract,
):
    """
    AI Decision Engine interface.
    """

    pass


class ExecutionEngineContract(
    EngineContract,
):
    """
    Execution Engine interface.
    """

    pass


class PaperTradingContract(
    EngineContract,
):
    """
    Paper Trading Engine interface.
    """

    pass