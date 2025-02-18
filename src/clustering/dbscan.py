import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
import os
from collections import Counter

def load_features(features_file):
    """Load features from JSON file and convert to numpy array."""
    with open(features_file, 'r') as f:
        features_dict = json.load(f)
    
    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(features_dict, orient='index')
    
    # Store mutant names for later reference
    mutant_names = list(features_dict.keys())
    
    # Convert to numpy array for clustering
    feature_matrix = df.values
    
    return feature_matrix, mutant_names, df

def perform_clustering(feature_matrix, eps=0.5, min_samples=2):
    """Perform DBSCAN clustering on normalized features."""
    # Normalize features
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(feature_matrix)
    
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(normalized_features)
    
    return clusters, normalized_features

def save_cluster_assignments(clusters, mutant_names, output_file):
    """Save cluster assignments to JSON file."""
    cluster_dict = {name: int(cluster) for name, cluster in zip(mutant_names, clusters)}
    
    with open(output_file, 'w') as f:
        json.dump(cluster_dict, f, indent=4)
    
    return cluster_dict

def visualize_clusters(normalized_features, clusters, output_file):
    """Create a 2D visualization of the clusters using PCA, matching HDBSCAN style."""
    # Reduce dimensionality to 2D using PCA
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(normalized_features)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Add jitter to prevent overlapping
    jittered_features = reduced_features + np.random.uniform(-0.05, 0.05, size=reduced_features.shape)
    
    # Create scatter plot with tab10 colormap
    scatter = plt.scatter(
        jittered_features[:, 0],
        jittered_features[:, 1],
        c=clusters,
        cmap='tab10',
        edgecolors='k',
        alpha=0.6
    )
    
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.title('DBSCAN Mutant Clustering')
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cluster ID')
    
    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # File paths
    features_file = "data/output/features.json"
    output_dir = "data/output/clustering/"
    os.makedirs(output_dir, exist_ok=True)
    
    visualization_file = os.path.join(output_dir, "dbscan_output.png")
    cluster_assignments_file = os.path.join(output_dir, "dbscan_cluster_assignments.json")
    
    # Load features
    feature_matrix, mutant_names, df = load_features(features_file)
    
    # Perform clustering
    clusters, normalized_features = perform_clustering(
        feature_matrix, 
        eps=2.0,  # Adjust this value based on your needs
        min_samples=2
    )
    
    # Save cluster assignments
    cluster_dict = save_cluster_assignments(clusters, mutant_names, cluster_assignments_file)
    
    # Visualize results
    visualize_clusters(normalized_features, clusters, visualization_file)
    
    # Print summary
    cluster_counts = Counter(clusters)
    print(f"🔢 Cluster distribution: {dict(cluster_counts)}")
    print(f"✅ Cluster assignments saved to {cluster_assignments_file}")
    print(f"📊 Clustering visualization saved to {visualization_file}")

if __name__ == "__main__":
    main()