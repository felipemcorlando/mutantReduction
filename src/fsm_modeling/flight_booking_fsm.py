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
        self.booking_fee = 100  # Base fee for booking
        self.machine = Machine(model=self, states=self.states, initial="idle")

        # Define state transitions
        self.machine.add_transition(trigger="search_flights", source="idle", dest="searching")
        self.machine.add_transition(trigger="select_flight", source="searching", dest="selecting", after=self.apply_discount)
        self.machine.add_transition(trigger="enter_payment", source="selecting", dest="booking", after=self.add_tax)
        self.machine.add_transition(trigger="confirm_booking", source="booking", dest="confirmed")

    def apply_discount(self):
        """Applies a discount if the user selects a flight early."""
        if self.booking_fee > 50 and self.booking_fee <= 100:
            discount_rate = 0.1  # 10% discount
            self.booking_fee = self.booking_fee - (self.booking_fee * discount_rate)  # Subtraction + Multiplication
        if self.booking_fee > 100:
            discount_rate = 0.2  # 20% discount
            self.booking_fee = self.booking_fee - (self.booking_fee * discount_rate)  # Subtraction + Multiplication

    def add_tax(self):
        """Adds tax to the booking fee."""
        tax_rate = 0.2  # 20% tax
        self.booking_fee = self.booking_fee + (self.booking_fee * tax_rate)  # Addition + Multiplication


    def get_state(self):
        """
        Returns the current state of the FSM.
        """
        return self.state


# Example usage
if __name__ == "__main__":
    booking = FlightBookingFSM()

    print(f"Initial State: {booking.get_state()} - Fee: {booking.booking_fee}")  # 'idle'

    booking.search_flights()
    print(f"State after searching: {booking.get_state()} - Fee: {booking.booking_fee}")  # 'searching'

    booking.select_flight()
    print(f"State after selecting: {booking.get_state()} - Fee: {booking.booking_fee}")  # 'selecting' (discount applied)

    booking.enter_payment()
    print(f"State after entering payment: {booking.get_state()} - Fee: {booking.booking_fee}")  # 'booking' (tax applied)

    booking.confirm_booking()
    print(f"Final State: {booking.get_state()} - Fee: {booking.booking_fee}")  # 'confirmed'
