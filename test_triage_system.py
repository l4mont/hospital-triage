"""Behavior tests for the TriageSystem public interface."""

import unittest

from triage_system import TriageSystem


class TestTriageSystem(unittest.TestCase):
    def setUp(self):
        self.triage = TriageSystem()

    def test_higher_severity_is_processed_first(self):
        self.triage.add_patient("Low", 1)
        self.triage.add_patient("High", 5)
        self.triage.add_patient("Middle", 3)
        self.assertEqual(self.triage.process_next(), ("High", 5))
        self.assertEqual(self.triage.process_next(), ("Middle", 3))
        self.assertEqual(self.triage.process_next(), ("Low", 1))

    def test_equal_severity_preserves_arrival_order(self):
        self.triage.add_patient("Zoe", 4)
        self.triage.add_patient("Alice", 4)
        self.assertEqual(self.triage.process_next(), ("Zoe", 4))
        self.assertEqual(self.triage.process_next(), ("Alice", 4))

    def test_peek_does_not_remove_patient(self):
        self.triage.add_patient("Sofia", 5)
        self.assertEqual(self.triage.peek_next(), ("Sofia", 5))
        self.assertEqual(self.triage.size(), 1)
        self.assertEqual(self.triage.process_next(), ("Sofia", 5))

    def test_empty_queue_returns_none(self):
        self.assertIsNone(self.triage.process_next())
        self.assertIsNone(self.triage.peek_next())

    def test_invalid_input_leaves_queue_unchanged(self):
        self.triage.add_patient("Waiting", 3)
        invalid_patients = [
            ("", 3), ("   ", 3), (None, 3), ("Patient", 0),
            ("Patient", 6), ("Patient", 3.0), ("Patient", True),
        ]
        for name, severity in invalid_patients:
            with self.subTest(name=name, severity=severity):
                with self.assertRaises(ValueError):
                    self.triage.add_patient(name, severity)
                self.assertEqual(self.triage.size(), 1)
                self.assertEqual(self.triage.peek_next(), ("Waiting", 3))
        self.assertEqual(self.triage.process_next(), ("Waiting", 3))
        self.assertIsNone(self.triage.process_next())

    def test_size_is_empty_and_clear_after_removal(self):
        self.assertTrue(self.triage.is_empty())
        self.assertEqual(self.triage.size(), 0)
        self.triage.add_patient("First", 4)
        self.triage.add_patient("Second", 2)
        self.assertFalse(self.triage.is_empty())
        self.assertEqual(self.triage.size(), 2)
        self.triage.process_next()
        self.assertEqual(self.triage.size(), 1)
        self.triage.clear()
        self.assertTrue(self.triage.is_empty())
        self.assertEqual(self.triage.size(), 0)
        self.assertIsNone(self.triage.peek_next())

    def test_new_arrival_can_precede_waiting_patient(self):
        self.triage.add_patient("First", 4)
        self.triage.add_patient("Waiting", 2)
        self.assertEqual(self.triage.process_next(), ("First", 4))
        self.triage.add_patient("Urgent", 5)
        self.assertEqual(self.triage.process_next(), ("Urgent", 5))
        self.assertEqual(self.triage.process_next(), ("Waiting", 2))


if __name__ == "__main__":
    unittest.main()
