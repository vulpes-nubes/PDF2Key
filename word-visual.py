import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain  # Louvain method for clustering
import plotly.graph_objs as go

# Paths to the word list and CSV directory
word_list_file = 'word_list.txt'  # Replace with the path to your word list txt file
csv_dir = 'csv_files_directory'   # Replace with the path to your CSV files directory

# Step 1: Load the word list
with open(word_list_file, 'r') as f:
    words = [line.strip() for line in f]

# Create an empty graph
G = nx.Graph()

# Add nodes to the graph
G.add_nodes_from(words)

# Step 2: Read CSV files and add edges
for word in words:
    csv_file = os.path.join(csv_dir, f'{word}.csv')
    
    if os.path.exists(csv_file):
        # Step 3: Load the CSV file
        df = pd.read_csv(csv_file)
        
        # Step 4: For each keyword in the CSV, create an edge with the frequency (count)
        for _, row in df.iterrows():
            target_word = row['Keyword']  # The word from the 'Keyword' column
            frequency = row['Count']  # The frequency from the 'Count' column
            
            if target_word in words:  # Ensure the target word is in the word list
                # Add the edge with weight as frequency (or increase it if already exists)
                if G.has_edge(word, target_word):
                    G[word][target_word]['weight'] += frequency
                else:
                    G.add_edge(word, target_word, weight=frequency)

# Step 5: Cluster Detection using Louvain Method
partition = community_louvain.best_partition(G)  # Detect communities

# Assign colors to nodes based on their community
node_colors = [partition[node] for node in G.nodes()]

# Identify "center-piece" of each cluster (the most connected node in each cluster)
clusters = {}
for node, cluster_id in partition.items():
    if cluster_id not in clusters:
        clusters[cluster_id] = []
    clusters[cluster_id].append(node)

# Calculate centrality within each cluster
cluster_centers = {}
for cluster_id, nodes in clusters.items():
    subgraph = G.subgraph(nodes)  # Create a subgraph for each cluster
    center_node = max(subgraph.degree, key=lambda x: x[1])[0]  # Node with the highest degree
    cluster_centers[cluster_id] = center_node

# Step 6: Set edge thickness based on frequency (weight)
edge_thickness = [G[u][v]['weight'] for u, v in G.edges()]

### Part 1: Save the static visualization as a PNG using Matplotlib ###
plt.figure(figsize=(10, 10))  # Adjust the figure size
pos = nx.spring_layout(G)  # Force-directed layout

# Draw the nodes with colors corresponding to their clusters
nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.viridis, node_size=500)

# Draw the edges with varying thickness
nx.draw_networkx_edges(G, pos, width=edge_thickness)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10)

# Highlight the center-piece of each cluster
nx.draw_networkx_nodes(G, pos, nodelist=cluster_centers.values(), node_color='red', node_size=800, label='Center')

plt.title("Word Co-occurrence Graph with Clusters")

# Save the figure as a PNG
plt.savefig("word_graph_clusters.png", format="PNG", dpi=300)
plt.show()

### Part 2: Save the interactive visualization as an HTML using Plotly ###
# Create the network layout (reusing the same layout as Matplotlib)
edge_trace = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace.append(go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        line=dict(width=edge[2]['weight'], color='gray'),
        hoverinfo='none',
        mode='lines'))

# Extract node trace for Plotly (nodes colored by cluster)
node_trace = go.Scatter(
    x=[], y=[], text=[], mode='markers+text',
    marker=dict(showscale=True, colorscale='Viridis', color=[], size=10, colorbar=dict(thickness=15)),
    textposition="top center")

# Add the node positions and cluster information
for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['marker']['color'] += tuple([partition[node]])  # Color by cluster
    node_trace['text'] += tuple([node])

# Highlight center nodes in red
center_node_trace = go.Scatter(
    x=[], y=[], text=[], mode='markers',
    marker=dict(color='red', size=15, symbol='circle', line=dict(width=2)))

for center_node in cluster_centers.values():
    x, y = pos[center_node]
    center_node_trace['x'] += tuple([x])
    center_node_trace['y'] += tuple([y])
    center_node_trace['text'] += tuple([center_node])

# Create the plot layout
layout = go.Layout(
    title="Interactive Word Co-occurrence Graph with Clusters",
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0,l=0,r=0,t=50),
    annotations=[dict(
        showarrow=False,
        text="Word Co-occurrence Graph",
        xref="paper", yref="paper",
        x=0.005, y=-0.002 )],
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

# Combine edge and node traces into a figure
fig = go.Figure(data=edge_trace + [node_trace, center_node_trace], layout=layout)

# Save as an HTML file
fig.write_html("interactive_word_graph_clusters.html")

# If you want to show the plot in a notebook or browser, you can use:
# fig.show()

print("PNG saved as 'word_graph_clusters.png'")
print("Interactive HTML saved as 'interactive_word_graph_clusters.html'")
