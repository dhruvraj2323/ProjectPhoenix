"""
Project Phoenix - MT5 Configuration Audit
M62.2.3.2
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping

from config.mt5_configuration_audit_models import (
    MT5ConfigurationAuditResult,
    MT5ConfigurationCheck,
)


class MT5ConfigurationAudit:
    """
    Audits the MT5 configuration without connecting to MT5.

    Validation sources:

    Environment:
        MT5_LOGIN
        MT5_PASSWORD
        MT5_SERVER
        MT5_PATH

    Credential file:
        config/mt5_credentials.json
            login
            password
            server
    """

    DEFAULT_CREDENTIAL_FILE = (
        Path("config") / "mt5_credentials.json"
    )

    MT5_LOGIN = "MT5_LOGIN"
    MT5_PASSWORD = "MT5_PASSWORD"
    MT5_SERVER = "MT5_SERVER"
    MT5_PATH = "MT5_PATH"

    def __init__(
        self,
        environment: Mapping[str, str] | None = None,
        credential_file: Path | str | None = None,
    ) -> None:
        """
        Initialize the MT5 configuration audit.

        A custom environment and credential file can be supplied
        for deterministic testing.
        """
        self._environment = (
            dict(os.environ)
            if environment is None
            else dict(environment)
        )

        self._credential_file = Path(
            credential_file
            if credential_file is not None
            else self.DEFAULT_CREDENTIAL_FILE
        )

    def audit(self) -> MT5ConfigurationAuditResult:
        """
        Execute the complete MT5 configuration audit.
        """
        checks: list[MT5ConfigurationCheck] = []
        errors: list[str] = []
        warnings: list[str] = []

        environment_checks = (
            self._audit_environment()
        )
        checks.extend(environment_checks)

        environment_valid = all(
            check.approved
            for check in environment_checks
            if check.required
        )

        (
            credential_file_present,
            credential_file_valid,
            credentials,
            credential_checks,
        ) = self._audit_credential_file()

        checks.extend(credential_checks)

        consistency_checks = (
            self._audit_consistency(
                credentials=credentials,
                credential_file_valid=(
                    credential_file_valid
                ),
            )
        )
        checks.extend(consistency_checks)

        consistency_valid = all(
            check.approved
            for check in consistency_checks
            if check.required
        )

        errors.extend(
            check.message
            for check in checks
            if check.required and not check.approved
        )

        if not credential_file_present:
            warnings.append(
                "MT5 credential file is not present."
            )

        approved = not errors

        return MT5ConfigurationAuditResult(
            approved=approved,
            credential_file_present=(
                credential_file_present
            ),
            credential_file_valid=(
                credential_file_valid
            ),
            environment_valid=environment_valid,
            consistency_valid=consistency_valid,
            checks=tuple(checks),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    # --------------------------------------------------
    # Environment Audit
    # --------------------------------------------------

    def _audit_environment(
        self,
    ) -> tuple[MT5ConfigurationCheck, ...]:
        return (
            self._check_login(),
            self._check_password(),
            self._check_server(),
            self._check_path(),
        )

    def _check_login(
        self,
    ) -> MT5ConfigurationCheck:
        value = self._get(
            self.MT5_LOGIN
        )

        if not value:
            return MT5ConfigurationCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN is missing.",
            )

        try:
            login = int(value)
        except ValueError:
            return MT5ConfigurationCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN must be numeric.",
            )

        if login <= 0:
            return MT5ConfigurationCheck(
                name=self.MT5_LOGIN,
                approved=False,
                required=True,
                message="MT5_LOGIN must be positive.",
            )

        return MT5ConfigurationCheck(
            name=self.MT5_LOGIN,
            approved=True,
            required=True,
            message="MT5_LOGIN is valid.",
        )

    def _check_password(
        self,
    ) -> MT5ConfigurationCheck:
        value = self._get(
            self.MT5_PASSWORD
        )

        return MT5ConfigurationCheck(
            name=self.MT5_PASSWORD,
            approved=bool(value),
            required=True,
            message=(
                "MT5_PASSWORD is configured."
                if value
                else "MT5_PASSWORD is missing."
            ),
            sensitive=True,
        )

    def _check_server(
        self,
    ) -> MT5ConfigurationCheck:
        value = self._get(
            self.MT5_SERVER
        )

        return MT5ConfigurationCheck(
            name=self.MT5_SERVER,
            approved=bool(value),
            required=True,
            message=(
                "MT5_SERVER is configured."
                if value
                else "MT5_SERVER is missing."
            ),
        )

    def _check_path(
        self,
    ) -> MT5ConfigurationCheck:
        value = self._get(
            self.MT5_PATH
        )

        if not value:
            return MT5ConfigurationCheck(
                name=self.MT5_PATH,
                approved=False,
                required=True,
                message="MT5_PATH is missing.",
            )

        path = Path(value)

        if not path.exists():
            return MT5ConfigurationCheck(
                name=self.MT5_PATH,
                approved=False,
                required=True,
                message="MT5_PATH does not exist.",
            )

        if not path.is_file():
            return MT5ConfigurationCheck(
                name=self.MT5_PATH,
                approved=False,
                required=True,
                message="MT5_PATH is not a file.",
            )

        return MT5ConfigurationCheck(
            name=self.MT5_PATH,
            approved=True,
            required=True,
            message="MT5_PATH is valid.",
        )

    # --------------------------------------------------
    # Credential File Audit
    # --------------------------------------------------

    def _audit_credential_file(
        self,
    ) -> tuple[
        bool,
        bool,
        dict[str, object] | None,
        tuple[MT5ConfigurationCheck, ...],
    ]:
        if not self._credential_file.exists():
            return (
                False,
                False,
                None,
                (
                    MT5ConfigurationCheck(
                        name="MT5_CREDENTIAL_FILE",
                        approved=False,
                        required=True,
                        message=(
                            "MT5 credential file "
                            "is missing."
                        ),
                    ),
                ),
            )

        try:
            with self._credential_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                credentials = json.load(file)
        except (OSError, json.JSONDecodeError):
            return (
                True,
                False,
                None,
                (
                    MT5ConfigurationCheck(
                        name="MT5_CREDENTIAL_FILE",
                        approved=False,
                        required=True,
                        message=(
                            "MT5 credential file "
                            "is invalid JSON."
                        ),
                    ),
                ),
            )

        if not isinstance(credentials, dict):
            return (
                True,
                False,
                None,
                (
                    MT5ConfigurationCheck(
                        name="MT5_CREDENTIAL_FILE",
                        approved=False,
                        required=True,
                        message=(
                            "MT5 credential file "
                            "must contain a JSON object."
                        ),
                    ),
                ),
            )

        checks = (
            self._check_credential_field(
                credentials,
                "login",
                sensitive=False,
            ),
            self._check_credential_field(
                credentials,
                "password",
                sensitive=True,
            ),
            self._check_credential_field(
                credentials,
                "server",
                sensitive=False,
            ),
        )

        valid = all(
            check.approved
            for check in checks
        )

        return (
            True,
            valid,
            credentials if valid else credentials,
            checks,
        )

    def _check_credential_field(
        self,
        credentials: dict[str, object],
        field_name: str,
        sensitive: bool,
    ) -> MT5ConfigurationCheck:
        value = credentials.get(
            field_name
        )

        if value is None:
            return MT5ConfigurationCheck(
                name=f"credential.{field_name}",
                approved=False,
                required=True,
                message=(
                    f"MT5 credential field "
                    f"'{field_name}' is missing."
                ),
                sensitive=sensitive,
            )

        if field_name == "login":
            try:
                login = int(value)
            except (TypeError, ValueError):
                return MT5ConfigurationCheck(
                    name="credential.login",
                    approved=False,
                    required=True,
                    message=(
                        "MT5 credential login "
                        "must be numeric."
                    ),
                )

            if login <= 0:
                return MT5ConfigurationCheck(
                    name="credential.login",
                    approved=False,
                    required=True,
                    message=(
                        "MT5 credential login "
                        "must be positive."
                    ),
                )

        elif not isinstance(value, str) or not value.strip():
            return MT5ConfigurationCheck(
                name=f"credential.{field_name}",
                approved=False,
                required=True,
                message=(
                    f"MT5 credential field "
                    f"'{field_name}' is invalid."
                ),
                sensitive=sensitive,
            )

        return MT5ConfigurationCheck(
            name=f"credential.{field_name}",
            approved=True,
            required=True,
            message=(
                f"MT5 credential field "
                f"'{field_name}' is configured."
            ),
            sensitive=sensitive,
        )

    # --------------------------------------------------
    # Consistency Audit
    # --------------------------------------------------

    def _audit_consistency(
        self,
        credentials: dict[str, object] | None,
        credential_file_valid: bool,
    ) -> tuple[MT5ConfigurationCheck, ...]:
        if not credential_file_valid or credentials is None:
            return ()

        checks: list[MT5ConfigurationCheck] = []

        checks.append(
            self._compare_login(
                credentials
            )
        )

        checks.append(
            self._compare_secret(
                credentials
            )
        )

        checks.append(
            self._compare_server(
                credentials
            )
        )

        return tuple(checks)

    def _compare_login(
        self,
        credentials: dict[str, object],
    ) -> MT5ConfigurationCheck:
        environment_value = self._get(
            self.MT5_LOGIN
        )

        credential_value = credentials.get(
            "login"
        )

        try:
            environment_login = int(
                environment_value
            )
            credential_login = int(
                credential_value  # type: ignore[arg-type]
            )
        except (TypeError, ValueError):
            return MT5ConfigurationCheck(
                name="MT5_LOGIN_CONSISTENCY",
                approved=False,
                required=True,
                message=(
                    "MT5 login configuration "
                    "is inconsistent."
                ),
            )

        return MT5ConfigurationCheck(
            name="MT5_LOGIN_CONSISTENCY",
            approved=(
                environment_login
                == credential_login
            ),
            required=True,
            message=(
                "MT5 login configuration "
                "is consistent."
                if environment_login
                == credential_login
                else
                "MT5 login configuration "
                "does not match the credential file."
            ),
        )

    def _compare_secret(
        self,
        credentials: dict[str, object],
    ) -> MT5ConfigurationCheck:
        environment_value = self._get(
            self.MT5_PASSWORD
        )

        credential_value = credentials.get(
            "password"
        )

        matches = (
            isinstance(credential_value, str)
            and environment_value
            == credential_value
        )

        return MT5ConfigurationCheck(
            name="MT5_PASSWORD_CONSISTENCY",
            approved=matches,
            required=True,
            message=(
                "MT5 password configuration "
                "is consistent."
                if matches
                else
                "MT5 password configuration "
                "does not match the credential file."
            ),
            sensitive=True,
        )

    def _compare_server(
        self,
        credentials: dict[str, object],
    ) -> MT5ConfigurationCheck:
        environment_value = self._get(
            self.MT5_SERVER
        )

        credential_value = credentials.get(
            "server"
        )

        matches = (
            isinstance(credential_value, str)
            and environment_value
            == credential_value
        )

        return MT5ConfigurationCheck(
            name="MT5_SERVER_CONSISTENCY",
            approved=matches,
            required=True,
            message=(
                "MT5 server configuration "
                "is consistent."
                if matches
                else
                "MT5 server configuration "
                "does not match the credential file."
            ),
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _get(
        self,
        name: str,
    ) -> str:
        return self._environment.get(
            name,
            "",
        ).strip()