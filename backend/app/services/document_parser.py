from pathlib import Path
import fitz
import docx
import pandas as pd

def parse_pdf(path: Path) -> str:
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def parse_docx(path: Path) -> str:
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_csv(path: Path) -> str:
    df = pd.read_csv(path)
    return df.to_string(index=False)

def parse_excel(path: Path) -> str:
    df = pd.read_excel(path)
    return df.to_string(index=False)

def parse_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(path)
    elif suffix == ".docx":
        return parse_docx(path)
    elif suffix == ".csv":
        return parse_csv(path)
    elif suffix == ".xlsx":
        return parse_excel(path)
    else:
        raise ValueError("Unsupported file type for parsing")
    