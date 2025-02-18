import json
from collections import defaultdict

# 📂 Paths
clusters_path = "data/output/clustering/kmeans_cluster_assignments.json"  # Change if using a different clustering method
features_path = "data/output/features.json"
output_path = "data/output/representative_mutants.json"

# 📌 Load cluster assignments
with open(clusters_path, "r") as f:
    cluster_assignments = json.load(f)

# 📌 Load extracted features (used for computing representative mutant)
with open(features_path, "r") as f:
    features_data = json.load(f)

# 🏷️ Group mutants by cluster
clusters = defaultdict(list)
for mutant, cluster in cluster_assignments.items():
    if cluster != -1:  # Ignore noise points (outliers)
        clusters[cluster].append(mutant)

# 🔍 Select the most representative mutant per cluster
representative_mutants = {}

for cluster, mutants in clusters.items():
    # Compute mean feature vector for cluster
    cluster_vectors = [features_data[mutant] for mutant in mutants]
    
    # Compute centroid of the cluster
    centroid = {feature: sum(d[feature] for d in cluster_vectors) / len(cluster_vectors) for feature in cluster_vectors[0]}
    
    # Find mutant closest to the centroid
    def distance(mutant_features):
        return sum(abs(mutant_features[feature] - centroid[feature]) for feature in centroid)

    most_representative = min(mutants, key=lambda m: distance(features_data[m]))
    representative_mutants[cluster] = most_representative

# 💾 Save results
with open(output_path, "w") as f:
    json.dump(representative_mutants, f, indent=4)

print(f"✅ Representative mutants saved to {output_path}")
