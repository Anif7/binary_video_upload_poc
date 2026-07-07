from django.urls import path
from .views import VideoUploadInitView, VideoUploadCompleteView, MinIOWebhookView

urlpatterns = [
    path('videos/upload/init', VideoUploadInitView.as_view(), name='video-upload-init'),
    path('videos/upload/<uuid:asset_id>/complete', VideoUploadCompleteView.as_view(), name='video-upload-complete'),
    path('videos/webhook/minio', MinIOWebhookView.as_view(), name='video-upload-webhook'),
]
