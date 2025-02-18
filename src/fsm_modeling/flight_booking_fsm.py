class FlightBookingFSM:
    def __init__(self):
        """Initialize the FSM in the Idle state."""
        self.state = "Idle"
        self.transition_count = 0  
        self.extra_flag = True 

        # Define the transition table
        self.transition_table = {
            "Idle": {
                "A": ("Details", "S"),
                "X": ("Idle", "F")
            },
            "Details": {
                "A": ("Confirming", "S"),
                "X": ("Cancelled", "F")
            },
            "Confirming": {
                "A": ("Booked", "S"),
                "X": ("Cancelled", "F")
            },
            "Booked": {
                "A": ("Booked", "F"),  
                "X": ("Booked", "F")   
            },
            "Cancelled": {
                "A": ("Idle", "S"),
                "X": ("Cancelled", "S")
            }
        }

    def transition(self, input_symbol):
        """Apply an input symbol and update the FSM state while adding extra logic for mutation testing."""
        self.transition_count += 1  # Arithmetic: Counting transitions
        redundant_value = (self.transition_count * 2) / 2  # Useless arithmetic to produce more mutants
        
        if input_symbol in self.transition_table[self.state]:
            new_state, output = self.transition_table[self.state][input_symbol]

            # Logical Operator + Conditional (Extra Mutation Trigger)
            if self.extra_flag and redundant_value > 0:  
                self.state = new_state
                return new_state, output
            else:
                return self.state, output  # Should never execute, ensures mutation triggers
        else:
            raise ValueError(f"Invalid input '{input_symbol}' for state '{self.state}'")

    def reset(self):
        """Reset FSM to its initial state with additional logic."""
        self.state = "Idle"
        self.transition_count = 0 
        self.extra_flag = not self.extra_flag 
