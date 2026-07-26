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

        long_exposure = 0.0
        short_exposure = 0.0

        symbol_exposure = {}
        currency_exposure = {}

        for position in context.positions:

            if position.volume <= 0:
                raise ValueError(
                    "Position volume must be greater than zero."
                )

            if position.direction == PositionDirection.BUY:
                long_exposure += position.volume
            else:
                short_exposure += position.volume

            symbol_exposure[position.symbol] = (
                symbol_exposure.get(
                    position.symbol,
                    0.0,
                )
                + position.volume
            )

            currency_exposure[position.currency] = (
                currency_exposure.get(
                    position.currency,
                    0.0,
                )
                + position.volume
            )

        gross_exposure = (
            long_exposure
            + short_exposure
        )

        net_exposure = (
            long_exposure
            - short_exposure
        )

        return ExposureInfo(
            gross_exposure=round(gross_exposure, 2),
            net_exposure=round(net_exposure, 2),
            long_exposure=round(long_exposure, 2),
            short_exposure=round(short_exposure, 2),
            symbol_exposure=symbol_exposure,
            currency_exposure=currency_exposure,
        )