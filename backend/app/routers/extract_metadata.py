import fitz  # PyMuPDF
import re

def extract_metadata(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    clean_text = text.replace("\n", " ").strip()

    # ✅ Extract name from top of document using better heuristic
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if re.match(r"^[A-Z][A-Z\s]+$", lines[0]) else None

    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", clean_text)
    phone = re.findall(r"\b\d{10}\b", clean_text)
    address_match = re.search(r"(Mumbai(?:,?\s+India)?)", clean_text)  # crude fallback

    metadata = {
        "name": name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "address": address_match.group(0) if address_match else None,
    }

    return text, metadata
