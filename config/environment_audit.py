"""
Project Phoenix - Environment Configuration Audit
M62.2.2.2
"""

from __future__ import annotations

import os

from config.environment_audit_models import (
    EnvironmentAuditResult,
    EnvironmentCheck,
)
from config.telegram_config import TelegramConfiguration
from config.telegram_config_validator import TelegramConfigurationValidator


class EnvironmentAudit:
    """
    Audits Project Phoenix environment configuration.

    This audit validates configuration only.
    It does not connect to MT5, Telegram, or execute trades.
    """

    MT5_LOGIN = "MT5_LOGIN"
    MT5_PASSWORD = "MT5_PASSWORD"
    MT5_SERVER = "MT5_SERVER"
    MT5_PATH = "MT5_PATH"

    TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"
    TELEGRAM_ENABLED = "TELEGRAM_ENABLED"

    _TRUE_VALUES = {"true"}
    _FALSE_VALUES = {"false"}

    def __init__(
        self,
        environment: dict[str, str] | None = None,
    ) -> None:
        """
        Initialize the environment audit.

        A custom environment mapping is supported so the audit can be
        tested without modifying the real process environment.
        """
        self._environment = (
            dict(os.environ)
            if environment is None
            else dict(environment)
        )

    def audit(self) -> EnvironmentAuditResult:
        """
        Execute the complete environment configuration audit.
        """
        checks: list[EnvironmentCheck] = []
        errors: list[str] = []
        warnings: list[str] = []

        checks.extend(
            [
                self._check_mt5_login(),
                self._check_mt5_password(),
                self._check_mt5_server(),
                self._check_mt5_path(),
            ]
        )

        telegram_enabled_check = (
            self._check_telegram_enabled()
        )
        checks.append(telegram_enabled_check)

        telegram_enabled = (
            telegram_enabled_check.approved
            and self._telegram_enabled()
        )

        if telegram_enabled:
            telegram_checks = (
                self._check_telegram_configuration()
            )
            checks.extend(telegram_checks)

        else:
            warnings.append(
                "Telegram alerting is disabled."
            )

        failed_required_checks = [
            check
            for check in checks
            if check.required and not check.approved
        ]

        errors.extend(
            check.message
            for check in failed_required_checks
        )

        return EnvironmentAuditResult(
            approved=not errors,
            checks=tuple(checks),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    def _check_mt5_login(self) -> EnvironmentCheck:
        value = self._get(self.MT5_LOGIN)

        if not value:
            return EnvironmentCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN is missing.",
            )

        try:
            login = int(value)
        except ValueError:
            return EnvironmentCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN must be numeric.",
            )

        if login <= 0:
            return EnvironmentCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN must be positive.",
            )

        return EnvironmentCheck(
            name=self.MT5_LOGIN,
            approved=True,
            required=True,
            message="MT5_LOGIN is valid.",
        )

    def _check_mt5_password(self) -> EnvironmentCheck:
        return self._check_non_empty_secret(
            self.MT5_PASSWORD,
            "MT5_PASSWORD is missing.",
        )

    def _check_mt5_server(self) -> EnvironmentCheck:
        return self._check_non_empty(
            self.MT5_SERVER,
            "MT5_SERVER is missing.",
        )

    def _check_mt5_path(self) -> EnvironmentCheck:
        return self._check_non_empty(
            self.MT5_PATH,
            "MT5_PATH is missing.",
        )

    def _check_telegram_enabled(self) -> EnvironmentCheck:
        value = self._get(
            self.TELEGRAM_ENABLED
        ).strip().lower()

        if not value:
            return EnvironmentCheck(
                name=self.TELEGRAM_ENABLED,
                approved=False,
                required=True,
                message=(
                    "TELEGRAM_ENABLED is missing."
                ),
            )

        if value not in (
            self._TRUE_VALUES
            | self._FALSE_VALUES
        ):
            return EnvironmentCheck(
                name=self.TELEGRAM_ENABLED,
                approved=False,
                required=True,
                message=(
                    "TELEGRAM_ENABLED must be "
                    "either 'true' or 'false'."
                ),
            )

        return EnvironmentCheck(
            name=self.TELEGRAM_ENABLED,
            approved=True,
            required=True,
            message=(
                "TELEGRAM_ENABLED is valid."
            ),
        )

    def _check_telegram_configuration(
        self,
    ) -> tuple[EnvironmentCheck, ...]:
        bot_token = self._get(
            self.TELEGRAM_BOT_TOKEN
        )
        chat_id = self._get(
            self.TELEGRAM_CHAT_ID
        )

        checks: list[EnvironmentCheck] = []

        if not bot_token:
            checks.append(
                EnvironmentCheck(
                    name=self.TELEGRAM_BOT_TOKEN,
                    approved=False,
                    required=True,
                    message=(
                        "TELEGRAM_BOT_TOKEN is missing."
                    ),
                    sensitive=True,
                )
            )
        else:
            checks.append(
                EnvironmentCheck(
                    name=self.TELEGRAM_BOT_TOKEN,
                    approved=True,
                    required=True,
                    message=(
                        "TELEGRAM_BOT_TOKEN is present."
                    ),
                    sensitive=True,
                )
            )

        if not chat_id:
            checks.append(
                EnvironmentCheck(
                    name=self.TELEGRAM_CHAT_ID,
                    approved=False,
                    required=True,
                    message=(
                        "TELEGRAM_CHAT_ID is missing."
                    ),
                )
            )
        else:
            checks.append(
                EnvironmentCheck(
                    name=self.TELEGRAM_CHAT_ID,
                    approved=True,
                    required=True,
                    message=(
                        "TELEGRAM_CHAT_ID is present."
                    ),
                )
            )

        if bot_token and chat_id:
            configuration = TelegramConfiguration(
                bot_token=bot_token,
                chat_id=chat_id,
                enabled=True,
            )

            valid = (
                TelegramConfigurationValidator.validate(
                    configuration
                )
            )

            if not valid:
                checks.append(
                    EnvironmentCheck(
                        name="TELEGRAM_CONFIGURATION",
                        approved=False,
                        required=True,
                        message=(
                            "Telegram configuration "
                            "failed validation."
                        ),
                    )
                )
            else:
                checks.append(
                    EnvironmentCheck(
                        name="TELEGRAM_CONFIGURATION",
                        approved=True,
                        required=True,
                        message=(
                            "Telegram configuration "
                            "passed validation."
                        ),
                    )
                )

        return tuple(checks)

    def _telegram_enabled(self) -> bool:
        return (
            self._get(self.TELEGRAM_ENABLED)
            .strip()
            .lower()
            == "true"
        )

    def _check_non_empty(
        self,
        name: str,
        error_message: str,
    ) -> EnvironmentCheck:
        value = self._get(name)

        return EnvironmentCheck(
            name=name,
            approved=bool(value),
            required=True,
            message=(
                "Configuration is present."
                if value
                else error_message
            ),
        )

    def _check_non_empty_secret(
        self,
        name: str,
        error_message: str,
    ) -> EnvironmentCheck:
        value = self._get(name)

        return EnvironmentCheck(
            name=name,
            approved=bool(value),
            required=True,
            message=(
                "Secret is present."
                if value
                else error_message
            ),
            sensitive=True,
        )

    def _get(self, name: str) -> str:
        return self._environment.get(name, "").strip()