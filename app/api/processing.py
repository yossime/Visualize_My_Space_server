import uuid
from fastapi import APIRouter, Form, HTTPException
from app.core.gcs import download_from_gcs, upload_to_gcs
from app.utils import process_image
from google.cloud import firestore

router = APIRouter()
firestore_client = firestore.Client()



@router.post("/process")
async def process_uploaded_image(file_id: str = Form(...), pergola_style: str = Form(...)):
    try:
        doc_ref = firestore_client.collection("images").document(file_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Image not found.")
        
        metadata = doc.to_dict()
        file_url = metadata.get("file_url")

        if not file_url:
            raise HTTPException(status_code=400, detail="File URL not found in metadata.")

        try:
            image_data = download_from_gcs(file_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download image from GCS: {str(e)}")

        try:
            processed_image = process_image(image_data, pergola_style)  
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

        processed_file_name = f"processed/{uuid.uuid4()}.png"
        
        try:
            processed_file_url = upload_to_gcs(processed_image, processed_file_name, "image/png")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload processed image to GCS: {str(e)}")

        doc_ref.update({"processed_file_url": processed_file_url})

        return {"message": "Image processed successfully", "processed_file_url": processed_file_url}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

