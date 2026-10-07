import os
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .models import ValidationResult, NimdpConfig
from .config import load_config
from .core import aggregate_scores, read_file_text

app = FastAPI(title="NIMDP Command Center API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValidationRequest(BaseModel):
    project_name: str
    token_map: str = "token_map.yaml"

@app.get("/packs")
async def list_packs():
    packs_dir = Path("packs")
    if not packs_dir.exists():
        return []
    return [p.name for p in packs_dir.glob("*.yaml")]

@app.post("/validate", response_model=ValidationResult)
async def validate_spec(
    project_name: str = Form(...),
    token_map: str = Form("token_map.yaml"),
    files: List[UploadFile] = File(...)
):
    # 1. Save uploaded files to temp dir
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    
    file_paths = []
    for file in files:
        file_path = temp_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
        
    try:
        # 2. Load Config
        config_path = Path("packs") / token_map
        if not config_path.exists():
            # Fallback to root or default
            config_path = Path(token_map)
            
        config = load_config(config_path if config_path.exists() else None)
        
        # 3. Read texts
        texts = []
        for p in file_paths:
            t = read_file_text(p)
            if t:
                texts.append(t)
                
        if not texts:
            raise HTTPException(status_code=400, detail="No readable content in files")
            
        # 4. Run Validation
        result = aggregate_scores(texts, config)
        return result
        
    finally:
        # Cleanup
        for p in file_paths:
            if p.exists():
                p.unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
