import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd

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

def visualize_clusters(normalized_features, clusters, mutant_names, output_file):
    """Create a 2D visualization of the clusters using PCA."""
    # Reduce dimensionality to 2D using PCA
    pca = PCA(n_components=2)
    features_2d = pca.fit_transform(normalized_features)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Get unique clusters
    unique_clusters = np.unique(clusters)
    
    # Create a colormap with distinct colors for each cluster
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_clusters)))
    
    # Plot points for each cluster with different colors
    for cluster_id, color in zip(unique_clusters, colors):
        mask = clusters == cluster_id
        label = 'Noise' if cluster_id == -1 else f'Cluster {cluster_id}'
        plt.scatter(features_2d[mask, 0], features_2d[mask, 1], 
                   c=[color], label=label, alpha=0.7)
    
    # Add small dots to show exact positions
    plt.scatter(features_2d[:, 0], features_2d[:, 1], c='black', s=1, alpha=0.5)
    
    # Print information about potential overlapping points
    unique_positions = set()
    overlapping_points = []
    
    for i, (x, y) in enumerate(features_2d):
        pos = (round(x, 4), round(y, 4))  # Round to 4 decimal places
        if pos in unique_positions:
            overlapping_points.append(mutant_names[i])
        unique_positions.add(pos)
    
    if overlapping_points:
        print("\nOverlapping points detected:")
        print("The following mutants have identical or very similar positions:")
        for point in overlapping_points:
            print(f"- {point}")
    
    # Print total points
    print(f"\nTotal mutants: {len(mutant_names)}")
    print(f"Unique positions on plot: {len(unique_positions)}")
    
    plt.title('Mutant Clusters Visualization')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.legend()
    
    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_clusters(clusters, mutant_names, df):
    """Analyze and print information about the clusters."""
    unique_clusters = np.unique(clusters)
    
    print("\nCluster Analysis:")
    print("=" * 50)
    
    for cluster in unique_clusters:
        cluster_mask = clusters == cluster
        cluster_mutants = np.array(mutant_names)[cluster_mask]
        cluster_features = df.iloc[cluster_mask]
        
        if cluster == -1:
            print("\nNoise points (outliers):")
        else:
            print(f"\nCluster {cluster}:")
        
        print(f"Number of mutants: {len(cluster_mutants)}")
        print("Mutants:", ", ".join(cluster_mutants))
        
        print("\nCluster characteristics (mean values):")
        for feature in df.columns:
            mean_value = cluster_features[feature].mean()
            print(f"{feature}: {mean_value:.2f}")
        
        print("-" * 50)

def main():
    # File paths
    features_file = "data/output/features.json"
    visualization_file = "data/output/clustering/dbscan_output.png"
    
    # Load features
    feature_matrix, mutant_names, df = load_features(features_file)
    
    # Perform clustering
    clusters, normalized_features = perform_clustering(
        feature_matrix, 
        eps=2.0,  # Adjust this value based on your needs
        min_samples=2
    )
    
    # Visualize results
    visualize_clusters(normalized_features, clusters, mutant_names, visualization_file)
    
    # Analyze clusters
    analyze_clusters(clusters, mutant_names, df)
    
    # Print summary
    n_clusters = len(np.unique(clusters)) - (1 if -1 in clusters else 0)
    print(f"\nSummary:")
    print(f"Total number of clusters found: {n_clusters}")
    print(f"Number of noise points: {list(clusters).count(-1)}")
    print(f"Visualization saved to: {visualization_file}")

if __name__ == "__main__":
    main()