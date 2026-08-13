"""
=================================================
Project Phoenix
Trading Cycle
M61.3
=================================================
"""

from __future__ import annotations

from deployment.execution_summary import (
    CycleExecutionSummary,
    SymbolExecutionResult,
    SymbolExecutionStatus,
)

from deployment.live_market_data import (
    LiveMarketData,
)

from deployment.market_data_adapter import (
    MarketDataAdapter,
)

from deployment.runtime_config import (
    RuntimeConfig,
)

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)

from market_pipeline.pipeline_context import (
    PipelineContext,
)

from reporting.reporting_engine import (
    ReportingEngine,
)

from reporting.trade_record_mapper import (
    TradeRecordMapper,
)

from risk_engine.risk_engine import (
    RiskEngine,
)

from strategy.strategy_engine import (
    StrategyEngine,
)


class TradingCycle:
    """
    Executes one complete
    Project Phoenix trading cycle.

    M61.3:

    Each configured symbol is processed
    independently.

    Each symbol produces one explicit
    execution outcome:

    - EXECUTED
    - NO_TRADE
    - FAILED

    The complete cycle exposes a
    CycleExecutionSummary.

    A failure for one symbol must not
    prevent the remaining symbols from
    being processed.
    """

    def __init__(
        self,
    ) -> None:

        # ==================================================
        # Market Services
        # ==================================================

        self.market = (
            LiveMarketData()
        )

        self.config = (
            RuntimeConfig()
        )

        self.market_adapter = (
            MarketDataAdapter()
        )

        self.market_data = {}

        self.candles = []

        self.pipeline_context = None

        self.current_symbol = ""

        # ==================================================
        # Runtime Status
        # ==================================================

        self.connected = False

        self.pipeline_completed = False

        self.execution_completed = False

        self.paper_trading_completed = False

        self.last_error = ""

        # ==================================================
        # Analysis Engines
        # ==================================================

        self.market_pipeline = (
            MarketPipelineEngine()
        )

        self.strategy_engine = (
            StrategyEngine()
        )

        self.risk_engine = (
            RiskEngine()
        )

        # ==================================================
        # Reporting Services
        # ==================================================

        self.reporting_engine = (
            ReportingEngine()
        )

        self.trade_record_mapper = (
            TradeRecordMapper()
        )

        self.trade_records = []

        self.daily_report = None

        # ==================================================
        # M61.3 Execution Summary
        # ==================================================

        self.execution_summary = (
            CycleExecutionSummary()
        )

    # ==================================================
    # Initialize
    # ==================================================

    def _initialize(
        self,
    ) -> None:

        print()

        print(
            "======================================"
        )

        print(
            "Starting Trading Cycle"
        )

        print(
            "======================================"
        )

    # ==================================================
    # MT5 Connection
    # ==================================================

    def _connect_mt5(
        self,
    ) -> None:
        """
        Connect to MT5.
        """

        print(
            "Step 1 : MT5 Connection"
        )

        if not self.market.connect():

            self.last_error = (
                "MT5 Connection Failed"
            )

            raise RuntimeError(
                self.last_error
            )

        self.connected = True

    # ==================================================
    # Live Market Data
    # ==================================================

    def _load_market_data(
        self,
    ) -> None:
        """
        Download live market data.
        """

        print(
            "Step 2 : Live Market Data"
        )

        self.market_data = (
            self.market.get_multi_timeframe_data(
                symbol=self.current_symbol,
                bars=self.config.bars,
            )
        )

        self.candles = (
            self.market_adapter.normalize(
                self.market_data[
                    self.config.timeframe
                ]
            )
        )

        print(
            f"M15 Candles Loaded : "
            f"{len(self.candles)}"
        )

    # ==================================================
    # Market Pipeline
    # ==================================================

    def _run_market_pipeline(
        self,
    ) -> None:
        """
        Execute Market Pipeline
        using live MT5 candles.
        """

        print(
            "Step 3 : Market Pipeline"
        )

        context = PipelineContext(

            pipeline_id="LIVE-PIPELINE",

            symbol=self.current_symbol,

            timeframe=self.config.timeframe,
        )

        context.candles = self.candles

        context = (
            self.market_pipeline.engine.run(
                context,
            )
        )

        if not context.approved:

            raise RuntimeError(

                f"Pipeline Failed : "
                f"{context.reason}"

            )

        self.pipeline_context = context

        self.pipeline_completed = (
            context.completed
        )

        self.execution_completed = (
            context.execution_result is not None
        )

        self.paper_trading_completed = (
            context.execution_result is not None
        )

        print(
            f"Pipeline Approved : "
            f"{len(context.candles)} candles"
        )

    # ==================================================
    # Validate Pipeline Output
    # ==================================================

    def _validate_pipeline_result(
        self,
    ) -> None:
        """
        Validate pipeline outputs before
        completing the trading cycle.
        """

        if self.pipeline_context is None:

            raise RuntimeError(
                "Pipeline context not available."
            )

        context = self.pipeline_context

        if len(context.candles) == 0:

            raise RuntimeError(
                "No candles available."
            )

        if not context.indicators:

            raise RuntimeError(
                "Indicators not generated."
            )

        if context.patterns is None:

            raise RuntimeError(
                "Patterns not generated."
            )

        if context.strategy_result is None:

            raise RuntimeError(
                "Strategy result missing."
            )

        if context.signals is None:

            raise RuntimeError(
                "Signal result missing."
            )

        if context.risk_result is None:

            raise RuntimeError(
                "Risk result missing."
            )

        if context.ai_result is None:

            raise RuntimeError(
                "AI result missing."
            )

        if context.execution_result is None:

            raise RuntimeError(
                "Execution result missing."
            )

        if context.portfolio_result is None:

            raise RuntimeError(
                "Portfolio result missing."
            )

        print()

        print(
            "Pipeline Validation Passed"
        )

    # ==================================================
    # Collect Execution Record
    # ==================================================

    def _collect_execution_record(
        self,
    ) -> bool:
        """
        Convert a successful execution context
        into a TradeRecord and store it for the
        consolidated trading-cycle report.

        Returns:

            True:
                Executed trade collected.

            False:
                No executed trade.

        A rejected or non-executed pipeline is a
        valid trading-cycle outcome and therefore
        does not create a TradeRecord.
        """

        if self.pipeline_context is None:

            raise RuntimeError(
                "Pipeline context not available."
            )

        context = self.pipeline_context

        # --------------------------------------------------
        # Execution Result
        # --------------------------------------------------

        execution_result = (
            context.execution_result
        )

        if execution_result is None:

            print()

            print(
                "No execution result available."
            )

            return False

        # --------------------------------------------------
        # No Executed Trade
        #
        # Rejected execution is a valid cycle outcome.
        # Do not create a TradeRecord.
        # --------------------------------------------------

        if not execution_result.accepted:

            print()

            print(
                "No executed trade for this cycle."
            )

            print(
                "Execution Status : "
                f"{execution_result.status}"
            )

            return False

        # --------------------------------------------------
        # Map ExecutionContext -> TradeRecord
        # --------------------------------------------------

        trade_record = (
            self.trade_record_mapper.map(
                context,
            )
        )

        # --------------------------------------------------
        # Store Trade Record
        # --------------------------------------------------

        self.trade_records.append(
            trade_record,
        )

        print()

        print(
            "===== TRADE RECORD COLLECTED ====="
        )

        print(
            f"Trade ID    : "
            f"{trade_record.trade_id}"
        )

        print(
            f"Symbol      : "
            f"{trade_record.symbol}"
        )

        print(
            f"Direction   : "
            f"{trade_record.direction}"
        )

        print(
            f"Entry Price : "
            f"{trade_record.entry_price}"
        )

        print(
            f"Volume      : "
            f"{trade_record.volume}"
        )

        print(
            f"Status      : "
            f"{trade_record.status}"
        )

        print(
            "=================================="
        )

        return True

    # ==================================================
    # M61.3 Record Symbol Result
    # ==================================================

    def _record_symbol_result(
        self,
        symbol: str,
        status: SymbolExecutionStatus,
        trade_id: str = "",
        error: str = "",
    ) -> None:
        """
        Record the final execution outcome
        for one symbol.
        """

        result = (
            SymbolExecutionResult(
                symbol=symbol,
                status=status,
                trade_id=trade_id,
                error=error,
            )
        )

        self.execution_summary.add_result(
            result
        )

    # ==================================================
    # Consolidated Trading Report
    # ==================================================

    def _generate_consolidated_report(
        self,
    ) -> None:
        """
        Generate one consolidated report for
        all executed trades in the trading cycle.
        """

        if not self.trade_records:

            print()

            print(
                "No executed trades found."
            )

            return

        self.daily_report = (
            self.reporting_engine.run(
                self.trade_records,
            )
        )

        print()

        print(
            "===== CONSOLIDATED REPORT ====="
        )

        print(
            f"Trades Reported : "
            f"{len(self.trade_records)}"
        )

        print(
            f"Report File     : "
            f"{self.daily_report.output_file}"
        )

        print(
            "==============================="
        )

    # ==================================================
    # Trading Cycle Report
    # ==================================================

    def _generate_trading_report(
        self,
    ) -> None:
        """
        Generate Trading Cycle Summary.
        """

        if self.pipeline_context is None:

            return

        context = self.pipeline_context

        print()

        print(
            "========================================"
        )

        print(
            "Project Phoenix Trading Cycle Report"
        )

        print(
            "========================================"
        )

        print(
            f"Symbol              : "
            f"{context.symbol}"
        )

        print(
            f"Timeframe           : "
            f"{context.timeframe}"
        )

        print(
            f"Candles             : "
            f"{len(context.candles)}"
        )

        print(
            f"Indicators          : "
            f"{len(context.indicators)}"
        )

        print(
            f"Patterns            : "
            f"{len(context.patterns)}"
        )

        print(
            f"Signals             : "
            f"{len(context.signals)}"
        )

        print(
            f"Pipeline Approved   : "
            f"{context.approved}"
        )

        print(
            f"Decision            : "
            f"{context.decision}"
        )

        print(
            f"Reason              : "
            f"{context.reason}"
        )

        print(
            "========================================"
        )

    # ==================================================
    # Symbol Failure Handler
    # ==================================================

    def _handle_symbol_failure(
        self,
        symbol: str,
        error: Exception,
    ) -> None:
        """
        Handle an isolated symbol failure.

        A failure for one symbol is recorded
        and logged, but must not stop the
        remaining configured symbols.
        """

        message = (
            f"{symbol}: {error}"
        )

        self.last_error = message

        self._record_symbol_result(
            symbol=symbol,
            status=SymbolExecutionStatus.FAILED,
            error=str(error),
        )

        print()

        print(
            "===== SYMBOL PROCESSING ERROR ====="
        )

        print(
            f"Symbol : {symbol}"
        )

        print(
            f"Reason : {error}"
        )

        print(
            "Action : Continue with next symbol"
        )

        print(
            "==================================="
        )

    # ==================================================
    # Finish
    # ==================================================

    def _finish(
        self,
    ) -> None:
        """
        Complete Trading Cycle.
        """

        self.market.disconnect()

        print()

        print(
            "========== SYSTEM STATUS =========="
        )

        print(
            f"MT5 Connected        : "
            f"{self.connected}"
        )

        print(
            f"Pipeline Completed   : "
            f"{self.pipeline_completed}"
        )

        print(
            f"Execution Completed  : "
            f"{self.execution_completed}"
        )

        print(
            f"Paper Trading        : "
            f"{self.paper_trading_completed}"
        )

        print(
            "==================================="
        )

        print()

        print(
            "--------------------------------------"
        )

        print(
            "Trading Cycle Completed"
        )

        print(
            "--------------------------------------"
        )

        print()

    # ==================================================
    # Execute
    # ==================================================

    def execute(
        self,
    ) -> bool:
        """
        Execute one complete
        Project Phoenix trading cycle.

        M61.3:

        Every configured symbol is isolated.

        Each symbol receives an explicit
        execution result:

        - EXECUTED
        - NO_TRADE
        - FAILED

        The complete cycle result is exposed
        through execution_summary.

        The existing execute() -> bool contract
        is preserved.
        """

        self._initialize()

        self._connect_mt5()

        # --------------------------------------------------
        # Reset Cycle-Level State
        # --------------------------------------------------

        self.trade_records = []

        self.daily_report = None

        self.last_error = ""

        self.pipeline_context = None

        self.execution_summary = (
            CycleExecutionSummary()
        )

        self.pipeline_completed = False

        self.execution_completed = False

        self.paper_trading_completed = False

        try:

            # --------------------------------------------------
            # Process All Configured Symbols
            # --------------------------------------------------

            for symbol in self.config.symbols:

                print()

                print(
                    "=" * 50
                )

                print(
                    f"Scanning : {symbol}"
                )

                print(
                    "=" * 50
                )

                self.current_symbol = symbol

                # --------------------------------------------------
                # Clear Previous Symbol Context
                # --------------------------------------------------

                self.pipeline_context = None

                self.market_data = {}

                self.candles = []

                self.pipeline_completed = False

                self.execution_completed = False

                self.paper_trading_completed = False

                try:

                    # --------------------------------------------------
                    # Symbol Processing Pipeline
                    # --------------------------------------------------

                    self._load_market_data()

                    self._run_market_pipeline()

                    self._validate_pipeline_result()

                    executed = (
                        self._collect_execution_record()
                    )

                    # --------------------------------------------------
                    # M61.3 Symbol Outcome
                    # --------------------------------------------------

                    if executed:

                        trade_record = (
                            self.trade_records[-1]
                        )

                        self._record_symbol_result(
                            symbol=symbol,
                            status=(
                                SymbolExecutionStatus.EXECUTED
                            ),
                            trade_id=(
                                trade_record.trade_id
                            ),
                        )

                    else:

                        self._record_symbol_result(
                            symbol=symbol,
                            status=(
                                SymbolExecutionStatus.NO_TRADE
                            ),
                        )

                    self._generate_trading_report()

                except Exception as exc:

                    # --------------------------------------------------
                    # M61.2 SYMBOL ISOLATION
                    #
                    # One symbol failure must not stop
                    # the remaining symbols.
                    # --------------------------------------------------

                    self._handle_symbol_failure(
                        symbol=symbol,
                        error=exc,
                    )

                    continue

            # --------------------------------------------------
            # Generate One Consolidated Report
            # --------------------------------------------------

            self._generate_consolidated_report()

            # --------------------------------------------------
            # M61.3 Cycle Summary
            # --------------------------------------------------

            print()

            print(
                "===== CYCLE EXECUTION SUMMARY ====="
            )

            print(
                f"Total Symbols   : "
                f"{self.execution_summary.total_symbols}"
            )

            print(
                f"Executed        : "
                f"{self.execution_summary.executed_symbols}"
            )

            print(
                f"No Trade        : "
                f"{self.execution_summary.no_trade_symbols}"
            )

            print(
                f"Failed          : "
                f"{self.execution_summary.failed_symbols}"
            )

            print(
                f"Cycle Status    : "
                f"{self.execution_summary.status.value}"
            )

            print(
                "===================================="
            )

            return True

        finally:

            # --------------------------------------------------
            # Always Disconnect / Finish
            # --------------------------------------------------

            self._finish()