import fitz


def extract_korean_english_text(file_path: str) -> str:
    text_data = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text_data += page.get_text("text", sort=True) + "\n"

    return text_data