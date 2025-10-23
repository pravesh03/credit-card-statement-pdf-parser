# Railway Deployment Guide - Backend API

This guide will help you deploy your FastAPI backend to Railway so it can serve your Vercel-deployed frontend.

## 🚀 Quick Start

### Step 1: Sign Up for Railway
1. Go to [Railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with your GitHub account

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `pravesh03/credit-card-statement-parser`
4. Railway will automatically detect it

### Step 3: Configure Backend
1. In the project settings, click "Add Service"
2. Select "GitHub Repo"
3. Choose your repository again
4. Railway will auto-detect the project structure

### Step 4: Set Root Directory
1. Click on the service
2. Go to "Settings"
3. Find "Root Directory" setting
4. Set it to: `backend`
5. Save changes

### Step 5: Configure Environment Variables
1. Go to "Variables" tab
2. Add these environment variables:

```bash
DATABASE_URL=sqlite:///./credit_card_parser.db
AI_PROVIDER=mock
UPLOAD_DIR=uploads
TESSERACT_LANG=eng
OCR_CONFIDENCE_THRESHOLD=0.6
```

### Step 6: Set Start Command
1. Go to "Settings"
2. Find "Start Command"
3. Set it to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Save changes

### Step 7: Deploy
1. Railway will automatically detect your FastAPI app
2. Click "Deploy"
3. Wait for deployment to complete
4. Your backend will be live!

## 📋 Post-Deployment

### Get Your Backend URL
1. Once deployed, click on your service
2. Go to "Settings"
3. Find "Generate Domain" or use the provided Railway domain
4. Copy the URL (e.g., `https://your-app.railway.app`)

### Configure Vercel Frontend
1. Go to your Vercel project
2. Navigate to "Settings" → "Environment Variables"
3. Add new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: Your Railway backend URL (e.g., `https://your-app.railway.app`)
4. Save and redeploy

## 🔧 Railway Configuration

Railway will automatically detect:
- ✅ Python 3.11+
- ✅ FastAPI framework
- ✅ Requirements from `requirements.txt`

### Manual Configuration (if needed)
Create a `railway.json` in the backend folder:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  }
}
```

## 🌐 Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Click "Generate Domain" or add your custom domain
3. Configure DNS if using custom domain

## 📊 Monitoring

Railway provides:
- ✅ Real-time logs
- ✅ Metrics and analytics
- ✅ Deployment history
- ✅ Auto-scaling

## 🔒 Security

Railway automatically handles:
- ✅ HTTPS/SSL certificates
- ✅ Environment variable encryption
- ✅ Secure connections
- ✅ Docker security

## 💰 Pricing

Railway offers:
- **Free Tier**: $5 credit per month
- **Pro**: $20/month for production use
- **Your app**: Should fit in free tier for testing

## 🚨 Troubleshooting

### Issue: Build Failed
**Solution**: Check logs in Railway dashboard, ensure all dependencies are in `requirements.txt`

### Issue: Port Error
**Solution**: Make sure you're using `$PORT` environment variable in start command

### Issue: Database Not Found
**Solution**: SQLite database is created automatically on first run

### Issue: CORS Error
**Solution**: Frontend will connect once you set `VITE_API_URL` in Vercel

## 📝 Next Steps

1. ✅ Deploy backend on Railway
2. ✅ Copy backend URL
3. ✅ Add `VITE_API_URL` to Vercel
4. ✅ Redeploy frontend
5. ✅ Test upload functionality

## 🎯 Your Deployment URLs

- **Frontend**: Your Vercel URL
- **Backend**: Your Railway URL
- **API Docs**: `https://your-railway-url.railway.app/api/docs`

## 📞 Support

If you encounter issues:
1. Check Railway logs
2. Check Vercel logs
3. Verify environment variables
4. Ensure backend is running

---

**Ready to deploy? Start with Step 1 above!** 🚀
