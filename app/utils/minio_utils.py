from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_minio_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_SSL
    )

def generate_presigned_upload_url(object_name: str, expiry_minutes: int = 60) -> str:
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME
    
    try:
        url = client.presigned_put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(minutes=expiry_minutes)
        )
        return url
    except S3Error as e:
        logger.error(f"Failed to generate presigned URL: {e}")
        raise e

def check_object_exists(object_name: str):
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME
    
    try:
        stat = client.stat_object(bucket_name, object_name)
        return {
            'exists': True,
            'size': stat.size,
            'content_type': stat.content_type
        }
    except S3Error as e:
        if e.code == "NoSuchKey":
            return {'exists': False}
        logger.error(f"Failed to check object status in MinIO: {e}")
        raise e

