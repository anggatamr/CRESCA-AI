# Cresca AI Sentinel — Google Cloud Run Production Dockerfile
# Optimized for lightweight image size & scale-to-zero cold-start performance

FROM python:3.11-slim

# Prevent Python from writing pyc files to disk and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies for scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure data and reports directories exist
RUN mkdir -p /app/reports /app/data/firestore_local_store

# Expose standard Cloud Run port
EXPOSE 8080

# Run FastAPI microservice
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
