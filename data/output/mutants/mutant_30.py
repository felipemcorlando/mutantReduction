from transitions import Machine


class FlightBookingFSM:
    """
    FSM for modeling the states of a flight booking service.
    """
    states = ['idle', 'searching', 'selecting', 'booking', 'confirmed']

    def __init__(self):
        """
        Initializes the FSM with transitions defining user interactions.
        """
        self.machine = Machine(model=self, states=self.states, initial='idle')
        self.machine.add_transition(trigger='search_flights', source='idle',
            dest='searching')
        self.machine.add_transition(trigger='select_flight', source=
            'searching', dest='selecting', after=self.apply_discount)
        self.machine.add_transition(trigger='enter_payment', source=
            'selecting', dest='booking', after=self.add_tax)
        self.machine.add_transition(trigger='confirm_booking', source=
            'booking', dest='confirmed')

    def apply_discount(self):
        """Applies a discount if the user selects a flight early."""
        if self.booking_fee > 100:
            discount_rate = 0.2
            self.booking_fee = (self.booking_fee - self.booking_fee *
                discount_rate)

    def add_tax(self):
        """Adds tax to the booking fee."""
        tax_rate = 0.2

    def get_state(self):
        return self.state


if __name__ == '__main__':
    booking = FlightBookingFSM()
    print(f'Initial State: {booking.get_state()} - Fee: {booking.booking_fee}')
    booking.search_flights()
    print(
        f'State after searching: {booking.get_state()} - Fee: {booking.booking_fee}'
        )
    booking.select_flight()
    print(
        f'State after selecting: {booking.get_state()} - Fee: {booking.booking_fee}'
        )
    booking.enter_payment()
    print(
        f'State after entering payment: {booking.get_state()} - Fee: {booking.booking_fee}'
        )
    booking.confirm_booking()
    print(f'Final State: {booking.get_state()} - Fee: {booking.booking_fee}')
