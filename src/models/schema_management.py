import http, logging
from http.client import HTTPException


def check_object_details(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if object details isnt null( {metadata}")
    for value in metadata["object_details"]:
        if value is None:
            raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"object_details null")
    logging.debug(f"Object details pass: {metadata}")
    return True


def check_digital_capture(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if digital capture isnt null( {metadata}")
    for value in metadata["digital_capture"]:
        if value is None:
            raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"digital_capture null")
    logging.debug(f"Digital capture pass: {metadata}")
    return True


def check_place(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if place isnt null( {metadata}")
    keys = list(metadata.keys())
    place = keys[3]
    for value in metadata[place]:
        if value is None:
            raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"place null")
    logging.debug(f"Place pass: {metadata}")
    return True


def check_all_exist(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if asset id and type isnt null( {metadata}")
    if metadata["asset_id"] is not None and metadata["asset_type"] is not None:
        logging.debug(f"asset id and type pass {metadata}")
        if check_object_details(metadata) and check_digital_capture(metadata) and check_place(metadata):
            return True
        else:
            raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"asset_id or asset_type null")
    else:
        raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"asset_id null")


def validation(metadata: dict) -> dict | http.HTTPStatus:
    logging.debug(f"Metadata in {metadata}")
    if check_all_exist(metadata):
        logging.debug(f"validation pass {metadata}")
        return metadata
    raise HTTPException(http.HTTPStatus.UNPROCESSABLE_CONTENT,"validation failed")

