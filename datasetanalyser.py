import pandas as pd

# Parameters
input_file = 'summary_output.csv'  # Replace with the path to your input dataset
output_file = 'output_data.csv'  # Path to the output CSV file
x = 10  # Set this to the number of top results you want to extract for each unique pair

# Load dataset
df = pd.read_csv(input_file)

# Initialize a dictionary to store the results with unique (row, column) combinations
results_dict = {}

# Ensure all columns except the first (words) are numeric
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Iterate over each row to calculate values
for row_index, row in df.iterrows():
    word_row = row[0]  # The word in the first column
    row_values = row[1:]  # The interaction counts (numeric)
    
    # Drop NaN values after coercion to numeric
    row_values = row_values.dropna()

    for col_index in range(len(row_values)):
        value = row_values.iloc[col_index]  # Get the current interaction count
        col_name = df.columns[col_index + 1]  # Get the actual column name (adjusted for index shift)
        
        # Skip identical pairs
        if word_row == col_name:
            continue
        
        # Create a sorted tuple of (row, column) to ensure symmetry is handled
        word_pair = tuple(sorted([word_row, col_name]))
        
        # Add the interaction count to the results dictionary
        if word_pair in results_dict:
            results_dict[word_pair] += value
        else:
            results_dict[word_pair] = value

# Convert the results into a list for CSV export
results = [[pair[0], pair[1], total] for pair, total in results_dict.items()]

# Create a DataFrame from the results
output_df = pd.DataFrame(results, columns=['row name', 'column name', 'total'])

# Group by pairs and extract the top x entries for each unique pair
top_results = output_df.groupby(['row name', 'column name']).apply(lambda group: group.nlargest(x, 'total')).reset_index(drop=True)

# Export the top results to CSV
top_results.to_csv(output_file, index=False)

print(f"Top {x} results for each unique pair saved to {output_file}")
