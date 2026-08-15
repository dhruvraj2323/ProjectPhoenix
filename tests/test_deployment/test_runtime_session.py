"""
=================================================
Project Phoenix
Runtime Session Tests
M62.7.2 - Runtime Session Control
=================================================
"""

import pytest

from deployment.runtime_session import (
    RuntimeSession,
)


# =================================================
# Creation
# =================================================


def test_runtime_session_can_be_created():

    session = RuntimeSession.create()

    assert isinstance(
        session,
        RuntimeSession,
    )


def test_runtime_session_has_unique_identity():

    first = RuntimeSession.create()
    second = RuntimeSession.create()

    assert (
        first.session_id
        != second.session_id
    )


def test_new_session_is_inactive():

    session = RuntimeSession.create()

    assert session.active is False


def test_new_session_is_not_terminal():

    session = RuntimeSession.create()

    assert session.terminal is False


def test_new_session_has_no_start_time():

    session = RuntimeSession.create()

    assert session.started_at is None


def test_new_session_has_no_stop_time():

    session = RuntimeSession.create()

    assert session.stopped_at is None


# =================================================
# Start
# =================================================


def test_session_can_start():

    session = RuntimeSession.create()

    started = session.start()

    assert started.active is True


def test_start_records_start_time():

    session = RuntimeSession.create()

    started = session.start()

    assert started.started_at is not None


def test_start_preserves_session_identity():

    session = RuntimeSession.create()

    started = session.start()

    assert (
        started.session_id
        == session.session_id
    )


def test_started_session_is_not_terminal():

    session = RuntimeSession.create()

    started = session.start()

    assert started.terminal is False


def test_started_session_has_no_stop_time():

    session = RuntimeSession.create()

    started = session.start()

    assert started.stopped_at is None


# =================================================
# Duplicate Start Protection
# =================================================


def test_active_session_cannot_start_again():

    session = RuntimeSession.create()

    started = session.start()

    with pytest.raises(
        RuntimeError,
        match="already active",
    ):

        started.start()


# =================================================
# Stop
# =================================================


def test_active_session_can_stop():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    assert stopped.active is False


def test_stop_records_stop_time():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    assert stopped.stopped_at is not None


def test_stopped_session_is_terminal():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    assert stopped.terminal is True


def test_stop_preserves_session_identity():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    assert (
        stopped.session_id
        == session.session_id
    )


def test_stop_preserves_start_time():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    assert (
        stopped.started_at
        == started.started_at
    )


# =================================================
# Duplicate Stop Protection
# =================================================


def test_inactive_session_cannot_stop():

    session = RuntimeSession.create()

    with pytest.raises(
        RuntimeError,
        match="not active",
    ):

        session.stop()


def test_terminal_session_cannot_stop_again():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    with pytest.raises(
        RuntimeError,
        match="not active",
    ):

        stopped.stop()


# =================================================
# Terminal Session Protection
# =================================================


def test_terminal_session_cannot_start_again():

    session = RuntimeSession.create()

    started = session.start()

    stopped = started.stop()

    with pytest.raises(
        RuntimeError,
        match="already terminal",
    ):

        stopped.start()


# =================================================
# Immutability
# =================================================


def test_runtime_session_is_immutable():

    session = RuntimeSession.create()

    with pytest.raises(
        AttributeError,
    ):

        session.session_id = "changed"


# =================================================
# State Progression
# =================================================


def test_session_progression():

    session = RuntimeSession.create()

    assert session.active is False
    assert session.terminal is False

    started = session.start()

    assert started.active is True
    assert started.terminal is False

    stopped = started.stop()

    assert stopped.active is False
    assert stopped.terminal is True