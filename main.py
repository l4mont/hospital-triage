"""Demonstrate the triage queue using the assignment's sample patients."""

from triage_system import TriageSystem


def main():
    triage = TriageSystem()
    arrivals = [
        ("Sofia", 5), ("Bob", 2), ("Charlie", 4), ("Diana", 3),
        ("Eli", 1), ("Tom", 4), ("Alice", 5), ("Rachel", 4),
    ]
    for name, severity in arrivals:
        triage.add_patient(name, severity)

    size_before = triage.size()
    print(f"Next patient: {triage.peek_next()}")
    size_after = triage.size()
    if size_before != size_after:
        raise RuntimeError("Peeking changed the queue size.")
    print(f"Queue size before and after peek: {size_before}, {size_after}")

    print("Treatment order:")
    while not triage.is_empty():
        name, severity = triage.process_next()
        print(f"{name} (severity {severity})")

    print(f"Process on empty queue: {triage.process_next()}")
    print(f"Peek on empty queue: {triage.peek_next()}")
    try:
        triage.add_patient("Morgan", 6)
    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
