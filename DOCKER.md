# Docker Usage Guide

This document explains how to use the USB PD Parser with Docker for consistent, reproducible environments.

## 🐳 Quick Start with Docker

### Using Docker Compose (Recommended)
```bash
# Build and run with sample PDF
docker-compose up usb-pd-parser

# For development with mounted source code
docker-compose --profile dev up usb-pd-parser-dev
```

### Using Docker Directly
```bash
# Build the image
docker build -t usb-pd-parser .

# Run with mounted volumes
docker run -v $(pwd)/assets:/app/assets:ro \
           -v $(pwd)/outputs:/app/outputs \
           usb-pd-parser \
           python main.py --input assets/sample.pdf --out outputs/docker_output.jsonl
```

## 🛠️ System Dependencies Included

The Docker image includes:
- **Tesseract OCR**: For scanned PDF processing
- **Poppler utilities**: For PDF manipulation
- **Python 3.11**: Latest stable Python version
- **All Python dependencies**: From requirements.txt

## 📁 Volume Mounts

### Required Volumes
- **Input**: Mount your PDF files to `/app/assets`
- **Output**: Mount output directory to `/app/outputs`
- **Config**: Optionally mount config to `/app/application.yml`

### Example with Custom Files
```bash
docker run -v /path/to/your/pdfs:/app/assets:ro \
           -v /path/to/outputs:/app/outputs \
           -v /path/to/config.yml:/app/application.yml:ro \
           usb-pd-parser \
           python main.py --input assets/your_file.pdf --out outputs/results.jsonl
```

## 🔧 Configuration

### Environment Variables
- `PYTHONUNBUFFERED=1`: Ensures real-time log output
- `PYTHONPATH=/app`: Sets Python module path

### Custom Configuration
Create a custom `application.yml` and mount it:
```yaml
pdf_input_file: "assets/your_document.pdf"
output_directory: "outputs"
toc_file: "outputs/parsed_toc.jsonl"
ocr_fallback: true
max_pages: null
```

## 🚀 Development with Docker

### Development Setup
```bash
# Use development profile with mounted source
docker-compose --profile dev up usb-pd-parser-dev

# Or build development image
docker build -t usb-pd-parser:dev .
docker run -v $(pwd):/app usb-pd-parser:dev bash
```

### Running Tests in Container
```bash
# Run tests
docker run -v $(pwd):/app usb-pd-parser:dev python run_tests.py

# Run specific tests
docker run -v $(pwd):/app usb-pd-parser:dev pytest tests/test_parser.py -v
```

## 📊 Performance Considerations

### Memory Usage
- Base image: ~200MB
- With dependencies: ~400MB
- Runtime memory: Depends on PDF size

### Optimization Tips
- Use `.dockerignore` to exclude unnecessary files
- Multi-stage builds for smaller production images
- Volume mount large PDFs instead of copying

## 🔍 Troubleshooting

### Common Issues

**Permission Errors**:
```bash
# Fix output directory permissions
sudo chown -R $(id -u):$(id -g) outputs/
```

**OCR Not Working**:
```bash
# Verify Tesseract installation
docker run usb-pd-parser tesseract --version
```

**Large PDF Processing**:
```bash
# Increase memory limit
docker run --memory=2g usb-pd-parser python main.py --input large_file.pdf
```

### Debug Mode
```bash
# Run with debug logging
docker run -v $(pwd)/assets:/app/assets:ro \
           -v $(pwd)/outputs:/app/outputs \
           usb-pd-parser \
           python main.py --input assets/sample.pdf --debug
```

## 🏗️ Building Custom Images

### Dockerfile Customization
```dockerfile
FROM usb-pd-parser:latest

# Add custom dependencies
RUN pip install your-custom-package

# Add custom configuration
COPY your-config.yml /app/application.yml

# Set custom entrypoint
ENTRYPOINT ["python", "main.py"]
```

### Multi-stage Build Example
```dockerfile
# Build stage
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
# ... rest of Dockerfile
```

## 📋 Docker Compose Services

### Production Service
```yaml
services:
  usb-pd-parser:
    build: .
    volumes:
      - ./assets:/app/assets:ro
      - ./outputs:/app/outputs
    command: python main.py --input assets/document.pdf
```

### Development Service
```yaml
services:
  usb-pd-parser-dev:
    build: .
    volumes:
      - .:/app  # Mount entire project
    command: bash
    profiles:
      - dev
```

## 🔐 Security Considerations

### Non-root User
The container runs as a non-root user (`app`) for security.

### Read-only Mounts
Mount input directories as read-only (`:ro`) when possible.

### Network Isolation
The container doesn't expose any ports by default.

## 📈 Monitoring and Logging

### Log Output
```bash
# Follow logs in real-time
docker-compose logs -f usb-pd-parser

# View specific service logs
docker logs container_name
```

### Health Checks
Add health checks to docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import src.app; print('OK')"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🚀 Production Deployment

### Docker Swarm
```bash
# Deploy as a service
docker service create --name usb-pd-parser \
  --mount type=bind,source=/data/pdfs,target=/app/assets,readonly \
  --mount type=bind,source=/data/outputs,target=/app/outputs \
  usb-pd-parser
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: usb-pd-parser
spec:
  replicas: 1
  selector:
    matchLabels:
      app: usb-pd-parser
  template:
    metadata:
      labels:
        app: usb-pd-parser
    spec:
      containers:
      - name: usb-pd-parser
        image: usb-pd-parser:latest
        volumeMounts:
        - name: assets
          mountPath: /app/assets
          readOnly: true
        - name: outputs
          mountPath: /app/outputs
      volumes:
      - name: assets
        hostPath:
          path: /data/pdfs
      - name: outputs
        hostPath:
          path: /data/outputs
```