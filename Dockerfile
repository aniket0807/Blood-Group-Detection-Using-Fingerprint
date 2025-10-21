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

# Copy the full repo early so model file (if present) can be inspected at build time
COPY . .

# Copy requirements (they are already in the repo, but keep local copies for clarity)
COPY requirements-prod.txt ./
COPY requirements-prod-legacy.txt ./

# Upgrade pip tools
RUN pip install --upgrade pip setuptools wheel

# Decide which requirements to install based on model's saved keras_version (if model present):
# - If model/model.h5 exists and its keras_version starts with '3.' -> install modern requirements (requirements-prod.txt)
# - Otherwise, if legacy file exists, install legacy requirements
RUN python - <<'PY'
import os, sys
kv = None
path = 'model/model.h5'
if os.path.exists(path):
    try:
        import h5py
        f = h5py.File(path, 'r')
        kv = f.attrs.get('keras_version')
        f.close()
    except Exception:
        kv = None

if kv is not None:
    kvs = kv.decode('utf-8') if isinstance(kv, bytes) else str(kv)
    print('Detected model keras_version:', kvs)
    if kvs.startswith('3.'):
        # modern Keras -> use modern requirements
        sys.exit(0)
    else:
        # legacy keras -> prefer legacy requirements
        sys.exit(2)
else:
    # no model to inspect; prefer modern requirements if present
    sys.exit(1)
PY
RUN rc=$?; \
    if [ "$rc" -eq 0 ]; then pip install -r requirements-prod.txt; \
    elif [ "$rc" -eq 2 ]; then pip install -r requirements-prod-legacy.txt; \
    else pip install -r requirements-prod.txt || pip install -r requirements-prod-legacy.txt; fi

EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
