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
