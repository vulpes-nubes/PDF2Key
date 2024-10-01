import os
import pandas as pd
import networkx as nx
from bokeh.plotting import figure, from_networkx, output_file, save, show
from bokeh.models import Circle, MultiLine, LabelSet, ColumnDataSource
from bokeh.io.export import export_png
from bokeh.layouts import layout
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
import matplotlib.pyplot as plt

# Load words from the txt file
def load_word_list(txt_file):
    with open(txt_file, 'r') as f:
        words = [line.strip() for line in f.readlines()]
    return words

# Function to read CSV files from a directory and construct the graph
def process_csv_files(word_list, csv_folder):
    G = nx.Graph()
    word_frequencies = {word: 0 for word in word_list}  # Track total frequency of each word
    edge_weights = {}  # Track edge weights between words

    # Iterate over all CSV files in the directory
    for word in word_list:
        csv_file = os.path.join(csv_folder, f"{word}.csv")
        
        # Check if the file exists
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)

            for _, row in df.iterrows():
                keyword = row['Keyword']
                count = row['Count']
                
                if keyword in word_frequencies:
                    word_frequencies[keyword] += count

                # Store connection (edge) between the word and the keyword
                if (word, keyword) not in edge_weights:
                    edge_weights[(word, keyword)] = 0
                edge_weights[(word, keyword)] += count

    # Add nodes and edges to the graph
    for word, frequency in word_frequencies.items():
        if frequency > 0:  # Only add nodes with non-zero frequency
            G.add_node(word, size=frequency)

    for (word, keyword), weight in edge_weights.items():
        if weight > 0:  # Only add edges with non-zero weight
            G.add_edge(word, keyword, weight=weight)

    return G

# Plot the interactive graph using Bokeh
def plot_interactive_graph(G):
    output_file("word_network.html")

    # Prepare the Bokeh plot
    plot = figure(title="Word Network Graph", x_range=(-2, 2), y_range=(-2, 2),
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom')

    # Define the layout and node sizes based on frequency
    pos = nx.spring_layout(G)
    node_indices = list(G.nodes())
    node_sizes = [G.nodes[node]['size'] * 10 for node in node_indices]  # Adjust node size scaling

    # Assign colors to clusters (using a simple color mapper based on node size)
    node_color_map = linear_cmap('size', Viridis256, min(node_sizes), max(node_sizes))

    # Create a Bokeh graph from the networkx graph
    graph = from_networkx(G, pos)

    # Set node renderer properties
    graph.node_renderer.glyph = Circle(size='size', fill_color=node_color_map)
    graph.node_renderer.data_source.data = {'index': node_indices, 'size': node_sizes}

    # Set edge renderer properties
    edge_weights = [G.edges[edge]['weight'] for edge in G.edges()]
    graph.edge_renderer.glyph = MultiLine(line_color="black", line_width=edge_weights)

    # Add labels to nodes
    labels = LabelSet(x='x', y='y', text='index', level='glyph', text_align='center',
                      text_baseline='middle', source=ColumnDataSource(
                        {'x': [pos[node][0] for node in G.nodes()],
                         'y': [pos[node][1] for node in G.nodes()],
                         'index': list(G.nodes())}))
    plot.add_layout(labels)

    # Add the graph to the plot
    plot.renderers.append(graph)

    # Save the HTML file
    save(plot)

    # Export PNG file
    export_png(plot, filename="word_network.png")

    # Show the plot in browser
    show(plot)

# Static PNG visualization with Matplotlib
def plot_static_png(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(15, 15))

    # Draw nodes with sizes based on frequency
    node_sizes = [G.nodes[node]['size'] * 10 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)

    # Draw edges with thickness based on weights
    edge_weights = [G.edges[edge]['weight'] for edge in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Save the PNG file
    plt.savefig("word_network_static.png", dpi=300)
    plt.show()

# Define file paths
word_list_file = '/home/gray221/Documents/batch/output/stoplist.txt'  # Replace with your actual word list file path
csv_directory = '/home/gray221/Documents/batch/output/keywords'  # Replace with your actual CSV directory path

# Load the word list
words = load_word_list(word_list_file)

# Process the CSV files to build the graph
G = process_csv_files(words, csv_directory)

# Run the interactive plot generation
plot_interactive_graph(G)

# Run the static PNG generation
plot_static_png(G)
