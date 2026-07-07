## 1. Environment Setup

- [x] 1.1 Initialize Django project (`django-admin startproject videopoc`)
- [x] 1.2 Create Django app for API (`python manage.py startapp app`)
- [x] 1.3 Configure Django settings (installed apps, DRF)
- [x] 1.4 Install dependencies (`django`, `djangorestframework`, `minio`, `python-dotenv`)
- [x] 1.5 Configure MinIO credentials and endpoint in environment variables

## 2. MinIO Integration (Direct Uploads)

- [x] 2.1 Create MinIO client utility to connect to existing MinIO instance using env vars
- [x] 2.2 Create utility function to generate a pre-signed PUT URL for an object
- [x] 2.3 Create utility function to verify if an object exists in MinIO (stat_object)
- [x] 2.4 Configure MinIO bucket CORS policy to allow uploads from the frontend

## 3. Backend Upload API

- [ ] 3.1 Create URL routing for `/api/videos/upload/init` and `/api/videos/upload/confirm`
- [ ] 3.2 Implement `init` APIView: Validate file extension, generate `asset_uuid`, and return pre-signed URL
- [ ] 3.3 Implement `confirm` APIView: Validate upload with MinIO stat_object and return success JSON

## 4. Frontend Client

- [ ] 4.1 Create HTML template with a file picker and upload button
- [ ] 4.2 Write JavaScript to fetch pre-signed URL from `/init` endpoint
- [ ] 4.3 Write JavaScript to perform `XMLHttpRequest` PUT directly to the MinIO URL with progress bar
- [ ] 4.4 Write JavaScript to call `/confirm` endpoint after successful PUT request
- [ ] 4.5 Display success response JSON or error message on completion

## 5. Documentation & Polish

- [ ] 5.1 Create `README.md` explaining the direct-to-object-storage upload flow (with diagram)
- [ ] 5.2 Add API testing examples (curl, fetch) to `README.md`
- [ ] 5.3 Ensure code is well-commented and clean
