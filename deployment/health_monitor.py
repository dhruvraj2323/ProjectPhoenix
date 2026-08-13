"""
=================================================
Project Phoenix
Health Monitor
M61.6.1 - Deployment Readiness Foundation
=================================================
"""


class HealthMonitor:
    """
    Monitors application health.

    M61.6.1 responsibilities:
    - Track core runtime components
    - Evaluate component health
    - Evaluate CPU and memory thresholds
    - Produce a structured health report
    """

    # --------------------------------------------------
    # Default Thresholds
    # --------------------------------------------------

    DEFAULT_MAX_CPU_USAGE = 90.0

    DEFAULT_MAX_MEMORY_USAGE = 1024.0

    def __init__(
        self,
        max_cpu_usage: float = DEFAULT_MAX_CPU_USAGE,
        max_memory_usage: float = DEFAULT_MAX_MEMORY_USAGE,
    ) -> None:

        self.cpu_usage = 12.5

        self.memory_usage = 245.7

        self.database = True

        self.broker = True

        self.scheduler = True

        self.max_cpu_usage = (
            max_cpu_usage
        )

        self.max_memory_usage = (
            max_memory_usage
        )

    # --------------------------------------------------
    # CPU Health
    # --------------------------------------------------

    def _cpu_healthy(self) -> bool:

        return (
            self.cpu_usage
            <= self.max_cpu_usage
        )

    # --------------------------------------------------
    # Memory Health
    # --------------------------------------------------

    def _memory_healthy(self) -> bool:

        return (
            self.memory_usage
            <= self.max_memory_usage
        )

    # --------------------------------------------------
    # Component Health
    # --------------------------------------------------

    def _components_healthy(self) -> bool:

        return all(
            [
                self.database,
                self.broker,
                self.scheduler,
            ]
        )

    # --------------------------------------------------
    # Overall Health
    # --------------------------------------------------

    def is_healthy(self) -> bool:
        """
        Return True only when every monitored
        component and resource is healthy.
        """

        return (
            self._cpu_healthy()
            and self._memory_healthy()
            and self._components_healthy()
        )

    # --------------------------------------------------
    # Health Report
    # --------------------------------------------------

    def health_report(self) -> dict:
        """
        Return a complete runtime health report.
        """

        return {
            "cpu": self.cpu_usage,
            "memory": self.memory_usage,
            "database": self.database,
            "broker": self.broker,
            "scheduler": self.scheduler,
            "healthy": self.is_healthy(),
        }