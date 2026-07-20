"""
=================================================
Project Phoenix
Scheduler Queue
=================================================

Task queue management.
"""


class SchedulerQueue:
    """
    Maintains execution queue.
    """

    def __init__(self):

        self.tasks = []

    def register(self, task):

        self.tasks.append(task)

    def remove(self, task):

        if task in self.tasks:
            self.tasks.remove(task)

    def execute(self):

        executed = []

        for task in self.tasks:

            executed.append(task())

        return executed