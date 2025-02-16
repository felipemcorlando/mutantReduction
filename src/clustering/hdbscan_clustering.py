import os
import json
import numpy as np
import pandas as pd
import hdbscan
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Define paths
features_path = "data/output/features.json"
output_dir = "data/output/clustering/"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# 📂 Load extracted features from JSON
with open(features_path, "r") as f:
    features_data = json.load(f)

# 🔄 Convert features to DataFrame
df = pd.DataFrame.from_dict(features_data, orient="index")

# 🏷️ Store mutant names
mutant_names = df.index.tolist()

# 📊 Normalize features (Standardization)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

# 🔍 Apply HDBSCAN clustering
clusterer = hdbscan.HDBSCAN(min_cluster_size=4, min_samples=2, metric='euclidean')
cluster_labels = clusterer.fit_predict(scaled_features)

# 📌 Store results in a dictionary
cluster_assignments = {mutant_names[i]: int(cluster_labels[i]) for i in range(len(mutant_names))}

# 💾 Save cluster assignments to JSON
output_path = "data/output/cluster_assignments.json"
with open(output_path, "w") as f:
    json.dump(cluster_assignments, f, indent=4)
print(f"✅ Cluster assignments saved to {output_path}")

# 📈 Reduce dimensions for visualization using PCA
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(scaled_features)

# 🎨 Plot clusters
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    reduced_features[:, 0], reduced_features[:, 1], c=cluster_labels, cmap="tab10", edgecolors="k"
)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("HDBSCAN Mutant Clustering")
plt.colorbar(label="Cluster ID")
plt.grid()

# Save the figure
output_image_path = os.path.join(output_dir, "hdbscan_clustering.png")
plt.savefig(output_image_path)
print(f"📊 Clustering visualization saved to {output_image_path}")

plt.show()
