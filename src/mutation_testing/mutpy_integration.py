import os
import json
import subprocess
import ast
import astor
import random
from src.fsm_modeling.fsm_analysis import FSMAnalyzer
from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM

class MutPyIntegration:
    """
    Handles mutant generation using MutPy and integrates FSM analysis.
    """

    def __init__(self, target_file="src/fsm_modeling/flight_booking_fsm.py", 
                 test_file="tests/test_fsm.py", 
                 mutants_dir="data/output/mutants/", 
                 fsm_output_file="data/output/fsm_transitions.json"):
        self.target_file = target_file
        self.test_file = test_file
        self.mutants_dir = mutants_dir
        self.fsm_output_file = fsm_output_file
        self.analyzer = FSMAnalyzer()

        # Ensure output directory exists
        os.makedirs(self.mutants_dir, exist_ok=True)

    def run_mutation_testing(self):
        """
        Runs MutPy to generate mutants and executes FSM analysis on each mutant.
        """
        command = [
            "mut.py",
            "--target", self.target_file,
            "--unit-test", self.test_file,
            "--operator", "AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL"
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("MutPy Output:\n", result.stdout)

            # Process MutPy output and extract mutants
            self.process_mutants(result.stdout)

        except subprocess.CalledProcessError as e:
            print("Error running MutPy:\n", e.stderr)

    def process_mutants(self, output):
        """
        Parses MutPy output, extracts mutants, and runs FSM analysis.
        """
        mutants_info = {}
        mutant_counter = 0

        for line in output.split("\n"):
            print(f"🔍 Debug: Processing line -> {line}")  # ✅ Debugging

            if "[# " in line:  # Identify mutation lines
                parts = line.split()  # Split by space to handle inconsistent formatting
                
                # Extract mutation ID (handling edge cases)
                mutant_id = parts[1].strip("[]") if len(parts) > 1 else "UNKNOWN_ID"

                # Extract mutation type by scanning for valid types
                mutation_type = None
                for part in parts:
                    if part in ["AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL"]:  # Mutation types
                        mutation_type = part
                        break  # Stop once we find a valid mutation type
                
                if mutation_type is None:
                    print(f"⚠️ Warning: Could not extract mutation type from line: {line}")
                    continue  # Skip invalid mutations

                print(f"🛠 Applying mutation: {mutation_type}")  # ✅ Confirm extracted type

                mutant_file = f"mutant_{mutant_counter}.py"
                mutant_path = os.path.join(self.mutants_dir, mutant_file)

                # Generate a mutated version of the original FSM
                mutated_code = self.apply_mutation(mutation_type)

                # Check if mutation was applied
                if "No mutations applied" in mutated_code:
                    print(f"⚠️ Mutation {mutant_id} ({mutation_type}) had no effect!")

                # Save the mutant to a file
                with open(mutant_path, "w") as file:
                    file.write(mutated_code)

                # Run FSM analysis on the mutant
                fsm_result = self.analyzer.compare_fsm_behaviors(
                    original_events=["search_flights", "select_flight", "enter_payment", "confirm_booking"],
                    mutant_events=["search_flights", "select_flight", "confirm_booking"]
                )

                mutants_info[mutant_file] = {
                    "id": mutant_id,
                    "type": mutation_type,
                    "fsm_transitions": fsm_result
                }

                mutant_counter += 1

        # Save FSM results
        with open(self.fsm_output_file, "w") as f:
            json.dump(mutants_info, f, indent=4)
        print(f"✅ FSM transition data saved to {self.fsm_output_file}")


    def apply_mutation(self, mutation_type):
        """
        Applies a mutation to the FSM model ensuring unique changes for each mutant.
        """
        with open(self.target_file, "r") as file:
            tree = ast.parse(file.read())

        class MutantTransformer(ast.NodeTransformer):
            def __init__(self):
                super().__init__()
                self.mutations_applied = 0  # Track how many changes were made

            def visit_BinOp(self, node):
                """Applies Arithmetic Operator Replacement (AOR)."""
                if mutation_type == "AOR":
                    self.mutations_applied += 1
                    if isinstance(node.op, ast.Add):
                        node.op = ast.Sub()
                    elif isinstance(node.op, ast.Sub):
                        node.op = ast.Add()
                    elif isinstance(node.op, ast.Mult):
                        node.op = ast.Div()
                    elif isinstance(node.op, ast.Div):
                        node.op = ast.Mult()
                return self.generic_visit(node)

            def visit_Compare(self, node):
                """Applies Relational Operator Replacement (ROR)."""
                if mutation_type == "ROR":
                    self.mutations_applied += 1
                    if isinstance(node.ops[0], ast.Gt):
                        node.ops[0] = ast.Lt()
                    elif isinstance(node.ops[0], ast.Lt):
                        node.ops[0] = ast.Gt()
                    elif isinstance(node.ops[0], ast.Eq):
                        node.ops[0] = ast.NotEq()
                    elif isinstance(node.ops[0], ast.NotEq):
                        node.ops[0] = ast.Eq()
                return self.generic_visit(node)

            def visit_If(self, node):
                """Applies Conditional Operator Insertion (COI)."""
                if mutation_type == "COI":
                    self.mutations_applied += 1
                    node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                return self.generic_visit(node)

            def visit_FunctionDef(self, node):
                """Applies Statement Deletion (SDL)."""
                if mutation_type == "SDL" and node.body:
                    self.mutations_applied += 1
                    del node.body[random.randint(0, len(node.body) - 1)]  # Delete a random statement
                return self.generic_visit(node)

        transformer = MutantTransformer()
        mutated_tree = transformer.visit(tree)

        if transformer.mutations_applied == 0:
            print(f"⚠️ Warning: No mutations applied for {mutation_type}, something might be wrong!")

        return astor.to_source(mutated_tree)

if __name__ == "__main__":
    mutpy = MutPyIntegration()
    mutpy.run_mutation_testing()
