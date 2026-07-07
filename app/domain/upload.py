import os
import math
import urllib.parse
from app.models.video import VideoAsset, Status
from app.utils.minio_utils import create_multipart_upload, generate_presigned_part_url, complete_multipart_upload

class VideoUploadService:
    ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.webm'}
    CHUNK_SIZE = 5 * 1024 * 1024

    @classmethod
    def validate_extension(cls, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        if ext.lower() not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(f"Invalid extension. Allowed: {cls.ALLOWED_EXTENSIONS}")
        return ext.lower()

    @classmethod
    def get_object_name(cls, asset: VideoAsset) -> str:
        _, ext = os.path.splitext(asset.original_filename)
        return f"videos/{asset.id}{ext.lower()}"

    @classmethod
    def init_upload(cls, filename: str, file_size: int) -> dict:
        cls.validate_extension(filename)
        
        asset = VideoAsset.objects.create(original_filename=filename)
        object_name = cls.get_object_name(asset)
        
        try:
            upload_id = create_multipart_upload(object_name)
            part_urls = cls._generate_part_urls(object_name, upload_id, file_size)
        except Exception as e:
            asset.status = Status.FAILED
            asset.save()
            raise Exception("Failed to initialize multipart upload") from e
            
        return {
            "asset_uuid": str(asset.id),
            "upload_id": upload_id,
            "part_urls": part_urls,
            "object_name": object_name
        }

    @classmethod
    def _generate_part_urls(cls, object_name: str, upload_id: str, file_size: int) -> dict:
        num_parts = math.ceil(file_size / cls.CHUNK_SIZE) if file_size > 0 else 1
        return {
            i: generate_presigned_part_url(object_name, upload_id, i)
            for i in range(1, num_parts + 1)
        }

    @classmethod
    def complete_upload(cls, asset: VideoAsset, upload_id: str, parts: list) -> dict:
        object_name = cls.get_object_name(asset)
        try:
            complete_multipart_upload(object_name, upload_id, parts)
        except Exception as e:
            raise Exception(f"Failed to stitch chunks in MinIO: {e}") from e
            
        return {"status": "Complete signal sent to MinIO. Awaiting Webhook..."}

    @classmethod
    def handle_webhook(cls, payload: dict) -> dict:
        event_name, object_key, size = cls._extract_event_data(payload)
        
        if not event_name.startswith('s3:ObjectCreated:'):
            return {"status": "ignored", "reason": f"Event {event_name} is not a creation event"}
            
        asset_uuid = cls._parse_uuid_from_key(object_key)
        asset = cls._update_asset(asset_uuid, size)
        
        return {
            "status": "processed",
            "asset_uuid": str(asset.id),
            "size": asset.size
        }

    @classmethod
    def _extract_event_data(cls, payload: dict) -> tuple[str, str, int]:
        records = payload.get('Records', [])
        if not records:
            raise ValueError("No records in webhook payload")
            
        record = records[0]
        event_name = record.get('eventName', '')
        obj_data = record.get('s3', {}).get('object', {})
        
        object_key = obj_data.get('key')
        if not object_key:
            raise ValueError("Missing object key in payload")
            
        object_key = urllib.parse.unquote(object_key)
        size = obj_data.get('size', 0)
        
        return event_name, object_key, size

    @classmethod
    def _parse_uuid_from_key(cls, object_key: str) -> str:
        try:
            filename = object_key.split('/')[-1]
            return filename.split('.')[0]
        except IndexError:
            raise ValueError(f"Malformed object key: {object_key}")

    @classmethod
    def _update_asset(cls, asset_uuid: str, size: int) -> VideoAsset:
        try:
            asset = VideoAsset.objects.get(id=asset_uuid)
        except VideoAsset.DoesNotExist:
            raise FileNotFoundError(f"VideoAsset with id {asset_uuid} not found")
            
        asset.status = Status.UPLOADED
        asset.size = size
        asset.save()
        return asset
