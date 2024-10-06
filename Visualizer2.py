
# Required libraries:
# pip install pandas numpy networkx matplotlib community

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

# Load the CSV file
df = pd.read_csv('summary_output.csv', index_col=0)

# Remove duplicate rows, keeping the first occurrence
square_df = df[~df.index.duplicated(keep='first')]

print("Shape of the square dataframe:", square_df.shape)
print("First few rows and columns of the square dataframe:")
print(square_df.iloc[:5, :5])

# Calculate total edge weights and node sizes
edge_weights = {}
node_sizes = {}

# Iterate over each word to calculate node sizes and edge weights
for word in square_df.index:
    # Calculate node size as the sum of the row
    node_size = square_df.loc[word].sum()
    node_sizes[word] = node_size
    
    # Calculate edge weights for each pair
    for other_word in square_df.index:
        if word != other_word:
            edge_weight = square_df.loc[word, other_word] + square_df.loc[other_word, word]
            if edge_weight > 0:
                edge_weights[(word, other_word)] = edge_weight

print("Number of nodes:", len(node_sizes))
print("Number of edges:", len(edge_weights))

# Find the top 10 nodes by size
top_nodes = sorted(node_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by size:")
for node, size in top_nodes:
    print(f"{node}: {size}")

# Find the top 10 edges by weight
top_edges = sorted(edge_weights.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 edges by weight:")
for (node1, node2), weight in top_edges:
    print(f"{node1} - {node2}: {weight}")

# Create a new graph with updated edge weights and node sizes
G_updated = nx.Graph()

# Add nodes with sizes
for word, size in node_sizes.items():
    G_updated.add_node(word, size=size)

# Add edges with weights
for (word1, word2), weight in edge_weights.items():
    G_updated.add_edge(word1, word2, weight=weight)

# Apply community detection
communities_updated = community_louvain.best_partition(G_updated)

# Get a color for each community
num_communities_updated = len(set(communities_updated.values()))
color_map_updated = plt.cm.get_cmap('tab20')
color_list_updated = [color_map_updated(i / num_communities_updated) for i in communities_updated.values()]

# Draw the updated graph
plt.figure(figsize=(30, 30))

# Position nodes using Fruchterman-Reingold force-directed algorithm
pos_updated = nx.spring_layout(G_updated, k=0.7, iterations=100)

# Draw nodes with sizes proportional to their total occurrences
node_sizes_list = [node_sizes[node] for node in G_updated.nodes()]
nx.draw_networkx_nodes(G_updated, pos_updated, node_size=np.array(node_sizes_list) / max(node_sizes_list) * 1000, node_color=color_list_updated, alpha=0.8)

# Draw edges with widths proportional to their total weights
edges_updated = G_updated.edges(data=True)
weights_updated = [edge[2]['weight'] for edge in edges_updated]
nx.draw_networkx_edges(G_updated, pos_updated, edgelist=edges_updated, width=np.array(weights_updated) / max(weights_updated) * 3, alpha=0.2)

# Draw labels for nodes with high degree (important nodes)
degree_dict_updated = dict(G_updated.degree())
labels_updated = {node: node for node, degree in degree_dict_updated.items() if degree > np.percentile(list(degree_dict_updated.values()), 97)}
nx.draw_networkx_labels(G_updated, pos_updated, labels_updated, font_size=10, font_weight='bold')

plt.title('Word Connection Graph with Updated Edge Weights and Node Sizes', fontsize=24)
plt.axis('off')
plt.tight_layout()
plt.savefig('updated_word_graph.png', dpi=300, bbox_inches='tight')
plt.close()

print("Updated graph created and saved as 'updated_word_graph.png'.")

# Calculate and print some statistics
print(f"Number of nodes: {G_updated.number_of_nodes()}")
print(f"Number of edges: {G_updated.number_of_edges()}")
print(f"Number of communities: {num_communities_updated}")

# Find the top 10 nodes by degree
top_nodes_degree = sorted(degree_dict_updated.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by degree:")
for node, degree in top_nodes_degree:
    print(f"{node}: {degree}")