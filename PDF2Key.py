#Coded by Vulpes Nubes, with help from ChatGPT
#Free to use and fork !!!
#requires installastion of tkinter, nltk and PyPDF2

import os
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader
import csv
import re
import nltk
from collections import Counter
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def convert_pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def tokenize_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    words = nltk.word_tokenize(text.lower())
    return words

def is_latin_number(word):
    latin_number_pattern = r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv|xvi|xvii|xviii|xix|xx|xxi|xxii|xxiii|xxiv|xxv|xxvi|xxvii|xxviii|xxix|xxx)$'
    return re.match(latin_number_pattern, word) is not None

def filter_words(words):
    filtered_words = [word for word in words if re.match(r'^[a-zA-Z]{2,}$', word)]
    return filtered_words

def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
    return lemmatized_words

def count_words(words):
    word_counts = Counter(words)
    return word_counts

def save_word_counts_to_csv(word_counts, output_path):
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Word", "Count"])
        for word, count in sorted_word_counts:
            writer.writerow([word, count])

def filter_keywords(word_counts, exclude_words):
    stop_words = set(stopwords.words('english'))
    additional_stopwords = {'cf', 'sig', 'vol', 'dictionary'}
    stop_words.update(additional_stopwords)
    stop_words.update(exclude_words)
    keywords = {word: count for word, count in word_counts.items() if word not in stop_words and not is_latin_number(word)}
    return keywords

def save_keywords_to_csv(keywords, output_path):
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Keyword", "Count"])
        for keyword, count in sorted_keywords:
            writer.writerow([keyword, count])

def main():
    # Hide Tkinter root window
    Tk().withdraw()
    
    # Prompt user to select a PDF file
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        print("No file selected. Exiting.")
        return

    # Convert PDF to text
    text = convert_pdf_to_text(pdf_path)
    
    # Create output text file path
    txt_output_path = os.path.splitext(pdf_path)[0] + ".txt"
    
    # Save text to file
    save_text_to_file(text, txt_output_path)
    
    print(f"Text successfully extracted to {txt_output_path}")
    
    # Read text from file
    with open(txt_output_path, 'r', encoding='utf-8') as text_file:
        text = text_file.read()
    
    # Extract the base name and remove the .pdf extension
    base_name = os.path.basename(pdf_path)
    file_name_without_extension = os.path.splitext(base_name)[0]
    exclude_word = file_name_without_extension.split()[0].lower()
    exclude_words = {exclude_word}

    # Tokenize, filter, lemmatize, and count words in text
    words = tokenize_text(text)
    filtered_words = filter_words(words)
    lemmatized_words = lemmatize_words(filtered_words)
    word_counts = count_words(lemmatized_words)
    
    # Create output CSV file paths
    word_counts_output_path = os.path.splitext(txt_output_path)[0] + "_word_counts.csv"
    keywords_output_path = os.path.splitext(txt_output_path)[0] + "_keywords.csv"
    
    # Save word counts to CSV
    save_word_counts_to_csv(word_counts, word_counts_output_path)
    
    # Filter keywords and save to CSV
    keywords = filter_keywords(word_counts, exclude_words)
    save_keywords_to_csv(keywords, keywords_output_path)
    
    print(f"Word counts successfully saved to {word_counts_output_path}")
    print(f"Keywords successfully saved to {keywords_output_path}")

if __name__ == "__main__":
    main()
