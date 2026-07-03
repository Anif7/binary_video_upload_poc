## Context

We are building a Proof of Concept (POC) to demonstrate how a backend API can accept video files directly uploaded from a client and store them in object storage (MinIO) using an asset UUID. This helps in understanding binary upload flows as a foundation for services like TPStreams.

## Goals / Non-Goals

**Goals:**
- Implement a Django backend with a `POST /api/videos/upload` endpoint.
- Process `multipart/form-data` containing binary video files.
- Validate video file formats.
- Upload the file to an existing MinIO bucket using credentials from environment variables.
- Return structured JSON response with `asset_uuid`.
- Build a simple HTML/JS frontend to demonstrate the upload process with a progress bar.
- Provide curl and fetch examples.

**Non-Goals:**
- Production-ready deployment setup.
- Authentication/Authorization.
- Advanced video processing (transcoding, thumbnail generation).
- Direct-to-S3 client uploads (pre-signed URLs) - this POC specifically tests server-side handling of binary uploads.

## Decisions

- **Framework**: Django and Django REST Framework. DRF provides robust serialization and API view handling, simplifying the upload endpoint creation.
- **Storage**: MinIO, accessed via the `minio` Python SDK. We will use an already running MinIO instance configured via environment variables.
- **Frontend**: Plain HTML, CSS, and vanilla JavaScript using `XMLHttpRequest` to easily implement the upload progress bar (as `fetch` doesn't natively support upload progress yet).

## Risks / Trade-offs

- **Memory/Disk Usage**: Handling large binary uploads directly in Django requires reading the stream. Django handles this by streaming large files to temporary disk space. However, for a production environment, direct-to-cloud uploads (e.g., S3 pre-signed URLs) are preferred to avoid proxying large files through the app server. This POC will document this limitation and the path to adaptation.
