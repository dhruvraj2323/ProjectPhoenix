"""
=================================================
Project Phoenix
Health Monitor Tests
M61.6.1 - Deployment Readiness Foundation
=================================================
"""

from deployment.health_monitor import (
    HealthMonitor,
)


# =========================================================
# Test A
# Default Health
# =========================================================

def test_health_monitor_default_health():

    monitor = HealthMonitor()

    report = (
        monitor.health_report()
    )

    assert report["cpu"] == 12.5

    assert report["memory"] == 245.7

    assert report["database"] is True

    assert report["broker"] is True

    assert report["scheduler"] is True

    assert report["healthy"] is True

    assert (
        monitor.is_healthy()
        is True
    )


# =========================================================
# Test B
# Database Failure
# =========================================================

def test_health_monitor_database_failure():

    monitor = HealthMonitor()

    monitor.database = False

    report = (
        monitor.health_report()
    )

    assert report["database"] is False

    assert report["healthy"] is False

    assert (
        monitor.is_healthy()
        is False
    )


# =========================================================
# Test C
# Broker Failure
# =========================================================

def test_health_monitor_broker_failure():

    monitor = HealthMonitor()

    monitor.broker = False

    report = (
        monitor.health_report()
    )

    assert report["broker"] is False

    assert report["healthy"] is False

    assert (
        monitor.is_healthy()
        is False
    )


# =========================================================
# Test D
# Scheduler Failure
# =========================================================

def test_health_monitor_scheduler_failure():

    monitor = HealthMonitor()

    monitor.scheduler = False

    report = (
        monitor.health_report()
    )

    assert report["scheduler"] is False

    assert report["healthy"] is False

    assert (
        monitor.is_healthy()
        is False
    )


# =========================================================
# Test E
# CPU Threshold
# =========================================================

def test_health_monitor_cpu_threshold():

    monitor = HealthMonitor(
        max_cpu_usage=90.0,
    )

    monitor.cpu_usage = 95.0

    report = (
        monitor.health_report()
    )

    assert report["cpu"] == 95.0

    assert report["healthy"] is False

    assert (
        monitor.is_healthy()
        is False
    )


# =========================================================
# Test F
# Memory Threshold
# =========================================================

def test_health_monitor_memory_threshold():

    monitor = HealthMonitor(
        max_memory_usage=1024.0,
    )

    monitor.memory_usage = 1200.0

    report = (
        monitor.health_report()
    )

    assert report["memory"] == 1200.0

    assert report["healthy"] is False

    assert (
        monitor.is_healthy()
        is False
    )


# =========================================================
# Test G
# Multiple Failures
# =========================================================

def test_health_monitor_multiple_failures():

    monitor = HealthMonitor()

    monitor.database = False

    monitor.broker = False

    monitor.cpu_usage = 95.0

    report = (
        monitor.health_report()
    )

    assert report["database"] is False

    assert report["broker"] is False

    assert report["healthy"] is False


# =========================================================
# Test H
# Recovery
# =========================================================

def test_health_monitor_recovery():

    monitor = HealthMonitor()

    monitor.database = False

    assert (
        monitor.is_healthy()
        is False
    )

    monitor.database = True

    assert (
        monitor.is_healthy()
        is True
    )