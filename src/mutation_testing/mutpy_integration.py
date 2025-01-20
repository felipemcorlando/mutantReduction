import subprocess
import os

class MutPyIntegration:
    def __init__(self, target_file, test_file, output_dir="data/output/"):
        self.target_file = target_file
        self.test_file = test_file
        self.output_dir = output_dir

    def run_mutation_testing(self):
        """
        Runs MutPy using the CLI and captures the output.
        """
        command = [
            "mut.py",
            "--target", self.target_file,
            "--unit-test", self.test_file
        ]
        try:
            # Run MutPy CLI
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("MutPy Output:\n", result.stdout)

            # Save the output to a log file
            log_path = os.path.join(self.output_dir, "mutpy_results.log")
            with open(log_path, "w") as log_file:
                log_file.write(result.stdout)
            print(f"MutPy results saved to: {log_path}")

        except subprocess.CalledProcessError as e:
            print("Error running MutPy:\n", e.stderr)

if __name__ == "__main__":
    # Input files
    target = "data/input/flask_app/app.py"
    test = "data/input/flask_app/tests/test_app.py"

    # Output directory for logs
    output_dir = "data/output/"

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run MutPy
    mutpy = MutPyIntegration(target, test, output_dir)
    mutpy.run_mutation_testing()
