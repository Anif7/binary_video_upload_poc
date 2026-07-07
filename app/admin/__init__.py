from django.contrib import admin
from app.models.video import VideoAsset

@admin.register(VideoAsset)
class VideoAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'status', 'size', 'created', 'modified')
    list_filter = ('status', 'created')
    search_fields = ('id', 'original_filename')
    readonly_fields = ('id', 'created', 'modified')
    ordering = ('-created',)
