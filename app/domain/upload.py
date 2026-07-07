import os
from app.models.video import VideoAsset, Status
from app.utils.minio_utils import generate_presigned_upload_url, check_object_exists

class VideoUploadService:
    ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.webm'}

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
    def init_upload(cls, filename: str) -> dict:
        cls.validate_extension(filename)
        
        asset = VideoAsset.objects.create(original_filename=filename)
        object_name = cls.get_object_name(asset)
        
        try:
            upload_url = generate_presigned_upload_url(object_name)
        except Exception as e:
            asset.status = Status.FAILED
            asset.save()
            raise Exception("Failed to generate upload URL") from e
            
        return {
            "asset_uuid": str(asset.id),
            "upload_url": upload_url,
            "object_name": object_name
        }

    @classmethod
    def handle_webhook(cls, payload: dict) -> dict:
        records = payload.get('Records', [])
        if not records:
            raise ValueError("No records in webhook payload")
            
        record = records[0]
        event_name = record.get('eventName', '')
        
        if not event_name.startswith('s3:ObjectCreated:'):
            # We only care about creation events
            return {"status": "ignored", "reason": f"Event {event_name} is not a creation event"}
            
        s3_data = record.get('s3', {})
        obj_data = s3_data.get('object', {})
        
        object_key = obj_data.get('key')
        size = obj_data.get('size')
        
        import urllib.parse
        
        if not object_key:
            raise ValueError("Missing object key in payload")
            
        object_key = urllib.parse.unquote(object_key)
            
        # Extract UUID from "videos/<uuid>.ext"
        # Example: "videos/123e4567-e89b-12d3-a456-426614174000.mp4"
        try:
            filename = object_key.split('/')[-1]
            asset_uuid = filename.split('.')[0]
        except IndexError:
            raise ValueError(f"Malformed object key: {object_key}")
            
        try:
            asset = VideoAsset.objects.get(id=asset_uuid)
        except VideoAsset.DoesNotExist:
            raise FileNotFoundError(f"VideoAsset with id {asset_uuid} not found")
            
        asset.status = Status.UPLOADED
        asset.size = size
        asset.save()
        
        return {
            "status": "processed",
            "asset_uuid": str(asset.id),
            "size": asset.size
        }
