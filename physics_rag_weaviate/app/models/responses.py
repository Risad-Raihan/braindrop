"""
Response models for Physics RAG API with Weaviate
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
import time


class SearchResult(BaseModel):
    """Individual search result from Weaviate"""
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Search relevance score")
    rank: int = Field(..., description="Result rank")
    doc_id: int = Field(..., description="Document ID")
    search_type: str = Field(..., description="Type of search used")
    search_time: Optional[float] = Field(None, description="Search time in seconds")


class SearchResponse(BaseModel):
    """Response model for search endpoint"""
    results: List[SearchResult] = Field(..., description="Search results")
    query: str = Field(..., description="Original query")
    search_type: str = Field(..., description="Type of search performed")
    total_results: int = Field(..., description="Total number of results")
    search_time: Optional[float] = Field(None, description="Total search time in seconds")


class SourceInfo(BaseModel):
    """Source information for chat responses"""
    content_preview: str = Field(..., description="Preview of source content")
    score: float = Field(..., description="Relevance score")
    doc_id: Optional[int] = Field(None, description="Document ID")
    rank: int = Field(..., description="Source rank")
    search_type: str = Field(..., description="Type of search used")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Generated response")
    sources: List[SourceInfo] = Field(default_factory=list, description="Source information")
    confidence: float = Field(..., description="Response confidence score", ge=0.0, le=1.0)
    total_time: float = Field(..., description="Total processing time in seconds")
    search_results_count: int = Field(..., description="Number of search results used")
    search_type: str = Field(..., description="Type of search used")
    message: str = Field(..., description="Original user message")


class ConceptResponse(BaseModel):
    """Response model for concept explanation endpoint"""
    explanation: str = Field(..., description="Detailed concept explanation")
    concept: str = Field(..., description="Original concept")
    sources: List[SearchResult] = Field(default_factory=list, description="Supporting sources")


class SimilarContent(BaseModel):
    """Similar content item"""
    content: str = Field(..., description="Similar content")
    similarity_score: float = Field(..., description="Similarity score")
    doc_id: int = Field(..., description="Document ID")


class SimilarityResponse(BaseModel):
    """Response model for similarity search endpoint"""
    similar_content: List[SimilarContent] = Field(..., description="Similar content results")
    reference_text: str = Field(..., description="Original reference text")
    total_results: int = Field(..., description="Total number of similar content found")


class ServiceStats(BaseModel):
    """Service statistics"""
    service_status: str = Field(..., description="Overall service status")
    initialized: bool = Field(..., description="Whether the service is initialized")
    total_documents: Optional[int] = Field(None, description="Total number of documents")
    collection_name: Optional[str] = Field(None, description="Weaviate collection name")
    weaviate_url: Optional[str] = Field(None, description="Weaviate URL")
    use_local_weaviate: Optional[bool] = Field(None, description="Whether using local Weaviate")
    models: Optional[Dict[str, str]] = Field(None, description="Model information")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Service configuration")


class HealthCheckService(BaseModel):
    """Health check for individual service"""
    status: str = Field(..., description="Service status")
    error: Optional[str] = Field(None, description="Error message if unhealthy")
    document_count: Optional[int] = Field(None, description="Document count for Weaviate service")
    dimension: Optional[int] = Field(None, description="Embedding dimension")
    collection_name: Optional[str] = Field(None, description="Collection name")
    url: Optional[str] = Field(None, description="Service URL")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Overall health status")
    services: Dict[str, HealthCheckService] = Field(..., description="Individual service health")
    timestamp: float = Field(default_factory=time.time, description="Health check timestamp")


class InitializeResponse(BaseModel):
    """Response model for collection initialization"""
    success: bool = Field(..., description="Whether initialization was successful")
    message: str = Field(..., description="Status message")
    documents_count: Optional[int] = Field(None, description="Number of documents initialized")
    collection_name: str = Field(..., description="Collection name")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: float = Field(default_factory=time.time, description="Error timestamp")
    service: Optional[str] = Field(None, description="Service that caused the error")
