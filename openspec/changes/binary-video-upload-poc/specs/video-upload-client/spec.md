## ADDED Requirements

### Requirement: Provide upload interface
The client SHALL provide an HTML interface with a file picker and an upload button.

#### Scenario: Select and upload file
- **WHEN** user selects a file and clicks upload
- **THEN** client initiates a `multipart/form-data` POST request to the backend API

### Requirement: Display upload progress
The client SHALL display a progress bar updating in real-time during the upload.

#### Scenario: Upload in progress
- **WHEN** a file is uploading
- **THEN** progress bar visually indicates the percentage of bytes transferred

### Requirement: Display upload result
The client SHALL display a success or error message upon completion of the upload attempt.

#### Scenario: Upload success
- **WHEN** the backend returns a successful JSON response
- **THEN** client displays the response details and a success message

#### Scenario: Upload failure
- **WHEN** the backend returns an error (e.g., 400 Bad Request)
- **THEN** client displays the error message provided by the backend
