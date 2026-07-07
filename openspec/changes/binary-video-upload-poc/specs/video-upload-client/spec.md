## ADDED Requirements

### Requirement: Provide upload interface
The client SHALL provide an HTML interface with a file picker and an upload button.

#### Scenario: Select and upload file
- **WHEN** user selects a file and clicks upload
- **THEN** client initiates the two-step direct upload process

### Requirement: Initialize Upload
The client SHALL call the backend initialization API to get a pre-signed URL before uploading.

#### Scenario: Fetch pre-signed URL
- **WHEN** upload begins
- **THEN** client makes a POST request to `/api/videos/upload/init` with file metadata and receives the `upload_url`

### Requirement: Direct Upload with Progress
The client SHALL upload the file directly to the pre-signed URL and display a progress bar updating in real-time.

#### Scenario: Upload in progress
- **WHEN** client receives the `upload_url`
- **THEN** client makes a PUT request directly to MinIO and the progress bar visually indicates the percentage of bytes transferred

### Requirement: Confirm Upload
The client SHALL notify the backend once the direct upload to MinIO completes successfully.

#### Scenario: Notify backend
- **WHEN** the PUT request to MinIO returns a successful status (e.g., 200 OK)
- **THEN** client makes a POST request to `/api/videos/upload/confirm` to finalize the upload

### Requirement: Display upload result
The client SHALL display a success or error message upon completion of the entire upload attempt.

#### Scenario: Overall success
- **WHEN** the confirm endpoint returns a successful JSON response
- **THEN** client displays the response details and a success message

#### Scenario: Overall failure
- **WHEN** any step in the process (init, upload, or confirm) fails
- **THEN** client displays an appropriate error message
