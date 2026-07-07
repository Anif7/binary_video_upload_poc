import sys
import requests
import time
import os
import django

# Setup Django ORM to verify database state
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videopoc.settings')
django.setup()
from app.models.video import VideoAsset, Status

BASE_URL = "http://localhost:8000/api/videos/upload"
TEST_FILE = "test_video.mp4"

def main():
    _create_dummy_video()
    
    asset_uuid, upload_url = _initiate_upload()
    _upload_to_storage(upload_url)
    
    print("\n3. Waiting for MinIO Webhook to process...")
    _verify_upload_status(asset_uuid)
    
    print("\nDirect-to-Object-Storage Upload Flow Complete! 🎉")

def _initiate_upload() -> tuple[str, str]:
    print("1. Calling /init endpoint...")
    response = requests.post(f"{BASE_URL}/init", json={"filename": TEST_FILE})
    
    if response.status_code != 201:
        print(f"Init failed: {response.status_code} - {response.text}")
        sys.exit(1)
        
    data = response.json()
    print(f"   Success! Asset UUID: {data['asset_uuid']}")
    return data['asset_uuid'], data['upload_url']

def _upload_to_storage(upload_url: str):
    print("\n2. Uploading file directly to MinIO using pre-signed URL...")
    start_time = time.time()
    
    with open(TEST_FILE, 'rb') as f:
        response = requests.put(upload_url, data=f)
        
    if response.status_code != 200:
        print(f"Upload failed: {response.status_code} - {response.text}")
        sys.exit(1)
        
    duration = time.time() - start_time
    print(f"   Success! Uploaded in {duration:.2f} seconds.")

def _verify_upload_status(asset_uuid: str):
    max_retries = 10
    for i in range(max_retries):
        time.sleep(1)
        # Refresh from database
        asset = VideoAsset.objects.get(id=asset_uuid)
        if asset.status == Status.UPLOADED:
            print(f"   Success! Webhook received. Asset size updated to: {asset.size} bytes")
            return
        print(f"   Waiting... current status: {asset.get_status_display()}")
        
    print("Error: Webhook was not received in time.")
    sys.exit(1)

def _create_dummy_video():
    if not os.path.exists(TEST_FILE):
        print(f"Creating dummy file {TEST_FILE} (10MB)...")
        with open(TEST_FILE, "wb") as f:
            f.write(os.urandom(10 * 1024 * 1024))

if __name__ == "__main__":
    main()
