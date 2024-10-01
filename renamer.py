import os

def clean_filename(filename):
    # Split the filename at the first comma and take the part before it
    if ',' in filename:
        cleaned_filename = filename.split(',', 1)[0]  # Keep everything before the first comma
    else:
        cleaned_filename = filename  # If no comma, keep the whole filename
    
    # Return the cleaned filename
    return cleaned_filename

# Set the path to your directory
directory = '/path/to/pdfs'

# Loop over all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        # Clean the filename (remove everything after the first comma)
        new_filename = clean_filename(filename)
        
        # Ensure the new filename has the .pdf extension
        new_filename = f"{new_filename}.pdf"
        
        # Get the full path for the old and new filenames
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")

print("Renaming completed!")

