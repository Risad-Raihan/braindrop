"""
FastAPI application for Physics RAG System with Weaviate
"""

import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config.settings import get_settings, Settings
from .services.rag_service import WeaviateRAGService
from .models.requests import (
    SearchRequest, ChatRequest, ConceptRequest, 
    SimilarityRequest, InitializeRequest
)
from .models.responses import (
    SearchResponse, ChatResponse, ConceptResponse,
    SimilarityResponse, ServiceStats, HealthCheckResponse,
    InitializeResponse, ErrorResponse
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global RAG service instance
rag_service: WeaviateRAGService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global rag_service
    
    try:
        # Startup
        logger.info("Starting Physics RAG API with Weaviate...")
        settings = get_settings()
        rag_service = WeaviateRAGService(settings)
        logger.info("RAG service initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {str(e)}")
        raise
    finally:
        # Shutdown
        if rag_service:
            rag_service.close()
        logger.info("Physics RAG API shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Physics RAG API with Weaviate",
    description="Bengali Physics RAG System using Weaviate Vector Database",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_rag_service() -> WeaviateRAGService:
    """Dependency to get RAG service instance"""
    if rag_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service not initialized"
        )
    return rag_service


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            service="api"
        ).dict()
    )


@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Physics RAG API with Weaviate",
        "version": "1.0.0",
        "description": "Bengali Physics RAG System using Weaviate Vector Database",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheckResponse, summary="Health check")
async def health_check(service: WeaviateRAGService = Depends(get_rag_service)):
    """Comprehensive health check for all services"""
    try:
        health_result = await service.health_check()
        
        if health_result['status'] == 'healthy':
            return HealthCheckResponse(**health_result)
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=health_result
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


@app.get("/stats", response_model=ServiceStats, summary="Service statistics")
async def get_stats(service: WeaviateRAGService = Depends(get_rag_service)):
    """Get service statistics and configuration"""
    try:
        stats = service.get_service_stats()
        return ServiceStats(**stats)
    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@app.post("/initialize", response_model=InitializeResponse, summary="Initialize collection")
async def initialize_collection(
    request: InitializeRequest,
    service: WeaviateRAGService = Depends(get_rag_service)
):
    """Initialize Weaviate collection with physics data"""
    try:
        logger.info(f"Initializing collection, force_reset: {request.force_reset}")
        
        success = await service.initialize_collection(force_reset=request.force_reset)
        
        if success:
            stats = service.get_service_stats()
            return InitializeResponse(
                success=True,
                message="Collection initialized successfully",
                documents_count=stats.get('total_documents', 0),
                collection_name=stats.get('collection_name', '')
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize collection"
            )
            
    except Exception as e:
        logger.error(f"Collection initialization failed: {str(e)}")
        return InitializeResponse(
            success=False,
            message=f"Initialization failed: {str(e)}",
            collection_name=get_settings().WEAVIATE_COLLECTION
        )


@app.post("/search", response_model=SearchResponse, summary="Search physics content")
async def search_physics(
    request: SearchRequest,
    service: WeaviateRAGService = Depends(get_rag_service)
):
    """Search for physics content using hybrid, vector, or keyword search"""
    try:
        logger.info(f"Search request: {request.query[:50]}... (type: {request.search_type})")
        
        results = await service.search(
            query=request.query,
            search_type=request.search_type,
            top_k=request.top_k,
            alpha=request.alpha
        )
        
        return SearchResponse(
            results=results,
            query=request.query,
            search_type=request.search_type,
            total_results=len(results),
            search_time=results[0].get('search_time') if results else None
        )
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse, summary="Chat with physics assistant")
async def chat_physics(
    request: ChatRequest,
    service: WeaviateRAGService = Depends(get_rag_service)
):
    """Chat with the physics assistant using RAG"""
    try:
        logger.info(f"Chat request: {request.message[:50]}...")
        
        response = await service.chat(
            message=request.message,
            include_sources=request.include_sources,
            search_type=request.search_type,
            top_k=request.top_k
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@app.post("/explain", response_model=ConceptResponse, summary="Explain physics concept")
async def explain_concept(
    request: ConceptRequest,
    service: WeaviateRAGService = Depends(get_rag_service)
):
    """Get detailed explanation of a physics concept"""
    try:
        logger.info(f"Concept explanation request: {request.concept}")
        
        response = await service.explain_concept(
            concept=request.concept,
            top_k=request.top_k
        )
        
        return ConceptResponse(**response)
        
    except Exception as e:
        logger.error(f"Concept explanation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Concept explanation failed: {str(e)}"
        )


@app.post("/similar", response_model=SimilarityResponse, summary="Find similar content")
async def find_similar(
    request: SimilarityRequest,
    service: WeaviateRAGService = Depends(get_rag_service)
):
    """Find content similar to the provided text"""
    try:
        logger.info(f"Similarity search request: {request.text[:50]}...")
        
        similar_content = await service.get_similar_content(
            text=request.text,
            top_k=request.top_k
        )
        
        return SimilarityResponse(
            similar_content=similar_content,
            reference_text=request.text,
            total_results=len(similar_content)
        )
        
    except Exception as e:
        logger.error(f"Similarity search failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Similarity search failed: {str(e)}"
        )


# Development endpoints
@app.get("/debug/config", summary="Debug: Show configuration")
async def debug_config():
    """Debug endpoint to show current configuration"""
    settings = get_settings()
    return {
        "weaviate_url": settings.WEAVIATE_URL,
        "use_local_weaviate": settings.USE_LOCAL_WEAVIATE,
        "collection_name": settings.WEAVIATE_COLLECTION,
        "embedding_model": settings.EMBEDDING_MODEL,
        "generation_model": settings.GENERATION_MODEL,
        "api_key_set": bool(settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "GOOGLE_API")
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
