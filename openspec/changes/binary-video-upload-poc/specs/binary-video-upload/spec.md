## ADDED Requirements

### Requirement: Initialize Upload
The system SHALL provide a `POST /api/videos/upload/init` endpoint that generates a pre-signed URL for direct client upload to MinIO.

#### Scenario: Valid initialization
- **WHEN** client sends a request with a valid `.mp4` filename and content type
- **THEN** system generates an `asset_uuid`, creates a `VideoAsset` with status `INIT`, and returns a JSON response containing `asset_uuid` and the `upload_url` (pre-signed PUT URL)

### Requirement: Validate video formats during initialization
The system SHALL reject initialization requests for file extensions that are not `.mp4`, `.mov`, `.mkv`, or `.webm`.

#### Scenario: Invalid file format
- **WHEN** client attempts to initialize upload for a `.pdf` file
- **THEN** system returns a 400 Bad Request with an error message indicating unsupported format

### Requirement: Webhook Confirmation
The system SHALL provide a `POST /api/videos/webhook/minio` endpoint that receives bucket notifications directly from MinIO when an object is uploaded.

#### Scenario: Successful upload notification
- **WHEN** MinIO successfully receives a file and triggers a webhook with `s3:ObjectCreated:*`
- **THEN** system parses the payload to extract the `object_name`, finds the corresponding `VideoAsset`, updates its size, and marks its status as `UPLOADED`.

#### Scenario: Invalid webhook
- **WHEN** MinIO (or a malicious client) sends a webhook payload that cannot be parsed
- **THEN** system returns a 400 Bad Request error.
