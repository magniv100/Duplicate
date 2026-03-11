import http, logging


def check_object_details(metadata: dict) -> bool | http.HTTPStatus:
    for value in metadata["object_details"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Object details: {metadata}")
    return True


def check_digital_capture(metadata: dict) -> bool | http.HTTPStatus:
    for value in metadata["digital_capture"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Digital capture: {metadata}")
    return True


def check_place(metadata: dict) -> bool | http.HTTPStatus:
    keys = list(metadata.keys())
    place = keys[3]
    for value in metadata[place]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    logging.debug(f"Place: {metadata}")
    return True


def check_all_exist(metadata: dict) -> bool | http.HTTPStatus:
    if metadata["asset_id"] is not None and metadata["asset_type"] is not None:
        if check_object_details(metadata) and check_digital_capture(metadata) and check_place(metadata):
            logging.debug(f"Existing asset: {metadata}")
            return True
        else:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    else:
        return http.HTTPStatus.UNPROCESSABLE_CONTENT


def main(metadata: dict) -> dict | http.HTTPStatus:
    logging.debug(f"Metadata in {metadata}")
    if check_all_exist(metadata):
        return metadata
    return http.HTTPStatus.UNPROCESSABLE_CONTENT

