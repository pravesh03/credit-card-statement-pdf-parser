# 🚀 Railway Deployment - Step by Step

## Simple 7-Step Guide

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub

### Step 2: Create Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `pravesh03/credit-card-statement-parser`

### Step 3: Deploy Backend
1. Railway will show your project
2. Click "New Service"
3. Select "GitHub Repo"
4. Choose your repository again
5. **Important**: Set **Root Directory** to `backend`
6. Click "Deploy"
7. Backend will start deploying automatically

### Step 4: Deploy Frontend
1. Click "New Service" again
2. Select "GitHub Repo"
3. Choose your repository
4. **Important**: Set **Root Directory** to `frontend`
5. Click "Deploy"
6. Frontend will start deploying automatically

### Step 5: Copy Backend URL
1. Go to your Backend service
2. Click "Settings"
3. Find "Generate Domain" or use the provided domain
4. Copy the URL (e.g., `https://your-backend.railway.app`)

### Step 6: Configure Frontend
1. Go to your Frontend service
2. Click "Variables" tab
3. Click "New Variable"
4. Add: `VITE_API_URL` = `https://your-backend.railway.app`
5. Save

### Step 7: Redeploy Frontend
1. Go to your Frontend service
2. Click "Deployments"
3. Click "Redeploy"
4. Wait for deployment to complete

## ✅ Done!

Your full-stack application is now deployed on Railway!

### Your URLs:
- **Frontend**: `https://your-frontend.railway.app`
- **Backend**: `https://your-backend.railway.app`
- **API Docs**: `https://your-backend.railway.app/api/docs`

## 🎯 Quick Tips

- Both services deploy automatically on git push
- Railway provides free SSL certificates
- Monitor logs in real-time
- Free tier: $5 credit per month

## 🆘 Need Help?

See `RAILWAY_FULL_STACK.md` for detailed information.
