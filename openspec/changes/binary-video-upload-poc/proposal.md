## Why

To understand how direct binary uploads work and how a service like TPStreams could expose a Server API for video uploads. The goal is to demonstrate a **direct-to-object-storage architecture** where a backend API generates a pre-signed URL, and the client uploads the video directly to MinIO, bypassing the backend server completely.

## What Changes

- Create a simple backend application using Django and Django REST Framework (Python).
- Create a `POST /api/videos/upload/init` endpoint that generates an `asset_uuid` and returns a MinIO pre-signed PUT URL.
- Create a `POST /api/videos/upload/confirm` endpoint to verify the upload was successful.
- Integrate MinIO Python SDK to generate pre-signed URLs and verify object existence.
- Implement validation for file types (`.mp4`, `.mov`, `.mkv`, `.webm`).
- Return a JSON response with upload details.
- Create a simple HTML client with a file picker, upload button, progress bar, and success/error message.
- Provide API testing examples and document the binary upload workflow.

## Capabilities

### New Capabilities
- `binary-video-upload`: A backend capability to receive and store binary video files to MinIO object storage.
- `video-upload-client`: A simple HTML frontend client to demonstrate the video upload with a progress bar.

### Modified Capabilities

## Impact

- New Django project setup with Django REST Framework.
- Existing MinIO service credentials configured via environment variables.
- New API endpoints and static HTML file.
