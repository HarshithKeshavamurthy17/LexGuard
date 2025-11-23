# LexGuard Setup Guide

## Quick Setup Instructions

### 1. Environment Setup

Create a `.env` file in the project root with the following content:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_PROVIDER=sentence-transformers  # or "openai"

# Storage Configuration
CHROMA_DB_PATH=./data/chroma
DATA_DIR=./data

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit Configuration
STREAMLIT_PORT=8501
```

### 2. Install Dependencies

```bash
poetry install
```

If you don't have Poetry installed:
```bash
pip install poetry
```

### 3. (Optional) Install Tesseract OCR

For scanned PDF support:

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 4. Run the Application

```bash
make run
```

Or run services separately:
```bash
# Terminal 1 - Backend
make api

# Terminal 2 - Frontend
make ui
```

### 5. Access the Application

- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running commands through Poetry:
```bash
poetry run python -m pytest
poetry run uvicorn backend.main:app
```

### ChromaDB Issues

If ChromaDB fails to initialize:
```bash
rm -rf data/chroma
mkdir -p data/chroma
```

### OpenAI API Errors

Verify your API key:
```bash
echo $OPENAI_API_KEY
```

Test with a simple API call or check https://platform.openai.com/api-keys

### Port Already in Use

If port 8000 or 8501 is taken:
```bash
# Kill process on port
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

Or change ports in `.env` file.

## Development Workflow

### Running Tests
```bash
make test
```

### Code Quality
```bash
make lint     # Check code quality
make format   # Auto-format code
```

### Clean Up
```bash
make clean    # Remove data and cache
```

## Project Structure Overview

```
lexguard-contract-ai/
├── lexguard/          # Core library
├── backend/           # FastAPI server
├── app/               # Streamlit UI
├── tests/             # Test suite
├── data/              # Generated at runtime
│   ├── contracts/     # Stored contracts
│   ├── uploads/       # Uploaded PDFs
│   ├── reports/       # Generated reports
│   └── chroma/        # Vector database
└── pyproject.toml     # Dependencies
```

## Next Steps

1. Upload a sample contract PDF
2. Explore the risk analysis
3. Try the chat feature
4. Download a PDF report

Enjoy using LexGuard! 🚀



