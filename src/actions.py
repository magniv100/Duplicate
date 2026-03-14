from fastapi import UploadFile

from src.models.requests import InsertRequest


def insert_image(insert_req: InsertRequest, image: UploadFile):
    metadata = validation(insert_req.metadata)
    if metadata is not None:
        rabbit_mq_writer(metadata, image)
        upload_s3_store_first(metadata, image)
        return {"status_code": 200, "detail": "success"}
    return {"status_code": 422, "detail": "didn't pass validation"}
