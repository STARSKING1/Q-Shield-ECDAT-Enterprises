FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Generate dynamic initial assets
RUN python main.py && python generate_dashboard.py

# Expose Uvicorn port
EXPOSE 8000

# Run production FastAPI server
CMD ["uvicorn", "q_shield.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
