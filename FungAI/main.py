from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.routers import predict, general, sample_data

# Paths and directories
base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "api" / "static"

# FastAPI application setup
app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(predict.router)
app.include_router(general.router)
app.include_router(sample_data.router)

if __name__ == "__main__":
    print("Running app with uvicorn")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)