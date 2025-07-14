# src/load_pdf.py
import fitz  # PyMuPDF

def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += text + "\n"
    return full_text

