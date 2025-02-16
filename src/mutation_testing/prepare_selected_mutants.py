import os
import json
import shutil

# 📂 Define paths
mutants_dir = "data/output/mutants/"
evaluation_dir = "data/output/evaluation_mutants/"
representative_path = "data/output/clustering/representative_mutants.json"

# 📝 Load selected mutants from JSON
with open(representative_path, "r") as f:
    representative_mutants = json.load(f)

selected_mutants = set(representative_mutants.values())  # Unique selected mutants

# 🧹 Clear and recreate evaluation directory
if os.path.exists(evaluation_dir):
    shutil.rmtree(evaluation_dir)  # Remove if exists
os.makedirs(evaluation_dir, exist_ok=True)

# 🔄 Move selected mutants into the evaluation directory
for mutant_file in selected_mutants:
    src_path = os.path.join(mutants_dir, mutant_file)
    dest_path = os.path.join(evaluation_dir, mutant_file)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"✅ Copied {mutant_file} to evaluation directory.")
    else:
        print(f"⚠️ Warning: Mutant file {mutant_file} not found!")

print(f"🚀 Selected mutants prepared in {evaluation_dir}. Ready for evaluation!")
