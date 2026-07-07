import os
from app.models.video import VideoAsset
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
            asset.status = VideoAsset.Status.FAILED
            asset.save()
            raise Exception("Failed to generate upload URL") from e
            
        return {
            "asset_uuid": str(asset.id),
            "upload_url": upload_url,
            "object_name": object_name
        }

    @classmethod
    def confirm_upload(cls, asset: VideoAsset) -> dict:
        object_name = cls.get_object_name(asset)
        stat_info = check_object_exists(object_name)
            
        if not stat_info.get('exists'):
            raise FileNotFoundError("File not found in MinIO")
            
        asset.status = VideoAsset.Status.UPLOADED
        asset.size = stat_info.get('size')
        asset.save()
        
        return {
            "message": "Upload confirmed",
            "asset_uuid": str(asset.id),
            "size": asset.size,
            "status": asset.get_status_display()
        }
