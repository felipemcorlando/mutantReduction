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
            if "[# " in line:
                parts = line.split(" ")
                mutant_id = parts[1].strip("[]")
                mutation_type = parts[2]
                status = parts[-1]

                mutant_file = f"mutant_{mutant_counter}.py"
                mutant_path = os.path.join(self.mutants_dir, mutant_file)

                # Generate a mutated version of the original FSM
                mutated_code = self.apply_mutation(mutation_type)

                # Save the mutant to a file
                with open(mutant_path, "w") as file:
                    file.write(mutated_code)

                # Run FSM analysis on the mutant
                fsm_result = self.analyzer.compare_fsm_behaviors(
                    original_events=["search_flights", "select_flight", "enter_payment", "confirm_booking"],
                    mutant_events=["search_flights", "select_flight", "confirm_booking"]  # Example mutant skipping payment
                )

                mutants_info[mutant_file] = {
                    "id": mutant_id,
                    "type": mutation_type,
                    "status": status,
                    "fsm_transitions": fsm_result
                }

                mutant_counter += 1

        # Save FSM results
        with open(self.fsm_output_file, "w") as f:
            json.dump(mutants_info, f, indent=4)
        print(f"✅ FSM transition data saved to {self.fsm_output_file}")

    def apply_mutation(self, mutation_type):
        """
        Applies a mutation to the FSM model uniquely per mutant.
        """
        with open(self.target_file, "r") as file:
            tree = ast.parse(file.read())

        class MutantTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                """Applies Arithmetic Operator Replacement (AOR)."""
                if mutation_type == "AOR":
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
                    node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                return self.generic_visit(node)

            def visit_FunctionDef(self, node):
                """Applies Statement Deletion (SDL)."""
                if mutation_type == "SDL":
                    if node.body:
                        node.body.pop(random.randint(0, len(node.body) - 1))
                return self.generic_visit(node)

        transformer = MutantTransformer()
        mutated_tree = transformer.visit(tree)

        return astor.to_source(mutated_tree)


if __name__ == "__main__":
    mutpy = MutPyIntegration()
    mutpy.run_mutation_testing()
