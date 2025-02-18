import os
import json
from itertools import combinations
from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM  

# Paths
mutants_dir = "data/output/mutants/"
cluster_assignments_path = "data/output/clustering/kmeans_cluster_assignments.json"
output_path = "data/output/equivalence_testing/cluster_equivalence_results.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Distinguishing Sequence (DS)
DS_SEQUENCE = ["A", "A", "A", "A"]

# DS-Method Test Suite
TEST_SUITE = [
    ["A", "A", "A", "A"],  # Idle → DS
    ["A", "A", "A", "A", "A"],  # Details → DS
    ["A", "A", "A", "A", "A", "A"],  # Confirming → DS
    ["X", "A", "A", "A", "A"],  # Cancelled → DS
    ["A", "X", "A", "A", "A", "A"],  # Cancelled (Alternative) → DS
    ["A", "A", "A", "X", "A", "A", "A", "A"],  # Confirming → Cancelled → DS
    ["A", "A", "A", "X", "A", "A", "A", "A", "A"],  # Confirming → Cancelled → DS
    ["A", "A", "A", "A", "X", "A", "A", "A", "A"],  # Booked → DS
    ["A", "A", "A", "A", "X", "A", "A", "A", "A", "A"],  # Booked → DS
    ["A", "A", "X", "A", "A", "A", "A"]  # Details → Cancelled → DS
]

# Execute Test Suite on FSM
def execute_fsm(fsm, sequence):
    """
    Runs the FSM on a given sequence and returns the final state & outputs.
    """
    fsm.reset()
    outputs = []
    for input_symbol in sequence:
        try:
            _, output = fsm.transition(input_symbol)
            outputs.append(output)
        except ValueError as e:
            return "Error", []  # Return error flag if FSM encounters invalid input
    return fsm.state, outputs

# Compare two FSM mutants for equivalence
def are_mutants_equivalent(fsm1, fsm2):
    """
    Compare FSM outputs using the DS-method test suite.
    """
    for seq in TEST_SUITE:
        state1, outputs1 = execute_fsm(fsm1, seq)
        state2, outputs2 = execute_fsm(fsm2, seq)
        
        if state1 == "Error" or state2 == "Error":
            return False  # If any FSM throws an error, they are NOT equivalent

        if state1 != state2 or outputs1 != outputs2:
            return False  # Different behavior → NOT equivalent

    return True  # No difference detected → Equivalent mutant

# Load Cluster Assignments
with open(cluster_assignments_path, "r") as f:
    cluster_assignments = json.load(f)

# Group mutants by cluster
clusters = {}
for mutant, cluster in cluster_assignments.items():
    clusters.setdefault(cluster, []).append(mutant)

# Run Equivalence Testing Within Each Cluster
equivalence_results = {}

for cluster_id, mutants in clusters.items():
    print(f"🔍 Checking equivalence within Cluster {cluster_id}...")

    # Compare all mutant pairs in the cluster
    for mutant1, mutant2 in combinations(mutants, 2):
        mutant1_path = os.path.join(mutants_dir, mutant1)
        mutant2_path = os.path.join(mutants_dir, mutant2)

        try:
            fsm1 = FlightBookingFSM()
            fsm2 = FlightBookingFSM()

            # Check equivalence
            if are_mutants_equivalent(fsm1, fsm2):
                equivalence_results[f"{mutant1} ↔ {mutant2}"] = "Equivalent"
            else:
                equivalence_results[f"{mutant1} ↔ {mutant2}"] = "Non-Equivalent"
        except Exception as e:
            equivalence_results[f"{mutant1} ↔ {mutant2}"] = f"Error: {str(e)}"

# 💾 Save Results
with open(output_path, "w") as f:
    json.dump(equivalence_results, f, indent=4)

print(f"✅ Cluster-Based Equivalence Results Saved to {output_path}")
