import unittest
from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM


class TestFlightBookingFSM(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh FSM instance before each test."""
        self.fsm = FlightBookingFSM()

    def test_initial_state(self):
        """Test that FSM starts in the Idle state."""
        self.assertEqual(self.fsm.state, "Idle")

    def test_valid_transitions(self):
        """Test valid FSM transitions using different input sequences."""
        test_cases = [
            (["A", "A", "A", "A"], "Booked"),  # Valid full sequence
            (["A", "X"], "Cancelled"),  # Cancel early
            (["X"], "Idle"),  # Stay in Idle
            (["A", "A", "X"], "Cancelled"),  # Cancel at Confirming
            (["A", "A", "A", "X"], "Booked"),  # X in Booked does nothing
        ]

        for inputs, expected_final_state in test_cases:
            with self.subTest(inputs=inputs, expected_state=expected_final_state):
                self.fsm.reset()
                for inp in inputs:
                    self.fsm.transition(inp)
                self.assertEqual(self.fsm.state, expected_final_state)

    def test_invalid_input(self):
        """Test that FSM raises an error on invalid input."""
        with self.assertRaises(ValueError):
            self.fsm.transition("B")  # Invalid input should raise an exception

    def test_reset_function(self):
        """Test the FSM reset functionality."""
        self.fsm.transition("A")
        self.assertNotEqual(self.fsm.state, "Idle")
        self.fsm.reset()
        self.assertEqual(self.fsm.state, "Idle")


if __name__ == "__main__":
    unittest.main()
