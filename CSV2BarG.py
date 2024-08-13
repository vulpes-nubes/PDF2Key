#coded by NubesVulpes with help from ChatGPT
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox

def load_and_plot_csv():
    # Prompt the user to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    output_path = os.path.splitext(file_path)[0] + "_top15_graph.png"

    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Ensure the DataFrame has the expected structure
        if 'Keyword' not in df.columns or 'Count' not in df.columns:
            messagebox.showerror("Error", "CSV must have 'Keyword' and 'Count' columns")
            return

        # Sort the DataFrame by count and select the top 15 words
        df_top15 = df.sort_values(by='Count', ascending=False).head(15)

        # Create the bar plot using seaborn
        plt.figure(figsize=(10, 8))
        sns.barplot(x='Count', y='Keyword', data=df_top15, palette='viridis')
        plt.xlabel('Count')
        plt.ylabel('Keywords')
        plt.title('Top 15 Keywords by Count')
        plt.savefig(output_path)  # Save the plot as a PNG file
        plt.show()  # Display the plot

        messagebox.showinfo("Success", f"Bar graph saved as {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the tkinter GUI
root = tk.Tk()
root.title("CSV to Bar Graph")

# Add a button to trigger the CSV load and plot
load_button = tk.Button(root, text="Load CSV and Plot", command=load_and_plot_csv)
load_button.pack(pady=20)

# Run the tkinter main loop
root.mainloop()
