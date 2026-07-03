## Why

To understand how direct binary uploads work and how a service like TPStreams could expose a Server API for video uploads. The goal is to demonstrate how a backend API can accept a video file uploaded directly from a client via `multipart/form-data` and store it in a local MinIO object storage using an asset UUID.

## What Changes

- Create a simple backend application using Django and Django REST Framework (Python).
- Create a `POST /api/videos/upload` endpoint that accepts video files via `multipart/form-data`.
- Integrate MinIO Python SDK to save uploaded files directly to MinIO using paths like `videos/{asset_uuid}/{original_filename}`.
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
