FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for OpenCV/TensorFlow and building some wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    curl \
    libsm6 \
    libxrender1 \
    libxext6 \
    libglib2.0-0 \
    libgl1 \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements-prod.txt ./
COPY requirements-prod-legacy.txt ./
RUN pip install --upgrade pip setuptools wheel
# If a legacy requirements file exists, prefer it (useful to load older models).
RUN if [ -f requirements-prod-legacy.txt ]; then pip install -r requirements-prod-legacy.txt; else pip install -r requirements-prod.txt; fi

# Copy rest of the app
COPY . .

EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
