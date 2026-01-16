FROM python:3.11-slim

WORKDIR /app

# Copy application code first (needed for pip install)
COPY pyproject.toml ./
COPY az_sim ./az_sim
COPY api ./api

# Install dependencies
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
