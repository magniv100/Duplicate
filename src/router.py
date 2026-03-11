from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException

from src.actions import insert_picture
from src.models.requests import InsertRequest

main_router = APIRouter()

@main_router.post("/upload-image/")
async def upload_image(file: Annotated[UploadFile, File(...)], insert_req: InsertRequest):
    if file.content_type not in ["image/jpeg", "image/peg", "image/tiff", "image/webp", "image/avif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PEG, TIFF, AVIF, and WEBP allowed.")
    return insert_picture(insert_req)