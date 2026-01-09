import os
import django
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def verify_cloudinary():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pustakam.settings')
    django.setup()

    print("Checking Cloudinary Configuration...")
    
    # Check Settings
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    creds = settings.CLOUDINARY_STORAGE
    print(f"Cloud Name present: {'Yes' if creds.get('CLOUD_NAME') else 'No'}")
    print(f"API Key present: {'Yes' if creds.get('API_KEY') else 'No'}")
    print(f"API Secret present: {'Yes' if creds.get('API_SECRET') else 'No'}")

    if not all([creds.get('CLOUD_NAME'), creds.get('API_KEY'), creds.get('API_SECRET')]):
        print("ERROR: Missing Cloudinary credentials. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET environment variables.")
        return

    # Try Upload
    try:
        print("Attempting to upload a test file...")
        path = default_storage.save('test_cloud.txt', ContentFile(b'Cloudinary integration works!'))
        url = default_storage.url(path)
        print(f"SUCCESS: File uploaded to {url}")
        
        # Cleanup (Optional, Cloudinary doesn't strictly require delete for test)
        # default_storage.delete(path)
        
    except Exception as e:
        print(f"UPLOAD FAILED: {str(e)}")

if __name__ == "__main__":
    verify_cloudinary()
