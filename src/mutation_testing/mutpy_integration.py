import subprocess
import os
import json
import re

class MutPyIntegration:
    def __init__(self, target_file, test_file, output_dir="/app/data/output/"):
        self.target_file = target_file
        self.test_file = test_file
        self.output_dir = output_dir

        # Ensure the output directory exists (inside container)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_mutants(self, mutants_info):
        """
        Save each mutant's source code and metadata to separate files.
        """
        for index, mutant_data in enumerate(mutants_info):
            file_path = os.path.join(self.output_dir, f"mutant_{index}.py")
            metadata_path = os.path.join(self.output_dir, f"mutant_{index}.json")

            # Save placeholder mutant source code
            with open(file_path, "w") as file:
                file.write("# Example Mutant Code\n# Replace this with real mutant source code.")

            # Save metadata
            metadata = {
                "id": index,
                "type": mutant_data[1],
                "status": mutant_data[2],
            }
            with open(metadata_path, "w") as meta_file:
                json.dump(metadata, meta_file, indent=4)

            print(f"Saved mutant {index}: {file_path}")

    def parse_mutpy_output(self, output):
        """
        Parse the CLI output to extract mutant details.
        """
        mutants_info = []
        pattern = re.compile(r" - \[#\s*(\d+)\] (\w+) .*?: \[.*?\] (killed|incompetent|survived|timeout)")
        matches = pattern.findall(output)

        for match in matches:
            index, mutation_type, status = match
            mutants_info.append((int(index), mutation_type, status))

        return mutants_info

    def run_mutation_testing(self):
        """
        Runs MutPy using the CLI and saves mutants to files.
        """
        command = [
            "mut.py",
            "--target", self.target_file,
            "--unit-test", self.test_file,
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("MutPy Output:\n", result.stdout)

            # Save output to a log file
            log_path = os.path.join(self.output_dir, "mutpy_results.log")
            with open(log_path, "w") as log_file:
                log_file.write(result.stdout)

            # Extract mutants
            mutants_info = self.parse_mutpy_output(result.stdout)
            self.save_mutants(mutants_info)

        except subprocess.CalledProcessError as e:
            print("Error running MutPy:\n", e.stderr)


if __name__ == "__main__":
    target = "data/input/flask_app/app.py"
    test = "data/input/flask_app/tests/test_app.py"

    output_dir = "/app/data/output/"  # Matches the mounted volume in Docker

    mutpy = MutPyIntegration(target, test, output_dir)
    mutpy.run_mutation_testing()
