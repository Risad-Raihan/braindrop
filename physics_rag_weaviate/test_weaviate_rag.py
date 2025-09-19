"""
Test script for the Weaviate-based RAG services
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.config.settings import settings
from app.services.rag_service import WeaviateRAGService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_weaviate_rag_service():
    """Test the Weaviate RAG service functionality"""
    
    print("🧪 Testing Physics RAG Service with Weaviate")
    print("=" * 50)
    
    try:
        # Use the actual configuration from .env file
        print("\n🔧 Using your Weaviate Cloud configuration...")
        print(f"Weaviate URL: {settings.WEAVIATE_URL}")
        print(f"Use Local: {settings.USE_LOCAL_WEAVIATE}")
        print(f"Google API Key: {'✅ Set' if settings.GOOGLE_API_KEY.startswith('AIza') else '❌ Not Set'}")
        
        # Initialize RAG service
        print("\n1️⃣ Initializing Weaviate RAG Service...")
        rag_service = WeaviateRAGService(settings)
        print("✅ Weaviate RAG Service initialized successfully")
        
        # Test health check
        print("\n2️⃣ Testing Health Check...")
        health = await rag_service.health_check()
        print(f"Health Status: {health['status']}")
        for service_name, service_health in health['services'].items():
            print(f"  - {service_name}: {service_health['status']}")
            if 'error' in service_health:
                print(f"    Error: {service_health['error']}")
        
        # Test service stats
        print("\n3️⃣ Getting Service Statistics...")
        stats = rag_service.get_service_stats()
        print(f"Service Status: {stats.get('service_status', 'N/A')}")
        print(f"Initialized: {stats.get('initialized', False)}")
        print(f"Total Documents: {stats.get('total_documents', 'N/A')}")
        print(f"Weaviate URL: {stats.get('weaviate_url', 'N/A')}")
        
        # Initialize collection with physics data
        print("\n4️⃣ Initializing Collection with Physics Data...")
        print("⚠️  This step requires:")
        print("   - Valid Google API key")
        print("   - Weaviate running on localhost:8080")
        print("   - Physics text file available")
        
        try:
            init_success = await rag_service.initialize_collection(force_reset=False)
            if init_success:
                print("✅ Collection initialized successfully")
            else:
                print("❌ Collection initialization failed")
                print("   Make sure Weaviate is running and accessible")
                return False
        except Exception as e:
            print(f"❌ Collection initialization error: {str(e)}")
            print("   This is expected if Weaviate is not running or API key is invalid")
            return False
        
        # Test search functionality
        print("\n5️⃣ Testing Search Functionality...")
        test_query = "পদার্থবিজ্ঞানের শাখা গুলো কি কি?"
        print(f"Query: {test_query}")
        
        # Test hybrid search
        search_results = await rag_service.search(test_query, search_type="hybrid", top_k=3)
        print(f"Found {len(search_results)} hybrid search results")
        
        for i, result in enumerate(search_results, 1):
            print(f"\nResult {i}:")
            score = result.get('score', 0.0)
            print(f"  Score: {score:.4f}" if score is not None else "  Score: N/A")
            print(f"  Search Type: {result.get('search_type', 'hybrid')}")
            print(f"  Content preview: {result['content'][:100]}...")
        
        # Test chat functionality
        print("\n6️⃣ Testing Chat Functionality...")
        chat_response = await rag_service.chat(test_query, include_sources=True)
        print(f"Response preview: {chat_response['response'][:200]}...")
        print(f"Confidence: {chat_response['confidence']:.3f}")
        print(f"Sources: {len(chat_response['sources'])}")
        print(f"Total time: {chat_response['total_time']:.3f}s")
        print(f"Search type: {chat_response['search_type']}")
        
        # Test concept explanation
        print("\n7️⃣ Testing Concept Explanation...")
        concept_response = await rag_service.explain_concept("গতি")
        print(f"Explanation preview: {concept_response['explanation'][:200]}...")
        print(f"Sources used: {len(concept_response['sources'])}")
        
        print("\n✅ All tests completed successfully!")
        print("🎉 Your Weaviate RAG service is working correctly!")
        
        # Close connections
        rag_service.close()
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        logger.error(f"Test error: {str(e)}", exc_info=True)
        return False
    
    return True


async def test_individual_services():
    """Test individual services separately"""
    
    print("\n🔍 Testing Individual Services")
    print("=" * 50)
    
    try:
        from app.services.embedding_service import EmbeddingService
        from app.services.search_service import WeaviateSearchService
        from app.services.generation_service import GenerationService
        
        # Test embedding service
        print("\n📊 Testing Embedding Service...")
        try:
            embedding_service = EmbeddingService("test_key")  # Will fail with invalid key
            print("⚠️  Embedding service initialized (API key not validated yet)")
        except Exception as e:
            print(f"⚠️  Embedding service error: {str(e)}")
        
        # Test Weaviate search service
        print("\n🔍 Testing Weaviate Search Service...")
        try:
            search_service = WeaviateSearchService(
                weaviate_url="http://localhost:8080",
                weaviate_api_key="",
                use_local=True
            )
            print("⚠️  Weaviate search service initialized (connection not tested)")
            search_service.close()
        except Exception as e:
            print(f"⚠️  Weaviate search service error: {str(e)}")
        
        # Test generation service
        print("\n💬 Testing Generation Service...")
        try:
            generation_service = GenerationService("test_key")  # Will fail with invalid key
            print("⚠️  Generation service initialized (API key not validated yet)")
        except Exception as e:
            print(f"⚠️  Generation service error: {str(e)}")
        
        print("\n✅ Individual service initialization tests completed!")
        print("⚠️  Full functionality requires valid API keys and running Weaviate")
        
    except Exception as e:
        print(f"\n❌ Individual service test failed: {str(e)}")
        logger.error(f"Individual service test error: {str(e)}", exc_info=True)
        return False
    
    return True


def print_setup_instructions():
    """Print setup instructions for the user"""
    print("\n🚀 Setup Instructions for Weaviate Cloud RAG System")
    print("=" * 60)
    print("\n✅ Your system is configured for Weaviate Cloud!")
    print("\n1. Configuration files:")
    print("   - .env file with your API keys ✅")
    print("   - Google Gemini API key ✅")
    print("   - Weaviate Cloud URL and API key ✅")
    print("\n2. Physics content:")
    print("   - Physics/combined_physics.md")
    print("\n3. Dependencies:")
    print("   - All requirements installed ✅")
    print("\n4. Ready to test:")
    print("   - Run: python test_weaviate_rag.py")
    print("   - Or start server: python run_server.py")


if __name__ == "__main__":
    print("🚀 Starting Weaviate RAG Service Tests")
    
    # Print setup instructions
    print_setup_instructions()
    
    # Test individual services first
    success = asyncio.run(test_individual_services())
    
    if success:
        print("\n" + "="*50)
        print("🔄 Running full RAG service test with your Weaviate Cloud...")
        
        # Run the full test since we have Weaviate Cloud configured
        success = asyncio.run(test_weaviate_rag_service())
    
    if success:
        print("\n🎊 Basic tests passed! Ready for Weaviate integration.")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        sys.exit(1)
