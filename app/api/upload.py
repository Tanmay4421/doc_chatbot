from fastapi import APIRouter, UploadFile
import shutil
from ingestion.ingest import ingest_files
from core.config import UPLOAD_DIR

router = APIRouter()

@router.post("/upload")
async def upload(files: list[UploadFile]):
    paths = []

    for file in files:
        path = UPLOAD_DIR / file.filename
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        paths.append(str(path))

    collection_name = ingest_files(paths)

    return {
        "status": "ingested",
        "collection_name": collection_name,
    }
