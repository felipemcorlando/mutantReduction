import ast
import os
import json

class StructuralMetricsExtractor(ast.NodeVisitor):
    def __init__(self):
        self.func_calls = 0
        self.conditionals = 0
        self.arithmetic_ops = 0
        self.logical_ops = 0
        self.complexity = 1  # Cyclomatic Complexity (default 1 for base function)
        self.num_lines = 0  # Count number of lines

    def visit_FunctionDef(self, node):
        """Counts function definitions (for complexity)."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        """Counts function calls."""
        self.func_calls += 1
        self.generic_visit(node)

    def visit_If(self, node):
        """Counts conditional statements."""
        self.conditionals += 1
        self.complexity += 1  # Increases complexity for each condition
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """Counts arithmetic operations (+, -, *, /)."""
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            self.arithmetic_ops += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Counts logical operations (and, or)."""
        self.logical_ops += 1
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        """Counts negations (not)."""
        if isinstance(node.op, ast.Not):
            self.logical_ops += 1
        self.generic_visit(node)

    def extract_metrics(self, file_path):
        """Parses the Python file and extracts structural metrics."""
        with open(file_path, "r") as file:
            source_code = file.readlines()

        self.num_lines = len(source_code)  # Count number of lines in the file

        tree = ast.parse("".join(source_code))
        self.visit(tree)

        return {
            "num_lines": self.num_lines,
            "func_calls": self.func_calls,
            "conditionals": self.conditionals,
            "arithmetic_ops": self.arithmetic_ops,
            "logical_ops": self.logical_ops,
            "cyclomatic_complexity": self.complexity
        }

def process_all_mutants(mutants_dir, output_file):
    """Processes all mutant files and extracts features."""
    features = {}

    for filename in os.listdir(mutants_dir):
        if filename.endswith(".py"):  # Process only Python mutant files
            mutant_path = os.path.join(mutants_dir, filename)
            extractor = StructuralMetricsExtractor()
            features[filename] = extractor.extract_metrics(mutant_path)
            print(f"✅ Extracted features for {filename}: {features[filename]}")

    # Save features to JSON
    with open(output_file, "w") as f:
        json.dump(features, f, indent=4)

    print(f"🚀 Feature extraction complete. Saved to {output_file}")

if __name__ == "__main__":
    mutants_dir = "data/output/mutants/"  # Directory where mutants are stored
    output_file = "data/output/features.json"  # JSON file to store extracted features

    process_all_mutants(mutants_dir, output_file)
