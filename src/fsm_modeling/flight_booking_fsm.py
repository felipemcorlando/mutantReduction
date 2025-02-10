from transitions import Machine

class FlightBookingFSM:
    """
    FSM for modeling the states of a flight booking service.
    """

    states = ["idle", "searching", "selecting", "booking", "confirmed"]

    def __init__(self):
        """
        Initializes the FSM with transitions defining user interactions.
        """
        self.machine = Machine(model=self, states=self.states, initial="idle")

        # Define state transitions
        self.machine.add_transition(trigger="search_flights", source="idle", dest="searching")
        self.machine.add_transition(trigger="select_flight", source="searching", dest="selecting")
        self.machine.add_transition(trigger="enter_payment", source="selecting", dest="booking")
        self.machine.add_transition(trigger="confirm_booking", source="booking", dest="confirmed")

    def get_state(self):
        """
        Returns the current state of the FSM.
        """
        return self.state


# Example usage
if __name__ == "__main__":
    booking = FlightBookingFSM()

    print(f"Initial State: {booking.get_state()}")  # Should be 'idle'

    booking.search_flights()
    print(f"State after searching: {booking.get_state()}")  # Should be 'searching'

    booking.select_flight()
    print(f"State after selecting: {booking.get_state()}")  # Should be 'selecting'

    booking.enter_payment()
    print(f"State after entering payment: {booking.get_state()}")  # Should be 'booking'

    booking.confirm_booking()
    print(f"Final State: {booking.get_state()}")  # Should be 'confirmed'
