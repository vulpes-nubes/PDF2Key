import pandas as pd
import networkx as nx
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, TapTool, CustomJS
from bokeh.models import MultiLine, Circle
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
            if word2 in df.columns and word1 in df.columns:
                count1 = df.at[i, word2] if word2 in df.columns else 0
                count2 = df.at[j, word1] if word1 in df.columns else 0
                total_count = count1 + count2
                
                if total_count > 0:
                    G.add_edge(word1, word2, weight=total_count)

# Identify the 4 nodes with the highest degree
degree_dict = dict(G.degree())
highest_degree_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)[:4]

# Assign the corner positions for the highest degree nodes
corner_positions = {
    highest_degree_nodes[0]: (1, 1),       # Top-right corner
    highest_degree_nodes[1]: (1, -1),      # Bottom-right corner
    highest_degree_nodes[2]: (-1, 1),      # Top-left corner
    highest_degree_nodes[3]: (-1, -1)      # Bottom-left corner
}

# Start with the corner positions for the top nodes
pos = {node: corner_positions.get(node, (np.random.uniform(-1, 1), np.random.uniform(-1, 1))) for node in words}

# Recalculate positions using spring layout for the rest
remaining_nodes = set(words) - set(highest_degree_nodes)
remaining_positions = nx.spring_layout(G.subgraph(remaining_nodes), pos=pos, k=2, iterations=150)

# Update the positions with remaining nodes
pos.update(remaining_positions)

# Create a Bokeh plot
output_file("word_frequency_visualization_with_interactivity.html")

# Prepare data for Bokeh
node_x = [pos[word][0] for word in words]
node_y = [pos[word][1] for word in words]
node_sizes = [G.nodes[word]['size'] / df['Total_Count'].max() * 50 for word in words]

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
    edges_start_x.append([pos[word1][0], pos[word2][0]])
    edges_start_y.append([pos[word1][1], pos[word2][1]])
    weights.append(weight_data['weight'])

# Convert cluster labels to color
source = ColumnDataSource(data=dict(
    x=node_x,
    y=node_y,
    word=words,
    total_count=df['Total_Count'],
    sizes=node_sizes,
    cluster=['0'] * len(words)  # Placeholder for clusters
))

edge_source = ColumnDataSource(data=dict(
    start_x=edges_start_x,
    start_y=edges_start_y,
    weight=weights
))

# Create a Bokeh figure
p = figure(title="2D Word Frequency Visualization with Connections",
           tools="pan,wheel_zoom,reset,tap",  # Added tap tool for interaction
           width=1000, height=1000)

# Create scatter for nodes
nodes = p.scatter('x', 'y', size='sizes', source=source, color=factor_cmap('cluster', palette=['#1f77b4'], factors=['0']), alpha=0.8)

# Draw edges (connections) with varying thickness based on total count
p.multi_line(xs='start_x', ys='start_y', line_width='weight', source=edge_source, color='green', alpha=0.5)

# Add labels to the nodes
labels = LabelSet(x='x', y='y', text='word', source=source, text_font_size='10pt', text_align='center', text_baseline='middle')
p.add_layout(labels)

# JavaScript callback for tap event
callback = CustomJS(args=dict(source=source, edge_source=edge_source, p=p), code="""
    const indices = source.selected.indices;
    if (indices.length > 0) {
        const selected_index = indices[0];
        const selected_word = source.data['word'][selected_index];

        // Clear previous highlights
        for (let i = 0; i < edge_source.data['start_x'].length; i++) {
            edge_source.data['start_x'][i] = [];
            edge_source.data['start_y'][i] = [];
        }

        // Highlight edges connected to the selected word
        for (let i = 0; i < edge_source.data['start_x'].length; i++) {
            const word1 = source.data['word'][i];
            const word2 = source.data['word'][i];
            if (p.select({type: MultiLine}).some(line => line.start_x === word1 && line.end_x === word2)) {
                edge_source.data['start_x'].push([source.data['x'][selected_index], source.data['x'][i]]);
                edge_source.data['start_y'].push([source.data['y'][selected_index], source.data['y'][i]]);
            }
        }

        edge_source.change.emit();
    }
""")

# Link the TapTool to the callback
nodes.js_on_event('tap', callback)

# Show the plot
show(p)
