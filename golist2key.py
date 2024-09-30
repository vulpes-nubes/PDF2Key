import csv
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to open a file dialog and select the word list
def load_word_list(text_file_base_name):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Select Word List", "Please select the TXT file containing the word list.")
    
    file_path = filedialog.askopenfilename(
        title="Select Word List",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if file_path:
        with open(file_path, 'r') as file:
            word_list = [line.strip() for line in file.readlines()]
        
        # Exclude the base name of the text file from the word list
        word_list = [word for word in word_list if word.lower() != text_file_base_name.lower()]
        return word_list
    else:
        messagebox.showerror("Error", "No file selected. Exiting.")
        root.quit()

# Function to load the text file for searching
def load_text_file():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Select Text File", "Please select the TXT file for word frequency analysis.")
    
    file_path = filedialog.askopenfilename(
        title="Select Text File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read().lower()  # Convert to lowercase for case-insensitive matching
        # Extract the base name (without extension) to exclude it from the word list
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        return text, file_path, base_name
    else:
        messagebox.showerror("Error", "No file selected. Exiting.")
        root.quit()

# Function to count word frequencies in the text
def count_word_frequencies(word_list, text):
    word_count = {}
    for word in word_list:
        count = len(re.findall(rf'\b{re.escape(word)}\b', text))
        word_count[word] = count
    return word_count

# Function to export word frequency to CSV, named after the provided text file
def export_to_csv(word_count, text_file_path):
    base_name = os.path.splitext(os.path.basename(text_file_path))[0]
    output_file = f"{base_name}_word_frequencies.csv"
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['keyword', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for word, count in word_count.items():
            writer.writerow({'keyword': word, 'count': count})
    
    messagebox.showinfo("Success", f"Word frequencies have been saved to {output_file}")

# Main function to tie everything together
def main():
    text, text_file_path, base_name = load_text_file()
    word_list = load_word_list(base_name)
    word_count = count_word_frequencies(word_list, text)
    export_to_csv(word_count, text_file_path)

if __name__ == "__main__":
    main()
