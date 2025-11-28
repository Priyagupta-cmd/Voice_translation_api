from sqlalchemy import Column, String, Integer, Float, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.session import Base

class AudioFile(Base):
    """Audio file metadata"""
    __tablename__ = "audio_files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    gcs_bucket_path = Column(Text, nullable=False)
    file_format = Column(String(10))
    duration_seconds = Column(Float)
    file_size_bytes = Column(Integer)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
    
    transcription = relationship("Transcription", back_populates="audio_file", uselist=False)
    
    def __repr__(self):
        return f"<AudioFile {self.filename}>"

class Transcription(Base):
    """Transcription results"""
    __tablename__ = "transcriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_file_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id"), index=True)
    original_language = Column(String(10))
    original_text = Column(Text)
    english_translation = Column(Text)
    confidence_score = Column(Float)
    transcription_status = Column(String(20), default="processing", index=True)
    retry_count = Column(Integer, default=0)
    is_user_edited = Column(Boolean, default=False)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    audio_file = relationship("AudioFile", back_populates="transcription")
    
    def __repr__(self):
        return f"<Transcription {self.id} - {self.transcription_status}>"

class Issue(Base):
    """Public issues"""
    __tablename__ = "issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    title = Column(String(255))
    description = Column(Text)
    category = Column(String(50), index=True)
    location = Column(String(255))
    status = Column(String(20), default="open", index=True)
    audio_file_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id"), nullable=True)
    transcription_id = Column(UUID(as_uuid=True), ForeignKey("transcriptions.id"), nullable=True)
    is_voice_report = Column(Boolean, default=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Issue {self.title} - {self.status}>"
