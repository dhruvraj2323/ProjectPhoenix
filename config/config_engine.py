"""
Project Phoenix
Milestone M18 - Configuration & Settings Engine

Module:
    config_engine.py

Purpose:
    Coordinates the complete Configuration Engine.
"""

from __future__ import annotations

from config.config_loader import (
    ConfigurationLoader,
)
from config.config_logger import (
    ConfigurationLogger,
)
from config.config_models import (
    ConfigurationContext,
    ConfigurationDecision,
    ConfigurationStatus,
)
from config.config_validator import (
    ConfigurationValidator,
)


class ConfigurationEngine:
    """
    Coordinates the complete
    Configuration Engine.
    """

    def __init__(self) -> None:

        self.loader = ConfigurationLoader()

        self.validator = ConfigurationValidator()

        self.logger = ConfigurationLogger()

    def run(
        self,
        context: ConfigurationContext,
    ) -> ConfigurationDecision:
        """
        Execute complete configuration workflow.
        """

        items = self.loader.load(
            context
        )

        validation = self.validator.validate(
            items
        )

        decision = ConfigurationDecision(

            status=(
                ConfigurationStatus.APPROVED
                if validation.valid
                else ConfigurationStatus.REJECTED
            ),

            items=items,

            approved=validation.valid,

            reason=validation.reason,

        )

        self.logger.log(
            context,
            decision,
        )

        return decision