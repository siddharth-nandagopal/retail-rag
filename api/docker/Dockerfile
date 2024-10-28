# Use a lightweight Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock for dependency installation
# COPY pyproject.toml poetry.lock /app/

# Copy the application code
COPY . /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# # Copy the application code
# COPY . /app

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
