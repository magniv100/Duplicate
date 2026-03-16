from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException

from src.api.actions import insert_image
from src.models.requests import InsertRequest
import logging

main_router = APIRouter()

@main_router.post("/upload-image/")
async def upload_image(image: Annotated[UploadFile, File(...)], insert_req: InsertRequest):
    if image.content_type not in ["image/jpeg", "image/peg", "image/tiff", "image/webp", "image/avif"]:
        logging.log(10, f"image type not allowed - {image.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PEG, TIFF, AVIF, and WEBP allowed.")
    return insert_image(insert_req, image)