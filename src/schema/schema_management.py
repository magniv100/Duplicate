def check_object_details(metadata: dict) -> bool:
    for value in metadata["object_details"]:
        if value is None:
            return False
    return True


def check_digital_capture(metadata: dict) -> bool:
    for value in metadata["digital_capture"]:
        if value is None:
            return False
    return True


def check_place(metadata: dict) -> bool:
    keys = list(metadata.keys())
    place = keys[3]
    for value in metadata[place]:
        if value is None:
            return False
    return True


def check_all_exist(metadata: dict) -> bool:
    if metadata["asset_id"] is not None and metadata["asset_type"] is not None:
        if check_object_details(metadata) and check_digital_capture(metadata) and check_place(metadata):
            return True
        else:
            return False
    else:
        return False

def main(metadata: dict) -> dict:
    if check_all_exist(metadata):
        return metadata
    return None

