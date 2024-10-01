import os

def clean_filename(filename):
    # Remove commas from the filename
    cleaned_filename = filename.replace(',', '')
    
    # Split by spaces and preserve the first part (could be hyphenated)
    first_part = cleaned_filename.split()[0]
    
    # Remove any extra extensions that might exist (e.g., .csv.csv)
    first_part = first_part.rstrip('.pdf')
    
    return first_part

# Set the path to your directory
directory = '/home/gray221/Documents/batch'

# Loop over all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        # Clean the filename (remove commas and keep hyphenated words)
        new_filename = clean_filename(filename)
        
        # Ensure the new filename has a single .csv extension
        new_filename = f"{new_filename}.pdf"
        
        # Get the full path for the old and new filenames
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")

print("Renaming completed!")
