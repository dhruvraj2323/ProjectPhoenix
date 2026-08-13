"""
=================================================
Project Phoenix
Main Entry Point Tests
M61.7.3 - Deployment Startup Integration
=================================================
"""

from unittest.mock import MagicMock, patch

import main


# =========================================================
# Test A
# Approved Bootstrap
# =========================================================

def test_main_approved_startup():

    bootstrap = MagicMock()

    bootstrap.start.return_value = True

    with patch(
        "main.Bootstrap",
        return_value=bootstrap,
    ):

        result = main.main()

    assert result == 0

    bootstrap.start.assert_called_once()


# =========================================================
# Test B
# Keyboard Interrupt
# =========================================================

def test_main_keyboard_interrupt():

    bootstrap = MagicMock()

    bootstrap.start.side_effect = (
        KeyboardInterrupt()
    )

    with patch(
        "main.Bootstrap",
        return_value=bootstrap,
    ):

        result = main.main()

    assert result == 0

    bootstrap.start.assert_called_once()

    bootstrap.stop.assert_called_once()


# =========================================================
# Test C
# Fatal Startup Error
# =========================================================

def test_main_fatal_error():

    bootstrap = MagicMock()

    bootstrap.start.side_effect = (
        RuntimeError(
            "Simulated startup failure."
        )
    )

    with patch(
        "main.Bootstrap",
        return_value=bootstrap,
    ):

        result = main.main()

    assert result == 1

    bootstrap.start.assert_called_once()

    bootstrap.stop.assert_called_once()


# =========================================================
# Test D
# Bootstrap Approval Boundary
# =========================================================

def test_main_uses_bootstrap_approval_boundary():

    bootstrap = MagicMock()

    bootstrap.start.return_value = False

    with patch(
        "main.Bootstrap",
        return_value=bootstrap,
    ):

        result = main.main()

    # main.py itself does not reinterpret the
    # DeploymentResult. Bootstrap owns the
    # deployment approval decision.

    assert result == 0

    bootstrap.start.assert_called_once()

    bootstrap.stop.assert_not_called()