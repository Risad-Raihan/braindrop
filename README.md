# Bengali Physics RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system for Bengali physics education, powered by Weaviate vector database and Google Gemini AI models.

## 🎯 Project Overview

This repository contains a production-ready RAG system that helps students learn physics in Bengali. The system can:

- **Search** through Bengali physics content using hybrid search (vector + keyword)
- **Answer questions** about physics concepts in Bengali
- **Explain concepts** in detail with educational context
- **Find similar content** for deeper understanding

The project evolved from Jupyter notebooks to a scalable FastAPI application with proper architecture, testing, and documentation.

## 🚀 Quick Demo

Once set up, you can interact with the system like this:

```bash
# Ask a physics question in Bengali
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "গতি কি? এর প্রকারভেদ ব্যাখ্যা করো।"}'

# Search for specific physics topics
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "পদার্থবিজ্ঞানের শাখা", "search_type": "hybrid"}'
```

## Features

- **Hybrid Search**: Combines vector similarity and keyword matching
- **Bengali Physics Content**: Specialized for Bengali physics education
- **Multiple Search Types**: Hybrid, pure vector, pure keyword
- **RAG Chat**: Conversational physics assistant
- **Concept Explanations**: Detailed physics concept explanations
- **FastAPI**: Modern, fast, web API framework
- **Weaviate Integration**: Scalable vector database

## Quick Start

### Prerequisites

1. **Python 3.12+** with pyenv virtual environment
2. **Docker** for running Weaviate
3. **Google AI API Key**

### Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Risad-Raihan/physics_embeddings.git
   cd physics_embeddings/physics_rag_weaviate
   ```

2. **Activate your virtual environment:**
   ```bash
   pyenv activate edubot
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Weaviate locally:**
   ```bash
   docker run -p 8080:8080 -p 50051:50051 \
     cr.weaviate.io/semitechnologies/weaviate:1.24.6
   ```

5. **Set your Google API key:**
   ```bash
   export GOOGLE_API_KEY='your_actual_google_api_key_here'
   ```
   
   Or update it in `app/config/settings.py`:
   ```python
   GOOGLE_API_KEY: str = "your_actual_google_api_key_here"
   ```

6. **Ensure physics text file exists:**
   Make sure `Physics/combined_physics.md` is accessible in the parent directory.

### Running the API

1. **Start the FastAPI server:**
   ```bash
   python run_server.py
   ```

2. **Access the API:**
   - **API**: http://localhost:8000
   - **Interactive Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

### First Time Setup

1. **Initialize the collection with physics data:**
   ```bash
   curl -X POST "http://localhost:8000/initialize" \
     -H "Content-Type: application/json" \
     -d '{"force_reset": false}'
   ```

2. **Check service status:**
   ```bash
   curl http://localhost:8000/health
   ```

## API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /stats` - Service statistics
- `POST /initialize` - Initialize collection with physics data

### Search & RAG Endpoints

- `POST /search` - Search physics content
- `POST /chat` - Chat with physics assistant
- `POST /explain` - Explain physics concepts
- `POST /similar` - Find similar content

### Example Usage

#### Search for Physics Content
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "পদার্থবিজ্ঞানের শাখা গুলো কি কি?",
    "search_type": "hybrid",
    "top_k": 5
  }'
```

#### Chat with Physics Assistant
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "গতি কি?",
    "include_sources": true,
    "search_type": "hybrid"
  }'
```

#### Explain a Concept
```bash
curl -X POST "http://localhost:8000/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "সরণ",
    "top_k": 3
  }'
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Google AI API
export GOOGLE_API_KEY="your_google_api_key"

# Weaviate Configuration
export WEAVIATE_URL="http://localhost:8080"
export WEAVIATE_API_KEY=""  # Empty for localhost
export USE_LOCAL_WEAVIATE="true"

# Logging
export LOG_LEVEL="INFO"
```

### Settings

Key settings in `app/config/settings.py`:

- `GOOGLE_API_KEY`: Google AI API key
- `WEAVIATE_URL`: Weaviate instance URL
- `WEAVIATE_COLLECTION`: Collection name (default: "PhysicsChunk")
- `USE_LOCAL_WEAVIATE`: Whether to use local Weaviate
- `DEFAULT_TOP_K`: Default number of search results
- `HYBRID_ALPHA`: Balance between vector and keyword search

## Project Structure

```
physics_embeddings/                 # Main repository
├── README.md                      # This file - main project documentation
├── physics_rag_weaviate/          # FastAPI RAG application
│   ├── app/
│   │   ├── main.py                # FastAPI application
│   │   ├── services/
│   │   │   ├── embedding_service.py   # Google Gemini embeddings
│   │   │   ├── search_service.py      # Weaviate search operations
│   │   │   ├── generation_service.py  # Response generation
│   │   │   └── rag_service.py         # Main RAG orchestrator
│   │   ├── config/
│   │   │   └── settings.py           # Configuration management
│   │   └── models/
│   │       ├── requests.py           # Pydantic request models
│   │       └── responses.py          # Pydantic response models
│   ├── requirements.txt              # Python dependencies
│   ├── run_server.py                # Server startup script
│   └── test_weaviate_rag.py        # Test script
├── Physics/                        # Bengali physics content
│   └── combined_physics.md         # Combined physics textbook
├── full_book_weaviate.ipynb       # Original Weaviate notebook
└── [other development files]
```

## Development

### Testing

Run the test script to verify functionality:
```bash
cd physics_rag_weaviate
python test_weaviate_rag.py
```

### Adding New Features

1. Add new endpoints in `app/main.py`
2. Extend the RAG service in `app/services/rag_service.py`
3. Add request/response models in `app/models/`
4. Update configuration in `app/config/settings.py`

## Troubleshooting

### Common Issues

1. **Weaviate Connection Failed**
   - Ensure Weaviate is running: `docker ps`
   - Check Weaviate logs: `docker logs <container_id>`
   - Verify URL: `curl http://localhost:8080/v1/meta`

2. **Google API Key Issues**
   - Verify API key is set: `echo $GOOGLE_API_KEY`
   - Check API key permissions in Google Cloud Console
   - Ensure billing is enabled for the project

3. **Physics Text Not Found**
   - Verify file path: `Physics/combined_physics.md`
   - Check file permissions
   - Update path in `app/config/settings.py`

### Logs

Check application logs for debugging:
```bash
# When running with uvicorn
tail -f /var/log/uvicorn.log

# Or check console output when running locally
```

## Next Steps

1. **Frontend Integration**: Connect with Next.js frontend
2. **Authentication**: Add user authentication
3. **Caching**: Implement response caching
4. **Monitoring**: Add metrics and monitoring
5. **Deployment**: Deploy to cloud platforms

## License

This project is for educational purposes.
