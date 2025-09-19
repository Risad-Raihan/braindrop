"""
Configuration settings for Physics RAG API with Weaviate
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings for Weaviate-based RAG"""
    
    # API Configuration
    API_TITLE: str = "Physics RAG API with Weaviate"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Bengali Physics RAG System using Weaviate Vector Database"
    
    # Google AI Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "your_actual_google_api_key_here")
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    GENERATION_MODEL: str = "gemini-2.5-flash"
    
    # Weaviate Configuration
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "your_weaviate_cluster_url_here")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY", "your_weaviate_api_key_here")
    WEAVIATE_COLLECTION: str = "PhysicsChunk"
    USE_LOCAL_WEAVIATE: bool = os.getenv("USE_LOCAL_WEAVIATE", "false").lower() == "true"
    
    # File Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    PHYSICS_TEXT_PATH: str = str(Path(__file__).parent.parent.parent.parent / "Physics" / "combined_physics.md")
    
    # Search Configuration
    DEFAULT_TOP_K: int = 5
    HYBRID_ALPHA: float = 0.5  # Balance between vector (1.0) and keyword (0.0) search
    
    # Generation Configuration
    MAX_RESPONSE_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3000",
        "http://localhost:3002",  # Another alternative port
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "https://*.vercel.app",  # Vercel deployments
        "https://braindrop.vercel.app",  # Production frontend
        "https://braindrop-*.vercel.app",  # Preview deployments
    ]
    
    # Health Check
    HEALTH_CHECK_TIMEOUT: int = 5
    
    @classmethod
    def validate_physics_text(cls) -> bool:
        """Validate that physics text file exists"""
        physics_path = Path(cls.PHYSICS_TEXT_PATH)
        
        if not physics_path.exists():
            # Try alternative paths
            alternative_paths = [
                Path(__file__).parent.parent.parent.parent / "Physics" / "combined_physics.md",
                Path.cwd() / "Physics" / "combined_physics.md",
                Path("/home/risad/projects/physics_embedding/Physics/combined_physics.md")
            ]
            
            for alt_path in alternative_paths:
                if alt_path.exists():
                    cls.PHYSICS_TEXT_PATH = str(alt_path)
                    return True
            
            raise FileNotFoundError(f"Physics text file not found. Searched paths: {[str(p) for p in alternative_paths]}")
        
        return True
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate that Google API key is set"""
        if not cls.GOOGLE_API_KEY or cls.GOOGLE_API_KEY == "GOOGLE_API":
            raise ValueError("GOOGLE_API_KEY must be set to a valid Google AI API key")
        return True
    
    @classmethod
    def validate_weaviate_config(cls) -> bool:
        """Validate Weaviate configuration"""
        if not cls.WEAVIATE_URL:
            raise ValueError("WEAVIATE_URL must be set")
        
        # For cloud Weaviate, API key is required
        if not cls.USE_LOCAL_WEAVIATE and not cls.WEAVIATE_API_KEY:
            raise ValueError("WEAVIATE_API_KEY is required for cloud Weaviate")
        
        return True
    
    @classmethod
    def get_weaviate_config(cls) -> dict:
        """Get Weaviate configuration as dictionary"""
        return {
            'url': cls.WEAVIATE_URL,
            'api_key': cls.WEAVIATE_API_KEY,
            'collection_name': cls.WEAVIATE_COLLECTION,
            'use_local': cls.USE_LOCAL_WEAVIATE
        }


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings


def setup_for_localhost():
    """Configure settings for localhost Weaviate"""
    settings.WEAVIATE_URL = "http://localhost:8080"
    settings.WEAVIATE_API_KEY = ""
    settings.USE_LOCAL_WEAVIATE = True
    return settings


def setup_for_cloud(weaviate_url: str, weaviate_api_key: str):
    """Configure settings for Weaviate Cloud"""
    settings.WEAVIATE_URL = weaviate_url
    settings.WEAVIATE_API_KEY = weaviate_api_key
    settings.USE_LOCAL_WEAVIATE = False
    return settings
