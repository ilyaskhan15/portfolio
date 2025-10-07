# 🌐 Custom Domain Setup for muhammadilyas.tech

## ✅ Heroku Configuration Complete

Your custom domain has been successfully added to Heroku! Here's what we've done:

### 🔧 **Domains Added to Heroku:**
- ✅ `muhammadilyas.tech` 
- ✅ `www.muhammadilyas.tech`

### 🔧 **Django Settings Updated:**
- ✅ `ALLOWED_HOSTS`: Updated to include your domain
- ✅ `CSRF_TRUSTED_ORIGINS`: Updated to include your domain

---

## 🛠️ DNS Configuration Required

Now you need to configure your DNS provider (where you bought muhammadilyas.tech) to point to Heroku:

### **For muhammadilyas.tech (Root Domain):**
```
Type: ALIAS or ANAME (or A record if ALIAS not supported)
Name: @ (or muhammadilyas.tech)
Value: fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com
TTL: 300 (or automatic)
```

### **For www.muhammadilyas.tech (Subdomain):**
```
Type: CNAME
Name: www
Value: pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com
TTL: 300 (or automatic)
```

---

## 📋 Step-by-Step DNS Setup

### **1. Login to Your DNS Provider**
Log into the control panel where you manage muhammadilyas.tech (e.g., Namecheap, GoDaddy, Cloudflare, etc.)

### **2. Find DNS Management**
Look for "DNS Management", "DNS Zone", or "Advanced DNS" in your control panel

### **3. Add/Update DNS Records**

#### **Option A: If your provider supports ALIAS/ANAME records:**
- **Record 1:**
  - Type: `ALIAS` or `ANAME`
  - Host/Name: `@` or `muhammadilyas.tech`
  - Value/Target: `fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com`

- **Record 2:**
  - Type: `CNAME`
  - Host/Name: `www`
  - Value/Target: `pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com`

#### **Option B: If your provider only supports A records:**
1. First, get the IP address of your Heroku DNS target:
```bash
nslookup fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com
```

2. Add A records:
- **Record 1:**
  - Type: `A`
  - Host/Name: `@`
  - Value: [IP address from nslookup]

- **Record 2:**
  - Type: `CNAME`
  - Host/Name: `www`
  - Value: `pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com`

### **4. Delete Conflicting Records**
Remove any existing A, AAAA, or CNAME records for `@` and `www` that might conflict

### **5. Save Changes**
Save your DNS configuration changes

---

## ⏱️ DNS Propagation

- **Propagation Time**: 5 minutes to 48 hours (usually within 1-2 hours)
- **Check Status**: Use tools like `nslookup` or online DNS checkers
- **Test Command**: 
```bash
nslookup muhammadilyas.tech
nslookup www.muhammadilyas.tech
```

---

## 🔍 Verification Steps

### **1. Check Domain Status in Heroku:**
```bash
heroku domains -a ilyas-protfolio
```

### **2. Test Your Domains:**
Once DNS propagates, test these URLs:
- https://muhammadilyas.tech
- https://www.muhammadilyas.tech

### **3. SSL Certificate:**
Heroku will automatically provision SSL certificates for your custom domain once DNS is configured properly.

---

## 🔧 Common DNS Provider Instructions

### **Cloudflare:**
1. Go to DNS tab
2. Add CNAME record: `www` → `pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com`
3. Add CNAME record: `@` → `fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com`
4. Set Proxy status to "DNS only" (gray cloud)

### **Namecheap:**
1. Go to Advanced DNS
2. Add CNAME: `www` → `pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com`
3. Add ALIAS: `@` → `fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com`

### **GoDaddy:**
1. Go to DNS Management
2. Add CNAME: `www` → `pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com`
3. Add A record: `@` → [Get IP from DNS target]

---

## 🚀 After DNS Propagation

Once your DNS is configured and propagated:

1. **Your site will be accessible at:**
   - https://muhammadilyas.tech
   - https://www.muhammadilyas.tech
   - https://ilyas-protfolio-2f03a275bcb2.herokuapp.com (still works)

2. **SSL certificates will be automatically provisioned**

3. **Admin panel will be available at:**
   - https://muhammadilyas.tech/admin/

---

## ⚠️ Important Notes

- **Keep Heroku URL**: Don't delete your `.herokuapp.com` URL as a backup
- **SSL**: Heroku provides free SSL certificates for custom domains
- **WWW Redirect**: Consider setting up a redirect from non-www to www or vice versa
- **Cache**: Clear your browser cache if you see old content

---

## 🆘 Troubleshooting

### **Domain Not Loading:**
- Check DNS propagation with `nslookup muhammadilyas.tech`
- Verify DNS records are correct
- Wait for propagation (up to 48 hours)

### **SSL Issues:**
- Wait for Heroku to provision SSL (can take up to 30 minutes after DNS propagation)
- Use `heroku certs:info -a ilyas-protfolio` to check SSL status

### **Check Domain Status:**
```bash
heroku domains:wait muhammadilyas.tech -a ilyas-protfolio
```

---

## 🎉 Success!

Once DNS propagation is complete, your Django portfolio will be available at your custom domain with:
- ✅ HTTPS encryption
- ✅ Custom domain branding
- ✅ Professional appearance
- ✅ All Django functionality intact

**Your portfolio will be live at**: https://muhammadilyas.tech 🚀