import uuid
from fastapi import APIRouter, UploadFile, HTTPException
from google.cloud import firestore
from app.core.gcs import upload_to_gcs

router = APIRouter()
firestore_client = firestore.Client()

@router.post("/upload")
async def upload_image(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file format.")
    
    try:
        file_data = await file.read()
        
        file_name = f"uploads/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        
        file_url = upload_to_gcs(file_data, file_name, file.content_type)

        doc_ref = firestore_client.collection("images").document()
        doc_ref.set({
            "file_name": file_name,
            "file_url": file_url,
            "file_format": file.content_type  
        })

        return {"message": "File uploaded successfully", "file_url": file_url, "file_id": doc_ref.id}
    
    except Exception as e:
        print(f"Error in upload: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

