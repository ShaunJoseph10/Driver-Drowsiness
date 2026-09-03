FROM python:3.10-slim

# System dependencies for OpenCV & MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers", "1", "--threads", "2", "--bind", "0.0.0.0:5000", "app:app"]
