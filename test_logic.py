"""Run simple tests for the ClashCheck checking functions."""  # Explain the purpose of this file.

# Import Python's built-in testing tool.
import unittest  # Use Python's standard test system.

# Import the two functions that will be tested.
from clash_logic import find_clashes, time_to_minutes  # Load the functions being tested.


class ClashLogicTests(unittest.TestCase):  # Group the ClashCheck tests inside one test class.
    def test_time_to_minutes(self):  # Test that a normal time is converted correctly.
        result = time_to_minutes("09:30")  # Convert 9:30 am into minutes after midnight.
        self.assertEqual(result, 570)  # Check that 9 hours and 30 minutes equals 570 minutes.

    def test_overlapping_events(self):  # Test that overlapping events are found.
        events = [  # Create two events that overlap on Monday.
            {"day": "Monday", "name": "Lecture", "start": "09:00", "end": "10:30", "location": "City Campus"},  # Add the first event.
            {"day": "Monday", "name": "Tutorial", "start": "10:00", "end": "11:00", "location": "City Campus"},  # Add the second event.
        ]  # Finish the test event list.
        messages, rows = find_clashes(events, 20)  # Check the two events with a 20-minute travel rule.
        self.assertEqual(len(messages), 1)  # Check that exactly one problem was found.
        self.assertIn("overlaps", messages[0])  # Check that the message describes an overlap.
        self.assertEqual(rows, {0, 1})  # Check that both table rows are marked.

    def test_short_travel_time(self):  # Test that a short travel gap is found.
        events = [  # Create two events at different locations.
            {"day": "Tuesday", "name": "Class", "start": "09:00", "end": "10:00", "location": "City Campus"},  # Add the earlier event.
            {"day": "Tuesday", "name": "Work", "start": "10:10", "end": "12:00", "location": "Haymarket"},  # Add the later event.
        ]  # Finish the test event list.
        messages, rows = find_clashes(events, 20)  # Check the events using a 20-minute travel rule.
        self.assertEqual(len(messages), 1)  # Check that exactly one problem was found.
        self.assertIn("20 minutes are required", messages[0])  # Check that the message explains the rule.
        self.assertEqual(rows, {0, 1})  # Check that both table rows are marked.

    def test_safe_events(self):  # Test that safe events do not create warnings.
        events = [  # Create two events with enough travel time.
            {"day": "Wednesday", "name": "Lecture", "start": "09:00", "end": "10:00", "location": "City Campus"},  # Add the earlier event.
            {"day": "Wednesday", "name": "Study", "start": "10:30", "end": "11:00", "location": "Haymarket"},  # Add the later event.
        ]  # Finish the test event list.
        messages, rows = find_clashes(events, 20)  # Check the events using a 20-minute travel rule.
        self.assertEqual(messages, [])  # Check that no warning messages were created.
        self.assertEqual(rows, set())  # Check that no table rows were marked.


if __name__ == "__main__":  # Run the tests only when this file is opened directly.
    unittest.main()  # Start Python's test runner.
