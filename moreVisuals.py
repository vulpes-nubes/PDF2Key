import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
import networkx as nx

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

# Adding edges based on counts
for i, word1 in enumerate(words):
    for j, word2 in enumerate(words):
        if i != j:
            # Check if the column name exists
            if word2 in df.columns:
                count = df.at[i, word2]  # Use column name directly
                if count > 0:
                    G.add_edge(word1, word2, weight=count)

# Create positions for nodes using a layout algorithm with adjusted parameters
pos = nx.spring_layout(G, k=0.5, iterations=50)  # Adjust k value for spacing

# Create lists for lines and their corresponding widths
lines = []
line_widths = []

# Extract edges and their weights
for (word1, word2, data) in G.edges(data=True):
    x1, y1 = pos[word1]
    x2, y2 = pos[word2]
    lines.append([(x1, y1), (x2, y2)])
    line_widths.append(data['weight'])  # Use the weight as the line width

# Create a ColumnDataSource for Bokeh
source = ColumnDataSource(data=dict(
    x=[pos[word][0] for word in words],
    y=[pos[word][1] for word in words],
    size=sizes,
    word=words,
    total_count=df['Total_Count']
))

# Create a Bokeh figure
p = figure(title="Word Frequency Visualization", tools="pan,wheel_zoom,reset",
           width=800, height=800)  # Changed to width and height

# Add lines (connections) between words
for i, line in enumerate(lines):
    p.line(x=[line[0][0], line[1][0]], y=[line[0][1], line[1][1]],
           line_width=line_widths[i] / 5, line_color="gray", alpha=0.5)

# Add circles (points) for each word
p.circle('x', 'y', size='size', source=source, fill_alpha=0.6, line_color="navy")

# Add hover tool to display word and total count
hover = HoverTool(tooltips=[("Word", "@word"), ("Total Count", "@total_count")])
p.add_tools(hover)

# Add labels for each word
labels = LabelSet(x='x', y='y', text='word', source=source, 
                  text_font_size='10pt', text_align='center', 
                  text_baseline='middle', render_mode='canvas')
p.add_layout(labels)

# Output to an interactive HTML file
output_file("word_frequency_visualization_with_labels.html")  # Output file name
save(p)

print("Visualization saved as 'word_frequency_visualization_with_labels.html'.")
