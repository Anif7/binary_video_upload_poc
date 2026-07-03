## 1. Environment Setup

- [x] 1.1 Initialize Django project (`django-admin startproject videopoc`)
- [x] 1.2 Create Django app for API (`python manage.py startapp app`)
- [x] 1.3 Configure Django settings (installed apps, DRF)
- [x] 1.4 Install dependencies (`django`, `djangorestframework`, `minio`, `python-dotenv`)
- [ ] 1.5 Configure MinIO credentials and endpoint in environment variables

## 2. MinIO Integration

- [ ] 2.1 Create MinIO client utility to connect to existing MinIO instance using env vars
- [ ] 2.2 Create utility function to ensure upload bucket exists
- [ ] 2.3 Create utility function to upload a file to MinIO and return the object path

## 3. Backend Upload API

- [ ] 3.1 Create URL routing for `POST /api/videos/upload`
- [ ] 3.2 Implement DRF `APIView` to accept `multipart/form-data` request
- [ ] 3.3 Add validation for file extensions (mp4, mov, mkv, webm)
- [ ] 3.4 Generate `asset_uuid` and trigger MinIO upload utility
- [ ] 3.5 Construct and return the JSON response format

## 4. Frontend Client

- [ ] 4.1 Create HTML template with a file picker and upload button
- [ ] 4.2 Add UI element for upload progress bar
- [ ] 4.3 Write JavaScript to handle file selection and `XMLHttpRequest` for upload
- [ ] 4.4 Implement `progress` event listener to update the progress bar UI
- [ ] 4.5 Display success response JSON or error message on completion

## 5. Documentation & Polish

- [ ] 5.1 Create `README.md` explaining the binary upload flow (with diagram)
- [ ] 5.2 Add API testing examples (curl, fetch, requests, Postman) to `README.md`
- [ ] 5.3 Ensure code is well-commented and clean
