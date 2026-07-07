from django.urls import path
from .views import VideoUploadInitView, MinIOWebhookView

urlpatterns = [
    path('videos/upload/init', VideoUploadInitView.as_view(), name='video-upload-init'),
    path('videos/webhook/minio', MinIOWebhookView.as_view(), name='video-upload-webhook'),
]
