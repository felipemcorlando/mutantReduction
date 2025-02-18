import os
import json
import subprocess
import ast
import astor
import random
from src.fsm_modeling.flight_booking_fsm import FlightBookingFSM  

class MutPyIntegration:
    """
    Handles mutant generation using MutPy and stores them for later execution.
    """

    def __init__(self, target_file="src/fsm_modeling/flight_booking_fsm.py", 
                 test_file="tests/test_fsm.py",
                 mutants_dir="data/output/mutants/"):
        self.target_file = target_file
        self.test_file = test_file
        self.mutants_dir = mutants_dir
        os.makedirs(self.mutants_dir, exist_ok=True)  # Ensure mutants directory exists

    def run_mutation_testing(self):
        """
        Runs MutPy to generate FSM mutants and saves them.
        """
        command = [
            "mut.py",
            "--target", self.target_file,
            "--unit-test", self.test_file,  # ✅ Ensure unit test is included!
            "--operator", "AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL",
            "--report-html", "data/output/mutants_report",
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("MutPy Output:\n", result.stdout)
            self.process_mutants(result.stdout)  # Extract and store mutants
        except subprocess.CalledProcessError as e:
            print("Error running MutPy:\n", e.stderr)

    def process_mutants(self, output):
        """
        Parses MutPy output and extracts FSM-specific mutants.
        """
        mutant_counter = 0

        for line in output.split("\n"):
            if "[# " in line:  # Identify mutation lines
                parts = line.split()
                mutation_type = next((part for part in parts if part in 
                                    ["AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL", "FSM_TRANS"]), None)
                
                if not mutation_type:
                    print(f"⚠️ Warning: Could not extract mutation type from line: {line}")
                    continue  

                mutant_file = f"mutant_{mutant_counter}.py"
                mutant_path = os.path.join(self.mutants_dir, mutant_file)

                mutated_code = self.apply_mutation(mutation_type)

                if "No mutations applied" in mutated_code:
                    print(f"⚠️ Mutation {mutant_counter} ({mutation_type}) had no effect!")

                with open(mutant_path, "w") as file:
                    file.write(mutated_code)

                mutant_counter += 1

        print(f"✅ {mutant_counter} FSM mutants saved to {self.mutants_dir}")


    def apply_mutation(self, mutation_type):
        """
        Applies FSM-specific mutations.
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

            def visit_BoolOp(self, node):
                """Modifies logical expressions (and → or, or → and)."""
                if mutation_type == "COI":
                    self.mutations_applied += 1
                    if isinstance(node.op, ast.And):
                        node.op = ast.Or()
                    elif isinstance(node.op, ast.Or):
                        node.op = ast.And()
                return self.generic_visit(node)

            def visit_Dict(self, node):
                """Mutates FSM transition table by swapping states randomly."""
                if mutation_type in ["FSM_TRANS"]:
                    self.mutations_applied += 1
                    keys = list(node.keys)
                    if len(keys) > 1:
                        i, j = random.sample(range(len(keys)), 2)
                        node.keys[i], node.keys[j] = node.keys[j], node.keys[i]
                return self.generic_visit(node)

        transformer = MutantTransformer()
        mutated_tree = transformer.visit(tree)

        if transformer.mutations_applied == 0:
            print(f"⚠️ Warning: No mutations applied for {mutation_type}, something might be wrong!")

        return astor.to_source(mutated_tree)

if __name__ == "__main__":
    mutpy = MutPyIntegration()
    mutpy.run_mutation_testing()
