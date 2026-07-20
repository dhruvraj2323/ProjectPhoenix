"""
=================================================
Project Phoenix
Dashboard Renderer Test
=================================================
"""

from dashboard.dashboard_renderer import DashboardRenderer


def run_test():

    renderer = DashboardRenderer()

    result = renderer.render()

    assert result

    print()
    print("Dashboard Renderer Test Passed")


if __name__ == "__main__":

    run_test()