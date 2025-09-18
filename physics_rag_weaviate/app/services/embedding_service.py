"""
Embedding Service for Physics RAG System with Weaviate
Handles Google Gemini embeddings generation
"""

import google.generativeai as genai
import numpy as np
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the embedding service
        
        Args:
            api_key (str): Google AI API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model_name = "models/gemini-embedding-001"
        logger.info(f"EmbeddingService initialized with model: {self.model_name}")
    
    def get_embeddings(self, texts: Union[List[str], str]) -> np.ndarray:
        """
        Get embeddings for a list of texts or single text
        
        Args:
            texts: List of texts or single text to embed
            
        Returns:
            np.ndarray: Embeddings array with shape (n_texts, embedding_dim)
        """
        try:
            if isinstance(texts, str):
                texts = [texts]
            
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            result = genai.embed_content(
                model=self.model_name,
                content=texts
            )
            
            embeddings = np.array(result['embedding'], dtype='float32')
            
            # Handle single text case - ensure 2D array
            if len(texts) == 1 and embeddings.ndim == 1:
                embeddings = embeddings.reshape(1, -1)
            
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_single_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a single text as list (for Weaviate compatibility)
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float]: Embedding as list of floats
        """
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text
            )
            
            # Return as list for Weaviate compatibility
            embedding = result['embedding']
            logger.info(f"Generated single embedding with dimension: {len(embedding)}")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating single embedding: {str(e)}")
            raise
    
    def get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding for a search query (Weaviate format)
        
        Args:
            query (str): Search query
            
        Returns:
            List[float]: Query embedding as list of floats
        """
        return self.get_single_embedding(query)
    
    def get_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts in Weaviate-compatible format
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embeddings as lists of floats
        """
        try:
            logger.info(f"Generating batch embeddings for {len(texts)} texts")
            
            result = genai.embed_content(
                model=self.model_name,
                content=texts
            )
            
            embeddings = result['embedding']
            
            # Convert numpy array to list of lists if needed
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            
            logger.info(f"Generated {len(embeddings)} batch embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
