from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.uploads import router as uploads_router
from app.api.processing import router as processing_router
from app.api.download import router as download_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads_router)
app.include_router(processing_router)
app.include_router(download_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
