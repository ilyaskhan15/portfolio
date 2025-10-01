"""
Test Cloudinary connection and upload functionality.
Run this script to verify Cloudinary is configured correctly.

Usage:
    python test_cloudinary.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings.development')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import cloudinary
import cloudinary.uploader


def test_cloudinary_config():
    """Test if Cloudinary is configured correctly."""
    print("=" * 60)
    print("CLOUDINARY CONFIGURATION TEST")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME')
    api_key = settings.CLOUDINARY_STORAGE.get('API_KEY')
    api_secret = settings.CLOUDINARY_STORAGE.get('API_SECRET')
    
    if not cloud_name:
        print("❌ CLOUDINARY_CLOUD_NAME not set!")
        return False
    if not api_key:
        print("❌ CLOUDINARY_API_KEY not set!")
        return False
    if not api_secret:
        print("❌ CLOUDINARY_API_SECRET not set!")
        return False
    
    print(f"✅ Cloud Name: {cloud_name}")
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ API Secret: {api_secret[:10]}...")
    
    # Check DEFAULT_FILE_STORAGE
    print("\n2. Checking DEFAULT_FILE_STORAGE...")
    storage = settings.DEFAULT_FILE_STORAGE
    print(f"   Storage backend: {storage}")
    if 'cloudinary' in storage.lower():
        print("✅ Cloudinary storage is configured")
    else:
        print("❌ Cloudinary storage NOT configured!")
        return False
    
    # Check INSTALLED_APPS
    print("\n3. Checking INSTALLED_APPS order...")
    apps = settings.INSTALLED_APPS
    cloudinary_storage_index = apps.index('cloudinary_storage') if 'cloudinary_storage' in apps else -1
    staticfiles_index = apps.index('django.contrib.staticfiles') if 'django.contrib.staticfiles' in apps else -1
    
    if cloudinary_storage_index == -1:
        print("❌ 'cloudinary_storage' not in INSTALLED_APPS!")
        return False
    
    if staticfiles_index == -1:
        print("⚠️  'django.contrib.staticfiles' not found (might be okay)")
    elif cloudinary_storage_index < staticfiles_index:
        print("✅ 'cloudinary_storage' comes before 'django.contrib.staticfiles'")
    else:
        print("❌ 'cloudinary_storage' must come BEFORE 'django.contrib.staticfiles'!")
        return False
    
    return True


def test_cloudinary_upload():
    """Test actual file upload to Cloudinary."""
    print("\n4. Testing file upload to Cloudinary...")
    
    try:
        # Create a 1x1 pixel PNG image (minimal valid image)
        # This is a base64 encoded 1x1 transparent PNG
        import base64
        test_image = base64.b64decode(
            b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
        )
        test_filename = "test_upload.png"
        
        # Try to save using Django's default storage
        path = default_storage.save(f"test/{test_filename}", ContentFile(test_image))
        print(f"✅ File saved: {path}")
        
        # Get the URL
        url = default_storage.url(path)
        print(f"✅ File URL: {url}")
        
        if 'cloudinary' in url:
            print("✅ URL is from Cloudinary!")
        else:
            print("❌ URL is NOT from Cloudinary!")
            return False
        
        # Clean up
        default_storage.delete(path)
        print("✅ Test file deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_direct_cloudinary():
    """Test direct Cloudinary API upload."""
    print("\n5. Testing direct Cloudinary API...")
    
    try:
        # Configure cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
            api_key=settings.CLOUDINARY_STORAGE.get('API_KEY'),
            api_secret=settings.CLOUDINARY_STORAGE.get('API_SECRET')
        )
        
        # Test upload using cloudinary API directly
        result = cloudinary.uploader.upload(
            "data:text/plain;base64,VGVzdCBmaWxl",
            folder="test",
            resource_type="raw"
        )
        
        print(f"✅ Direct upload successful!")
        print(f"   Public ID: {result.get('public_id')}")
        print(f"   URL: {result.get('secure_url')}")
        
        # Clean up
        cloudinary.uploader.destroy(result.get('public_id'), resource_type="raw")
        print("✅ Test file deleted from Cloudinary")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    
    # Test configuration
    config_ok = test_cloudinary_config()
    
    if not config_ok:
        print("\n" + "=" * 60)
        print("❌ CONFIGURATION ERRORS FOUND!")
        print("=" * 60)
        print("\nPlease fix the configuration issues above and try again.")
        return
    
    # Test Django storage upload
    upload_ok = test_cloudinary_upload()
    
    # Test direct Cloudinary API
    direct_ok = test_direct_cloudinary()
    
    # Final report
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Configuration: {'✅ PASSED' if config_ok else '❌ FAILED'}")
    print(f"Django Storage Upload: {'✅ PASSED' if upload_ok else '❌ FAILED'}")
    print(f"Direct Cloudinary API: {'✅ PASSED' if direct_ok else '❌ FAILED'}")
    print("=" * 60)
    
    if config_ok and upload_ok and direct_ok:
        print("\n🎉 ALL TESTS PASSED! Cloudinary is working correctly!")
        print("\nYou can now:")
        print("1. Deploy to Render")
        print("2. Upload images through admin panel")
        print("3. Images will appear in Cloudinary Media Library")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("\nPlease check the errors above and:")
        print("1. Verify CLOUDINARY_* environment variables are set")
        print("2. Check INSTALLED_APPS order in settings")
        print("3. Ensure packages are installed: pip install cloudinary django-cloudinary-storage")


if __name__ == '__main__':
    main()
