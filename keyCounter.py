import os
import pandas as pd

# Define paths
txt_file_path = '/path to stoplist .txt'  # Path to the .txt file with the word list
csv_directory = '/path to CSVs'  # Directory with the CSV files
output_directory = os.path.join(csv_directory, 'KeyCounted')  # Directory to save the output files

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read the words from the txt file into a list
with open(txt_file_path, 'r') as f:
    words = [line.strip() for line in f.readlines()]

# Loop over each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_directory, csv_file)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Ensure the file has 'Keyword' and 'Count' columns
        if 'Word' in df.columns and 'Count' in df.columns:
            # Filter the DataFrame to only include rows where 'Keyword' is in the word list
            filtered_df = df[df['Word'].isin(words)]
            
            # Save the filtered DataFrame to a new CSV in the 'KeyCounted' subdirectory
            output_csv_path = os.path.join(output_directory, csv_file)
            filtered_df.to_csv(output_csv_path, index=False)
            
            print(f"Processed {csv_file} and saved to {output_csv_path}")
        else:
            print(f"Skipping {csv_file} due to missing 'Keyword' or 'Count' columns")
