from fastapi import FastAPI, HTTPException
from typing import Dict
from schemas import ExamSkeleton
from presets import PRESETS

app = FastAPI(
    title="PocketGrader API",
    description="Local RAG-powered Exam Generation & Grading System",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "PocketGrader API is running"}

@app.get("/presets", response_model=Dict[str, str])
def list_presets():
    """Returns a dictionary of available exam preset keys and titles."""
    return {key: skeleton.title for key, skeleton in PRESETS.items()}

@app.get("/presets/{preset_key}", response_model=ExamSkeleton)
def get_preset(preset_key: str):
    """Retrieves the full ExamSkeleton schema for a selected preset."""
    if preset_key not in PRESETS:
        raise HTTPException(
            status_code=404, 
            detail=f"Preset '{preset_key}' not found. Available presets: {list(PRESETS.keys())}"
        )
    return PRESETS[preset_key]