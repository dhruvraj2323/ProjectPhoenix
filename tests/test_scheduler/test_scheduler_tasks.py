"""
=================================================
Project Phoenix
Scheduler Tasks Test
=================================================
"""

from scheduler.scheduler_tasks import SchedulerTasks


def run_test():

    market = SchedulerTasks.market_update()
    signal = SchedulerTasks.signal_generation()
    risk = SchedulerTasks.risk_evaluation()
    paper = SchedulerTasks.paper_trading()
    dashboard = SchedulerTasks.dashboard_refresh()
    alert = SchedulerTasks.alert_dispatch()

    print("===== Scheduler Tasks =====")

    print(market)
    print(signal)
    print(risk)
    print(paper)
    print(dashboard)
    print(alert)

    assert market == "Market Update Executed"
    assert signal == "Signal Generation Executed"
    assert risk == "Risk Evaluation Executed"
    assert paper == "Paper Trading Executed"
    assert dashboard == "Dashboard Refresh Executed"
    assert alert == "Alert Dispatch Executed"

    print()
    print("Scheduler Tasks Test Passed")


if __name__ == "__main__":

    run_test()