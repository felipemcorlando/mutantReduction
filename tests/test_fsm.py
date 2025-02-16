import unittest
from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM
from transitions.core import MachineError  # To catch invalid transitions

class TestFlightBookingFSM(unittest.TestCase):
    """
    Unit tests for the FlightBookingFSM.
    """

    def setUp(self):
        """
        Set up a new FSM instance for each test.
        """
        self.booking = FlightBookingFSM()

    def test_initial_state(self):
        """Test that the FSM starts in 'idle' state."""
        self.assertEqual(self.booking.get_state(), "idle")

    def test_valid_transitions(self):
        """Test that valid transitions move to the correct states."""
        self.booking.search_flights()
        self.assertEqual(self.booking.get_state(), "searching")

        self.booking.select_flight()
        self.assertEqual(self.booking.get_state(), "selecting")

        self.booking.enter_payment()
        self.assertEqual(self.booking.get_state(), "booking")

        self.booking.confirm_booking()
        self.assertEqual(self.booking.get_state(), "confirmed")

    def test_invalid_transitions(self):
        """Test that invalid transitions raise an error."""
        with self.assertRaises(MachineError):
            self.booking.select_flight()  # Can't select flight before searching

        with self.assertRaises(MachineError):
            self.booking.enter_payment()  # Can't enter payment before selecting

        with self.assertRaises(MachineError):
            self.booking.confirm_booking()  # Can't confirm before payment

    def test_complete_flight_booking(self):
        """Test the full sequence from idle to confirmed."""
        self.booking.search_flights()
        self.booking.select_flight()
        self.booking.enter_payment()
        self.booking.confirm_booking()
        self.assertEqual(self.booking.get_state(), "confirmed")

if __name__ == "__main__":
    unittest.main()
