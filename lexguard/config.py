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
    llm_provider: Literal["ollama", "openai"] = os.getenv("LLM_PROVIDER", "ollama")
    
    # OpenAI Configuration (optional if using Ollama)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Ollama Configuration
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Embedding Configuration
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    embedding_provider: Literal["sentence-transformers", "openai"] = os.getenv(
        "EMBEDDING_PROVIDER", "sentence-transformers"
    )

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


# Global settings instance
settings = Settings()

