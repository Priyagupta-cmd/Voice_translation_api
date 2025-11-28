from app.db.session import engine, Base
from app.models.models import AudioFile, Transcription, Issue

def init_db():
    """Create all database tables"""
    print("🗄️  Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  ✓ audio_files")
        print("  ✓ transcriptions")
        print("  ✓ issues")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def drop_all_tables():
    """Drop all tables - USE WITH CAUTION!"""
    print("⚠️  WARNING: Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")

if __name__ == "__main__":
    init_db()
