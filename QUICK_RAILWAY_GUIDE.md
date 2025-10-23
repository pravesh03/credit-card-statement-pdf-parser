# 🚀 Railway Deployment - Quick Steps

## Step-by-Step Guide

### 1️⃣ Sign Up & Create Project
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with **GitHub** (recommended)

### 2️⃣ Deploy from GitHub
1. Click "**Deploy from GitHub repo**"
2. Select: `pravesh03/credit-card-statement-parser`
3. Railway will auto-detect your project

### 3️⃣ Configure Service
1. Railway will show your project
2. Click "**Generate Domain**" to get your backend URL
3. Your backend will start deploying automatically

### 4️⃣ Set Environment Variables (Optional)
Go to **Variables** tab and add:
```
DATABASE_URL=sqlite:///./credit_card_parser.db
AI_PROVIDER=mock
UPLOAD_DIR=uploads
```

### 5️⃣ Get Your Backend URL
Once deployed:
1. Go to **Settings**
2. Find your domain (e.g., `your-app.railway.app`)
3. Copy the URL

### 6️⃣ Configure Vercel Frontend
1. Go to your **Vercel project**
2. Settings → **Environment Variables**
3. Add: `VITE_API_URL` = `https://your-railway-url.railway.app`
4. **Redeploy** your frontend

### 7️⃣ Test Your Deployment
- Frontend: Your Vercel URL
- Backend: Your Railway URL
- API Docs: `https://your-railway-url.railway.app/api/docs`

## 🎯 Quick Checklist
- [ ] Sign up on Railway
- [ ] Deploy from GitHub
- [ ] Copy backend URL
- [ ] Add `VITE_API_URL` to Vercel
- [ ] Redeploy frontend
- [ ] Test upload functionality

## 🆘 Troubleshooting

**Issue**: Build fails
- Check Railway logs
- Ensure `requirements.txt` is in backend folder

**Issue**: CORS errors
- Add `VITE_API_URL` to Vercel environment variables

**Issue**: Database errors
- SQLite database is created automatically

## 📞 Need Help?
Check Railway logs in the dashboard for detailed error messages.
