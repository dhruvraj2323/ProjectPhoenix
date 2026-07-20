"""
=================================================
Project Phoenix
Runtime Manager Test
=================================================
"""

from deployment.runtime_manager import RuntimeManager


def run_test():

    runtime = RuntimeManager()

    runtime.start()

    print("===== Runtime Manager =====")

    print(f"Started        : {runtime.status()}")

    runtime.restart()

    print(f"Restarted      : {runtime.status()}")

    runtime.stop()

    print(f"Stopped        : {runtime.status()}")

    assert runtime.status() is False

    print()
    print("Runtime Manager Test Passed")


if __name__ == "__main__":

    run_test()