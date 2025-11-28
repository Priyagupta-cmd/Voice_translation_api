from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Voice reporting for Vox Maati",
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import router
from app.api.v1.endpoints import voice_issues

# Include router
app.include_router(
    voice_issues.router,
    prefix="/api/v1",
    tags=["voice-issues"]
)

@app.get("/")
def root():
    return {
        "message": "Vox Maati Voice API",
        "status": "active",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "project_id": settings.GCP_PROJECT_ID,
        "bucket": settings.GCS_BUCKET_NAME,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "vox-maati-voice-api",
        "gcp_configured": settings.GCP_PROJECT_ID != "your-project-id"
    }

@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.APP_NAME} starting...")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"☁️  GCP Project: {settings.GCP_PROJECT_ID}")
    print(f"📦 GCS Bucket: {settings.GCS_BUCKET_NAME}")
    print(f"📚 API Docs: http://127.0.0.1:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Shutting down...")
