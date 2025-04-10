# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from app.face_check import check_person

app = FastAPI()

@app.post("/verify/")
async def verify_face(file: UploadFile = File(...)):
    temp_dir = Path("app/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file = temp_dir / f"{uuid.uuid4()}.jpg"
    with temp_file.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    person = check_person(str(temp_file))
    temp_file.unlink()  # remove imagem temporária após o uso
    
    if person:
        return JSONResponse(content={"match": True, "person": person})
    else:
        return JSONResponse(content={"match": False, "person": None})
