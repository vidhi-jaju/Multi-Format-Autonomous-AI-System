import PyPDF2
from io import BytesIO

def extract_pdf_text(input_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(BytesIO(input_bytes))
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text 