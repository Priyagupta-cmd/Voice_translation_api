FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose port
EXPOSE 8080

# Run FastAPI
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
