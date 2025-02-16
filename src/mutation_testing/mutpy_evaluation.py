import os
import json
import shutil
import subprocess

# 📂 Define paths
evaluation_dir = "data/output/evaluation_mutants/"
output_file = "data/output/evaluation_results.json"
test_file = "tests/test_fsm.py"
target_file = "src/fsm_modeling/flight_booking_fsm.py"
backup_file = target_file + ".bak"

# 📄 Load selected mutants (representatives)
selected_mutants_path = "data/output/clustering/representative_mutants.json"
with open(selected_mutants_path, "r") as f:
    representative_mutants = json.load(f)

# Extracting the correct mutant filenames
selected_mutants = list(representative_mutants.values())  # Extract filenames properly

# 🏗️ Ensure evaluation directory exists
os.makedirs(evaluation_dir, exist_ok=True)

# ✅ Track mutation testing results
results = {
    "selected_mutants_count": len(selected_mutants),
    "original_mutants_count": len(os.listdir("data/output/mutants/")),
    "mutation_score": None,
    "raw_output": ""
}

# 🏆 Track killed & survived mutants
killed = 0
survived = 0

# 📌 Backup original FSM file
if not os.path.exists(backup_file):
    shutil.copy(target_file, backup_file)

for mutant in selected_mutants:
    mutant_path = os.path.join(evaluation_dir, mutant)

    # Replace FSM file with mutant
    shutil.copy(mutant_path, target_file)

    # 🚀 Run mutation testing with `pytest-mutagen`
    try:
        test_result = subprocess.run(["pytest", "--mutagen", test_file], capture_output=True, text=True)
        output = test_result.stdout

        # 📌 Check if mutant was killed
        if "FAILED" in output:
            killed += 1
        else:
            survived += 1

        results["raw_output"] += f"\n🔍 Mutant {mutant}:\n{output}\n"

    finally:
        # Restore the original FSM file
        shutil.copy(backup_file, target_file)

# 🏆 Compute Mutation Score
total_mutants = len(selected_mutants)
mutation_score = (killed / total_mutants) * 100 if total_mutants > 0 else 0
results["mutation_score"] = f"{mutation_score:.2f}% (Killed: {killed}, Survived: {survived})"

# 💾 Save results
with open(output_file, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ Mutation Testing Completed. Results saved to {output_file}")
