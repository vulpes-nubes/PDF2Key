import os
import pandas as pd

# Define paths
txt_file_path = '/path to wordlist .txt'  # Path to the .txt file with the word list
keycounted_directory = '/path to CSVs'  # Directory with the filtered CSV files
summary_output_file = 'summary_output.csv'  # Output summary CSV file

# Read the words from the txt file into a list
with open(txt_file_path, 'r') as f:
    words = [line.strip() for line in f.readlines()]

# Create an empty DataFrame to store the summary
summary_df = pd.DataFrame({'Word': words})

# Set 'Word' as the index for easier merging later
summary_df.set_index('Word', inplace=True)

# List to keep track of successfully processed file names
processed_files = []

# Loop over each CSV file in the 'KeyCounted' directory
for csv_file in os.listdir(keycounted_directory):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(keycounted_directory, csv_file)
        
        # Read the filtered CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Ensure the file has 'Word' and 'Count' columns
        if 'Word' in df.columns and 'Count' in df.columns:
            # Extract the filename without the extension for the column name
            file_name = os.path.splitext(csv_file)[0]
            processed_files.append(file_name)
            
            # Create a temporary DataFrame with 'Word' as index and 'Count' as the column
            temp_df = df[['Word', 'Count']].set_index('Word')
            
            # Rename the 'Count' column to the filename
            temp_df.columns = [file_name]
            
            # Merge the temporary DataFrame with the main summary DataFrame
            summary_df = summary_df.merge(temp_df, how='left', left_index=True, right_index=True)
        else:
            print(f"Skipping {csv_file} due to missing 'Word' or 'Count' columns")

# Replace NaN values with 0 (indicating that a word wasn't present in a particular file)
summary_df.fillna(0, inplace=True)

# Verification step: Check that there is exactly one column for each CSV file
expected_columns = set(os.path.splitext(f)[0] for f in os.listdir(keycounted_directory) if f.endswith('.csv'))
actual_columns = set(summary_df.columns)

if expected_columns == actual_columns:
    print(f"Verification successful! All {len(expected_columns)} files have been processed correctly.")
else:
    missing_files = expected_columns - actual_columns
    extra_columns = actual_columns - expected_columns
    print(f"Verification failed! Issues detected:")
    if missing_files:
        print(f"Missing columns for files: {missing_files}")
    if extra_columns:
        print(f"Extra columns found: {extra_columns}")

# Reset the index to make 'Word' a column again
summary_df.reset_index(inplace=True)

# Export the result to a CSV file
summary_df.to_csv(summary_output_file, index=False)

print(f"Data successfully summarized and exported to {summary_output_file}")
