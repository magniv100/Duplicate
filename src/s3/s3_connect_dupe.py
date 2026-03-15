import base64
import filecmp
import io
import os
from encodings.utf_8_sig import encode
from sys import prefix
from tokenize import group
import json
import boto3
from botocore.client import Config, logger
from botocore.exceptions import ClientError
from fastapi import UploadFile
import logging
access_key = ''
secret_key = ''
bucket_name =''


s3 = boto3.resource('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)


def upload_to_s3(meta_data: dict, source_path):
    logger.info(f'start uploading files to S3 bucket {bucket_name}')
    try:
        asset_id = meta_data['asset_id']
        if os.path.isfile(source_path):
            if check_dupelication_asset_id(meta_data):
                print(f'Asset {asset_id} already exists in bucket {bucket_name}')
                logger.info(f'Asset {asset_id} already exists in bucket {bucket_name}')
                return False
            else:
                upload_image(source_path, asset_id)
                upload_metadata(meta_data, asset_id)
                return True
        else:
            print(f'Invalid source path: {source_path}')
            return False
    except Exception as e:
        print(f'Error uploading files to S3 bucket {bucket_name}: {e}')
        return False

def upload_image(image: UploadFile, asset_id):
    try:
        #filename = str(image).split('\\')[-1]
        image_type = str(image).split('.')[-1]
        with open(image, 'rb') as data:
            s3.Bucket(bucket_name).put_object(Key='group3/store_first/' +  'image/' + asset_id + '.' + image_type,Body=data)
        logger.info(f'Image {asset_id} uploaded to S3 bucket {bucket_name}')
        print(f'File {image} uploaded to S3 bucket {bucket_name}')
    except Exception as e:
        logger.info(f'Error uploading files to S3 bucket {bucket_name}: {e}')
        print(f'Error uploading files to S3 bucket {bucket_name}: {e}')

def upload_metadata(meta_data: dict, asset_id):
    try:
        json_metadata = json.dumps(meta_data)
        print("🦐")
        s3.Bucket(bucket_name).put_object(Key='group3/store_first/' + 'metadata/' + asset_id + '.json' , Body=json_metadata)
        logger.info(f'Metadata uploaded to S3 bucket {bucket_name}')
        print(f'File {meta_data} uploaded to S3 bucket {bucket_name}')
    except Exception as e:
        logger.info(f'Error uploading metadata to S3 bucket {bucket_name}: {e}')
        print(f'Error uploading files to S3 bucket {bucket_name}: {e}')

def get_image_from_s3(asset_id):
    try:
        bucket = s3.Bucket(bucket_name)
        objects = list(bucket.objects.filter(Prefix='group3/store_first/' +  'image/' + asset_id ))
        if not objects:
            logger.info(f'Object {asset_id} does not exist in bucket {bucket_name}')
            print(f'Object {asset_id} does not exist in bucket {bucket_name}')
            return None
        image: s3.ObjectSummary = objects[0]
        return image
    except Exception as e:
        logger.info(f'Error getting object from S3 bucket {bucket_name}: {e}')
        print(f'Error getting object from S3 bucket {bucket_name}: {e}')
        return None

def get_metadata_from_s3(asset_id):
    try:
        bucket = s3.Bucket(bucket_name)
        objects = list(bucket.objects.filter(Prefix='group3/store_first/' + asset_id + '/metadata.json'))
        if not objects:
            logger.info(f'Object {asset_id} does not exist in bucket {bucket_name}')
            print(f'Object {asset_id} does not exist in bucket {bucket_name}')
            return None
        obj = objects[0]
        return obj
    except Exception as e:
        logger.info(f'Error getting object from S3 bucket {bucket_name}: {e}')
        print(f'Error getting object from S3 bucket {bucket_name}: {e}')
        return None

#todo do it just iterate over all the images
def check_dupelication_image(image_req: s3.ObjectSummary):
    try:
        bucket = s3.Bucket(bucket_name)
        images = list(bucket.objects.filter(Prefix='group3/store_first/' +  'image/'))

        for image in images:
            s3_object = image.get()
            image_req_object = image_req.get()
            # The 'Body' is a StreamingBody object that can be read

            content = s3_object['Body'].read()
            image_file = io.BytesIO(content)
            print(image_file)
            print(s3_object['Body'].read())
            if filecmp.cmp(image_req_object['Body'].read(), s3_object['Body'].read(), shallow=False):
                print("yas")
                return True
            else:
                print("nahh")
                return False
    except Exception as e:
        print(f'Error checking dupelication image {image_req}: {e}')

def check_dupelication_asset_id(metadata: dict) -> bool:
    bucket = s3.Bucket(bucket_name)
    objects = list(bucket.objects.filter(Prefix='group3/store_first/' + metadata["asset_id"] + '/metadata.json'))
    logger.info(f'Found {len(objects)} dupelication images')
    return objects


def main():
    meta_data: dict= {
        "asset_id": "550e8400-e29b-41d4-a716-446655440052",
        "asset_type": "Artistic Photograph",
        "object_details": {
            "title": "Urban Solitude",
            "artist": "Elena Rossi",
        },
        "capture_gps": {
            "type": "Sensor Location (Point)",
            "latitude": 48.8640,
            "longitude": 2.3250
        },
        "digital_capture":
        {
            "photographer": "Elena Rossi"
        }
    }
    #print(get_image_from_s3('550e8400-e29b-41d4-a716-446655440000'))
    #print(get_metadata_from_s3('550e8400-e29b-41d4-a716-446655440000'))
    #print(get_image_from_s3('550e8400-e29b-41d4-a716-446655440000'))
    #print(check_dupelication_image(get_image_from_s3('550e8400-e29b-41d4-a716-446655440000')))
    #print(check_dupelication_asset_id(meta_data))
    print(upload_to_s3(meta_data, source_path=r"C:\Users\niviw\Desktop\matmonRemote\projects\monalist\Duplicate\src\s3\slime.jpeg"))


if __name__ == "__main__":
    main()

