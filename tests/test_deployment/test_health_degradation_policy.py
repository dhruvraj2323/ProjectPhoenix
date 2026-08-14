"""
=================================================
Project Phoenix
Health Degradation Policy Tests
M62.4.1 - Runtime Health Degradation Policy
=================================================
"""

from deployment.health_degradation_policy import (
    HealthDegradationPolicy,
    HealthImpact,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)


def test_healthy_health_produces_healthy_impact():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        decision.health_state
        == WatchdogHealthState.HEALTHY
    )

    assert (
        decision.impact
        == HealthImpact.HEALTHY
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        decision.trading_paused
        is False
    )

    assert (
        decision.degraded
        is False
    )

    assert (
        decision.recovered
        is True
    )


def test_unhealthy_health_produces_degraded_impact():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        decision.health_state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        decision.impact
        == HealthImpact.DEGRADED
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        decision.trading_paused
        is True
    )

    assert (
        decision.degraded
        is True
    )

    assert (
        decision.recovered
        is False
    )


def test_healthy_decision_has_meaningful_reason():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        decision.reason
        == "Runtime health is healthy."
    )


def test_degraded_decision_has_meaningful_reason():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        "degraded"
        in decision.reason.lower()
    )

    assert (
        "trading"
        in decision.reason.lower()
    )


def test_decision_is_immutable():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    try:

        decision.trading_paused = False

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "HealthDegradationDecision must be immutable."
        )


def test_policy_does_not_expose_trading_permission():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert not hasattr(
        decision,
        "can_trade",
    )

    assert not hasattr(
        decision,
        "live_approved",
    )


def test_policy_does_not_expose_credentials():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert not hasattr(
        decision,
        "password",
    )

    assert not hasattr(
        decision,
        "bot_token",
    )

    assert not hasattr(
        decision,
        "api_key",
    )


def test_policy_does_not_control_runtime_lifecycle():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert not hasattr(
        decision,
        "stop_runtime",
    )

    assert not hasattr(
        decision,
        "restart_runtime",
    )

    assert not hasattr(
        decision,
        "pause_runner",
    )


def test_healthy_policy_does_not_request_trading_pause():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        decision.trading_paused
        is False
    )


def test_unhealthy_policy_requires_trading_pause():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        decision.trading_paused
        is True
    )