from fastapi import APIRouter, HTTPException
from fastapi.responses import  StreamingResponse
from app.core.firestore import get_image_metadata
from app.core.gcs import download_from_gcs
from google.cloud import firestore
from io import BytesIO

router = APIRouter()
firestore_client = firestore.Client()

@router.get("/image/{file_id}/original")
async def download_original_image(file_id: str):
    try:
        metadata = get_image_metadata(file_id)
        
        original_file_url = metadata.get("file_url")
        if not original_file_url:
            raise HTTPException(status_code=400, detail="Original image not found.")
        
        image_data = download_from_gcs(original_file_url)
        if not image_data:
            raise HTTPException(status_code=500, detail="Failed to download original image.")
        
        content_type = metadata.get("file_format", "image/jpeg")  
        return StreamingResponse(BytesIO(image_data), media_type=content_type)
    except Exception as e:
        print(f"Error in /image/{file_id}/processed: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Failed to get file: {str(e)}")



@router.get("/image/{file_id}/processed")
async def download_processed_image(file_id: str):
    try:
        metadata = get_image_metadata(file_id)
        
        processed_file_url = metadata.get("processed_file_url")
        if not processed_file_url:
            raise HTTPException(status_code=400, detail="Processed image not found.")
        
        image_data = download_from_gcs(processed_file_url)
        if not image_data:
            raise HTTPException(status_code=500, detail="Failed to download processed image.")
        
        content_type = metadata.get("processed_file_format", "image/png") 
        return StreamingResponse(BytesIO(image_data), media_type=content_type)
    
    except Exception as e:
        print(f"Error in /image/{file_id}/processed: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Failed to get file: {str(e)}")

