/**
 * Custom hook for managing chat functionality with Physics RAG API
 */

import { useState, useCallback, useRef } from 'react';
import { apiClient, ChatRequest, ChatResponse } from '@/lib/api';

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  subject?: string;
  sources?: Array<{
    content: string;
    chapter?: string;
    section?: string;
    score?: number;
  }>;
  searchTime?: number;
  generationTime?: number;
}

export interface UseChatOptions {
  includeSources?: boolean;
  searchType?: 'hybrid' | 'vector' | 'keyword';
  topK?: number;
}

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string, subject?: string) => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

export function useChat(options: UseChatOptions = {}): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Use ref to store the latest options to avoid stale closures
  const optionsRef = useRef(options);
  optionsRef.current = options;

  const sendMessage = useCallback(async (content: string, subject?: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content,
      sender: 'user',
      timestamp: new Date(),
      subject,
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const request: ChatRequest = {
        message: content,
        include_sources: optionsRef.current.includeSources ?? true,
        search_type: optionsRef.current.searchType ?? 'hybrid',
        top_k: optionsRef.current.topK ?? 5,
      };

      const response: ChatResponse = await apiClient.chat(request);

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: response.response,
        sender: 'ai',
        timestamp: new Date(),
        subject,
        sources: response.sources,
        searchTime: response.search_time,
        generationTime: response.generation_time,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      
      // Add error message to chat
      const errorAiMessage: Message = {
        id: `ai-error-${Date.now()}`,
        content: `I apologize, but I encountered an error: ${errorMessage}. Please try again or check if the physics assistant service is running.`,
        sender: 'ai',
        timestamp: new Date(),
        subject,
      };

      setMessages(prev => [...prev, errorAiMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    clearError,
  };
}
