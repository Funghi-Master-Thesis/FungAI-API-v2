from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import io
from PIL import Image
from models.model_loader import predict_image, predict_single_image

router = APIRouter()

# Path to save uploaded images temporarily
UPLOAD_DIR = Path(tempfile.gettempdir()) / "uploaded_images"
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/predict/", response_class=JSONResponse)
async def predict(file: UploadFile = File(...), ismasked: bool = Form(False)):
    """Unified prediction endpoint for FungAI."""
    try:
        # Save uploaded file
        image_bytes = await file.read()
        image_path = UPLOAD_DIR / file.filename
        Image.open(io.BytesIO(image_bytes)).save(image_path)

        # Run prediction
        predictions = predict_image(image_path, ismasked)

        # Delete the image after processing
        image_path.unlink(missing_ok=True)  # Remove the file

        # Return JSON response
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500,
        )

@router.post("/predict_single/", response_class=JSONResponse)
async def predict_single(file: UploadFile = File(...), ismasked: bool = Form(False)):
    """Unified prediction endpoint for FungAI."""
    try:
        # Save uploaded file
        image_bytes = await file.read()
        image_path = UPLOAD_DIR / file.filename
        Image.open(io.BytesIO(image_bytes)).save(image_path)

        # Run prediction
        predictions = predict_single_image(image_path, ismasked)

        # Delete the image after processing
        image_path.unlink(missing_ok=True)  # Remove the file

        # Return JSON response
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500,
        )
