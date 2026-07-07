from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models.video import VideoAsset
from app.domain.upload import VideoUploadService

class VideoUploadInitView(APIView):
    def post(self, request):
        filename = request.data.get('filename')
        if not filename:
            return Response({"error": "filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = VideoUploadService.init_upload(filename)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoUploadConfirmView(APIView):
    def post(self, request):
        asset_uuid = request.data.get('asset_uuid')
        if not asset_uuid:
            return Response({"error": "asset_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        asset = get_object_or_404(VideoAsset, id=asset_uuid)
        
        try:
            result = VideoUploadService.confirm_upload(asset)
            return Response(result, status=status.HTTP_200_OK)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to verify object with MinIO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
