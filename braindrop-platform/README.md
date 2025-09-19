# BrainDrop Physics Assistant

A Next.js frontend for the Physics RAG (Retrieval-Augmented Generation) system, providing an interactive chat interface for physics learning.

## Features

- 🤖 AI-powered physics assistant
- 📚 Access to physics textbook content through RAG
- 🔍 Real-time search with source citations
- 🌍 Bilingual support (English and Bengali)
- 📱 Responsive design
- ⚡ Fast and modern UI with Next.js 14

## Getting Started

### Prerequisites

Make sure you have the following running:

1. **Physics RAG Backend**: The Weaviate-based physics RAG API should be running on `http://localhost:8000`
2. **Node.js**: Version 18 or higher
3. **pnpm**: Package manager (or npm/yarn)

### Installation

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Configure API URL** (optional):
   
   Create a `.env.local` file in the project root:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the development server**:
   ```bash
   pnpm dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Backend Setup

Make sure your Physics RAG backend is running. From the `physics_rag_weaviate` directory:

```bash
# Install backend dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your Google API key and Weaviate configuration

# Run the backend
python run_server.py
```

The backend should be accessible at `http://localhost:8000`.

## Usage

1. **Select Physics Subject**: Choose physics from the subject selector
2. **Start Chatting**: Ask questions about physics concepts, problems, or explanations
3. **View Sources**: Click on "Sources" to see the textbook content used to generate responses
4. **Quick Questions**: Use the sidebar quick questions for common physics topics

### Example Questions

- "What is Newton's first law?"
- "Explain electromagnetic induction"
- "How does a transformer work?"
- "What is Ohm's law?"

## Project Structure

```
braindrop-platform/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── chat-interface.tsx # Main chat component
│   ├── header.tsx        # App header
│   └── ...
├── hooks/                # Custom React hooks
│   ├── use-chat.ts       # Chat functionality hook
│   └── ...
├── lib/                  # Utility libraries
│   ├── api.ts            # API client
│   ├── config.ts         # App configuration
│   └── utils.ts          # Utility functions
└── ...
```

## API Integration

The frontend communicates with the Physics RAG backend through:

- **Chat Endpoint**: `/chat` - Send messages and receive AI responses
- **Search Endpoint**: `/search` - Search physics content
- **Health Check**: `/health` - Check backend status

## Configuration

### API Settings

Edit `lib/config.ts` to modify:

- API URL
- Default search settings
- UI preferences

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Development

### Available Scripts

- `pnpm dev`: Start development server
- `pnpm build`: Build for production
- `pnpm start`: Start production server
- `pnpm lint`: Run ESLint

### Adding New Features

1. **API Changes**: Update `lib/api.ts` with new endpoints
2. **UI Components**: Add new components in `components/`
3. **Hooks**: Create custom hooks in `hooks/`
4. **Styling**: Use Tailwind CSS classes

## Troubleshooting

### Common Issues

1. **Backend Connection Error**:
   - Ensure the Physics RAG backend is running on port 8000
   - Check CORS settings in the backend
   - Verify API URL in configuration

2. **Build Errors**:
   - Run `pnpm install` to ensure all dependencies are installed
   - Check TypeScript errors with `pnpm lint`

3. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check component imports

### Backend Health Check

Visit `http://localhost:8000/health` to verify the backend is running properly.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Physics RAG system for educational purposes.
