/**
 * Configuration for the frontend application
 */

export const config = {
  // API Configuration
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  
  // Application settings
  appName: 'BrainDrop Physics Assistant',
  appDescription: 'AI-powered physics study companion for Class 9-10 students',
  
  // Chat settings
  defaultSearchType: 'hybrid' as const,
  defaultTopK: 5,
  maxMessageLength: 1000,
  
  // UI settings
  animationDuration: 300,
  scrollBehavior: 'smooth' as const,
} as const;

export type Config = typeof config;
