# Papergum Full-Stack Web Application

A modern web application built with Next.js frontend and FastAPI backend.

## Project Structure

```
papergum/
├── frontend/           # Next.js frontend application
│   ├── src/           # Source code
│   ├── public/        # Static files
│   └── package.json   # Frontend dependencies
│
├── backend/           # FastAPI backend application
│   ├── app/          # Application code
│   ├── tests/        # Backend tests
│   └── requirements.txt  # Backend dependencies
│
└── README.md         # Project documentation
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Development

- Frontend runs on: http://localhost:3000
- Backend API runs on: http://localhost:8000
- API documentation: http://localhost:8000/docs