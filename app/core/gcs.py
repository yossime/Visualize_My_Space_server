from google.cloud import storage
import uuid

from app.core.config import GCS_BUCKET_NAME

def upload_to_gcs(file_data, file_name, content_type):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_data, content_type=content_type)
    return blob.public_url



def download_from_gcs(file_url):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        file_name = '/'.join(file_url.split('/')[4:])  
        blob = bucket.blob(file_name)
        return blob.download_as_bytes()
    except Exception as e:
        print(f"Error downloading file from GCS: {e}")
        return None
