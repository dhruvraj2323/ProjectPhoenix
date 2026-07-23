"""
=================================================
Project Phoenix
Indicator Models
M32
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class IndicatorType(Enum):
    """
    Supported indicator types.
    """

    EMA = "EMA"
    SMA = "SMA"
    WMA = "WMA"
    VWMA = "VWMA"

    RSI = "RSI"
    STOCH_RSI = "STOCH_RSI"
    CCI = "CCI"
    MOMENTUM = "MOMENTUM"
    ROC = "ROC"

    ATR = "ATR"
    BOLLINGER = "BOLLINGER"
    STDDEV = "STDDEV"
    KELTNER = "KELTNER"

    OBV = "OBV"
    VWAP = "VWAP"
    MFI = "MFI"
    CMF = "CMF"

    ADX = "ADX"
    DMI = "DMI"
    PSAR = "PSAR"

    MACD = "MACD"
    AO = "AO"
    WILLIAMS_R = "WILLIAMS_R"
    TRIX = "TRIX"


class IndicatorStatus(Enum):
    """
    Indicator execution status.
    """

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


@dataclass(slots=True)
class IndicatorValue:
    """
    Single indicator output.
    """

    indicator: IndicatorType
    value: Any
    period: int
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class IndicatorSeries:
    """
    Complete indicator series.
    """

    indicator: IndicatorType
    values: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class IndicatorStatistics:
    """
    Indicator execution statistics.
    """

    total_indicators: int = 0
    execution_time_ms: float = 0.0
    calculated: int = 0
    failed: int = 0


@dataclass(slots=True)
class IndicatorResult:
    """
    Final Indicator Engine result.
    """

    status: IndicatorStatus
    approved: bool
    indicators: dict[str, Any] = field(default_factory=dict)
    statistics: IndicatorStatistics = field(
        default_factory=IndicatorStatistics
    )
    reason: str = ""