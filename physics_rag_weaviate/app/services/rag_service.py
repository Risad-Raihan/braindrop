"""
Main RAG Service for Physics RAG System with Weaviate
Combines embedding, search, and generation services
"""

import asyncio
import logging
from typing import Dict, List, Optional
import time
from pathlib import Path

from .embedding_service import EmbeddingService
from .search_service import WeaviateSearchService
from .generation_service import GenerationService
from ..config.settings import Settings

logger = logging.getLogger(__name__)


class WeaviateRAGService:
    """Main RAG service that orchestrates all Weaviate components"""
    
    def __init__(self, settings: Settings):
        """
        Initialize the Weaviate RAG service
        
        Args:
            settings (Settings): Application settings
        """
        self.settings = settings
        
        # Validate configuration
        settings.validate_api_key()
        settings.validate_weaviate_config()
        
        # Initialize services
        logger.info("Initializing Weaviate RAG services...")
        
        self.embedding_service = EmbeddingService(settings.GOOGLE_API_KEY)
        
        self.search_service = WeaviateSearchService(
            weaviate_url=settings.WEAVIATE_URL,
            weaviate_api_key=settings.WEAVIATE_API_KEY,
            collection_name=settings.WEAVIATE_COLLECTION,
            use_local=settings.USE_LOCAL_WEAVIATE
        )
        
        self.generation_service = GenerationService(
            settings.GOOGLE_API_KEY,
            settings.GENERATION_MODEL
        )
        
        self._initialized = False
        logger.info("Weaviate RAG services initialized successfully")
    
    async def initialize_collection(self, force_reset: bool = False) -> bool:
        """
        Initialize the Weaviate collection with physics data
        
        Args:
            force_reset (bool): Whether to reset existing collection
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info("Initializing Weaviate collection with physics data...")
            
            # Reset collection if requested
            if force_reset:
                self.search_service.reset_collection()
            
            # Check if collection already has data
            stats = self.search_service.get_collection_stats()
            if stats.get('total_documents', 0) > 0 and not force_reset:
                logger.info(f"Collection already contains {stats['total_documents']} documents")
                self._initialized = True
                return True
            
            # Load physics text and create chunks
            physics_text_path = Path(self.settings.PHYSICS_TEXT_PATH)
            if not physics_text_path.exists():
                self.settings.validate_physics_text()  # This will update the path or raise error
                physics_text_path = Path(self.settings.PHYSICS_TEXT_PATH)
            
            with open(physics_text_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks using the same method as notebook
            chunks = [t.strip() for t in content.split('*****') if t.strip()]
            logger.info(f"Created {len(chunks)} chunks from physics text")
            
            # Generate embeddings for all chunks
            embeddings = self.embedding_service.get_batch_embeddings(chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")
            
            # Insert into Weaviate
            success = self.search_service.insert_documents(chunks, embeddings)
            
            if success:
                self._initialized = True
                logger.info(f"Successfully initialized collection with {len(chunks)} documents")
                return True
            else:
                logger.error("Failed to insert documents into Weaviate")
                return False
            
        except Exception as e:
            logger.error(f"Error initializing collection: {str(e)}")
            return False
    
    async def search(self, query: str, 
                    search_type: str = "hybrid",
                    top_k: Optional[int] = None,
                    alpha: Optional[float] = None) -> List[Dict]:
        """
        Perform search using Weaviate
        
        Args:
            query (str): Search query
            search_type (str): Type of search ("hybrid", "vector", "keyword")
            top_k (Optional[int]): Number of results to return
            alpha (Optional[float]): Alpha for hybrid search (vector vs keyword balance)
            
        Returns:
            List[Dict]: Search results
        """
        if not self._initialized:
            await self.initialize_collection()
        
        if top_k is None:
            top_k = self.settings.DEFAULT_TOP_K
        
        if alpha is None:
            alpha = self.settings.HYBRID_ALPHA
        
        start_time = time.time()
        
        try:
            logger.info(f"Performing {search_type} search for query: {query[:50]}...")
            
            if search_type == "hybrid":
                # Get query embedding for hybrid search
                query_embedding = self.embedding_service.get_query_embedding(query)
                results = self.search_service.hybrid_search(
                    query_text=query,
                    query_vector=query_embedding,
                    alpha=alpha,
                    limit=top_k
                )
            elif search_type == "vector":
                # Pure vector search
                query_embedding = self.embedding_service.get_query_embedding(query)
                results = self.search_service.vector_search(
                    query_vector=query_embedding,
                    limit=top_k
                )
            elif search_type == "keyword":
                # Pure keyword search
                results = self.search_service.keyword_search(
                    query_text=query,
                    limit=top_k
                )
            else:
                raise ValueError(f"Invalid search_type: {search_type}")
            
            search_time = time.time() - start_time
            
            # Add timing information
            for result in results:
                result['search_time'] = search_time
                result['search_type'] = search_type
            
            logger.info(f"{search_type.title()} search completed in {search_time:.3f}s, returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in {search_type} search: {str(e)}")
            raise
    
    async def chat(self, message: str, 
                  include_sources: bool = True,
                  search_type: str = "hybrid",
                  top_k: Optional[int] = None) -> Dict:
        """
        Perform RAG-based chat using Weaviate
        
        Args:
            message (str): User message/question
            include_sources (bool): Whether to include source information
            search_type (str): Type of search to use
            top_k (Optional[int]): Number of search results to consider
            
        Returns:
            Dict: Chat response with generated answer and sources
        """
        if top_k is None:
            top_k = self.settings.DEFAULT_TOP_K
        
        start_time = time.time()
        
        try:
            logger.info(f"Processing chat message: {message[:50]}...")
            
            # Step 1: Search for relevant context
            search_results = await self.search(message, search_type=search_type, top_k=top_k)
            
            if not search_results:
                return {
                    'response': "দুঃখিত, এই প্রশ্নের জন্য কোনো প্রাসঙ্গিক তথ্য পাওয়া যায়নি।",
                    'sources': [],
                    'confidence': 0.0,
                    'total_time': time.time() - start_time,
                    'search_type': search_type
                }
            
            # Step 2: Generate response with sources
            if include_sources:
                result = self.generation_service.generate_with_sources(message, search_results)
            else:
                # Use only the top result for context
                context = search_results[0]['content']
                response_text = self.generation_service.generate_response(message, context)
                result = {
                    'response': response_text,
                    'sources': [],
                    'confidence': search_results[0].get('score', 0.0)
                }
            
            # Add timing and metadata
            result['total_time'] = time.time() - start_time
            result['search_results_count'] = len(search_results)
            result['search_type'] = search_type
            result['message'] = message
            
            logger.info(f"Chat completed in {result['total_time']:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return {
                'response': "দুঃখিত, উত্তর তৈরি করতে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
                'sources': [],
                'confidence': 0.0,
                'total_time': time.time() - start_time,
                'search_type': search_type,
                'error': str(e)
            }
    
    async def explain_concept(self, concept: str, top_k: Optional[int] = None) -> Dict:
        """
        Generate detailed explanation for a physics concept
        
        Args:
            concept (str): Physics concept to explain
            top_k (Optional[int]): Number of search results to consider
            
        Returns:
            Dict: Detailed explanation with sources
        """
        if top_k is None:
            top_k = 3  # Use fewer results for concept explanation
        
        try:
            logger.info(f"Generating explanation for concept: {concept}")
            
            # Search for relevant context using hybrid search
            search_results = await self.search(concept, search_type="hybrid", top_k=top_k)
            
            if not search_results:
                return {
                    'explanation': f"'{concept}' সম্পর্কে কোনো তথ্য পাওয়া যায়নি।",
                    'sources': []
                }
            
            # Use multiple contexts for richer explanation
            contexts = [result['content'] for result in search_results[:2]]
            explanation = self.generation_service.generate_multi_context_response(concept, contexts)
            
            return {
                'explanation': explanation,
                'sources': search_results[:2],  # Top 2 sources
                'concept': concept
            }
            
        except Exception as e:
            logger.error(f"Error generating concept explanation: {str(e)}")
            return {
                'explanation': f"'{concept}' সম্পর্কে ব্যাখ্যা তৈরি করতে সমস্যা হয়েছে।",
                'sources': [],
                'error': str(e)
            }
    
    async def get_similar_content(self, text: str, top_k: int = 5) -> List[Dict]:
        """
        Find content similar to given text using vector search
        
        Args:
            text (str): Reference text
            top_k (int): Number of similar contents to return
            
        Returns:
            List[Dict]: Similar content results
        """
        try:
            # Use vector search to find similar content
            results = await self.search(text, search_type="vector", top_k=top_k)
            
            # Format for similarity response
            similar_content = []
            for result in results:
                similar_content.append({
                    'content': result['content'],
                    'similarity_score': result['score'],
                    'doc_id': result['doc_id']
                })
            
            return similar_content
            
        except Exception as e:
            logger.error(f"Error finding similar content: {str(e)}")
            return []
    
    def get_service_stats(self) -> Dict:
        """
        Get statistics about the RAG service
        
        Returns:
            Dict: Service statistics
        """
        try:
            weaviate_stats = self.search_service.get_collection_stats()
            
            return {
                'service_status': 'healthy',
                'initialized': self._initialized,
                'total_documents': weaviate_stats.get('total_documents', 0),
                'collection_name': weaviate_stats.get('collection_name', ''),
                'weaviate_url': weaviate_stats.get('weaviate_url', ''),
                'use_local_weaviate': weaviate_stats.get('use_local', False),
                'models': {
                    'embedding': self.settings.EMBEDDING_MODEL,
                    'generation': self.settings.GENERATION_MODEL
                },
                'configuration': {
                    'default_top_k': self.settings.DEFAULT_TOP_K,
                    'hybrid_alpha': self.settings.HYBRID_ALPHA,
                    'max_response_tokens': self.settings.MAX_RESPONSE_TOKENS
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting service stats: {str(e)}")
            return {
                'service_status': 'error',
                'error': str(e)
            }
    
    async def health_check(self) -> Dict:
        """
        Perform health check on all services
        
        Returns:
            Dict: Health check results
        """
        health_status = {
            'status': 'healthy',
            'services': {},
            'timestamp': time.time()
        }
        
        try:
            # Test embedding service
            test_embedding = self.embedding_service.get_single_embedding("test")
            health_status['services']['embedding'] = {
                'status': 'healthy' if test_embedding else 'unhealthy',
                'dimension': len(test_embedding) if test_embedding else None
            }
            
        except Exception as e:
            health_status['services']['embedding'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        try:
            # Test Weaviate service
            stats = self.search_service.get_collection_stats()
            health_status['services']['weaviate'] = {
                'status': 'healthy',
                'document_count': stats.get('total_documents', 0),
                'collection_name': stats.get('collection_name', ''),
                'url': stats.get('weaviate_url', '')
            }
            
        except Exception as e:
            health_status['services']['weaviate'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        try:
            # Test generation service
            test_response = self.generation_service.generate_simple_response(
                "test", "test context"
            )
            health_status['services']['generation'] = {
                'status': 'healthy' if test_response else 'unhealthy'
            }
            
        except Exception as e:
            health_status['services']['generation'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        return health_status
    
    def close(self):
        """Close all service connections"""
        try:
            self.search_service.close()
            logger.info("RAG service connections closed")
        except Exception as e:
            logger.error(f"Error closing RAG service: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure connections are closed"""
        self.close()
