# Deployment Guide

## Current Deployment Status

### ✅ Frontend
- **Platform**: Vercel
- **URL**: Your Vercel deployment URL
- **Status**: Live and working

### ⚠️ Backend Deployment Options

Vercel is primarily designed for frontend deployments and serverless functions. For a full FastAPI backend, you have these options:

#### Option 1: Railway (Recommended)
- **Best for**: Full-stack Python applications
- **Setup**: See `RAILWAY_DEPLOYMENT.md`
- **URL**: Deploy backend on Railway
- **Config**: Connect frontend to Railway backend via `VITE_API_URL`

#### Option 2: Render
- **Best for**: Python web services
- **Setup**: Similar to Railway
- **URL**: Deploy backend on Render
- **Config**: Connect frontend to Render backend

#### Option 3: Heroku
- **Best for**: Traditional PaaS deployment
- **Setup**: Use Procfile in backend folder
- **URL**: Deploy backend on Heroku
- **Config**: Connect frontend to Heroku backend

#### Option 4: DigitalOcean App Platform
- **Best for**: Production applications
- **Setup**: Full PaaS with databases
- **URL**: Deploy backend on DigitalOcean
- **Config**: Connect frontend to DigitalOcean backend

## Current Configuration

### Frontend on Vercel
- Static React app built with Vite
- Optimized for production
- Fast CDN delivery
- Automatic HTTPS

### Backend Setup
- For local development: See README.md
- For production: Deploy on Railway/Render
- API URL: Set via `VITE_API_URL` environment variable

## Environment Variables

### Vercel Frontend
```
VITE_API_URL=https://your-backend-url.com
```

### Backend (Railway/Render)
```
DATABASE_URL=sqlite:///./credit_card_parser.db
AI_PROVIDER=mock
UPLOAD_DIR=uploads
```

## Quick Start

### 1. Deploy Frontend
```bash
# Already deployed on Vercel
vercel --prod
```

### 2. Deploy Backend
```bash
# On Railway
# See RAILWAY_DEPLOYMENT.md

# Or on Render
# See RENDER_DEPLOYMENT.md
```

### 3. Connect Frontend to Backend
```bash
# In Vercel settings
# Add environment variable: VITE_API_URL
# Value: Your backend URL
```

## Support

For deployment issues, check:
- Railway logs
- Render logs
- Vercel logs
- Backend logs
