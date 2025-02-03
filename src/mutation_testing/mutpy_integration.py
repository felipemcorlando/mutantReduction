import subprocess
import os
import json
import re
import ast
import astor  # Convert AST back to Python source code


class MutPyIntegration:
    def __init__(self, target_file, test_file, output_dir="data/output/"):
        self.target_file = target_file
        self.test_file = test_file
        self.output_dir = output_dir

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_mutants(self, mutants_info):
        """
        Save each mutant's actual source code and metadata to separate files.
        """
        for index, mutant_data in enumerate(mutants_info):
            file_path = os.path.join(self.output_dir, f"mutant_{index}.py")
            metadata_path = os.path.join(self.output_dir, f"mutant_{index}.json")

            # ✅ Save actual mutated source code
            with open(file_path, "w") as file:
                file.write(mutant_data["mutated_code"])

            # ✅ Save metadata
            metadata = {
                "id": index,
                "type": mutant_data["mutation_type"],
                "status": mutant_data["status"],
                "details": mutant_data["details"]
            }
            with open(metadata_path, "w") as meta_file:
                json.dump(metadata, meta_file, indent=4)

            print(f"✅ Saved mutant {index}: {file_path}")

    def extract_mutated_code(self, original_code, mutation_details):
        """
        Apply the mutation to the original code's AST and return the mutated code.
        """
        tree = ast.parse(original_code)

        # Example mutation: Modify binary operators (replace + with -)
        class MutantTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                # Replace + with -
                if isinstance(node.op, ast.Add):
                    node.op = ast.Sub()
                return self.generic_visit(node)

            def visit_Compare(self, node):
                # Replace > with <
                if isinstance(node.ops[0], ast.Gt):
                    node.ops[0] = ast.Lt()
                return self.generic_visit(node)

            def visit_If(self, node):
                # Flip the condition
                node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                return self.generic_visit(node)
        mutated_tree = MutantTransformer().visit(tree)
        try:
            mutated_code = astor.to_source(mutated_tree)
        except Exception as e:
            print(f"Skipping invalid mutant: {e}")
            return None

        return mutated_code

    def parse_mutpy_output(self, output):
        """
        Parse the CLI output to extract mutant details and mutated source code.
        """
        mutants_info = []

        # Read the original source code
        with open(self.target_file, "r") as f:
            original_code = f.read()

        # Regex to extract mutant details from MutPy output
        pattern = re.compile(
            r" - \[#\s*(\d+)\] (\w+) .*?: \[.*?\] (killed|incompetent|survived|timeout)"
        )
        matches = pattern.findall(output)

        # Extract real mutated code
        for match in matches:
            index, mutation_type, status = match

            mutated_code = self.extract_mutated_code(original_code, mutation_type)

            mutants_info.append({
                "index": int(index),
                "mutation_type": mutation_type,
                "status": status,
                "mutated_code": mutated_code,
                "details": {
                    "operator": mutation_type,
                    "result": status
                }
            })

        return mutants_info

    def run_mutation_testing(self):
        """
        Runs MutPy using the CLI and saves mutants to files.
        """
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath("data/input/flask_app")

        command = [
            "mut.py",
            "--target", self.target_file,
            "--unit-test", self.test_file,
            "--operator", "AOR", "ROR", "COI", "EXS", "EHD", "DDL", "SDL"  # Add more operators

        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, env=env)
            print("MutPy Output:\n", result.stdout)

            # ✅ Save output log
            log_path = os.path.join(self.output_dir, "mutpy_results.log")
            with open(log_path, "w") as log_file:
                log_file.write(result.stdout)

            # ✅ Parse mutants and save them
            mutants_info = self.parse_mutpy_output(result.stdout)
            self.save_mutants(mutants_info)

        except subprocess.CalledProcessError as e:
            print("❌ Error running MutPy:\n", e.stderr)
            print("⚠️ Full Output:\n", e.stdout)


if __name__ == "__main__":
    target = "data/input/flask_app/app.py"
    test = "data/input/flask_app/tests/test_app.py"
    output_dir = "data/output"

    mutpy = MutPyIntegration(target, test, output_dir)
    mutpy.run_mutation_testing()
