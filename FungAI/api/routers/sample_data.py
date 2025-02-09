from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pathlib import Path
import aiofiles
import zipfile
import io

router = APIRouter()

# Paths to sample data directories
SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "sample_data"
IBT_23255_DIR = SAMPLE_DATA_DIR / "IBT_23255"
IBT_32802_DIR = SAMPLE_DATA_DIR / "IBT_32802"

# Ensure directories exist
IBT_23255_DIR.mkdir(parents=True, exist_ok=True)
IBT_32802_DIR.mkdir(parents=True, exist_ok=True)

# Fetch files for a given type
@router.get("/sample-data/")
async def get_sample_files(fungal_type: str = Query(...)):
    if fungal_type == "IBT_23255":
        files = [file.name for file in IBT_23255_DIR.iterdir() if file.is_file()]
    elif fungal_type == "IBT_32802":
        files = [file.name for file in IBT_32802_DIR.iterdir() if file.is_file()]
    else:
        return JSONResponse(content={"error": "Invalid fungal type"}, status_code=400)
    return {"files": files}

# Download selected file
@router.get("/download/{fungal_type}/{file_name}")
async def download_file(fungal_type: str, file_name: str):
    folder = IBT_23255_DIR if fungal_type == "IBT_23255" else IBT_32802_DIR if fungal_type == "IBT_32802" else None
    if folder:
        file_path = folder / file_name
        if file_path.exists():
            return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
    return JSONResponse(content={"error": "File not found"}, status_code=404)

# Download and zip multiple files
@router.get("/download/")
async def download_selected_files(fungal_type: str, files: str):
    folder = IBT_23255_DIR if fungal_type == "IBT_23255" else IBT_32802_DIR if fungal_type == "IBT_32802" else None
    if not folder:
        return JSONResponse(content={"error": "Invalid fungal type"}, status_code=400)

    file_names = files.split(",")  # Parse the comma-separated file names
    zip_stream = io.BytesIO()

    with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name in file_names:
            file_path = folder / file_name
            if file_path.exists():
                async with aiofiles.open(file_path, "rb") as f:
                    content = await f.read()
                    zipf.writestr(file_name, content)

    zip_stream.seek(0)

    return StreamingResponse(
        zip_stream,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=selected_images.zip"
        },
    )
