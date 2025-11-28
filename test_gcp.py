from google.cloud import storage

def test_gcp_connection():
    """Test Google Cloud Platform connection using Application Default Credentials"""
    
    print("=" * 60)
    print("🧪 Testing Google Cloud Platform Connection")
    print("   Using Application Default Credentials (gcloud auth)")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Create client with default credentials
        print("1️⃣  Authenticating with Application Default Credentials...")
        client = storage.Client(project='naadatech')
        print("   ✅ Authenticated successfully")
        print()
        
        # Step 2: List buckets
        print("2️⃣  Fetching buckets from Google Cloud...")
        buckets = list(client.list_buckets())
        print(f"   ✅ Found {len(buckets)} bucket(s)")
        print()
        
        # Step 3: Display buckets
        print("📦 Your buckets:")
        for bucket in buckets:
            print(f"   • {bucket.name}")
            print(f"     Location: {bucket.location}")
            print(f"     Storage class: {bucket.storage_class}")
        print()
        
        # Step 4: Test specific bucket
        print("3️⃣  Testing access to naadatech-audio-storage...")
        target_bucket = client.bucket('naadatech-audio-storage')
        
        if target_bucket.exists():
            print("   ✅ Bucket is accessible!")
            print(f"   📍 Location: {target_bucket.location}")
            print(f"   🗂️  Storage class: {target_bucket.storage_class}")
        else:
            print("   ❌ Bucket not found or not accessible")
            return False
        
        print()
        print("=" * 60)
        print("🎉 All tests passed! GCP is ready to use.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Run: gcloud auth application-default login")
        print("2. Make sure you selected project: naadatech")
        print("3. Check that you have permissions")
        print()
        return False

if __name__ == "__main__":
    success = test_gcp_connection()
    
    if success:
        print("\n✅ Next step: Test the FastAPI endpoint")
        print("   Run: uvicorn app.main:app --reload")
        print("   Then open: http://127.0.0.1:8000/docs")
    else:
        print("\n⚠️  Run: gcloud auth application-default login")
