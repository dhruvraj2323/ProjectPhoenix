"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_exposure.py

Purpose:
    Calculates current portfolio exposure.
"""

from __future__ import annotations

from portfolio.portfolio_models import (
    ExposureInfo,
    PortfolioContext,
    PositionDirection,
)


class PortfolioExposure:
    """
    Calculates portfolio exposure.
    """

    def calculate(
        self,
        context: PortfolioContext,
    ) -> ExposureInfo:
        """
        Calculate portfolio exposure.
        """

        long_exposure = sum(

            position.volume

            for position in context.positions

            if position.direction
            == PositionDirection.BUY

        )

        short_exposure = sum(

            position.volume

            for position in context.positions

            if position.direction
            == PositionDirection.SELL

        )

        gross_exposure = (

            long_exposure
            +
            short_exposure

        )

        net_exposure = (

            long_exposure
            -
            short_exposure

        )

        symbol_exposure = {}

        currency_exposure = {}

        for position in context.positions:

            symbol_exposure[
                position.symbol
            ] = (

                symbol_exposure.get(
                    position.symbol,
                    0.0,
                )

                +

                position.volume

            )

            currency_exposure[
                position.currency
            ] = (

                currency_exposure.get(
                    position.currency,
                    0.0,
                )

                +

                position.volume

            )

        return ExposureInfo(

            gross_exposure=gross_exposure,

            net_exposure=net_exposure,

            long_exposure=long_exposure,

            short_exposure=short_exposure,

            symbol_exposure=symbol_exposure,

            currency_exposure=currency_exposure,

        )