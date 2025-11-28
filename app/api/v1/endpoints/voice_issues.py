from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.gcs_service import GCSService
from app.models.models import AudioFile
from app.core.config import get_settings
from pydub import AudioSegment
from datetime import datetime
import uuid
import io
import whisper
from googletrans import Translator
import tempfile
import os

router = APIRouter()
settings = get_settings()
ALLOWED_FORMATS = ["audio/wav", "audio/mpeg", "audio/mp3", "audio/x-wav"]

async def validate_audio_file(file: UploadFile) -> dict:
    """Validate audio file"""
    if file.content_type not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format. Supported: WAV, MP3. Got: {file.content_type}"
        )

    content = await file.read()
    await file.seek(0)
    file_size = len(content)
    max_size = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max: {settings.MAX_AUDIO_SIZE_MB}MB"
        )

    try:
        audio = AudioSegment.from_file(io.BytesIO(content))
        duration_seconds = len(audio) / 1000.0
        if duration_seconds > settings.MAX_AUDIO_DURATION:
            raise HTTPException(
                status_code=400,
                detail=f"Audio too long. Max: {settings.MAX_AUDIO_DURATION}s"
            )
        return {
            "duration": duration_seconds,
            "file_size": file_size,
            "content": content  # keep audio bytes for transcription
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio file: {str(e)}"
        )

def transcribe_audio_bytes(audio_bytes, file_extension):
    # Save audio to a temporary file for Whisper (expects filepath)
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        model = whisper.load_model("base")
        result = model.transcribe(tmp_path)
        transcript = result['text']
    finally:
        os.remove(tmp_path)
    return transcript

def translate_text_to_english(text):
    translator = Translator()
    translated = translator.translate(text, src='auto', dest='en')
    return translated.text

@router.post("/issues/voice/upload")
async def upload_voice_issue(
    file: UploadFile = File(...),
    category: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload voice recording, transcribe, translate"""
    validation = await validate_audio_file(file)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "mp3"
    filename = f"{timestamp}_{unique_id}.{file_extension}"
    date_folder = datetime.utcnow().strftime("%Y%m%d")
    gcs_path = f"audio/{date_folder}/{filename}"

    try:
        gcs_service = GCSService()
        audio_bytes = validation["content"]
        gcs_uri = gcs_service.upload_audio(audio_bytes, gcs_path)

        # ---- Speech-to-text transcription ----
        transcript = transcribe_audio_bytes(audio_bytes, file_extension)

        # ---- Translation to English ----
        translation = translate_text_to_english(transcript)

        dummy_user_id = uuid.uuid4()
        audio_file = AudioFile(
            user_id=dummy_user_id,
            filename=filename,
            gcs_bucket_path=gcs_uri,
            file_format=file_extension,
            duration_seconds=validation["duration"],
            file_size_bytes=validation["file_size"]
        )
        db.add(audio_file)
        db.commit()
        db.refresh(audio_file)

        return {
            "success": True,
            "message": "Audio uploaded and translated successfully",
            "data": {
                "audio_id": str(audio_file.id),
                "filename": filename,
                "gcs_uri": gcs_uri,
                "duration_seconds": validation["duration"],
                "file_size_bytes": validation["file_size"],
                "category": category,
                "location": location,
                "uploaded_at": audio_file.uploaded_at.isoformat(),
                "transcription": transcript,
                "translation_en": translation
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )
