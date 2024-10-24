# Stage 1: Build the application with dependencies using Poetry
FROM python:3.12-slim AS builder

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

COPY /generation/ /app/
# Copy pyproject.toml and poetry.lock first to leverage Docker cache
# COPY ../generation/pyproject.toml ../generation/poetry.lock* /app/

# Install dependencies in a virtual environment created by Poetry
RUN poetry config virtualenvs.in-project true && poetry install --no-dev

# Copy the rest of the application code and requirements
# COPY ../generation/ /app/
# COPY sql/init.sql /app/sql/

# Stage 2: Create the final image to run the application
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the virtual environment with dependencies from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application code from the builder stage
COPY --from=builder /app/ /app/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV GENERATED_DATA_DIR=/app/generated_data
RUN mkdir -p $GENERATED_DATA_DIR

# Command to run the data ingestion script
CMD ["python", "data_ingestion.py"]
