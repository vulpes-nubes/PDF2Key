# PDF2Key, TXT2Key, CSV2BarG and COMBOBREAKER 
These scripts do the following :
## PDF2Key : converts a PDF to TXT and extracts the word counts (excluding the file name)
## TXT2Key : Opens a TXT and extracts the word counts (excluding the file name)
## CSV2BarG : Opens a CSV created by either PDF2Key or TXT2KEY and pushes out a colourful bar graph of the main (X) words

-- 
# PDF2Key requires you to install tkinter, nltk and PyPDF2

Linux : 
sudo apt-get update
sudo apt-get install -y python3-tk
sudo pip install nltk PyPDF2

Windows (in powershell):
pip install nltk PyPDF2

---
# PDF2TXT-OCR requires you to install pymupdf pytesseract pillow tkinter and tesseract-ocr

Linux :
sudo apt-get install -y python3-tk
sudo pip install pymupdf pytesseract pillow
sudo apt-get install tesseract-ocr

Windows :
pip install pymupdf pytesseract pillow
Tesseract : https://github.com/UB-Mannheim/tesseract/wiki

---
# TXT2Key requires you to install tkinter and nltk
Linux : 
sudo apt-get update
sudo apt-get install -y python3-tk
sudo pip install nltk

Windows (in powershell):
pip install nltk

----
# CSV2BarG requires you to install pandas matplotlib and seaborn
Linux: 
sudo pip install pandas matplotlib seaborn

Windows:
pip install pandas matplotlib seaborn