import PyPDF2

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
