import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import Counter

# Define paths
features_path = "data/output/features.json"
output_dir = "data/output/clustering/"
os.makedirs(output_dir, exist_ok=True)

# Load extracted features from JSON
with open(features_path, "r") as f:
    features_data = json.load(f)

# Convert features to DataFrame
df = pd.DataFrame.from_dict(features_data, orient="index")

# Store mutant names
mutant_names = df.index.tolist()

# Normalize features (Standardization)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

# Function to find optimal k using elbow method
def find_optimal_k(data, max_k=10):
    inertias = []
    k_values = range(2, max_k + 1)
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
    
    # Plot elbow curve
    plt.figure(figsize=(12, 5))
    
    # Inertia plot
    plt.subplot(1, 2, 1)
    plt.plot(k_values, inertias, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    
    
    # Save the elbow curve
    plt.savefig(os.path.join(output_dir, "elbow_curve.png"))
    plt.close()
    
    return 5

# Find optimal number of clusters
optimal_k = find_optimal_k(scaled_features)
print(f"🔍 Optimal number of clusters (k): {optimal_k}")

# Apply K-means clustering with optimal k
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(scaled_features)

# Store results in a dictionary
cluster_assignments = {mutant_names[i]: int(cluster_labels[i]) for i in range(len(mutant_names))}

# Save cluster assignments to JSON
output_path = os.path.join(output_dir, "kmeans_cluster_assignments.json")
with open(output_path, "w") as f:
    json.dump(cluster_assignments, f, indent=4)
print(f"✅ Cluster assignments saved to {output_path}")

# Display cluster summary
cluster_counts = Counter(cluster_labels)
print(f"🔢 Cluster distribution: {dict(cluster_counts)}")

# Calculate cluster centers in original feature space
cluster_centers_scaled = kmeans.cluster_centers_
cluster_centers_original = scaler.inverse_transform(cluster_centers_scaled)
cluster_centers_df = pd.DataFrame(
    cluster_centers_original,
    columns=df.columns,
    index=[f"Cluster_{i}" for i in range(optimal_k)]
)

# Save cluster centers to CSV
centers_output_path = os.path.join(output_dir, "kmeans_cluster_centers.csv")
cluster_centers_df.to_csv(centers_output_path)
print(f"📊 Cluster centers saved to {centers_output_path}")

# Reduce dimensions for visualization using PCA
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(scaled_features)
reduced_centers = pca.transform(cluster_centers_scaled)

# Plot clusters with centers
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    reduced_features[:, 0],
    reduced_features[:, 1],
    c=cluster_labels,
    cmap="tab10",
    alpha=0.6,
    edgecolors="k"
)

# Plot cluster centers
plt.scatter(
    reduced_centers[:, 0],
    reduced_centers[:, 1],
    c='red',
    marker='x',
    s=200,
    linewidth=3,
    label='Cluster Centers'
)

plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("K-means Mutant Clustering")
plt.legend()

# Add cluster size legend
cbar = plt.colorbar(scatter)
cbar.set_label("Cluster ID")

# Save the figure
output_image_path = os.path.join(output_dir, "kmeans_clustering.png")
plt.savefig(output_image_path)
print(f"📊 Clustering visualization saved to {output_image_path}")

plt.close()