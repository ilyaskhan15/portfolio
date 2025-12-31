#!/usr/bin/env python3
"""
Favicon converter - converts an image to multiple favicon formats
Usage: python3 convert_favicon.py <input_image> [output_dir]
"""

import sys
import os
from PIL import Image

def convert_favicon(input_path, output_dir='static/img'):
    """Convert an image to multiple favicon formats."""
    
    if not os.path.exists(input_path):
        print(f"❌ Error: Image file not found: {input_path}")
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created output directory: {output_dir}")
    
    try:
        # Open and convert image to RGBA
        print(f"📷 Loading image: {input_path}")
        img = Image.open(input_path).convert('RGBA')
        original_size = img.size
        print(f"   Original size: {original_size[0]}x{original_size[1]} pixels")
        
        # Define favicon sizes and formats
        conversions = {
            'favicon-16x16.png': (16, 16, 'PNG'),
            'favicon-32x32.png': (32, 32, 'PNG'),
            'apple-touch-icon.png': (180, 180, 'PNG'),
            'favicon.ico': (32, 32, 'ICO'),
        }
        
        # Convert to each format
        print("\n🔄 Converting to favicon formats:")
        for filename, (width, height, fmt) in conversions.items():
            try:
                output_path = os.path.join(output_dir, filename)
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                resized.save(output_path, fmt)
                file_size = os.path.getsize(output_path) / 1024
                print(f"   ✓ {filename:30} ({width}x{height}) - {file_size:.1f} KB")
            except Exception as e:
                print(f"   ⚠ {filename:30} - Error: {e}")
        
        print("\n✅ Favicon conversion complete!")
        print(f"\nFiles saved to: {os.path.abspath(output_dir)}")
        print("\nNext steps:")
        print("1. Verify files: ls -lah static/img/favicon*")
        print("2. Test locally: python manage.py runserver")
        print("3. Deploy: git add static/img/favicon* && git commit -m 'Add favicon' && git push heroku main")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert_favicon.py <input_image> [output_dir]")
        print("\nExample:")
        print("  python3 convert_favicon.py ilyas-khan-logo.png")
        print("  python3 convert_favicon.py ilyas-khan-logo.png static/img")
        sys.exit(1)
    
    input_image = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else 'static/img'
    
    convert_favicon(input_image, output_directory)
