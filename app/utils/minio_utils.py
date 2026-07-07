from django.conf import settings
import boto3
from botocore.client import Config
import logging

logger = logging.getLogger(__name__)

def get_s3_client():
    protocol = "https" if settings.MINIO_USE_SSL else "http"
    endpoint_url = f"{protocol}://{settings.MINIO_ENDPOINT}"
    
    return boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1' # Default for MinIO
    )

def create_multipart_upload(object_name: str) -> str:
    client = get_s3_client()
    try:
        response = client.create_multipart_upload(
            Bucket=settings.MINIO_BUCKET_NAME,
            Key=object_name
        )
        return response['UploadId']
    except Exception as e:
        logger.error(f"Failed to create multipart upload: {e}")
        raise

def generate_presigned_part_url(object_name: str, upload_id: str, part_number: int, expiry_minutes: int = 60) -> str:
    client = get_s3_client()
    try:
        url = client.generate_presigned_url(
            ClientMethod='upload_part',
            Params={
                'Bucket': settings.MINIO_BUCKET_NAME,
                'Key': object_name,
                'UploadId': upload_id,
                'PartNumber': part_number
            },
            ExpiresIn=expiry_minutes * 60
        )
        return url
    except Exception as e:
        logger.error(f"Failed to generate presigned URL for part {part_number}: {e}")
        raise

def complete_multipart_upload(object_name: str, upload_id: str, parts: list[dict]):
    """
    parts: [{'ETag': '...', 'PartNumber': 1}, ...]
    """
    client = get_s3_client()
    try:
        response = client.complete_multipart_upload(
            Bucket=settings.MINIO_BUCKET_NAME,
            Key=object_name,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        return response
    except Exception as e:
        logger.error(f"Failed to complete multipart upload: {e}")
        raise

def check_object_exists(object_name: str):
    client = get_s3_client()
    try:
        response = client.head_object(
            Bucket=settings.MINIO_BUCKET_NAME,
            Key=object_name
        )
        return {
            'exists': True,
            'size': response['ContentLength'],
            'content_type': response['ContentType']
        }
    except Exception as e:
        if hasattr(e, 'response') and e.response.get('Error', {}).get('Code') == '404':
            return {'exists': False}
        logger.error(f"Failed to check object status: {e}")
        raise
