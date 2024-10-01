# data_analysis.py

import os
import pandas as pd
import networkx as nx
import pickle

# Load words from the txt file
def load_word_list(txt_file):
    print(f"Loading word list from {txt_file}...")
    with open(txt_file, 'r') as f:
        words = [line.strip() for line in f.readlines()]
    print(f"Loaded {len(words)} words.")
    return words

# Function to read CSV files from a directory and construct the graph
def process_csv_files(word_list, csv_folder):
    G = nx.Graph()
    word_frequencies = {word: 0 for word in word_list}  # Track total frequency of each word
    edge_weights = {}  # Track edge weights between words

    # Iterate over all CSV files in the directory
    print(f"Processing CSV files from directory: {csv_folder}")
    for word in word_list:
        csv_file = os.path.join(csv_folder, f"{word}.csv")
        if os.path.exists(csv_file):
            print(f"Processing {csv_file}...")
            df = pd.read_csv(csv_file)

            for _, row in df.iterrows():
                keyword = row['Keyword']
                count = row['Count']

                # Check for missing values
                if pd.isna(keyword) or pd.isna(count):
                    print(f"Missing value found in {csv_file}: keyword={keyword}, count={count}. Skipping this row.")
                    continue

                count = int(count)  # Convert to int, may raise error if count is not convertible

                # Update word frequency
                if keyword in word_frequencies:
                    word_frequencies[keyword] += count
                
                # Update edge weights
                if (word, keyword) not in edge_weights:
                    edge_weights[(word, keyword)] = 0
                edge_weights[(word, keyword)] += count

        else:
            print(f"File {csv_file} does not exist, skipping...")

    # Add nodes and edges to the graph
    print("Building graph from processed data...")
    for word, frequency in word_frequencies.items():
        if frequency > 0:  # Only add nodes with non-zero frequency
            G.add_node(word, size=frequency)
            print(f"Added node: {word} with size: {frequency}")

    for (word, keyword), weight in edge_weights.items():
        if weight > 0:  # Only add edges with non-zero weight
            G.add_edge(word, keyword, weight=weight)
            print(f"Added edge: ({word}, {keyword}) with weight: {weight}")

    print(f"Graph construction complete with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

# Example usage
if __name__ == "__main__":
    word_list_file = '/home/gray221/Documents/batch/output/stoplist.txt'  # Replace with your actual word list file path
    csv_directory = '/home/gray221/Documents/batch/output/keywords'  # Replace with your actual CSV directory path

    # Load the word list
    words = load_word_list(word_list_file)

    # Process the CSV files to build the graph
    G = process_csv_files(words, csv_directory)

    # Save the graph for plotting using pickle
    with open("word_network_graph.gpickle", "wb") as f:
        pickle.dump(G, f)
    print("Graph saved to word_network_graph.gpickle.")
