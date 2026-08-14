"""
Project Phoenix - Runtime Readiness Adapter
M62.3.1
"""

from __future__ import annotations

from dataclasses import dataclass

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)


@dataclass(frozen=True)
class RuntimeReadiness:
    """
    Represents runtime-facing configuration readiness.

    This is an adapter over the configuration readiness
    result. It does not connect to MT5 or start runtime.
    """

    ready: bool
    reason: str
    configuration_result: ConfigurationReadinessResult

    @property
    def configuration_ready(self) -> bool:
        """Return the underlying configuration readiness."""
        return self.configuration_result.ready


class RuntimeReadinessAdapter:
    """
    Convert configuration readiness into a runtime-facing
    readiness decision.
    """

    @staticmethod
    def evaluate(
        result: ConfigurationReadinessResult,
    ) -> RuntimeReadiness:
        """
        Adapt a configuration readiness result.

        No external connection or runtime startup is performed.
        """

        if result.ready:
            return RuntimeReadiness(
                ready=True,
                reason=(
                    "Runtime configuration is ready."
                ),
                configuration_result=result,
            )

        return RuntimeReadiness(
            ready=False,
            reason=(
                "Runtime configuration is not ready."
            ),
            configuration_result=result,
        )