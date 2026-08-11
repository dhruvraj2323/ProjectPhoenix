"""
=================================================
Project Phoenix
Report Generator
M57
=================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from reporting.reporting_models import (
    DailyReport,
    PerformanceSummary,
    TradeRecord,
)


class ReportGenerator:
    """
    Builds and writes Daily Trading Reports.

    Responsibilities:
    - Build DailyReport model
    - Create physical XLSX workbook
    - Write summary sheet
    - Write trades sheet
    - Store report under reports/Daily/
    """

    REPORT_DIRECTORY = Path("reports") / "Daily"

    def generate(
        self,
        trades: list[TradeRecord],
        summary: PerformanceSummary,
    ) -> DailyReport:
        """
        Generate complete daily report and
        create the physical XLSX file.
        """

        report = DailyReport()

        report.trades = trades
        report.summary = summary

        report.report_date = datetime.utcnow()
        report.generated_at = datetime.utcnow()

        report.report_name = (
            report.report_date.strftime("%Y-%m-%d")
            + "_Trading_Report"
        )

        self.REPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.REPORT_DIRECTORY
            / f"{report.report_name}.xlsx"
        )

        report.output_file = str(output_path)

        self._write_workbook(
            trades=trades,
            summary=summary,
            output_path=output_path,
            report_date=report.report_date,
            generated_at=report.generated_at,
        )

        return report

    # --------------------------------------------------
    # Workbook
    # --------------------------------------------------

    def _write_workbook(
        self,
        trades: list[TradeRecord],
        summary: PerformanceSummary,
        output_path: Path,
        report_date: datetime,
        generated_at: datetime,
    ) -> None:
        """
        Create and save the XLSX workbook.
        """

        workbook = Workbook()

        summary_sheet = workbook.active
        summary_sheet.title = "Summary"

        trades_sheet = workbook.create_sheet(
            title="Trades",
        )

        self._write_summary_sheet(
            worksheet=summary_sheet,
            summary=summary,
            report_date=report_date,
            generated_at=generated_at,
        )

        self._write_trades_sheet(
            worksheet=trades_sheet,
            trades=trades,
        )

        self._auto_size_columns(
            summary_sheet,
        )

        self._auto_size_columns(
            trades_sheet,
        )

        workbook.save(
            output_path,
        )

        workbook.close()

    # --------------------------------------------------
    # Summary Sheet
    # --------------------------------------------------

    def _write_summary_sheet(
        self,
        worksheet,
        summary: PerformanceSummary,
        report_date: datetime,
        generated_at: datetime,
    ) -> None:
        """
        Write performance summary into Summary sheet.
        """

        worksheet["A1"] = "Project Phoenix"
        worksheet["A1"].font = Font(
            bold=True,
            size=16,
        )

        worksheet["A2"] = "Daily Trading Report"
        worksheet["A2"].font = Font(
            bold=True,
            size=13,
        )

        worksheet["A4"] = "Report Date"
        worksheet["B4"] = report_date.strftime(
            "%Y-%m-%d"
        )

        worksheet["A5"] = "Generated At"
        worksheet["B5"] = generated_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        worksheet["A7"] = "Metric"
        worksheet["B7"] = "Value"

        worksheet["A7"].font = Font(
            bold=True,
        )

        worksheet["B7"].font = Font(
            bold=True,
        )

        metrics = [
            (
                "Total Trades",
                summary.total_trades,
            ),
            (
                "Winning Trades",
                summary.winning_trades,
            ),
            (
                "Losing Trades",
                summary.losing_trades,
            ),
            (
                "Win Rate (%)",
                summary.win_rate,
            ),
            (
                "Gross Profit",
                summary.gross_profit,
            ),
            (
                "Gross Loss",
                summary.gross_loss,
            ),
            (
                "Net Profit",
                summary.net_profit,
            ),
            (
                "Average Profit",
                summary.average_profit,
            ),
            (
                "Average Loss",
                summary.average_loss,
            ),
            (
                "Profit Factor",
                summary.profit_factor,
            ),
        ]

        start_row = 8

        for index, (metric, value) in enumerate(
            metrics,
            start=start_row,
        ):
            worksheet.cell(
                row=index,
                column=1,
                value=metric,
            )

            worksheet.cell(
                row=index,
                column=2,
                value=value,
            )

    # --------------------------------------------------
    # Trades Sheet
    # --------------------------------------------------

    def _write_trades_sheet(
        self,
        worksheet,
        trades: list[TradeRecord],
    ) -> None:
        """
        Write individual trade records into Trades sheet.
        """

        headers = [
            "Trade ID",
            "Symbol",
            "Direction",
            "Strategy",
            "Pattern",
            "Entry Price",
            "Exit Price",
            "Stop Loss",
            "Take Profit",
            "Volume",
            "Profit / Loss",
            "Status",
            "Opened At",
            "Closed At",
        ]

        for column_index, header in enumerate(
            headers,
            start=1,
        ):
            cell = worksheet.cell(
                row=1,
                column=column_index,
                value=header,
            )

            cell.font = Font(
                bold=True,
            )

        for row_index, trade in enumerate(
            trades,
            start=2,
        ):
            values = [
                trade.trade_id,
                trade.symbol,
                trade.direction,
                trade.strategy,
                trade.pattern,
                trade.entry_price,
                trade.exit_price,
                trade.stop_loss,
                trade.take_profit,
                trade.volume,
                trade.profit_loss,
                trade.status,
                trade.opened_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                trade.closed_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            ]

            for column_index, value in enumerate(
                values,
                start=1,
            ):
                worksheet.cell(
                    row=row_index,
                    column=column_index,
                    value=value,
                )

    # --------------------------------------------------
    # Column Width
    # --------------------------------------------------

    def _auto_size_columns(
        self,
        worksheet,
    ) -> None:
        """
        Automatically size worksheet columns.
        """

        for column_cells in worksheet.columns:
            max_length = 0

            column_letter = get_column_letter(
                column_cells[0].column,
            )

            for cell in column_cells:
                value = cell.value

                if value is None:
                    continue

                value_length = len(
                    str(value),
                )

                if value_length > max_length:
                    max_length = value_length

            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 2,
                40,
            )