from src.models.requests import InsertRequest


def insert_picture(insert_req: InsertRequest):
    metadata = validation(insert_req.metadata)
    if metadata is not None:
        rabbit_mq_writer(metadata, insert_req.picture)
        s3_store_first_writer(metadata, insert_req.picture)
        return {"status_code": 200, "detail": "success"}
    return {"status_code": 422, "detail": "didn't pass validation"}
