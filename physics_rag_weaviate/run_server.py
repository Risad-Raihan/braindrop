"""
Run script for the Physics RAG API with Weaviate
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def main():
    """Run the FastAPI server"""
    print("🚀 Starting Physics RAG API with Weaviate")
    print("=" * 50)
    print("📚 Bengali Physics RAG System")
    print("🔍 Powered by Weaviate Vector Database")
    print("🤖 Google Gemini AI Models")
    print()
    print("🌐 Server will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print()
    print("⚠️  Make sure you have:")
    print("   - Weaviate running on localhost:8080")
    print("   - Valid Google API key set")
    print("   - Physics text file available")
    print()
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
