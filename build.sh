#!/bin/bash

echo "🚀 Building Credit Card Statement Parser for Vercel..."

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Build frontend
echo "🔨 Building frontend..."
npm run build

echo "✅ Build completed successfully!"
echo "📁 Output directory: frontend/dist"
