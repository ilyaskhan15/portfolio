# Homepage Dynamic Content & Resume Download Fix

## Summary of Changes

This update makes the homepage display dynamic content from the database instead of static placeholders, and fixes the resume download functionality.

## Changes Made

### 1. Created Dynamic Home View (`portfolio/views.py`)
- Added `HomeView` class that fetches:
  - Latest published project
  - Latest football article
  - Latest 2 technical articles (non-football)
  - Featured skills for the skills section
  - Active profile information

### 2. Updated Homepage Template (`templates/home.html`)
- **Featured Projects Section**: Now displays the latest uploaded project dynamically
  - Shows project image, title, description
  - Displays technology tags
  - Links to project detail page and external URLs (GitHub, live demo)
  - Shows placeholder message if no projects exist
  
- **Latest Articles Section**: Now displays real blog posts
  - Shows the latest football article in the first card
  - Shows the latest 2 technical articles in remaining cards
  - Displays post images, titles, excerpts, categories, and reading time
  - Links to individual blog posts
  - Shows placeholder message if no posts exist

### 3. Fixed Resume Download (`portfolio/views.py`)
- Updated `ResumeDownloadView` to handle both local and Cloudinary-hosted files
- Added proper MIME type detection for different file formats (PDF, DOC, DOCX, etc.)
- For Cloudinary files: Redirects to the direct Cloudinary URL
- For local files: Serves via `FileResponse` with proper content type
- Added better error handling and debugging
- Maintains the filename format: `{Full_Name}_Resume.{extension}`

### 4. Updated URL Configuration (`portfolio_blog/urls.py`)
- Changed homepage from static `TemplateView` to dynamic `HomeView`
- Imported `HomeView` from portfolio.views

## Files Modified

1. `/home/ik/Desktop/BlogPost/portfolio/views.py`
   - Added `HomeView` class
   - Enhanced `ResumeDownloadView` with better file handling
   - Added imports: `FileResponse`, `mimetypes`

2. `/home/ik/Desktop/BlogPost/templates/home.html`
   - Updated "Featured Projects" section to display dynamic content
   - Updated "Latest Articles" section to display dynamic content
   - Fixed field names (category, reading_time)

3. `/home/ik/Desktop/BlogPost/portfolio_blog/urls.py`
   - Changed homepage URL to use `HomeView.as_view()`

## How It Works

### Dynamic Project Display
When you add a new project in the Django admin:
1. Go to Admin → Portfolio → Projects → Add Project
2. Fill in the details (title, description, image, technologies, etc.)
3. Set status to "Published"
4. The latest project will automatically appear on the homepage

### Dynamic Blog Posts Display
When you add a new blog post in the Django admin:
1. Go to Admin → Blog → Posts → Add Post
2. Fill in the details
3. Set category to "Football" for football articles (will appear in the first card)
4. Set category to anything else for technical articles (will appear in cards 2-3)
5. Set status to "Published"
6. The latest posts will automatically appear on the homepage

### Resume Download
When users click the resume download link:
1. System checks for active profile with resume file
2. If file is on Cloudinary → Redirects to Cloudinary URL
3. If file is local → Serves file with proper MIME type
4. If no resume → Shows a nice "Resume Not Available" page

## Testing

### Test Dynamic Content
1. Add a project in admin with status "Published"
2. Add a blog post with category "Football" and status "Published"
3. Add another blog post with different category and status "Published"
4. Visit homepage at `http://127.0.0.1:8000/`
5. Verify content appears correctly

### Test Resume Download
1. Go to Admin → Portfolio → Profiles
2. Add/edit profile with resume file (PDF or other format)
3. Visit `http://127.0.0.1:8000/portfolio/resume/`
4. Click download button
5. Verify file downloads correctly with proper name

## Benefits

✅ **Dynamic Content**: Homepage automatically updates when you add new projects or blog posts
✅ **Better UX**: Users see your latest work without manual template updates
✅ **Resume Download Fixed**: Works with both Cloudinary and local storage, supports multiple file formats
✅ **Fallback Messages**: Shows appropriate messages when no content is available
✅ **SEO Friendly**: Uses proper meta tags and structured data from the database

## Next Steps (Optional)

1. Add pagination to show more than just the latest 3 blog posts
2. Add featured flags to manually control which projects/posts appear on homepage
3. Add caching to improve performance
4. Add analytics tracking for homepage views
5. Consider adding a "Featured" section for handpicked content

## Notes

- The homepage will show placeholder text if no projects or blog posts exist yet
- Football articles are identified by the category name "Football" (case-insensitive)
- Resume download supports PDF, DOC, DOCX, and other file formats
- All images use Cloudinary storage in production
