import pytesseract
from PIL import Image
import io

def perform_ocr(image_bytes: bytes) -> str:
    """
    Perform OCR on the given image bytes and return extracted text.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
