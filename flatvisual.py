import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
import numpy as np

# Load the CSV file (update the file path as needed)
file_path = 'path/to/your/summary_output.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Calculate the total sum of counts for each word across all columns
df['Total_Count'] = df.iloc[:, 1:].sum(axis=1)

# Prepare the data for plotting: words, total counts, and generate random x and y positions for layout
words = df['Word']
sizes = df['Total_Count'] / df['Total_Count'].max() * 50  # Normalize sizes for better visualization
x = np.random.uniform(low=0, high=100, size=len(words))   # Random x-coordinates
y = np.random.uniform(low=0, high=100, size=len(words))   # Random y-coordinates

# Create a ColumnDataSource for Bokeh
source = ColumnDataSource(data=dict(
    x=x,
    y=y,
    size=sizes,
    word=words,
    total_count=df['Total_Count']
))

# Create a Bokeh figure
p = figure(title="Word Frequency Visualization", tools="pan,wheel_zoom,reset", 
           plot_width=800, plot_height=800)

# Add circles (points) for each word
p.circle('x', 'y', size='size', source=source, fill_alpha=0.6, line_color=None)

# Add hover tool to display word and total count
hover = HoverTool(tooltips=[("Word", "@word"), ("Total Count", "@total_count")])
p.add_tools(hover)

# Output to an interactive HTML file
output_file("word_frequency_visualization.html")  # Output file name
save(p)

print("Visualization saved as 'word_frequency_visualization.html'.")
