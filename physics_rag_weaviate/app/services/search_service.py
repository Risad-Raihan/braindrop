"""
Search Service for Physics RAG System with Weaviate
Handles Weaviate hybrid search (vector + keyword)
"""

import weaviate
from weaviate.classes.config import Configure
from typing import List, Dict, Optional, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class WeaviateSearchService:
    """Service for hybrid search using Weaviate"""
    
    def __init__(self, 
                 weaviate_url: str, 
                 weaviate_api_key: str,
                 collection_name: str = "PhysicsChunk",
                 use_local: bool = False):
        """
        Initialize the Weaviate search service
        
        Args:
            weaviate_url (str): Weaviate cluster URL or localhost URL
            weaviate_api_key (str): Weaviate API key (can be empty for localhost)
            collection_name (str): Name of the Weaviate collection
            use_local (bool): Whether to use local Weaviate instance
        """
        self.weaviate_url = weaviate_url
        self.weaviate_api_key = weaviate_api_key
        self.collection_name = collection_name
        self.use_local = use_local
        
        # Initialize Weaviate client
        self.client = self._connect_to_weaviate()
        
        # Get or create collection
        self.collection = self._setup_collection()
        
        logger.info(f"WeaviateSearchService initialized with collection: {collection_name}")
    
    def _connect_to_weaviate(self) -> weaviate.WeaviateClient:
        """Connect to Weaviate instance"""
        try:
            if self.use_local:
                # Connect to local Weaviate instance
                host = self.weaviate_url.replace('http://', '').replace('https://', '')
                if ':' in host:
                    host = host.split(':')[0]  # Remove port from URL if present
                client = weaviate.connect_to_local(
                    host=host,
                    port=8080,
                    grpc_port=50051
                )
                logger.info(f"Connected to local Weaviate at {self.weaviate_url}")
            else:
                # Connect to Weaviate Cloud
                client = weaviate.connect_to_weaviate_cloud(
                    cluster_url=self.weaviate_url,
                    auth_credentials=weaviate.auth.AuthApiKey(self.weaviate_api_key)
                )
                logger.info(f"Connected to Weaviate Cloud at {self.weaviate_url}")
            
            return client
            
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {str(e)}")
            raise
    
    def _setup_collection(self) -> Any:
        """Setup or get existing collection"""
        try:
            # Check if collection exists
            if self.client.collections.exists(self.collection_name):
                logger.info(f"Using existing collection: {self.collection_name}")
                return self.client.collections.get(self.collection_name)
            
            # Create new collection
            logger.info(f"Creating new collection: {self.collection_name}")
            self.client.collections.create(
                self.collection_name,
                vector_config=Configure.VectorIndex.hnsw(),
                # Note: Using newer API, no vectorizer_config needed since we provide vectors
            )
            
            return self.client.collections.get(self.collection_name)
            
        except Exception as e:
            logger.error(f"Failed to setup collection: {str(e)}")
            raise
    
    def insert_documents(self, documents: List[str], embeddings: List[List[float]]) -> bool:
        """
        Insert documents with embeddings into Weaviate
        
        Args:
            documents (List[str]): List of document texts
            embeddings (List[List[float]]): List of embedding vectors
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Inserting {len(documents)} documents into Weaviate")
            
            # Insert documents with embeddings
            with self.collection.batch.dynamic() as batch:
                for i, (doc, emb) in enumerate(zip(documents, embeddings)):
                    batch.add_object(
                        properties={"text": doc, "doc_id": i},
                        vector=emb
                    )
            
            logger.info(f"Successfully inserted {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting documents: {str(e)}")
            raise
    
    def hybrid_search(self, 
                     query_text: str, 
                     query_vector: List[float], 
                     alpha: float = 0.5,
                     limit: int = 5) -> List[Dict]:
        """
        Perform hybrid search (vector + keyword) using Weaviate
        
        Args:
            query_text (str): Search query text
            query_vector (List[float]): Query embedding vector
            alpha (float): Balance between vector (1.0) and keyword (0.0) search
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: Search results with content and metadata
        """
        try:
            logger.info(f"Performing hybrid search for: {query_text[:50]}...")
            
            # Perform hybrid search
            results = self.collection.query.hybrid(
                query=query_text,
                vector=query_vector,
                alpha=alpha,  # 0.5 balances vector and keyword search
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for rank, obj in enumerate(results.objects):
                result = {
                    'content': obj.properties.get('text', ''),
                    'doc_id': obj.properties.get('doc_id', rank),
                    'score': getattr(obj.metadata, 'score', 0.0) if hasattr(obj.metadata, 'score') else 0.0,
                    'rank': rank + 1,
                    'search_type': 'hybrid'
                }
                formatted_results.append(result)
            
            logger.info(f"Hybrid search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            raise
    
    def vector_search(self, 
                     query_vector: List[float], 
                     limit: int = 5) -> List[Dict]:
        """
        Perform pure vector search using Weaviate
        
        Args:
            query_vector (List[float]): Query embedding vector
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: Search results with content and metadata
        """
        try:
            logger.info("Performing vector search...")
            
            results = self.collection.query.near_vector(
                near_vector=query_vector,
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for rank, obj in enumerate(results.objects):
                result = {
                    'content': obj.properties.get('text', ''),
                    'doc_id': obj.properties.get('doc_id', rank),
                    'score': getattr(obj.metadata, 'distance', 1.0) if hasattr(obj.metadata, 'distance') else 1.0,
                    'rank': rank + 1,
                    'search_type': 'vector'
                }
                formatted_results.append(result)
            
            logger.info(f"Vector search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in vector search: {str(e)}")
            raise
    
    def keyword_search(self, 
                      query_text: str, 
                      limit: int = 5) -> List[Dict]:
        """
        Perform keyword search using Weaviate BM25
        
        Args:
            query_text (str): Search query text
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: Search results with content and metadata
        """
        try:
            logger.info(f"Performing keyword search for: {query_text[:50]}...")
            
            results = self.collection.query.bm25(
                query=query_text,
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for rank, obj in enumerate(results.objects):
                result = {
                    'content': obj.properties.get('text', ''),
                    'doc_id': obj.properties.get('doc_id', rank),
                    'score': getattr(obj.metadata, 'score', 0.0) if hasattr(obj.metadata, 'score') else 0.0,
                    'rank': rank + 1,
                    'search_type': 'keyword'
                }
                formatted_results.append(result)
            
            logger.info(f"Keyword search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in keyword search: {str(e)}")
            raise
    
    def get_document_by_id(self, doc_id: int) -> Optional[str]:
        """
        Get document content by ID
        
        Args:
            doc_id (int): Document ID
            
        Returns:
            Optional[str]: Document content or None if not found
        """
        try:
            results = self.collection.query.fetch_objects(
                where={"path": ["doc_id"], "operator": "Equal", "valueInt": doc_id},
                limit=1
            )
            
            if results.objects:
                return results.objects[0].properties.get('text', '')
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting document by ID: {str(e)}")
            return None
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection
        
        Returns:
            Dict: Collection statistics
        """
        try:
            # Get collection info
            aggregate_result = self.collection.aggregate.over_all()
            
            stats = {
                'total_documents': aggregate_result.total_count if hasattr(aggregate_result, 'total_count') else 0,
                'collection_name': self.collection_name,
                'weaviate_url': self.weaviate_url,
                'use_local': self.use_local
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {
                'total_documents': 0,
                'collection_name': self.collection_name,
                'error': str(e)
            }
    
    def reset_collection(self) -> bool:
        """
        Delete and recreate the collection (use with caution!)
        
        Returns:
            bool: True if successful
        """
        try:
            logger.warning(f"Resetting collection: {self.collection_name}")
            
            # Delete existing collection
            if self.client.collections.exists(self.collection_name):
                self.client.collections.delete(self.collection_name)
            
            # Recreate collection
            self.collection = self._setup_collection()
            
            logger.info(f"Collection {self.collection_name} reset successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")
            return False
    
    def close(self):
        """Close the Weaviate client connection"""
        try:
            if self.client:
                self.client.close()
                logger.info("Weaviate client connection closed")
        except Exception as e:
            logger.error(f"Error closing Weaviate client: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure client is closed"""
        self.close()
