from django.urls import path
from .views import VideoUploadInitView, VideoUploadConfirmView

urlpatterns = [
    path('videos/upload/init', VideoUploadInitView.as_view(), name='video-upload-init'),
    path('videos/upload/confirm', VideoUploadConfirmView.as_view(), name='video-upload-confirm'),
]
