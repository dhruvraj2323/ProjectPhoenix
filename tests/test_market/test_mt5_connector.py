"""
=================================================
Project Phoenix
MT5 Connection Manager Test
=================================================

Tests:
- Initialization
- Login
- Account Information
- Terminal Information
- Shutdown
"""

from dataclasses import dataclass


# -------------------------------------------------
# Mock MT5 Connection
# -------------------------------------------------


@dataclass
class MT5Connection:

    initialized: bool = False
    logged_in: bool = False
    shutdown_complete: bool = False

    def initialize(self):

        self.initialized = True
        return True

    def login(self):

        if not self.initialized:
            return False

        self.logged_in = True
        return True

    def account_info(self):

        return {
            "login": 12345678,
            "balance": 10000.0,
            "equity": 10000.0,
            "leverage": 100,
        }

    def terminal_info(self):

        return {
            "company": "MetaQuotes",
            "build": 4150,
            "version": "5.0",
        }

    def shutdown(self):

        self.shutdown_complete = True
        self.logged_in = False
        return True


# -------------------------------------------------
# Test
# -------------------------------------------------


def run_test():

    mt5 = MT5Connection()

    init_ok = mt5.initialize()

    login_ok = mt5.login()

    account = mt5.account_info()

    terminal = mt5.terminal_info()

    shutdown_ok = mt5.shutdown()

    print("===== MT5 Connection =====")

    print(f"Initialize : {'PASS' if init_ok else 'FAIL'}")
    print(f"Login      : {'PASS' if login_ok else 'FAIL'}")
    print(f"Account    : {'PASS' if account else 'FAIL'}")
    print(f"Terminal   : {'PASS' if terminal else 'FAIL'}")
    print(f"Shutdown   : {'PASS' if shutdown_ok else 'FAIL'}")

    assert init_ok
    assert login_ok
    assert account["balance"] == 10000.0
    assert terminal["company"] == "MetaQuotes"
    assert shutdown_ok

    print()
    print("MT5 Connection Test Passed")


# -------------------------------------------------
# Main
# -------------------------------------------------


if __name__ == "__main__":
    run_test()