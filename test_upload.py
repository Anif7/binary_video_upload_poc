import os
import requests
import time
import sqlite3

class MultipartUploadClient:
    BASE_URL = "http://localhost:8000/api/videos"
    FILENAME = "test_video.mp4"
    FILE_SIZE = 10 * 1024 * 1024
    CHUNK_SIZE = 5 * 1024 * 1024

    def run(self):
        self._create_dummy_file()
        init_data = self._initiate_upload()
        parts_info = self._upload_parts(init_data["part_urls"])
        self._complete_upload(init_data["asset_uuid"], init_data["upload_id"], parts_info)
        self._poll_database(init_data["asset_uuid"])

    def _create_dummy_file(self):
        print(f"Creating dummy file {self.FILENAME} ({self.FILE_SIZE // 1024 // 1024}MB)...")
        with open(self.FILENAME, "wb") as f:
            f.write(os.urandom(self.FILE_SIZE))

    def _initiate_upload(self) -> dict:
        print("\n1. Calling /init endpoint...")
        response = requests.post(
            f"{self.BASE_URL}/upload/init", 
            json={"filename": self.FILENAME, "file_size": self.FILE_SIZE}
        )
        if response.status_code != 201:
            raise RuntimeError(f"Init failed: {response.text}")
        
        data = response.json()
        print(f"   Success! Asset UUID: {data['asset_uuid']}")
        return data

    def _upload_parts(self, part_urls: dict) -> list[dict]:
        print("\n2. Uploading parts to MinIO...")
        parts_info = []
        
        with open(self.FILENAME, "rb") as f:
            for part_number_str, part_url in part_urls.items():
                part_number = int(part_number_str)
                chunk = f.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                    
                etag = self._upload_chunk(part_number, part_url, chunk)
                parts_info.append({"PartNumber": part_number, "ETag": etag})
                
        return parts_info

    def _upload_chunk(self, part_number: int, url: str, data: bytes) -> str:
        print(f"   Uploading part {part_number}...")
        start_time = time.time()
        
        response = requests.put(url, data=data)
        if response.status_code != 200:
            raise RuntimeError(f"Part {part_number} upload failed: {response.text}")
            
        etag = response.headers.get("ETag")
        print(f"   Success! Part {part_number} uploaded in {time.time() - start_time:.2f} seconds.")
        return etag

    def _complete_upload(self, asset_uuid: str, upload_id: str, parts: list[dict]):
        print("\n3. Calling /complete endpoint...")
        response = requests.post(
            f"{self.BASE_URL}/upload/{asset_uuid}/complete", 
            json={"upload_id": upload_id, "parts": parts}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Complete failed: {response.text}")
        print("   Success! Upload completed.")

    def _poll_database(self, asset_uuid: str):
        print("\n4. Waiting for MinIO Webhook to process...")
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        uuid_str = asset_uuid.replace('-', '')
        
        for _ in range(15):
            cursor.execute("SELECT status, size FROM app_videoasset WHERE id=?", (uuid_str,))
            row = cursor.fetchone()
            
            if row:
                if row[0] == 1:
                    print(f"   Success! Webhook received. Size is {row[1]} bytes.")
                    return
                elif row[0] == 2:
                    raise RuntimeError("   Failed! Webhook marked asset as FAILED.")
                else:
                    print(f"   Waiting... current status: Initialized")
            else:
                print("   Asset not found in database yet.")
                
            time.sleep(2)
            
        raise TimeoutError("Webhook was not received in time.")

if __name__ == "__main__":
    client = MultipartUploadClient()
    try:
        client.run()
    except Exception as e:
        print(f"Error: {e}")
