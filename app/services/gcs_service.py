from google.cloud import storage
from app.core.config import get_settings
from datetime import timedelta

settings = get_settings()

class GCSService:
    """Google Cloud Storage service"""

    def __init__(self):
        # Use application default credentials set up by gcloud auth
        self.client = storage.Client(project=settings.GCP_PROJECT_ID)
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)
        print(f"✅ GCS Service initialized: {settings.GCS_BUCKET_NAME}")

    
    def upload_audio(self, file_content: bytes, destination_path: str) -> str:
        """Upload audio file to GCS"""
        try:
            blob = self.bucket.blob(destination_path)
            
            blob.upload_from_string(
                file_content,
                content_type="audio/mpeg",
                timeout=60
            )
            
            print(f"✅ Uploaded: {destination_path}")
            
            gcs_uri = f"gs://{settings.GCS_BUCKET_NAME}/{destination_path}"
            return gcs_uri
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def get_signed_url(self, gcs_uri: str, expiration_hours: int = 1) -> str:
        """Generate signed URL for file access"""
        try:
            path = gcs_uri.replace(f"gs://{settings.GCS_BUCKET_NAME}/", "")
            blob = self.bucket.blob(path)
            
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expiration_hours),
                method="GET"
            )
            
            return url
            
        except Exception as e:
            print(f"❌ Failed to generate signed URL: {e}")
            raise
    
    def delete_file(self, gcs_uri: str) -> bool:
        """Delete file from GCS"""
        try:
            path = gcs_uri.replace(f"gs://{settings.GCS_BUCKET_NAME}/", "")
            blob = self.bucket.blob(path)
            blob.delete()
            print(f"✅ Deleted: {path}")
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
