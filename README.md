# ⚖️ LexGuard Contract AI

**AI-Powered Legal Contract Analysis with Risk Scoring, Clause Classification, and Interactive Q&A**

LexGuard is a comprehensive legal document analyzer that combines modern data engineering practices with LLM capabilities to help users understand contract risks, negotiate better terms, and get instant answers about their legal agreements.

---

## 🌟 Features

- **📄 PDF Document Ingestion**: Upload legal contracts (leases, NDAs, employment agreements) with automatic text extraction and OCR fallback
- **🎯 Intelligent Clause Classification**: Automatic categorization into termination, liability, payment, IP, non-compete, and more
- **⚠️ Risk Scoring**: AI-powered risk assessment with color-coded severity levels
- **💬 Contract Q&A Chat**: Ask questions about your contract in natural language using RAG (Retrieval-Augmented Generation)
- **📊 Interactive Dashboard**: Beautiful Streamlit UI with risk visualizations and clause explorer
- **📑 PDF Reports**: Generate professional lawyer-style risk reports with negotiation recommendations
- **🔍 Semantic Search**: ChromaDB-powered vector search for finding relevant clauses
- **🏗️ Production-Ready Architecture**: Clean separation of concerns with FastAPI backend and modular design

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                      │
│          (Upload, Dashboard, Chat, Report Download)          │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend                           │
│    /upload  /contracts  /chat  /risk  /report               │
└────┬───────────────┬───────────────┬─────────────────┬──────┘
     │               │               │                 │
┌────▼────┐  ┌──────▼──────┐  ┌────▼──────┐  ┌──────▼──────┐
│ Ingest  │  │     NLP     │  │    Risk   │  │   Reports   │
│ Pipeline│  │  Processing │  │  Scoring  │  │  Generator  │
│         │  │             │  │           │  │             │
│ • PDF   │  │ • Chunking  │  │ • Rule-   │  │ • Summary   │
│ • OCR   │  │ • Classify  │  │   based   │  │ • PDF Gen   │
│ • Clean │  │ • Embed     │  │ • LLM     │  │             │
└─────────┘  └──────┬──────┘  └───────────┘  └─────────────┘
                    │
             ┌──────▼───────┐
             │ Vector Store │
             │  (ChromaDB)  │
             └──────────────┘
```

---

## 🛠️ Tech Stack

### Backend & API
- **FastAPI** - Modern async Python web framework
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

### Data Engineering & NLP
- **pandas** - Data manipulation
- **pypdf** - PDF text extraction
- **pytesseract** - OCR support for scanned documents
- **sentence-transformers** - Local embedding generation
- **tiktoken** - Token counting and text chunking

### Vector Database & Search
- **ChromaDB** - Local vector database for semantic search
- **OpenAI Embeddings** - Alternative embedding provider

### LLM Integration
- **OpenAI API** - GPT models for analysis and chat
- Abstraction layer supporting multiple providers

### Frontend
- **Streamlit** - Interactive web dashboard

### Report Generation
- **ReportLab** - PDF generation

### Development Tools
- **Poetry** - Dependency management
- **pytest** - Testing framework
- **ruff** - Fast Python linter
- **black** - Code formatting

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- (Optional) Tesseract OCR for scanned PDFs

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lexguard-contract-ai
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   EMBEDDING_PROVIDER=sentence-transformers
   CHROMA_DB_PATH=./data/chroma
   DATA_DIR=./data
   ```

4. **Run the application**
   ```bash
   make run
   ```

   This starts both the FastAPI backend (port 8000) and Streamlit UI (port 8501) concurrently.

5. **Access the UI**
   
   Open your browser to: **http://localhost:8501**

---

## 📖 Usage

### Upload a Contract

1. Click **"Upload Contract"** in the sidebar
2. Select a PDF file (legal contract, NDA, lease, etc.)
3. Click **"Analyze Contract"**
4. Wait for processing (typically 10-30 seconds)

### View Risk Analysis

- Navigate to the **"Risk Overview"** tab
- See high/medium/low risk distribution
- Read AI-generated contract summary
- Review risk metrics

### Explore Clauses

- Go to **"Clause Details"** tab
- Filter by risk level
- Expand clauses to see:
  - Classification (termination, liability, payment, etc.)
  - Risk score and level
  - Full clause text

### Chat with Your Contract

- Switch to **"Chat"** tab
- Ask questions like:
  - "What are the termination conditions?"
  - "How much liability am I exposed to?"
  - "What are the payment terms?"
- Get AI-powered answers with relevant clause citations

### Download Risk Report

- Visit the **"Report"** tab
- Click **"Download PDF Report"**
- Receive a professional PDF with:
  - Executive summary
  - Risk breakdown
  - Clause-by-clause analysis
  - Negotiation recommendations

---

## 🗂️ Project Structure

```
lexguard-contract-ai/
├── lexguard/                   # Core Python package
│   ├── models/                 # Pydantic data models
│   │   ├── contract.py
│   │   ├── clause.py
│   │   └── risk.py
│   ├── ingest/                 # Document extraction & ETL
│   │   ├── pdf_extractor.py
│   │   ├── ocr_extractor.py
│   │   └── cleaner.py
│   ├── nlp/                    # NLP & embeddings
│   │   ├── chunker.py
│   │   ├── clause_classifier.py
│   │   ├── embedders.py
│   │   └── vector_store.py
│   ├── risk/                   # Risk assessment
│   │   ├── scoring.py
│   │   └── negotiation.py
│   ├── llm/                    # LLM abstraction
│   │   ├── base.py
│   │   ├── openai_client.py
│   │   └── prompts.py
│   ├── reports/                # Report generation
│   │   ├── summary_builder.py
│   │   └── pdf_report.py
│   ├── storage/                # Data persistence
│   │   ├── file_store.py
│   │   ├── chroma_store.py
│   │   └── schema.py
│   └── config.py               # Configuration management
├── backend/                    # FastAPI application
│   ├── main.py
│   └── routes/
│       ├── upload.py
│       ├── contract.py
│       └── chat.py
├── app/                        # Streamlit frontend
│   └── streamlit_app.py
├── tests/                      # Test suite
│   ├── test_chunker.py
│   ├── test_risk_scoring.py
│   └── test_end_to_end_dummy.py
├── pyproject.toml              # Poetry dependencies
├── Makefile                    # Development commands
└── README.md
```

---

## 🔬 How It Works

### 1. Document Ingestion Pipeline

```python
PDF Upload → Text Extraction (pypdf) → OCR Fallback → Text Cleaning → Ready for Analysis
```

- Extracts text from PDFs using `pypdf`
- Falls back to OCR for scanned documents
- Cleans headers, footers, and normalizes whitespace

### 2. Clause Identification & Classification

```python
Contract Text → Smart Chunking → Rule-Based Classification → (Optional) LLM Refinement → Classified Clauses
```

- Splits text using numbered sections, paragraphs, and legal patterns
- Classifies clauses using keyword matching
- Optional LLM refinement for ambiguous cases

### 3. Risk Assessment

```python
Clause + Type → Heuristic Scoring → LLM Enhancement → Risk Score (0-1) → Risk Level (low/medium/high)
```

**Risk Factors:**
- **Liability**: Unlimited terms, indemnification, no caps
- **Termination**: Short notice, immediate termination, "without cause"
- **Non-Compete**: Long duration (>12 months), broad geography
- **IP**: Broad assignment, no pre-existing IP carveouts
- **Payment**: Unpaid positions, at-will terms

### 4. Vector Search & RAG

```python
User Query → Generate Embedding → Search ChromaDB → Retrieve Top-K Clauses → Build Context → LLM Answer
```

- Embeds clauses using `sentence-transformers` or OpenAI
- Stores embeddings in ChromaDB for fast semantic search
- Retrieves relevant clauses for user queries
- Augments LLM prompt with context for accurate answers

### 5. Report Generation

```python
Contract Data → Summary Builder → Risk Aggregation → PDF Layout (ReportLab) → Professional Report
```

---

## 🧪 Testing

Run the test suite:

```bash
make test
```

Or with pytest directly:

```bash
poetry run pytest -v
```

**Test Coverage:**
- Chunking algorithms
- Risk scoring logic
- Clause classification
- End-to-end pipeline
- Data persistence

---

## 🛡️ Development Commands

```bash
make setup    # Install dependencies
make api      # Run FastAPI backend only
make ui       # Run Streamlit UI only
make run      # Run both concurrently
make lint     # Run ruff linter
make format   # Format code with black
make test     # Run pytest
make clean    # Remove data and cache files
```

---

## 🔮 Future Enhancements

### Features
- [ ] Multi-document comparison
- [ ] Contract templates library
- [ ] Jurisdiction-specific analysis
- [ ] Multi-language support
- [ ] Clause redlining suggestions
- [ ] Version tracking and diffs

### Technical Improvements
- [ ] User authentication & multi-tenancy
- [ ] PostgreSQL for contract metadata
- [ ] Background task queue (Celery/Redis)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Alternative LLM providers (Anthropic, Llama)

---

## 📝 API Documentation

Once the backend is running, visit:

**http://localhost:8000/docs**

Interactive Swagger UI with all endpoints documented.

### Key Endpoints

- `POST /api/upload` - Upload and process contract
- `GET /api/contracts/{id}` - Get contract details
- `GET /api/contracts/{id}/clauses` - List all clauses
- `GET /api/contracts/{id}/risk` - Get risk assessment
- `POST /api/contracts/{id}/chat` - Chat with contract
- `GET /api/contracts/{id}/report` - Download PDF report

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run `make lint` and `make test`
6. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- OpenAI for LLM capabilities
- ChromaDB team for excellent vector database
- Streamlit for rapid UI development
- The open-source Python community

---

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ using modern data engineering and AI best practices**


