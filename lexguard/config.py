"""Configuration management for LexGuard."""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # LLM Configuration
    llm_provider: Literal["ollama", "openai", "gemini"] = os.getenv("LLM_PROVIDER", "gemini")
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Ollama Configuration
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Embedding Configuration
    embedding_provider: Literal["sentence-transformers", "openai", "gemini"] = os.getenv(
        "EMBEDDING_PROVIDER", "sentence-transformers"
    )
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "")

    # Storage Configuration
    chroma_db_path: Path = Path(os.getenv("CHROMA_DB_PATH", "./data/chroma"))
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        """Initialize settings and create necessary directories."""
        super().__init__(**kwargs)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_db_path.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "contracts").mkdir(exist_ok=True)
        (self.data_dir / "uploads").mkdir(exist_ok=True)
        (self.data_dir / "reports").mkdir(exist_ok=True)

        # Ensure sensible defaults for embedding models per provider
        if self.embedding_provider == "sentence-transformers":
            if not self.embedding_model or self.embedding_model.startswith("models/"):
                self.embedding_model = "all-MiniLM-L6-v2"
        elif self.embedding_provider == "openai":
            if not self.embedding_model:
                self.embedding_model = "text-embedding-3-small"
        else:  # gemini
            if not self.embedding_model:
                self.embedding_model = "models/embedding-001"


# Global settings instance
settings = Settings()
