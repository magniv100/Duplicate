import filecmp, logging, json, boto3
from botocore.client import logger
from fastapi import UploadFile, HTTPException

access_key = ''
secret_key = ''
bucket_name =''


s3 = boto3.resource('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)


def upload_to_s3(meta_data: dict, image: UploadFile):
    logging.log(20, f'start uploading files to S3 bucket {bucket_name}')
    try:
        asset_id = meta_data['asset_id']
        if check_dupelication_asset_id(asset_id):
            logging.log(10, f'Asset {asset_id} already exists in bucket {bucket_name}')
            raise HTTPException(status_code=400, detail="Invalid file type. Only PEG, TIFF, AVIF, and WEBP allowed.")
        else:
            upload_image(image, asset_id)
            upload_metadata(meta_data, asset_id)


    except Exception as e:
        logging.log(10, f'Error uploading files to S3 bucket {bucket_name}: {e}')
        return False

def upload_image(image: UploadFile, asset_id: str):
    try:
        if check_dupelication_asset_id(asset_id):
            if check_duplication_image(image, asset_id):
                image_type = image.content_type
                s3.upload_fileobj(image.file, bucket_name, 'group3/store_first/' +  'image/' + asset_id + '.' + image_type)

        logging.log(20, f'Image {asset_id} uploaded to S3 bucket {bucket_name}')

    except Exception as e:
        logger.info(f'Error uploading files to S3 bucket {bucket_name}: {e}')


def upload_metadata(meta_data: dict, asset_id: str):
    try:
        json_metadata = json.dumps(meta_data)
        s3.Bucket(bucket_name).put_object(Key='group3/store_first/' + 'metadata/' + asset_id + '.json' , Body=json_metadata)

        logging.log(20, f'Metadata uploaded to S3 bucket {bucket_name}')

    except Exception as e:
        logging.log(20, f'Error uploading metadata to S3 bucket {bucket_name}: {e}')


def check_duplication_image(image_file: UploadFile, assetid: str) -> bool:
    try:
        bucket = s3.Bucket(bucket_name)
        images = list(bucket.objects.filter(Prefix='group3/store_first/' +  'image/'))

        for image in images:
            s3_object = image.get()

            if filecmp.cmp(image_file.file.read(), s3_object['Body'].read(), shallow=False):
                return False
        return True
    except Exception as e:
        print(f'Error checking dupelication image {assetid}: {e}')
        return False

def check_dupelication_asset_id(asset_id: str) -> bool:
    bucket = s3.Bucket(bucket_name)
    objects = list(bucket.objects.filter(Prefix='group3/store_first/' + asset_id + '/metadata.json'))

    if len(objects) != 1:
        return False

    logging.log(10, f'Found {len(objects)} dupelication images')
    return True


