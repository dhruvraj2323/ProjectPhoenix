"""
=================================================
Project Phoenix
Scheduler Test
M58
=================================================
"""

from deployment.runtime import (
    Runtime,
)

from deployment.scheduler import (
    Scheduler,
)


def test_scheduler():

    runtime = Runtime()

    scheduler = Scheduler(

        runtime=runtime,

        interval=1,

    )

    assert scheduler.running is False

    scheduler.run_once()

    assert runtime.running is True

    scheduler.stop()

    assert scheduler.running is False