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
            if "[# " in line:  # Identify mutation lines
                parts = line.split()
                
                mutant_id = parts[1].strip("[]") if len(parts) > 1 else "UNKNOWN_ID"

                mutation_type = None
                for part in parts:
                    if part in ["AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL"]:
                        mutation_type = part
                        break  
                
                if mutation_type is None:
                    print(f"⚠️ Warning: Could not extract mutation type from line: {line}")
                    continue  

                mutant_file = f"mutant_{mutant_counter}.py"
                mutant_path = os.path.join(self.mutants_dir, mutant_file)

                mutated_code = self.apply_mutation(mutation_type)

                if "No mutations applied" in mutated_code:
                    print(f"⚠️ Mutation {mutant_id} ({mutation_type}) had no effect!")

                with open(mutant_path, "w") as file:
                    file.write(mutated_code)

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
                self.mutations_applied = 0  

            def visit_BinOp(self, node):
                """Applies Arithmetic Operator Replacement (AOR)."""
                if mutation_type == "AOR":
                    self.mutations_applied += 1
                    if isinstance(node.op, ast.Add):
                        node.op = ast.Sub()
                    elif isinstance(node.op, ast.Sub):
                        node.op = ast.Mult()
                    elif isinstance(node.op, ast.Mult):
                        node.op = ast.Div()
                    elif isinstance(node.op, ast.Div):
                        node.op = ast.Add()
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
                    del node.body[random.randint(0, len(node.body) - 1)]
                return self.generic_visit(node)

            def visit_While(self, node):
                """Applies Loop Mutation (LOOP) to change flow of while-loops."""
                if mutation_type == "LOOP":
                    self.mutations_applied += 1
                    node.orelse = [ast.Break()]
                return self.generic_visit(node)

            def visit_BoolOp(self, node):
                """Modifies logical expressions (and → or, or → and)."""
                if mutation_type == "LOGIC":
                    self.mutations_applied += 1
                    if isinstance(node.op, ast.And):
                        node.op = ast.Or()
                    elif isinstance(node.op, ast.Or):
                        node.op = ast.And()
                return self.generic_visit(node)

            def visit_UnaryOp(self, node):
                """Flips 'not' operations."""
                if mutation_type == "LOGIC":
                    self.mutations_applied += 1
                    if isinstance(node.op, ast.Not):
                        return node.operand  
                return self.generic_visit(node)

        transformer = MutantTransformer()
        mutated_tree = transformer.visit(tree)

        if transformer.mutations_applied == 0:
            print(f"⚠️ Warning: No mutations applied for {mutation_type}, something might be wrong!")

        return astor.to_source(mutated_tree)

if __name__ == "__main__":
    mutpy = MutPyIntegration()
    mutpy.run_mutation_testing()
