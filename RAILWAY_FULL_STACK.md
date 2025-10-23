# Railway Full-Stack Deployment Guide

## 🚀 Deploy Both Frontend & Backend on Railway

Railway is perfect for deploying both your React frontend and FastAPI backend together!

## Quick Start

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: `pravesh03/credit-card-statement-parser`

### Step 3: Deploy Backend Service
1. Click "New Service"
2. Select "GitHub Repo"
3. Choose your repository
4. **Root Directory**: Set to `backend`
5. Railway will auto-detect FastAPI and deploy

### Step 4: Deploy Frontend Service
1. Click "New Service" again
2. Select "GitHub Repo"
3. Choose your repository
4. **Root Directory**: Set to `frontend`
5. Railway will auto-detect React/Vite

### Step 5: Configure Environment Variables

#### Backend Service:
```
DATABASE_URL=sqlite:///./credit_card_parser.db
AI_PROVIDER=mock
UPLOAD_DIR=uploads
TESSERACT_LANG=eng
OCR_CONFIDENCE_THRESHOLD=0.6
```

#### Frontend Service:
```
VITE_API_URL=https://your-backend-service.railway.app
```

### Step 6: Get Your URLs
- **Backend**: Railway will provide a URL (e.g., `https://your-app.railway.app`)
- **Frontend**: Railway will provide a URL (e.g., `https://your-frontend.railway.app`)

### Step 7: Connect Frontend to Backend
1. Copy your backend URL
2. Go to Frontend service → Variables
3. Add: `VITE_API_URL` = your backend URL
4. Redeploy frontend service

## 🎯 Why Railway is Better

✅ **Single Platform**: Both services in one place
✅ **Easy Configuration**: Just set root directories
✅ **Automatic HTTPS**: Both services get SSL
✅ **Free Tier**: $5 credit per month
✅ **Auto-Deploy**: Updates on git push
✅ **Monitoring**: Real-time logs for both services
✅ **Simple Setup**: No complex configuration

## 📊 Railway vs Vercel

| Feature | Railway | Vercel |
|---------|---------|---------|
| Full-Stack | ✅ Yes | ❌ Frontend only |
| Python Backend | ✅ Supported | ❌ Limited |
| File Storage | ✅ Supported | ❌ Requires external |
| Database | ✅ Supported | ❌ Requires external |
| Same Platform | ✅ Yes | ❌ No |
| Setup | ✅ Easy | ⚠️ Complex |

## 🎉 Your Deployment URLs

Once deployed:
- **Frontend**: `https://your-frontend.railway.app`
- **Backend**: `https://your-backend.railway.app`
- **API Docs**: `https://your-backend.railway.app/api/docs`

## 📝 Quick Checklist

- [ ] Sign up on Railway
- [ ] Create project from GitHub
- [ ] Deploy backend service (`backend` folder)
- [ ] Deploy frontend service (`frontend` folder)
- [ ] Configure backend environment variables
- [ ] Copy backend URL
- [ ] Add `VITE_API_URL` to frontend
- [ ] Redeploy frontend
- [ ] Test both services

## 🆘 Troubleshooting

**Issue**: Frontend can't connect to backend
- **Solution**: Check `VITE_API_URL` is set correctly

**Issue**: Backend build fails
- **Solution**: Check Railway logs, ensure `requirements.txt` exists

**Issue**: Frontend build fails
- **Solution**: Check Railway logs, ensure `package.json` exists

## 🎯 Next Steps

1. Follow the steps above
2. Test your deployment
3. Share your Railway URLs!

---

**Railway makes full-stack deployment simple!** 🚀
