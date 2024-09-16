import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import filedialog
import csv

# Download the required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to open file dialog and select a .txt file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path

# Function to read the contents of the selected file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to tag parts of speech and save the result in a CSV format
def tag_and_export(file_path):
    # Read the file contents
    text = read_file(file_path)
    
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Tag the tokens with their part-of-speech
    tagged_words = pos_tag(words)
    
    # Create a new file name for the tagged data output
    output_file_path = file_path.replace('.txt', '_tagged.csv')
    
    # Write the tagged data into a CSV file
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Word', 'POS Tag'])  # Write header row
        writer.writerows(tagged_words)        # Write word/tag pairs
    
    print(f"Tagged data has been saved to {output_file_path}")

# Main function
def main():
    # Ask the user to select a file
    file_path = select_file()
    
    if file_path:
        # Tag the file content and export the result
        tag_and_export(file_path)
    else:
        print("No file selected. Exiting.")

if __name__ == '__main__':
    main()
