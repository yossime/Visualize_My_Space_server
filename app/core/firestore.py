
from google.cloud import firestore
from fastapi import HTTPException

firestore_client = firestore.Client()

def get_image_metadata(file_id: str):
    try:
        doc_ref = firestore_client.collection("images").document(file_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Image not found.")
        return doc.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to access Firestore: {str(e)}")
