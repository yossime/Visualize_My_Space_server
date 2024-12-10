from app.api.uploads import router as uploads_router
from app.api.processing import router as processing_router
from app.api.download import router as download_router
from app.main import app

app.include_router(uploads_router)
app.include_router(processing_router)
app.include_router(download_router)
