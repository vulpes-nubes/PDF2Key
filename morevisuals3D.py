import pandas as pd
import networkx as nx
import plotly.graph_objs as go

# Load the CSV file (update the file path as needed)
file_path = 'summary_output.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Print column names to debug
print("Columns in DataFrame:", df.columns)

# Calculate the total sum of counts for each word across all columns
df['Total_Count'] = df.iloc[:, 1:].sum(axis=1)

# Prepare the data for plotting: words, total counts, and generate random x and y positions for layout
words = df['Word']
sizes = df['Total_Count'] / df['Total_Count'].max() * 50  # Normalize sizes for better visualization

# Create a graph to find connections based on counts
G = nx.Graph()

# Adding nodes to the graph
for word in words:
    G.add_node(word)

# Adding edges based on the sum of counts in both directions
for i, word1 in enumerate(words):
    for j, word2 in enumerate(words):
        if i != j:
            # Ensure both words exist in the columns (in case the matrix is not symmetric)
            if word2 in df.columns and word1 in df.columns:
                # Calculate total interaction value by summing both directional counts
                count1 = df.at[i, word2] if word2 in df.columns else 0
                count2 = df.at[j, word1] if word1 in df.columns else 0
                total_count = count1 + count2
                
                # If there's a non-zero interaction, create an edge
                if total_count > 0:
                    G.add_edge(word1, word2, weight=total_count)

# Create positions for nodes using a 3D layout algorithm
pos_3d = nx.spring_layout(G, dim=3, k=0.5, iterations=50)

# Create lists for lines and their corresponding widths
edges = []
edge_weights = []

for (word1, word2, data) in G.edges(data=True):
    x0, y0, z0 = pos_3d[word1]
    x1, y1, z1 = pos_3d[word2]
    edges.append([(x0, y0, z0), (x1, y1, z1)])
    edge_weights.append(data['weight'])  # Edge thickness will depend on the total interaction count

# Extract node positions and sizes
node_x = [pos_3d[word][0] for word in words]
node_y = [pos_3d[word][1] for word in words]
node_z = [pos_3d[word][2] for word in words]

# Create 3D scatter plot for nodes
node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers+text',
    marker=dict(
        size=sizes,
        color='navy',
        opacity=0.8,
    ),
    text=words,  # Word labels
    hoverinfo='text',
)

# Create 3D lines for edges
edge_traces = []
for edge, weight in zip(edges, edge_weights):
    x_vals = [edge[0][0], edge[1][0], None]
    y_vals = [edge[0][1], edge[1][1], None]
    z_vals = [edge[0][2], edge[1][2], None]
    
    edge_trace = go.Scatter3d(
        x=x_vals, y=y_vals, z=z_vals,
        mode='lines',
        line=dict(width=weight / 5, color='gray'),  # Adjust edge width based on interaction count
        opacity=0.5
    )
    edge_traces.append(edge_trace)

# Combine all traces (nodes and edges)
layout = go.Layout(
    title="3D Word Frequency Visualization with Edge Thickness",
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z'),
    ),
    showlegend=False
)

fig = go.Figure(data=[node_trace] + edge_traces, layout=layout)

# Show the figure
fig.show()
