# Soda AI Application

A full-stack application with FastAPI backend and React frontend for managing soda inventory and customer interactions with AI capabilities.

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Environment Setup

1. Copy the environment example file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your Google API key:
   ```
   GOOGLE_API_KEY=your-actual-google-api-key
   ```

### Production Mode

To run the application in production mode:

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Development Mode

To run the application in development mode with hot reload:

```bash
# Build and run in development mode
docker-compose -f docker-compose.dev.yml up --build

# Run in background
docker-compose -f docker-compose.dev.yml up -d --build
```

The application will be available at:

- Frontend: http://localhost:5173 (Vite dev server)
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Useful Commands

```bash
# Stop all services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Access backend container
docker-compose exec backend bash

# Access frontend container
docker-compose exec frontend sh
```

## Project Structure

```
├── src/                    # Backend FastAPI application
│   ├── domain/            # Domain models
│   ├── infra/             # Infrastructure (database)
│   ├── services/          # Business logic
│   ├── utils/             # Utilities
│   └── web/               # Web controllers
├── frontend/              # React frontend application
├── Dockerfile             # Backend Docker configuration
├── docker-compose.yml     # Production Docker Compose
├── docker-compose.dev.yml # Development Docker Compose
└── database.db           # SQLite database
```

## Technology Stack

### Backend

- FastAPI (Python web framework)
- SQLModel (SQL databases)
- Google Generative AI (Gemini)
- JWT Authentication
- SQLite Database

### Frontend

- React 19
- React Router 7
- TypeScript
- Tailwind CSS
- Vite (development server)
- Bun (package manager)

## Environment Variables

| Variable         | Description                | Default                 |
| ---------------- | -------------------------- | ----------------------- |
| `GOOGLE_API_KEY` | Google Gemini API key      | `your-google-api-key`   |
| `SECRET_JWT`     | JWT secret key             | `mysupersecretkey`      |
| `DATABASE_URL`   | Database connection string | `sqlite:///database.db` |
| `ROOT_URL`       | Backend API base URL       | `http://localhost:8000` |
