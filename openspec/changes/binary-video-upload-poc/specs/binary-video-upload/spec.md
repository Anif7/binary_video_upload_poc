## ADDED Requirements

### Requirement: Accept multipart/form-data video uploads
The system SHALL provide a `POST /api/videos/upload` endpoint that accepts video files via `multipart/form-data`.

#### Scenario: Valid video upload
- **WHEN** client sends a valid `.mp4` file
- **THEN** system processes the upload successfully

### Requirement: Validate video formats
The system SHALL reject file uploads that are not `.mp4`, `.mov`, `.mkv`, or `.webm`.

#### Scenario: Invalid file format
- **WHEN** client sends a `.pdf` file
- **THEN** system returns a 400 Bad Request with an error message indicating unsupported format


### Requirement: Store in MinIO
The system SHALL upload accepted video files to a MinIO bucket under the path `videos/{asset_uuid}/{original_filename}`.

#### Scenario: Successful MinIO upload
- **WHEN** a valid video is received
- **THEN** system generates a unique `asset_uuid`, uploads to MinIO, and returns a JSON response containing `success`, `video_id`, `asset_uuid`, `object_path`, `original_filename`, `size`, and `mime_type`
