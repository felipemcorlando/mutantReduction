from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM
from typing import List

class FSMAnalyzer:
    """
    Compares FSM transition sequences between the original program and its mutants.
    """

    def __init__(self):
        self.original_fsm = FlightBookingFSM()

    def get_fsm_transitions(self, events: List[str]) -> List[str]:
        """
        Executes a sequence of events in the FSM and returns the state transitions.
        
        :param events: List of event triggers to apply to the FSM.
        :return: List of states the FSM transitioned through.
        """
        fsm = FlightBookingFSM()
        transition_sequence = ["idle"]  # Initial state

        for event in events:
            if hasattr(fsm, event):  # Ensure event exists in FSM
                try:
                    getattr(fsm, event)()  # Trigger event
                    transition_sequence.append(fsm.get_state())  # Capture new state
                except Exception as e:
                    transition_sequence.append(f"ERROR: {e}")  # Capture errors
                    break

        return transition_sequence

    def compare_fsm_behaviors(self, original_events: List[str], mutant_events: List[str]) -> dict:
        """
        Compares FSM transition sequences between original and mutated programs.
        
        :param original_events: List of events for the original FSM.
        :param mutant_events: List of events for the mutant FSM.
        :return: Dictionary with differences between original and mutant behaviors.
        """
        original_transitions = self.get_fsm_transitions(original_events)
        mutant_transitions = self.get_fsm_transitions(mutant_events)

        differences = []
        for i in range(min(len(original_transitions), len(mutant_transitions))):
            if original_transitions[i] != mutant_transitions[i]:
                differences.append({
                    "step": i,
                    "original_state": original_transitions[i],
                    "mutant_state": mutant_transitions[i]
                })

        return {
            "original_transitions": original_transitions,
            "mutant_transitions": mutant_transitions,
            "differences": differences
        }

# Example usage
if __name__ == "__main__":
    analyzer = FSMAnalyzer()

    original_sequence = ["search_flights", "select_flight", "enter_payment", "confirm_booking"]
    mutant_sequence = ["search_flights", "select_flight", "confirm_booking"]  # Mutant skips payment

    result = analyzer.compare_fsm_behaviors(original_sequence, mutant_sequence)
    print("Original FSM Transitions:", result["original_transitions"])
    print("Mutant FSM Transitions:", result["mutant_transitions"])
    print("Differences:", result["differences"])
