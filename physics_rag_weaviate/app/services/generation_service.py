"""
Generation Service for Physics RAG System with Weaviate
Handles response generation using Google Gemini
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class GenerationService:
    """Service for generating responses using Google Gemini API"""
    
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        """
        Initialize the generation service
        
        Args:
            api_key (str): Google AI API key
            model_name (str): Gemini model name to use
        """
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        logger.info(f"GenerationService initialized with model: {model_name}")
    
    def create_physics_prompt(self, query: str, context: str, 
                            include_context_info: bool = True) -> str:
        """
        Create a prompt for physics question answering
        
        Args:
            query (str): User's question
            context (str): Retrieved context from search
            include_context_info (bool): Whether to include context source info
            
        Returns:
            str: Formatted prompt
        """
        base_prompt = f"""তুমি একজন বাংলা পদার্থবিজ্ঞানের শিক্ষক। এই প্রসঙ্গ ব্যবহার করে প্রশ্নটির উত্তর দাও:

প্রশ্ন: {query}

প্রসঙ্গ: {context}

উত্তর বাংলায় দাও এবং শিক্ষার্থীদের জন্য সহজবোধ্য করে ব্যাখ্যা করো।"""
        
        if include_context_info:
            base_prompt += """

নির্দেশনা:
- উত্তরটি স্পষ্ট ও সহজ ভাষায় দাও
- প্রয়োজনে উদাহরণ দিয়ে ব্যাখ্যা করো
- শিক্ষার্থীদের বোঝার উপযোগী করে উপস্থাপন করো
- বৈজ্ঞানিক পরিভাষা ব্যবহার করলে তার অর্থ ব্যাখ্যা করো"""
        
        return base_prompt
    
    def generate_response(self, query: str, context: str, 
                         include_context_info: bool = True,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate response using context
        
        Args:
            query (str): User's question
            context (str): Retrieved context from search
            include_context_info (bool): Whether to include additional context info
            max_tokens (Optional[int]): Maximum tokens in response
            
        Returns:
            str: Generated response
        """
        try:
            prompt = self.create_physics_prompt(query, context, include_context_info)
            
            logger.info(f"Generating response for query: {query[:50]}...")
            
            # Configure generation parameters
            generation_config = {}
            if max_tokens:
                generation_config['max_output_tokens'] = max_tokens
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config if generation_config else None
            )
            
            generated_text = response.text
            logger.info(f"Generated response of length: {len(generated_text)}")
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"দুঃখিত, উত্তর তৈরি করতে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
    
    def generate_simple_response(self, query: str, context: str) -> str:
        """
        Generate a simple response without extra formatting
        
        Args:
            query (str): User's question
            context (str): Retrieved context
            
        Returns:
            str: Simple generated response
        """
        simple_prompt = f"""প্রশ্ন: {query}
প্রসঙ্গ: {context}

সংক্ষেপে উত্তর দাও:"""
        
        try:
            response = self.model.generate_content(simple_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in simple response generation: {str(e)}")
            return "উত্তর তৈরি করতে সমস্যা হয়েছে।"
    
    def generate_explanation(self, concept: str, context: str) -> str:
        """
        Generate detailed explanation for a physics concept
        
        Args:
            concept (str): Physics concept to explain
            context (str): Related context from textbook
            
        Returns:
            str: Detailed explanation
        """
        explanation_prompt = f"""তুমি একজন পদার্থবিজ্ঞানের শিক্ষক। '{concept}' বিষয়টি বিস্তারিত ব্যাখ্যা করো।

প্রসঙ্গ: {context}

ব্যাখ্যায় অন্তর্ভুক্ত করো:
- মূল সংজ্ঞা
- গুরুত্বপূর্ণ বৈশিষ্ট্য
- দৈনন্দিন জীবনের উদাহরণ
- প্রয়োজনে গাণিতিক সূত্র

শিক্ষার্থীদের জন্য সহজ ভাষায় ব্যাখ্যা করো।"""
        
        try:
            response = self.model.generate_content(explanation_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return f"'{concept}' সম্পর্কে ব্যাখ্যা তৈরি করতে সমস্যা হয়েছে।"
    
    def generate_with_sources(self, query: str, search_results: List[Dict]) -> Dict:
        """
        Generate response with source information from Weaviate results
        
        Args:
            query (str): User's question
            search_results (List[Dict]): Search results from Weaviate
            
        Returns:
            Dict: Response with sources and metadata
        """
        if not search_results:
            return {
                'response': "দুঃখিত, এই প্রশ্নের জন্য কোনো প্রাসঙ্গিক তথ্য পাওয়া যায়নি।",
                'sources': [],
                'confidence': 0.0
            }
        
        # Use the best result as primary context
        primary_context = search_results[0]['content']
        
        try:
            response_text = self.generate_response(query, primary_context)
            
            # Prepare source information
            sources = []
            for result in search_results[:3]:  # Top 3 sources
                sources.append({
                    'content_preview': result['content'][:200] + "..." if len(result['content']) > 200 else result['content'],
                    'score': result.get('score', 0.0),
                    'doc_id': result.get('doc_id'),
                    'rank': result.get('rank', 0),
                    'search_type': result.get('search_type', 'hybrid')
                })
            
            # Estimate confidence based on top result score
            confidence = min(search_results[0].get('score', 0.0), 1.0)
            if confidence < 0:  # Handle distance scores (lower is better)
                confidence = max(0.0, 1.0 - abs(confidence))
            
            return {
                'response': response_text,
                'sources': sources,
                'confidence': confidence,
                'total_sources': len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error generating response with sources: {str(e)}")
            return {
                'response': "উত্তর তৈরি করতে সমস্যা হয়েছে।",
                'sources': [],
                'confidence': 0.0
            }
    
    def generate_multi_context_response(self, query: str, contexts: List[str]) -> str:
        """
        Generate response using multiple contexts
        
        Args:
            query (str): User's question
            contexts (List[str]): Multiple context texts
            
        Returns:
            str: Generated response
        """
        if not contexts:
            return "কোনো প্রসঙ্গ পাওয়া যায়নি।"
        
        # Combine contexts
        combined_context = "\n\n---\n\n".join(contexts[:3])  # Use top 3 contexts
        
        multi_context_prompt = f"""তুমি একজন বাংলা পদার্থবিজ্ঞানের শিক্ষক। নিচের একাধিক প্রসঙ্গ ব্যবহার করে প্রশ্নটির উত্তর দাও:

প্রশ্ন: {query}

প্রসঙ্গসমূহ:
{combined_context}

উত্তর বাংলায় দাও এবং বিভিন্ন প্রসঙ্গের তথ্য একসাথে করে সম্পূর্ণ উত্তর দাও।"""
        
        try:
            response = self.model.generate_content(multi_context_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating multi-context response: {str(e)}")
            return "একাধিক প্রসঙ্গ ব্যবহার করে উত্তর তৈরি করতে সমস্যা হয়েছে।"
    
    def validate_response(self, response: str) -> bool:
        """
        Basic validation of generated response
        
        Args:
            response (str): Generated response
            
        Returns:
            bool: True if response seems valid
        """
        if not response or len(response.strip()) < 10:
            return False
        
        # Check for common error patterns
        error_patterns = [
            "I cannot",
            "I'm sorry",
            "I don't know",
            "error",
            "failed"
        ]
        
        response_lower = response.lower()
        for pattern in error_patterns:
            if pattern in response_lower:
                return False
        
        return True
    
    def get_model_info(self) -> Dict:
        """
        Get information about the generation model
        
        Returns:
            Dict: Model information
        """
        return {
            'model_name': self.model_name,
            'api_configured': bool(self.api_key),
            'service_status': 'active'
        }
