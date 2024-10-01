# dataVisualiser_fast.py

import pickle  # Importing pickle for loading the graph
from bokeh.plotting import figure, from_networkx, output_file, save, show
from bokeh.models import Circle, MultiLine, LabelSet, ColumnDataSource
from bokeh.io.export import export_png
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
import networkx as nx

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

# Example usage
if __name__ == "__main__":
    # Load the graph from the pickle file
    with open("word_network_graph.gpickle", "rb") as f:
        G = pickle.load(f)

    # Run the interactive plot generation
    plot_interactive_graph(G)
