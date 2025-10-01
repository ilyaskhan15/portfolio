# Quick User Guide: Managing Homepage Content

## How to Add/Update Dynamic Homepage Content

### 🎯 Adding a New Project (Will appear on homepage)

1. Go to Django Admin: `http://127.0.0.1:8000/admin/` or `https://muhammadilyas.tech/admin/`
2. Log in with your credentials
3. Navigate to **Portfolio → Projects**
4. Click **Add Project**
5. Fill in the required fields:
   - **Title**: Your project name
   - **Short Description**: Brief one-liner (appears on homepage)
   - **Description**: Full project details
   - **Featured Image**: Upload a good quality image (recommended: 1200x800px)
   - **Technologies**: Select the skills/technologies used
   - **Project Type**: Select appropriate type (Web App, Mobile, etc.)
   - **Status**: Set to **"Published"** (important!)
   - **Live URL / GitHub URL**: Add your project links
6. Click **Save**
7. ✅ Your latest project will now appear on the homepage!

### ⚽ Adding a Football Article (Will appear on homepage)

1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Navigate to **Blog → Posts**
3. Click **Add Post**
4. Fill in the details:
   - **Title**: Your article title
   - **Excerpt**: Brief description (appears on homepage)
   - **Content**: Full article content
   - **Featured Image**: Upload an image
   - **Category**: Select or create "Football" category (case-insensitive)
   - **Status**: Set to **"Published"** (important!)
   - **Published At**: Set to current date/time
5. Click **Save**
6. ✅ Your latest football article will appear in the first card of Latest Articles section!

### 💻 Adding a Technical Article (Will appear on homepage)

1. Follow the same steps as football article
2. **Important difference**: Set category to anything OTHER than "Football"
   - Examples: Python, Django, JavaScript, React, Tutorial, etc.
3. The latest 2 technical articles will appear in cards 2 and 3

### 📄 Updating Your Resume/CV

1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Navigate to **Portfolio → Profiles**
3. Click on your profile (or create one if it doesn't exist)
4. Scroll to **Resume** field
5. Click **Choose File** and select your CV/Resume
   - Supports: PDF, DOC, DOCX, and other formats
   - Recommended: Use PDF for best compatibility
6. Set **Is Active** to checked
7. Click **Save**
8. ✅ Users can now download your resume from `http://127.0.0.1:8000/portfolio/resume/`

## Homepage Content Priority

### Latest Project Section
- Shows: **Most recently created published project**
- Sorting: Latest first (by created_at)
- Count: 1 project displayed

### Latest Articles Section
- Card 1: **Latest published football article** (category = "football")
- Cards 2-3: **Latest 2 published technical articles** (category != "football")
- Sorting: Latest first (by published_at)

## Tips & Best Practices

### For Projects
✅ Always add a featured image - makes your project look professional
✅ Fill in technologies to show what you used
✅ Add both GitHub URL and Live URL when available
✅ Write a compelling short description (this appears on homepage)
✅ Set order field to control which projects appear first

### For Blog Posts
✅ Always set a category - helps organize your content
✅ Write a good excerpt - this is what appears on homepage
✅ Add a featured image for better visual appeal
✅ Set published_at date correctly
✅ Use tags to improve discoverability

### For Resume
✅ Use PDF format for best compatibility
✅ Name your file appropriately (e.g., "Muhammad_Ilyas_Resume.pdf")
✅ Keep file size under 5MB
✅ Update regularly to keep it current

## Troubleshooting

### Project not showing on homepage?
- Check if status is set to "Published"
- Verify created_at date is recent
- Make sure you saved the project

### Football article not appearing?
- Check if category name is exactly "Football" (case doesn't matter)
- Verify status is "Published"
- Check if published_at date is set

### Resume download not working?
- Verify file is uploaded in Profile
- Check if profile is set to "Is Active"
- Try re-uploading the file
- Check file format is supported

### No content showing at all?
- Make sure you have at least one published project
- Make sure you have at least one published blog post
- Check Django admin for any error messages

## URLs Reference

- **Homepage**: `http://127.0.0.1:8000/` (local) or `https://muhammadilyas.tech/` (production)
- **Admin Panel**: `http://127.0.0.1:8000/admin/` or `https://muhammadilyas.tech/admin/`
- **All Projects**: `http://127.0.0.1:8000/portfolio/`
- **All Blog Posts**: `http://127.0.0.1:8000/blog/`
- **Resume Download**: `http://127.0.0.1:8000/portfolio/resume/`
- **Skills**: `http://127.0.0.1:8000/portfolio/skills/`

## Need Help?

If you encounter any issues:
1. Check the Django admin for error messages
2. Look at the server console for errors
3. Verify all required fields are filled
4. Make sure status is set to "Published"
5. Check that dates are set correctly

Happy content management! 🚀
