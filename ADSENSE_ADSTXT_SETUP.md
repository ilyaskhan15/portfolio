# Google AdSense ads.txt Setup

## Overview
The `ads.txt` file has been successfully added to your website to verify your Google AdSense account and prevent unauthorized ad inventory sales.

## File Location
- **Source file**: `/home/ik/Desktop/BlogPost/static/ads.txt`
- **Production file**: `/home/ik/Desktop/BlogPost/staticfiles/ads.txt`
- **Accessible URL**: `https://muhammadilyas.tech/ads.txt`

## Content
```
google.com, pub-7667391240665296, DIRECT, f08c47fec0942fa0
```

## How It Works

### Development (Local)
- File is served from `static/ads.txt`
- URL: `http://127.0.0.1:8000/ads.txt`
- Handled by custom view in `portfolio_blog/urls.py`

### Production (Live Site)
- File is served from `staticfiles/ads.txt` (collected during deployment)
- URL: `https://muhammadilyas.tech/ads.txt`
- Must be accessible at the root domain level

## Implementation Details

### 1. Created ads.txt File
Location: `static/ads.txt`
```
google.com, pub-7667391240665296, DIRECT, f08c47fec0942fa0
```

### 2. Added URL Route
In `portfolio_blog/urls.py`:
- Created custom view `serve_ads_txt()` to serve the file
- Added route: `path('ads.txt', serve_ads_txt, name='ads_txt')`
- Returns file with `content_type='text/plain'`

### 3. Static Files Collection
- File automatically copied to `staticfiles/` during `collectstatic`
- Will be available in production after deployment

## Verification Steps

### Local Testing
1. Start development server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/ads.txt`
3. Verify content displays correctly

### Production Testing (After Deployment)
1. Visit: `https://muhammadilyas.tech/ads.txt`
2. Verify the file is accessible
3. Content should show: `google.com, pub-7667391240665296, DIRECT, f08c47fec0942fa0`

### Google AdSense Verification
1. Go to Google AdSense dashboard
2. Navigate to **Sites** section
3. Check **ads.txt** status for `muhammadilyas.tech`
4. Should show status: **Ready** or **Not found** → **Ready** (after crawling)

## Deployment Notes

### When Deploying to Production:
1. Make sure to run `python manage.py collectstatic` during deployment
2. Ensure the ads.txt file is included in staticfiles
3. Verify the URL is accessible at the root level

### Build Script
Your `build.sh` should include:
```bash
python manage.py collectstatic --no-input
```

This ensures ads.txt is always included in the static files.

## Troubleshooting

### Issue: ads.txt not found (404 error)
**Solutions:**
- Run `python manage.py collectstatic --no-input`
- Restart your web server
- Check if `static/ads.txt` exists
- Verify URL route is properly configured

### Issue: Google AdSense shows "Needs attention"
**Solutions:**
- Wait 24-48 hours for Google to crawl your site
- Verify ads.txt is accessible at `https://muhammadilyas.tech/ads.txt`
- Check file content matches your AdSense publisher ID
- Ensure no robots.txt blocking ads.txt

### Issue: File not updating
**Solutions:**
- Clear browser cache
- Run `python manage.py collectstatic --clear --no-input`
- Redeploy your application
- Check if you modified the correct file (`static/ads.txt`)

## Important Notes

1. **Publisher ID**: The publisher ID `pub-7667391240665296` must match your Google AdSense account
2. **File Format**: Must be plain text, no HTML formatting
3. **Location**: Must be accessible at root level (not `/static/ads.txt`)
4. **Content Type**: Must be served as `text/plain`
5. **Case Sensitive**: URL must be exactly `/ads.txt` (lowercase)

## Additional Publishers
To add more ad networks or publishers, add new lines to `static/ads.txt`:
```
google.com, pub-7667391240665296, DIRECT, f08c47fec0942fa0
anotherpublisher.com, pub-123456789, DIRECT, f08c47fec0942fa0
```

## Testing URLs
- **Local**: http://127.0.0.1:8000/ads.txt
- **Production**: https://muhammadilyas.tech/ads.txt

## Status Check
After deployment, Google AdSense will automatically crawl and verify your ads.txt file within 24-48 hours. The status will change from "Getting ready" to "Ready" in the AdSense dashboard.

## Next Steps
1. ✅ File created in `static/ads.txt`
2. ✅ URL route added to `urls.py`
3. ✅ Static files collected
4. ⏳ Deploy to production
5. ⏳ Wait for Google to verify (24-48 hours)
6. ⏳ Check AdSense dashboard status

## References
- [Google AdSense ads.txt Guide](https://support.google.com/adsense/answer/7532444)
- [IAB ads.txt Specification](https://iabtechlab.com/ads-txt/)
