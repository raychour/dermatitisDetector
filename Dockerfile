FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-dev \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install dependencies
# Note: For GPU support, PyTorch will be installed by fastai/requirements.txt.
# If specific CUDA version is needed, it might need a separate command, 
# but usually pip handles it for standard setups.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app app/

# Expose port
EXPOSE 5000

# Run the server
CMD ["python", "app/server.py", "serve"]
