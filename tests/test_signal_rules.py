"""
Project Phoenix
M8 Test - signal_rules.py
"""

from signals.signal_rules import AlwaysHoldRule


def main():
    rule = AlwaysHoldRule()

    result = rule.evaluate()

    print("===== Rule Test =====")
    print(f"Rule Name : {result.rule_name}")
    print(f"Direction : {result.direction.name}")
    print(f"Strength  : {result.strength}")
    print(f"Passed    : {result.passed}")
    print(f"Reason    : {result.reason}")


if __name__ == "__main__":
    main()