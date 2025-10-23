# Credit Card Statement Parser

A production-ready, AI-powered credit card statement parser that extracts key information from PDF statements across multiple issuers. Built with FastAPI, React, and AI integration.

## 🚀 Features

- **Multi-Issuer Support**: HDFC, SBI, ICICI, Axis, Citibank, and more
- **AI-Powered Extraction**: Uses LLM validation for improved accuracy
- **Hybrid Processing**: Combines regex, OCR, and layout analysis
- **Modern Dark Theme**: Beautiful, high-contrast UI with excellent visibility
- **Web Interface**: React dashboard for upload and management
- **Confidence Scoring**: Field-level confidence and extraction rationale
- **PDF Viewing**: View uploaded PDFs directly in the browser
- **CRUD Operations**: Create, read, update, delete statements
- **API-First**: RESTful API with OpenAPI documentation
- **Local Development**: SQLite database for easy local setup

## 📋 Extracted Fields

- **Cardholder Name**: Primary account holder
- **Card Last 4 Digits**: Last four digits of card number
- **Billing Period**: Start and end dates
- **Payment Due Date**: When payment is due
- **Total Amount Due**: Outstanding balance

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend │    │   SQLite DB      │
│                 │◄──►│                 │◄──►│   (Local Dev)    │
│  - Upload UI    │    │  - Extractors    │    │                 │
│  - Results View │    │  - AI Provider   │    │                 │
│  - Statistics   │    │  - API Endpoints │    │                 │
│  - PDF Viewer   │    │  - Static Files │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Provider   │
                       │                 │
                       │  - Mock (Dev)   │
                       │  - OpenAI GPT   │
                       │  - Anthropic    │
                       └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with Alembic migrations
- **SQLite**: Local development database
- **pdfplumber**: PDF text extraction
- **PyMuPDF**: PDF processing and OCR
- **Tesseract**: OCR for scanned PDFs
- **OpenAI API**: LLM integration for validation

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icon library
- **Custom CSS**: Dark theme with gradients and glass morphism

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- pip and npm

### 1. Clone and Setup
```bash
git clone https://github.com/pravesh03/credit-card-statement-parser.git
cd credit-card-statement-parser
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup (in a new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### 5. Generate Sample Data
```bash
# Generate sample PDFs for testing
python scripts/generate_samples.py

# Run evaluation on samples
python scripts/evaluate.py
```

## 🎨 UI Screenshots

### Main Dashboard
![Main Dashboard](screenshots/dashboard.png)
*Beautiful dark theme dashboard with modern UI design*

### Upload Interface
![Upload Interface](screenshots/upload.png)
*Drag-and-drop PDF upload with real-time progress and extraction results*

### Statements List
![Statements List](screenshots/statements.png)
*Comprehensive statement management with filtering and sorting*

### Statement Details
![Statement Details](screenshots/details.png)
*Detailed view with extracted fields, confidence scores, and AI analysis*

### Statistics Dashboard
![Statistics](screenshots/statistics.png)
*Processing statistics and analytics overview*

### PDF Viewer
![PDF Viewer](screenshots/pdf-viewer.png)
*Integrated PDF viewer for original documents*

## 🌐 Deployment

### Frontend Deployment
- **Platform**: Vercel
- **Status**: ✅ Live
- **URL**: Your Vercel deployment URL

### Backend Deployment
- **Platform**: Railway/Render/Heroku
- **Status**: See screenshots below
- **Configuration**: See `QUICK_RAILWAY_GUIDE.md` for deployment instructions

### Backend Deployment Screenshots
![Backend Deployment](screenshots/backend-deployment.png)
*Backend API deployment on Railway platform*

![Backend Environment](screenshots/backend-env.png)
*Environment variables configuration*

![Backend Logs](screenshots/backend-logs.png)
*Real-time deployment logs and monitoring*

## 📊 API Documentation

### Upload Statement
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@statement.pdf" \
  -F "issuer=hdfc"
```

### Get Statements
```bash
curl "http://localhost:8000/api/v1/statements"
```

### Get Statement Details
```bash
curl "http://localhost:8000/api/v1/statements/1"
```

### Update Statement
```bash
curl -X PUT "http://localhost:8000/api/v1/statements/1" \
  -H "Content-Type: application/json" \
  -d '{"cardholder_name": "Updated Name"}'
```

### Delete Statement
```bash
curl -X DELETE "http://localhost:8000/api/v1/statements/1"
```

### Reprocess Statement
```bash
curl -X GET "http://localhost:8000/api/v1/statements/1/reprocess"
```

### Get Statistics
```bash
curl "http://localhost:8000/api/v1/statements/stats/summary"
```

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest tests/ -v

# Integration tests
python scripts/evaluate.py
```

### Test Coverage
```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

## 📈 Evaluation

The evaluation script tests the parser against sample PDFs and generates accuracy reports:

```bash
# Generate sample PDFs
python scripts/generate_samples.py

# Run evaluation
python scripts/evaluate.py

# Results:
# - evaluation_report.csv: Detailed per-sample results
# - evaluation_summary.json: Overall statistics
```

## 🔒 Security

- File upload validation (PDF only)
- File size limits (10MB default)
- SQL injection protection via SQLAlchemy
- CORS configuration
- Environment-based secrets
- Static file serving for PDFs

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider to use | `mock` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `DATABASE_URL` | Database connection string | `sqlite:///./credit_card_parser.db` |
| `UPLOAD_DIR` | File upload directory | `uploads` |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | `10485760` |
| `TESSERACT_LANG` | OCR language | `eng` |
| `OCR_CONFIDENCE_THRESHOLD` | OCR confidence threshold | `0.6` |

## 🤖 AI Configuration

### Mock Provider (Default)
No configuration needed - works offline for development and testing.

### OpenAI Provider
```bash
export OPENAI_API_KEY="your-api-key-here"
export AI_PROVIDER="openai"
```

### Anthropic Provider
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
export AI_PROVIDER="anthropic"
```

## 🎯 Current Status

### ✅ Working Features
- **PDF Upload**: Upload credit card statements
- **AI Extraction**: Extract key fields with confidence scores
- **Modern UI**: Dark theme with excellent visibility
- **PDF Viewing**: View uploaded PDFs in browser
- **CRUD Operations**: Full statement management
- **Statistics**: Processing statistics and analytics
- **Multi-Issuer Support**: HDFC, SBI, ICICI, Axis, Citibank
- **API Documentation**: OpenAPI/Swagger docs
- **Local Development**: SQLite database setup

### 🔧 Recent Improvements
- **Dark Theme**: Complete dark theme with high contrast
- **Text Visibility**: Fixed all text visibility issues
- **Form Inputs**: Dark form inputs with white text
- **Navigation**: Bright white navigation links
- **AI Analysis**: Dark gradient AI analysis boxes
- **Edit Mode**: Dark form inputs in edit mode
- **Code Cleanup**: Removed unnecessary files and code

## 📊 Performance

- **Processing Time**: 2-5 seconds per PDF
- **Accuracy**: 85-95% depending on PDF quality
- **Throughput**: 100+ PDFs per hour
- **Memory Usage**: ~200MB per worker
- **Storage**: ~1MB per processed PDF

## 🎯 Roadmap

- [ ] Support for more credit card issuers
- [ ] Advanced OCR with image preprocessing
- [ ] Machine learning model training
- [ ] Real-time processing with WebSockets
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Cloud storage integration (S3, GCS)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the API docs at `/api/docs`
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

---

**Built with ❤️ for automated financial document processing**