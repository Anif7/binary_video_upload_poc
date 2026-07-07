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

## 3. Database Models

- [x] 3.1 Create `VideoAsset` model with `id` (UUID), `original_filename`, `status`, and `size`
- [x] 3.2 Create and run database migrations

## 4. Backend Upload API

- [x] 4.1 Create URL routing for `/api/videos/upload/init` and `/api/videos/upload/confirm`
- [x] 4.2 Implement `init` APIView: Validate extension, create `VideoAsset(status=INIT)`, and return pre-signed URL
- [x] 4.3 Implement `confirm` APIView: Validate upload with MinIO stat_object, update `VideoAsset(status=UPLOADED)`, and return success JSON

## 5. Testing (Python Script)

- [ ] 5.1 Write `test_upload.py` to call `/init` endpoint, extract upload URL, perform `PUT` to MinIO, and call `/confirm`

## 6. Documentation & Polish

- [ ] 6.1 Create `README.md` explaining the direct-to-object-storage upload flow (with diagram)
- [ ] 6.2 Add API testing examples (curl, fetch) to `README.md`
- [ ] 6.3 Ensure code is well-commented and clean
