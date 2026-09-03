FROM python:3.10-slim

# Minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install lightweight dependencies directly without heavy extra packages (no matplotlib, no opencv-contrib, no sounddevice)
RUN pip install --no-cache-dir opencv-python-headless==4.8.1.78
RUN pip install --no-cache-dir --no-deps mediapipe==0.10.9
RUN pip install --no-cache-dir flask gunicorn boto3 scipy numpy protobuf attrs flatbuffers absl-py pillow

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers", "1", "--threads", "2", "--bind", "0.0.0.0:5000", "app:app"]
