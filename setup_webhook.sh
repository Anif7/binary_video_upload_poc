#!/bin/bash

# Auto-detect the machine's local IP address (works on Linux/WSL/macOS)
HOST_IP=$(hostname -I | awk '{print $1}')
# If for some reason it fails, fallback to a provided argument or localhost
HOST_IP=${HOST_IP:-127.0.0.1}

MINIO_ALIAS="myminio"
WEBHOOK_ENDPOINT="http://${HOST_IP}:8000/api/videos/webhook/minio"
BUCKET_NAME="streams"

echo "=========================================="
echo "Setting up MinIO Webhook Configuration"
echo "=========================================="
echo "Assuming MinIO Client (mc) is configured with alias: $MINIO_ALIAS"
echo "Webhook Endpoint: $WEBHOOK_ENDPOINT"
echo "Bucket: $BUCKET_NAME"
echo "------------------------------------------"

# 1. Set the webhook configuration
echo "1. Configuring webhook target..."
mc admin config set $MINIO_ALIAS notify_webhook:1 endpoint="$WEBHOOK_ENDPOINT"

# 2. Restart MinIO service
echo "2. Restarting MinIO to apply config..."
mc admin service restart $MINIO_ALIAS

echo "Waiting for MinIO to restart..."
sleep 5

# 3. Add the event to the bucket (listening only to PUT events under 'videos/' prefix)
echo "3. Subscribing bucket to webhook event..."
mc event add $MINIO_ALIAS/$BUCKET_NAME/videos arn:minio:sqs::1:webhook --event put

echo "=========================================="
echo "Done! MinIO will now notify Django when a video is uploaded."
