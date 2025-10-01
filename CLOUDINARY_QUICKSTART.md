# Quick Reference: Cloudinary Environment Variables for Render

## 🚀 What You Need to Do

### 1. Get Cloudinary Credentials
Sign up at: **https://cloudinary.com/users/register/free**

After signup, copy these from your dashboard:
```
Cloud Name: ___________________
API Key: ___________________
API Secret: ___________________
```

### 2. Add to Render Dashboard

Go to: **https://dashboard.render.com** → Your Service → **Environment** tab

Add these 3 environment variables:

| Variable Name | Value |
|--------------|-------|
| `CLOUDINARY_CLOUD_NAME` | (paste your cloud name) |
| `CLOUDINARY_API_KEY` | (paste your API key) |
| `CLOUDINARY_API_SECRET` | (paste your API secret) |

### 3. Deploy

```bash
git add .
git commit -m "Add Cloudinary for persistent media storage"
git push origin main
```

## ✅ That's It!

Your images will now:
- ✅ Stay permanent (won't disappear on restart)
- ✅ Load faster (CDN delivery)
- ✅ Auto-optimize (smaller file sizes)

## 🧪 Test It

1. Go to: `https://muhammadilyas.tech/admin/`
2. Upload an image
3. Check: `https://cloudinary.com/console/media_library`
4. Image should appear there ✅

---

## 📝 Files Modified

- ✅ `portfolio_blog/settings/base.py` - Added Cloudinary config
- ✅ `portfolio_blog/settings/production.py` - Removed local media settings
- ✅ All existing code works as-is (no model changes needed)

## 🆘 Troubleshooting

**Images still disappearing?**
→ Check environment variables are set in Render

**Upload errors?**
→ Check Render logs for Cloudinary connection errors

**Want to migrate old images?**
→ Re-upload them through admin panel

---

**Full guide**: See `CLOUDINARY_SETUP.md`
