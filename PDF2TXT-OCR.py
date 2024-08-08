#Coded by Vulpes Nubes, with help from ChatGPT
#Free to use and fork !!!
#requires tesserct, tkinter, PyMuPDF

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def pdf_to_text(pdf_path, output_text_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text_output = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Convert the Pixmap to a PIL Image
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        text_output += f"Page {page_num + 1}\n{text}\n"

    with open(output_text_file, 'w') as f:
        f.write(text_output)

    messagebox.showinfo("Success", f"OCR complete. Output saved to {output_text_file}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open file dialog to select PDF file
    pdf_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )

    if not pdf_path:
        messagebox.showerror("Error", "No file selected")
        return

    # Save the output text to the same directory as the PDF
    output_text_file = pdf_path.replace(".pdf", "_output.txt")

    pdf_to_text(pdf_path, output_text_file)

if __name__ == "__main__":
    main()
