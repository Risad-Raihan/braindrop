/**
 * API client for Physics RAG backend
 */

import { config } from './config';

const API_BASE_URL = config.apiUrl;

export interface SearchRequest {
  query: string;
  search_type?: 'hybrid' | 'vector' | 'keyword';
  top_k?: number;
  alpha?: number;
}

export interface ChatRequest {
  message: string;
  include_sources?: boolean;
  search_type?: 'hybrid' | 'vector' | 'keyword';
  top_k?: number;
}

export interface ChatResponse {
  response: string;
  sources?: Array<{
    content: string;
    chapter?: string;
    section?: string;
    score?: number;
  }>;
  search_time?: number;
  generation_time?: number;
}

export interface SearchResult {
  content: string;
  chapter?: string;
  section?: string;
  score?: number;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  search_type: string;
  total_results: number;
  search_time?: number;
}

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  services: {
    weaviate: string;
    embedding: string;
    generation: string;
  };
  collection_info?: {
    name: string;
    count: number;
    vectorizer: string;
  };
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || 
          errorData.message || 
          `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Unable to connect to the physics assistant. Please make sure the backend service is running.');
      }
      throw error;
    }
  }

  async healthCheck(): Promise<HealthCheckResponse> {
    return this.makeRequest<HealthCheckResponse>('/health');
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    return this.makeRequest<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async search(request: SearchRequest): Promise<SearchResponse> {
    return this.makeRequest<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async explainConcept(concept: string, topK: number = 5): Promise<{
    explanation: string;
    sources: SearchResult[];
  }> {
    return this.makeRequest('/explain', {
      method: 'POST',
      body: JSON.stringify({
        concept,
        top_k: topK,
      }),
    });
  }

  async findSimilar(text: string, topK: number = 5): Promise<{
    similar_content: SearchResult[];
    reference_text: string;
    total_results: number;
  }> {
    return this.makeRequest('/similar', {
      method: 'POST',
      body: JSON.stringify({
        text,
        top_k: topK,
      }),
    });
  }

  async getStats(): Promise<{
    total_documents: number;
    collection_name: string;
    embedding_model: string;
    generation_model: string;
    weaviate_url: string;
  }> {
    return this.makeRequest('/stats');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export class for testing or custom instances
export { ApiClient };
