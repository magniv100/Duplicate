from fastapi import UploadFile

from src.models.requests import InsertRequest
from src.rabitMq.rabbit_mq_writer import rabbit_mq_writer
from src.s3.s3_connect_dupe import upload_to_s3
from src.schema.schema_management import validation
import logging


def insert_image(insert_req: InsertRequest, image: UploadFile):
    logging.log(20, "validating metadata...")
    metadata = validation(insert_req.metadata)
    logging.log(20, "validation successful")
    if metadata is not None:
        logging.log(20, "passed validation")
        logging.log(20, "writing to rabbitmq...")
        rabbit_mq_writer(metadata, image)
        logging.log(20, "writing to s3 store first...")
        upload_to_s3(metadata, image)
        logging.log(20, "successfully uploaded to rabbitmq and s3")
        return {"status_code": 200, "detail": "success"}
    logging.log(20, "didn't pass validation")
    return {"status_code": 422, "detail": "didn't pass validation"}
