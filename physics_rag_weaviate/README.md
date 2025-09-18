# Physics RAG Weaviate Application

This directory contains the FastAPI application for the Bengali Physics RAG system.

## 📖 Main Documentation

**For complete setup instructions, features, and usage examples, please see the main project README:**

👉 **[Main README.md](../README.md)** 👈

## 🚀 Quick Start (from this directory)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Google API key:**
   ```bash
   export GOOGLE_API_KEY='your_actual_google_api_key_here'
   ```

3. **Start Weaviate:**
   ```bash
   docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.24.6
   ```

4. **Run the application:**
   ```bash
   python run_server.py
   ```

5. **Visit:** http://localhost:8000/docs

## 📁 Directory Contents

- `app/` - FastAPI application code
  - `main.py` - API endpoints
  - `services/` - RAG service implementations
  - `config/` - Configuration management
  - `models/` - Pydantic request/response models
- `requirements.txt` - Python dependencies
- `run_server.py` - Server startup script
- `test_*.py` - Testing scripts

## 🔗 Related Files

- `../Physics/combined_physics.md` - Bengali physics content
- `../full_book_weaviate.ipynb` - Original development notebook
- `../README.md` - **Complete project documentation**