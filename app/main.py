import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from google.cloud import storage
from .ocr import perform_ocr
from .layout_detection import detect_layout

app = FastAPI(
    title="Organize OCR Service",
    description="A custom OCR service to extract text and detect layout from images.",
    version="1.0.0",
)

storage_client = storage.Client()

GCS_BUCKET = os.getenv("GCS_BUCKET", "your-default-bucket-name")

@app.post("/ocr")
async def ocr_endpoint(bucket_name: str, file_name: str):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        image_bytes = blob.download_as_bytes()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download file: {e}")

    extracted_text = perform_ocr(image_bytes)
    if not extracted_text:
        raise HTTPException(status_code=500, detail="OCR failed to extract text.")

    layout = detect_layout(image_bytes)

    payload = {
        "document_id": file_name,
        "extracted_text": extracted_text,
        "layout": layout,
    }

    return JSONResponse(content=payload)

@app.get("/")
def read_root():
    return {"message": "Custom OCR Service is running."}
