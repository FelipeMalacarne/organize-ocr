import cv2
import numpy as np
import io
from PIL import Image

def detect_layout(image_bytes: bytes) -> dict:
    """
    Detect basic layout elements like text blocks, tables, and images.
    Returns a dictionary with detected elements and their positions.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        open_cv_image = np.array(image)

        image_cv = open_cv_image[:, :, ::-1].copy()

        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)


        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        layout = {"text_blocks": [], "images": [], "tables": []}

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if area < 1000:
                continue

            aspect_ratio = w / float(h)
            if aspect_ratio > 5:
                layout["tables"].append({"x": x, "y": y, "width": w, "height": h})
            elif aspect_ratio < 0.5:
                layout["images"].append({"x": x, "y": y, "width": w, "height": h})
            else:
                layout["text_blocks"].append({"x": x, "y": y, "width": w, "height": h})

        return layout
    except Exception as e:
        print(f"Layout Detection Error: {e}")
        return {}
