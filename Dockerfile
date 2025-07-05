# Backend Dockerfile for FastAPI application
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy Python dependency files
COPY pyproject.toml uv.lock ./

# Install UV package manager for faster dependency installation
RUN pip install uv

# Install Python dependencies
RUN uv sync --frozen

# Copy source code
COPY src/ ./src/
COPY database.db ./database.db

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV ROOT_URL=http://localhost:8000

# Command to run the application
CMD ["uv", "run", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
