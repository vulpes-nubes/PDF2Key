import os
import csv
import pandas as pd

# Define paths
txt_file_path = 'path_to_your_txt_file.txt'  # Path to the .txt file with the word list
csv_directory = 'path_to_your_csv_directory/'  # Directory with the CSV files
output_file = 'output.csv'  # Output file

# Read the words from the txt file
with open(txt_file_path, 'r') as f:
    words = [line.strip() for line in f.readlines()]

# Create an empty dictionary to store word counts
word_counts = {word: [] for word in words}

# Loop over each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_directory, csv_file)
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Ensure the file has 'Keyword' and 'Count' columns
        if 'Keyword' in df.columns and 'Count' in df.columns:
            # Check for each word in the current CSV file
            for word in words:
                # Get the 'Count' for the current word, if it exists
                count = df.loc[df['Keyword'] == word, 'Count'].sum()
                word_counts[word].append(count)
        else:
            # If file doesn't contain required columns, append zeros for the words
            for word in words:
                word_counts[word].append(0)

# Convert the word_counts dictionary into a DataFrame for exporting
df_output = pd.DataFrame.from_dict(word_counts, orient='index')
df_output.columns = [f'File_{i+1}' for i in range(df_output.shape[1])]

# Add the word as the first column
df_output.reset_index(inplace=True)
df_output.columns = ['Word'] + df_output.columns.tolist()[1:]

# Export the result to CSV
df_output.to_csv(output_file, index=False)

print(f"Data successfully exported to {output_file}")
