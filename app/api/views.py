from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models.video import VideoAsset
from app.domain.upload import VideoUploadService

class VideoUploadInitView(APIView):
    def post(self, request):
        filename = request.data.get('filename')
        file_size = request.data.get('file_size')
        
        if not filename or file_size is None:
            return Response({"error": "filename and file_size are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file_size = int(file_size)
            result = VideoUploadService.init_upload(filename, file_size)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoUploadCompleteView(APIView):
    def post(self, request, asset_id):
        upload_id = request.data.get('upload_id')
        parts = request.data.get('parts')
        
        if not upload_id or not parts:
            return Response({"error": "upload_id and parts are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        asset = get_object_or_404(VideoAsset, id=asset_id)
        
        try:
            result = VideoUploadService.complete_upload(asset, upload_id, parts)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MinIOWebhookView(APIView):
    def post(self, request):
        try:
            # MinIO webhooks usually have 'Records' list
            result = VideoUploadService.handle_webhook(request.data)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": "Failed to process webhook", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
