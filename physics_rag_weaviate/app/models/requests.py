"""
Request models for Physics RAG API with Weaviate
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class SearchRequest(BaseModel):
    """Request model for search endpoint"""
    query: str = Field(..., description="Search query", min_length=1, max_length=500)
    search_type: Literal["hybrid", "vector", "keyword"] = Field("hybrid", description="Type of search to perform")
    top_k: Optional[int] = Field(5, description="Number of results to return", ge=1, le=20)
    alpha: Optional[float] = Field(0.5, description="Alpha for hybrid search (0.0=keyword, 1.0=vector)", ge=0.0, le=1.0)


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User message/question", min_length=1, max_length=500)
    include_sources: Optional[bool] = Field(True, description="Include source information in response")
    search_type: Literal["hybrid", "vector", "keyword"] = Field("hybrid", description="Type of search to use")
    top_k: Optional[int] = Field(5, description="Number of search results to consider", ge=1, le=10)


class ConceptRequest(BaseModel):
    """Request model for concept explanation endpoint"""
    concept: str = Field(..., description="Physics concept to explain", min_length=1, max_length=100)
    top_k: Optional[int] = Field(3, description="Number of search results to consider", ge=1, le=5)


class SimilarityRequest(BaseModel):
    """Request model for similarity search endpoint"""
    text: str = Field(..., description="Reference text for similarity search", min_length=1, max_length=1000)
    top_k: Optional[int] = Field(5, description="Number of similar contents to return", ge=1, le=10)


class InitializeRequest(BaseModel):
    """Request model for collection initialization"""
    force_reset: Optional[bool] = Field(False, description="Force reset existing collection")
