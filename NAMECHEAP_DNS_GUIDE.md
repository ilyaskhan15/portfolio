# 🔧 NAMECHEAP DNS UPDATE - Step by Step Guide

## 🎯 **Your Situation:**
- **Domain**: muhammadilyas.tech
- **Current DNS**: Points to Render.com (suspended) - `216.24.57.7`
- **Registrar**: Namecheap (using registrar-servers.com nameservers)
- **Target**: Point to Heroku app

---

## 📋 **EXACT STEPS FOR NAMECHEAP:**

### **Step 1: Login to Namecheap**
1. Go to: https://www.namecheap.com
2. Click **"Sign In"** 
3. Login with your Namecheap account

### **Step 2: Access Domain Management**
1. Go to **"Domain List"** 
2. Find **muhammadilyas.tech**
3. Click **"Manage"** button next to your domain

### **Step 3: Go to Advanced DNS**
1. Click on **"Advanced DNS"** tab
2. You'll see current Host Records

### **Step 4: DELETE Old Records**
**IMPORTANT: Delete these existing records:**
- Any **A Record** with Host `@` pointing to `216.24.57.7`
- Any **A Record** with Host `@` pointing to `216.24.57.251`
- Any **CNAME** records for `www` pointing to old Render URLs

### **Step 5: ADD New Heroku Records**

**Click "Add New Record" and add these TWO records:**

#### **Record 1 - Root Domain:**
```
Type: ALIAS Record
Host: @
Value: fathomless-aardvark-lxgkxbfn2tefg9f6wtiqd8q1.herokudns.com
TTL: Automatic (or 300)
```

#### **Record 2 - WWW Subdomain:**
```
Type: CNAME Record  
Host: www
Value: pacific-dingo-9md3hro3qv0dt9ra93ktw5o6.herokudns.com
TTL: Automatic (or 300)
```

### **Step 6: Save Changes**
1. Click **"Save All Changes"**
2. Confirm the changes

---

## ⚠️ **IMPORTANT NOTES:**

### **If ALIAS Record Option Not Available:**
Some Namecheap accounts don't show ALIAS records. If you only see A, CNAME, etc:

**Use A Record instead:**
```
Type: A Record
Host: @
Value: 99.83.151.71
TTL: 300
```

### **Final DNS Records Should Look Like:**
```
@ (root)     → ALIAS or A    → fathomless-aardvark-... (or 99.83.151.71)
www          → CNAME         → pacific-dingo-...
```

---

## ⏱️ **TIMELINE:**

| Step | Time |
|------|------|
| DNS Update | 2-5 minutes |
| Namecheap Propagation | 5-30 minutes |  
| Global Propagation | 1-24 hours |
| SSL Certificate | Automatic after DNS |

---

## 🔍 **HOW TO VERIFY:**

### **Method 1: Command Line**
```bash
# Wait 10-15 minutes after making changes, then test:
nslookup muhammadilyas.tech

# Should show Heroku IPs like 99.83.151.71 instead of 216.24.57.7
```

### **Method 2: Online DNS Checker**
- Visit: https://dnschecker.org
- Enter: `muhammadilyas.tech`
- Should show Heroku IPs globally

### **Method 3: Browser Test**
- Wait 30 minutes after DNS change
- Visit: https://muhammadilyas.tech
- Should show your Django portfolio (not Render suspension)

---

## 🚨 **COMMON NAMECHEAP ISSUES:**

### **1. Can't Find Advanced DNS Tab**
- Make sure you clicked "Manage" next to the domain
- Look for tabs: Basic DNS, Advanced DNS, etc.

### **2. ALIAS Record Not Available**  
- Use **A Record** instead with IP: `99.83.151.71`

### **3. Changes Not Saving**
- Make sure to click "Save All Changes" button
- Check for any error messages

### **4. Still Seeing Old Site**
- Clear browser cache (Ctrl+F5)
- Try incognito/private browsing
- Wait longer for propagation

---

## 📞 **Need Help?**

### **Screenshots of Current DNS Records:**
Take screenshots of your current Namecheap Advanced DNS page and share them if you need help.

### **Verify Your Heroku Setup:**
```bash
heroku domains -a ilyas-protfolio
# Should show your domain is added
```

---

## 🎉 **SUCCESS INDICATORS:**

✅ **DNS Updated**: `nslookup` shows Heroku IPs  
✅ **Website Works**: https://muhammadilyas.tech loads your portfolio  
✅ **SSL Active**: Green lock icon in browser  
✅ **Admin Works**: https://muhammadilyas.tech/admin/  

Once you complete these steps, your professional Django portfolio will be live on your custom domain! 🚀

**Current Status**: Ready to update - just need DNS changes on Namecheap!