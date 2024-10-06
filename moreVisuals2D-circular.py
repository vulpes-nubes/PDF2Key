import pandas as pd
import networkx as nx
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models import MultiLine
from bokeh.transform import factor_cmap
from sklearn.cluster import KMeans
import numpy as np

# Load the CSV file
file_path = 'summary_output.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Calculate the total sum of counts for each word across all columns
df['Total_Count'] = df.iloc[:, 1:].sum(axis=1)

# Prepare the data for plotting: words, total counts, and generate random x and y positions for layout
words = df['Word']
sizes = df['Total_Count'] / df['Total_Count'].max() * 50  # Normalize sizes for better visualization

# Set a minimum circle size
min_circle_size = 10
sizes = np.maximum(sizes, min_circle_size)  # Ensure a minimum size

# Create a graph to find connections based on counts
G = nx.Graph()

# Adding nodes to the graph
for word in words:
    G.add_node(word, size=df.loc[df['Word'] == word, 'Total_Count'].values[0])

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

# Apply K-means clustering for node layout
pos = nx.spring_layout(G, k=1.5, iterations=150)  # Initial layout
X = np.array([pos[word] for word in words])

# Apply KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)  # Set 5 clusters (adjust as needed)
cluster_labels = kmeans.labels_

# Create a Bokeh plot
output_file("word_frequency_visualization_2d_kmeans.html")

# Prepare data for Bokeh
node_x = [pos[word][0] for word in words]
node_y = [pos[word][1] for word in words]
node_sizes = [G.nodes[word]['size'] / df['Total_Count'].max() * 50 for word in words]  # Scale the sizes

# Ensure the minimum circle size is applied
node_sizes = np.maximum(node_sizes, min_circle_size)

# Prepare edge data
edges_start_x = []
edges_start_y = []
edges_end_x = []
edges_end_y = []
weights = []

for edge in G.edges(data=True):
    word1, word2, weight_data = edge
    edges_start_x.append([pos[word1][0], pos[word2][0]])  # Line start and end points
    edges_start_y.append([pos[word1][1], pos[word2][1]])
    weights.append(weight_data['weight'])

# Convert cluster labels to color
source = ColumnDataSource(data=dict(
    x=node_x,
    y=node_y,
    word=words,
    total_count=df['Total_Count'],
    sizes=node_sizes,
    cluster=[str(label) for label in cluster_labels]  # Convert to strings for color mapping
))

edge_source = ColumnDataSource(data=dict(
    start_x=edges_start_x,
    start_y=edges_start_y,
    weight=weights
))

# Create a Bokeh figure
p = figure(title="2D Word Frequency Visualization with K-means Clustering",
           tools="pan,wheel_zoom,reset",
           width=1000, height=1000)

# Create a color map based on cluster labels
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Define distinct colors
p.scatter('x', 'y', size='sizes', source=source, color=factor_cmap('cluster', palette=colors, factors=['0', '1', '2', '3', '4']), alpha=0.8)

# Draw edges (connections) with varying thickness based on total count
p.multi_line(xs='start_x', ys='start_y', line_width='weight', source=edge_source, color='gray', alpha=0.5)

# Add labels to the nodes
labels = LabelSet(x='x', y='y', text='word', source=source, text_font_size='10pt', text_align='center', text_baseline='middle')
p.add_layout(labels)

# Show the plot
show(p)
