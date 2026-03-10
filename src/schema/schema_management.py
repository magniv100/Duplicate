import http


def check_object_details(metadata: dict) -> bool | http.HTTPStatus:
    for value in metadata["object_details"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    return True


def check_digital_capture(metadata: dict) -> bool | http.HTTPStatus:
    for value in metadata["digital_capture"]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    return True


def check_place(metadata: dict) -> bool | http.HTTPStatus:
    keys = list(metadata.keys())
    place = keys[3]
    for value in metadata[place]:
        if value is None:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    return True


def check_all_exist(metadata: dict) -> bool | http.HTTPStatus:
    if metadata["asset_id"] is not None and metadata["asset_type"] is not None:
        if check_object_details(metadata) and check_digital_capture(metadata) and check_place(metadata):
            return True
        else:
            return http.HTTPStatus.UNPROCESSABLE_CONTENT
    else:
        return http.HTTPStatus.UNPROCESSABLE_CONTENT


def main(metadata: dict) -> dict | http.HTTPStatus:
    if check_all_exist(metadata):
        return metadata
    return http.HTTPStatus.UNPROCESSABLE_CONTENT

