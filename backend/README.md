# ChatKit FastAPI Backend

FastAPI backend for ChatKit chatbot with structured architecture.

## Structure

\`\`\`
backend/
├── main.py                 # FastAPI application entry point
├── app/
│   └── chat/              # Chat service module
│       ├── models.py      # Pydantic models (requests/responses)
│       ├── services.py    # Business logic
│       ├── prompts.py     # System prompts and messages
│       ├── views.py       # Request handlers
│       ├── utils.py       # Utility functions
│       └── routers.py     # API routes
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── .env.example          # Environment variables template
\`\`\`

## Setup

1. Install dependencies:
\`\`\`bash
cd backend
pip install -r requirements.txt
\`\`\`

2. Create `.env` file:
\`\`\`bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
\`\`\`

3. Run the server:
\`\`\`bash
python main.py
\`\`\`

Or with uvicorn directly:
\`\`\`bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

## API Endpoints

- `POST /api/chat` - Chat completion with streaming
- `POST /api/upload` - File upload
- `GET /api/health` - Health check
- `GET /` - Root endpoint

## Docker

Build and run with Docker:
\`\`\`bash
docker build -t chatkit-backend .
docker run -p 8000:8000 --env-file .env chatkit-backend
\`\`\`

## Development

The backend follows a structured architecture:

- **models.py**: Data models split into All/Requests/Responses sections
- **services.py**: Business logic for chat and upload operations
- **prompts.py**: System prompts and error messages
- **views.py**: Request handlers split into sections
- **utils.py**: Helper functions
- **routers.py**: API route definitions
