FROM python:3.11-slim

WORKDIR /app

# Copy application code first (needed for pip install)
COPY pyproject.toml ./
COPY az_sim ./az_sim
COPY api ./api

# Install dependencies
RUN pip install --no-cache-dir .

# Expose port (Railway uses PORT env variable)
EXPOSE 8000

# Run the application - use PORT env var if set, otherwise default to 8000
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
