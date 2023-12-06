from PyPDF2 import PdfReader

from memory_copilot.tools import register_meta


@register_meta('Read raw file', returns={'content': 'str'})
def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


@register_meta('Read pdf file', returns={'content': 'str'})
def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text
