import os
import json
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean

# Define paths
cluster_path = "data/output/clustering/cluster_assignments.json"
features_path = "data/output/features.json"
output_dir = "data/output/clustering/"
os.makedirs(output_dir, exist_ok=True)

# 📂 Load cluster assignments
with open(cluster_path, "r") as f:
    cluster_assignments = json.load(f)

# 📂 Load extracted features
with open(features_path, "r") as f:
    features_data = json.load(f)

# 🔄 Convert features to DataFrame
df = pd.DataFrame.from_dict(features_data, orient="index")

# Group mutants by cluster
clustered_mutants = {}
for mutant, cluster in cluster_assignments.items():
    if cluster != -1:  # Ignore noise
        clustered_mutants.setdefault(cluster, []).append(mutant)

# 📌 Compute centroids and designate representatives
representatives = {}
pruned_mutants = {}  # Mutants removed per cluster

for cluster, mutants in clustered_mutants.items():
    # Get feature vectors for all mutants in this cluster
    cluster_vectors = df.loc[mutants].values
    
    # Compute centroid as the mean feature vector
    centroid = np.mean(cluster_vectors, axis=0)
    
    # Find the closest mutant to the centroid
    closest_mutant = min(mutants, key=lambda m: euclidean(df.loc[m].values, centroid))
    
    # Assign as representative
    representatives[cluster] = closest_mutant

    # Store pruned mutants (all except the representative)
    pruned_mutants[cluster] = [m for m in mutants if m != closest_mutant]

# 💾 Save representative mutants
rep_output_path = os.path.join(output_dir, "representative_mutants.json")
with open(rep_output_path, "w") as f:
    json.dump(representatives, f, indent=4)
print(f"✅ Representative mutants saved to {rep_output_path}")

# 💾 Save pruned mutants (the ones removed)
pruned_output_path = os.path.join(output_dir, "pruned_mutants.json")
with open(pruned_output_path, "w") as f:
    json.dump(pruned_mutants, f, indent=4)
print(f"🗑️ Pruned mutants saved to {pruned_output_path}")
