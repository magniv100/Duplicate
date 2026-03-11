import http, logging


def check_object_details(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if object details isnt null( {metadata}")
    for value in metadata["object_details"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Object details pass: {metadata}")
    return True


def check_digital_capture(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if digital capture isnt null( {metadata}")
    for value in metadata["digital_capture"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Digital capture pass: {metadata}")
    return True


def check_place(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if place isnt null( {metadata}")
    keys = list(metadata.keys())
    place = keys[3]
    for value in metadata[place]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Place pass: {metadata}")
    return True


def check_all_exist(metadata: dict) -> bool | http.HTTPStatus:
    logging.debug(f"start checking if asset id and type isnt null( {metadata}")
    if metadata["asset_id"] is not None and metadata["asset_type"] is not None:
        logging.debug(f"asset id and type pass {metadata}")
        if check_object_details(metadata) and check_digital_capture(metadata) and check_place(metadata):
            return True
        else:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    else:
        return http.HTTPStatus.UNPROCESSABLE_CONTENT


def validation(metadata: dict) -> dict | http.HTTPStatus:
    logging.debug(f"Metadata in {metadata}")
    if check_all_exist(metadata):
        logging.debug(f"validation pass {metadata}")
        return metadata
    return http.HTTPStatus.UNPROCESSABLE_CONTENT

