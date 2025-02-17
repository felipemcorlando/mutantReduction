import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from collections import Counter

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

# 🔍 Apply K-Means clustering (initially with 5 clusters)
n_clusters = 40
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(scaled_features)

# 📌 Store results in a dictionary
cluster_assignments = {mutant_names[i]: int(cluster_labels[i]) for i in range(len(mutant_names))}

# 💾 Save cluster assignments to JSON
output_path = os.path.join(output_dir, "kmeans_cluster_assignments.json")
with open(output_path, "w") as f:
    json.dump(cluster_assignments, f, indent=4)
print(f"✅ K-Means cluster assignments saved to {output_path}")

# 📊 Display cluster summary
cluster_counts = Counter(cluster_labels)
print(f"🔢 Cluster distribution: {dict(cluster_counts)}")

# 📈 Reduce dimensions for visualization using PCA
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(scaled_features)

# 🎨 Plot clusters with jittering and transparency
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    reduced_features[:, 0] + np.random.uniform(-0.05, 0.05, size=len(reduced_features)),
    reduced_features[:, 1] + np.random.uniform(-0.05, 0.05, size=len(reduced_features)),
    c=cluster_labels, cmap="tab10", edgecolors="k", alpha=0.6
)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("K-Means Mutant Clustering")

# Add cluster size legend
cbar = plt.colorbar(scatter)
cbar.set_label("Cluster ID")

# Save the figure
output_image_path = os.path.join(output_dir, "kmeans_clustering.png")
plt.savefig(output_image_path)
print(f"📊 Clustering visualization saved to {output_image_path}")

plt.show()
