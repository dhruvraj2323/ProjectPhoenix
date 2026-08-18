"""
=================================================
Project Phoenix
Daily Trade Ledger
Post-M63 Reporting Reliability
=================================================
"""
from __future__ import annotations
from dataclasses import fields
from datetime import UTC, date, datetime
import json
from pathlib import Path
from typing import Any
from reporting.reporting_models import TradeRecord
class DailyTradeLedger:
    """
    Persistent daily trade ledger used by live/demo reporting.
    The ledger is intentionally separate from the XLSX workbook so that
    repeated 5-minute cycles do not overwrite previously collected trades.
    A trade is de-duplicated primarily by trade_id. When trade_id is empty,
    a deterministic fallback key is built from the trade's identifying fields.
    """
    LEDGER_DIRECTORY_NAME = ".trade_ledger"
    def __init__(
        self,
        report_directory: Path,
    ) -> None:
        self.report_directory = Path(
            report_directory,
        )
        self.ledger_directory = (
            self.report_directory
            / self.LEDGER_DIRECTORY_NAME
        )
    def merge(
        self,
        trades: list[TradeRecord],
        report_date: datetime | date | None = None,
    ) -> list[TradeRecord]:
        """
        Load, merge, de-duplicate and persist one day's trades.
        """
        target_date = self._resolve_date(
            report_date,
        )
        ledger_path = self._ledger_path(
            target_date,
        )
        existing = self._load(
            ledger_path,
        )
        merged: dict[str, TradeRecord] = {}
        for trade in existing:
            merged[
                self._trade_key(trade)
            ] = trade
        for trade in trades:
            merged[
                self._trade_key(trade)
            ] = trade
        result = list(
            merged.values(),
        )
        result.sort(
            key=self._sort_key,
        )
        self._save(
            ledger_path,
            result,
        )
        return result
    def _resolve_date(
        self,
        report_date: datetime | date | None,
    ) -> date:
        if report_date is None:
            return datetime.now(
                UTC,
            ).date()
        if isinstance(
            report_date,
            datetime,
        ):
            return report_date.date()
        return report_date
    def _ledger_path(
        self,
        target_date: date,
    ) -> Path:
        return (
            self.ledger_directory
            / f"{target_date.isoformat()}.json"
        )
    @staticmethod
    def _trade_key(
        trade: TradeRecord,
    ) -> str:
        if trade.trade_id:
            return (
                f"trade_id:{trade.trade_id}"
            )
        opened_at = (
            DailyTradeLedger._datetime_value(
                trade.opened_at,
            )
        )
        return (
            "fallback:"
            + "|".join(
                [
                    trade.symbol,
                    trade.direction,
                    trade.strategy,
                    opened_at,
                    str(trade.entry_price),
                    str(trade.volume),
                ]
            )
        )
    @staticmethod
    def _sort_key(
        trade: TradeRecord,
    ) -> tuple[str, str, str]:
        return (
            DailyTradeLedger._datetime_value(
                trade.opened_at,
            ),
            trade.symbol,
            trade.trade_id,
        )
    def _load(
        self,
        ledger_path: Path,
    ) -> list[TradeRecord]:
        if not ledger_path.exists():
            return []
        try:
            payload = json.loads(
                ledger_path.read_text(
                    encoding="utf-8",
                )
            )
        except (
            OSError,
            ValueError,
            TypeError,
        ):
            return []
        if not isinstance(
            payload,
            list,
        ):
            return []
        records: list[TradeRecord] = []
        for item in payload:
            if not isinstance(
                item,
                dict,
            ):
                continue
            try:
                records.append(
                    self._deserialize_trade(
                        item,
                    )
                )
            except (
                TypeError,
                ValueError,
            ):
                continue
        return records
    def _save(
        self,
        ledger_path: Path,
        trades: list[TradeRecord],
    ) -> None:
        self.ledger_directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        payload = [
            self._serialize_trade(
                trade,
            )
            for trade in trades
        ]
        temporary_path = (
            ledger_path.with_suffix(
                ".json.tmp",
            )
        )
        temporary_path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        temporary_path.replace(
            ledger_path,
        )
    @staticmethod
    def _serialize_trade(
        trade: TradeRecord,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for field in fields(
            TradeRecord,
        ):
            value = getattr(
                trade,
                field.name,
            )
            if isinstance(
                value,
                datetime,
            ):
                payload[
                    field.name
                ] = value.isoformat()
            else:
                payload[
                    field.name
                ] = value
        return payload
    @staticmethod
    def _deserialize_trade(
        payload: dict[str, Any],
    ) -> TradeRecord:
        valid_names = {
            field.name
            for field in fields(
                TradeRecord,
            )
        }
        values = {
            key: value
            for key, value in payload.items()
            if key in valid_names
        }
        for name in (
            "opened_at",
            "closed_at",
        ):
            value = values.get(
                name,
            )
            if isinstance(
                value,
                str,
            ):
                values[name] = (
                    datetime.fromisoformat(
                        value,
                    )
                )
        return TradeRecord(
            **values,
        )
    @staticmethod
    def _datetime_value(
        value: datetime,
    ) -> str:
        if value.tzinfo is None:
            value = value.replace(
                tzinfo=UTC,
            )
        return value.astimezone(
            UTC,
        ).isoformat()