"""
Project Phoenix
Milestone M18 - Configuration & Settings Engine

Module:
    config_validator.py

Purpose:
    Validates configuration items.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.config_models import (
    ConfigurationItem,
)


@dataclass
class ConfigurationValidationResult:
    """
    Result returned by the Configuration Validator.
    """

    valid: bool

    reason: str


class ConfigurationValidator:
    """
    Validates configuration items.
    """

    def validate(
        self,
        items: list[ConfigurationItem],
    ) -> ConfigurationValidationResult:
        """
        Validate configuration.
        """

        if not items:

            return ConfigurationValidationResult(

                valid=False,

                reason="No configuration items found.",

            )

        keys: set[str] = set()

        for item in items:

            if not item.key.strip():

                return ConfigurationValidationResult(

                    valid=False,

                    reason="Configuration key is required.",

                )

            if item.key in keys:

                return ConfigurationValidationResult(

                    valid=False,

                    reason=f"Duplicate configuration key: {item.key}",

                )

            keys.add(item.key)

            if item.value is None:

                return ConfigurationValidationResult(

                    valid=False,

                    reason=f"Configuration value missing for '{item.key}'.",

                )

        return ConfigurationValidationResult(

            valid=True,

            reason="Configuration validation passed.",

        )