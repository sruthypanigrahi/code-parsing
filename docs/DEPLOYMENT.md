# Deployment Guide

Complete deployment guide for USB PD Specification Parser in various environments.

## Production Deployment

### 1. Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Create output directory
RUN mkdir -p outputs

# Expose port (if running as web service)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.pdf_extractor import PDFExtractor; print('OK')" || exit 1

# Default command
CMD ["python", "main.py", "--mode", "3"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  usb-pd-parser:
    build: .
    container_name: usb-pd-parser
    volumes:
      - ./assets:/app/assets:ro
      - ./outputs:/app/outputs
      - ./application.yml:/app/application.yml:ro
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=INFO
    restart: unless-stopped
    mem_limit: 2g
    cpus: 2.0
    
  # Optional: Web interface
  web-interface:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "8080:8000"
    depends_on:
      - usb-pd-parser
    environment:
      - PARSER_SERVICE_URL=http://usb-pd-parser:8000
```

#### Build and Run
```bash
# Build image
docker build -t usb-pd-parser .

# Run container
docker run -d \
  --name usb-pd-parser \
  -v $(pwd)/assets:/app/assets:ro \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/application.yml:/app/application.yml:ro \
  --memory=2g \
  --cpus=2.0 \
  usb-pd-parser

# Using Docker Compose
docker-compose up -d

# Check logs
docker logs usb-pd-parser

# Execute commands in container
docker exec -it usb-pd-parser python main.py --mode 1
```

### 2. Kubernetes Deployment

#### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: usb-pd-parser
  labels:
    app: usb-pd-parser
spec:
  replicas: 2
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
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: PYTHONPATH
          value: "/app"
        volumeMounts:
        - name: config-volume
          mountPath: /app/application.yml
          subPath: application.yml
        - name: assets-volume
          mountPath: /app/assets
        - name: outputs-volume
          mountPath: /app/outputs
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "from src.pdf_extractor import PDFExtractor; print('OK')"
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import sys; sys.exit(0)"
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: config-volume
        configMap:
          name: usb-pd-parser-config
      - name: assets-volume
        persistentVolumeClaim:
          claimName: assets-pvc
      - name: outputs-volume
        persistentVolumeClaim:
          claimName: outputs-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: usb-pd-parser-service
spec:
  selector:
    app: usb-pd-parser
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: usb-pd-parser-config
data:
  application.yml: |
    pdf_input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
    output_directory: "outputs"
    ocr_fallback: true
    max_pages: null
```

#### Deploy to Kubernetes
```bash
# Apply configuration
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods

# Check logs
kubectl logs -l app=usb-pd-parser

# Scale deployment
kubectl scale deployment usb-pd-parser --replicas=3

# Update deployment
kubectl set image deployment/usb-pd-parser usb-pd-parser=usb-pd-parser:v2.0
```

### 3. Cloud Deployment

#### AWS ECS Deployment
```json
{
  "family": "usb-pd-parser",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "usb-pd-parser",
      "image": "your-account.dkr.ecr.region.amazonaws.com/usb-pd-parser:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "efs-storage",
          "containerPath": "/app/outputs"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/usb-pd-parser",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "volumes": [
    {
      "name": "efs-storage",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-12345678"
      }
    }
  ]
}
```

#### Google Cloud Run
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: usb-pd-parser
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/memory: "2Gi"
        run.googleapis.com/cpu: "1000m"
        run.googleapis.com/execution-environment: gen2
    spec:
      containerConcurrency: 1
      timeoutSeconds: 3600
      containers:
      - image: gcr.io/project-id/usb-pd-parser:latest
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: INFO
        resources:
          limits:
            memory: 2Gi
            cpu: 1000m
        volumeMounts:
        - name: gcs-storage
          mountPath: /app/outputs
      volumes:
      - name: gcs-storage
        csi:
          driver: gcsfuse.csi.storage.gke.io
          volumeAttributes:
            bucketName: your-storage-bucket
```

### 4. Serverless Deployment

#### AWS Lambda
```python
# lambda_handler.py
import json
import boto3
from pathlib import Path
import tempfile
import os
from src.pipeline_orchestrator import PipelineOrchestrator

def lambda_handler(event, context):
    """AWS Lambda handler for PDF processing."""
    
    try:
        # Get S3 bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Download PDF from S3
        s3 = boto3.client('s3')
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            s3.download_file(bucket, key, tmp_file.name)
            pdf_path = tmp_file.name
        
        try:
            # Process PDF
            orchestrator = PipelineOrchestrator()
            results = orchestrator.run_full_pipeline(mode=3)  # Memory-safe mode
            
            # Upload results to S3
            output_bucket = os.environ['OUTPUT_BUCKET']
            
            for file_type, file_path in [
                ('toc', results['toc_path']),
                ('content', results['content_path']),
                ('spec', results['spec_path'])
            ]:
                s3_key = f"processed/{Path(key).stem}_{file_type}.jsonl"
                s3.upload_file(file_path, output_bucket, s3_key)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Processing completed successfully',
                    'results': results
                })
            }
            
        finally:
            # Clean up temporary file
            os.unlink(pdf_path)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
```

#### Serverless Framework Configuration
```yaml
# serverless.yml
service: usb-pd-parser

provider:
  name: aws
  runtime: python3.9
  region: us-west-2
  memorySize: 3008
  timeout: 900
  environment:
    OUTPUT_BUCKET: ${self:custom.outputBucket}
  iamRoleStatements:
    - Effect: Allow
      Action:
        - s3:GetObject
        - s3:PutObject
      Resource: 
        - "arn:aws:s3:::${self:custom.inputBucket}/*"
        - "arn:aws:s3:::${self:custom.outputBucket}/*"

functions:
  processPDF:
    handler: lambda_handler.lambda_handler
    events:
      - s3:
          bucket: ${self:custom.inputBucket}
          event: s3:ObjectCreated:*
          rules:
            - suffix: .pdf

custom:
  inputBucket: usb-pd-parser-input
  outputBucket: usb-pd-parser-output

plugins:
  - serverless-python-requirements

package:
  exclude:
    - tests/**
    - docs/**
    - .git/**
```

## Environment-Specific Configurations

### 1. Development Environment

```yaml
# application.dev.yml
pdf_input_file: "assets/sample.pdf"
output_directory: "dev_outputs"
ocr_fallback: false
max_pages: 50

# Development logging
logging:
  level: DEBUG
  file: "dev_outputs/parser.log"

# Development database
database:
  url: "sqlite:///dev_parser.db"
```

### 2. Staging Environment

```yaml
# application.staging.yml
pdf_input_file: "assets/staging_document.pdf"
output_directory: "/var/app/outputs"
ocr_fallback: true
max_pages: null

# Staging logging
logging:
  level: INFO
  file: "/var/log/usb-pd-parser/parser.log"

# Staging database
database:
  url: "postgresql://user:pass@staging-db:5432/parser"

# Performance settings
performance:
  max_workers: 4
  batch_size: 100
  timeout: 1800
```

### 3. Production Environment

```yaml
# application.prod.yml
pdf_input_file: "${PDF_INPUT_PATH}"
output_directory: "${OUTPUT_DIRECTORY}"
ocr_fallback: true
max_pages: null

# Production logging
logging:
  level: WARNING
  file: "/var/log/usb-pd-parser/parser.log"
  max_size: "100MB"
  backup_count: 5

# Production database
database:
  url: "${DATABASE_URL}"
  pool_size: 20
  max_overflow: 30

# Production performance
performance:
  max_workers: 8
  batch_size: 200
  timeout: 3600
  memory_limit: "4GB"

# Monitoring
monitoring:
  enabled: true
  metrics_endpoint: "${METRICS_ENDPOINT}"
  health_check_port: 8080
```

## Monitoring and Logging

### 1. Application Monitoring

```python
# monitoring.py
import psutil
import time
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Metrics
PROCESSED_PDFS = Counter('processed_pdfs_total', 'Total processed PDFs')
PROCESSING_TIME = Histogram('processing_time_seconds', 'PDF processing time')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')

class MonitoringService:
    def __init__(self, port=8080):
        self.port = port
        start_http_server(port)
    
    def record_processing(self, processing_time):
        PROCESSED_PDFS.inc()
        PROCESSING_TIME.observe(processing_time)
    
    def update_system_metrics(self):
        process = psutil.Process()
        MEMORY_USAGE.set(process.memory_info().rss)
        CPU_USAGE.set(process.cpu_percent())

# Usage in main application
monitoring = MonitoringService()

@PROCESSING_TIME.time()
def process_pdf():
    # Processing logic
    pass
```

### 2. Structured Logging

```python
# structured_logging.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        handler = logging.StreamHandler()
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            if hasattr(record, 'extra_data'):
                log_entry.update(record.extra_data)
            
            return json.dumps(log_entry)
    
    def info(self, message, **kwargs):
        self.logger.info(message, extra={'extra_data': kwargs})
    
    def error(self, message, **kwargs):
        self.logger.error(message, extra={'extra_data': kwargs})

# Usage
logger = StructuredLogger('usb-pd-parser')
logger.info("Processing started", pdf_file="document.pdf", mode=1)
```

### 3. Health Checks

```python
# health_check.py
from flask import Flask, jsonify
import psutil
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health/detailed')
def detailed_health_check():
    """Detailed health check with system metrics."""
    
    # Check system resources
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Check required directories
    required_dirs = ['assets', 'outputs']
    dir_status = {}
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        dir_status[dir_name] = {
            'exists': dir_path.exists(),
            'writable': os.access(dir_path, os.W_OK) if dir_path.exists() else False
        }
    
    # Check dependencies
    try:
        import fitz
        import pdfplumber
        dependencies_ok = True
    except ImportError:
        dependencies_ok = False
    
    health_status = {
        'status': 'healthy' if dependencies_ok else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'system': {
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'cpu_percent': psutil.cpu_percent()
        },
        'directories': dir_status,
        'dependencies': dependencies_ok
    }
    
    status_code = 200 if dependencies_ok else 503
    return jsonify(health_status), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Security Considerations

### 1. Container Security

```dockerfile
# Security-hardened Dockerfile
FROM python:3.9-slim

# Install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc g++ libmupdf-dev && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set secure permissions
WORKDIR /app
COPY --chown=appuser:appgroup . .

# Install dependencies as root, then switch to non-root
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER appuser

# Remove unnecessary packages
RUN apt-get autoremove -y gcc g++

# Set security options
LABEL security.scan="enabled"
```

### 2. Network Security

```yaml
# docker-compose.yml with network security
version: '3.8'

services:
  usb-pd-parser:
    build: .
    networks:
      - internal
    # Don't expose ports directly
    
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - internal
      - external
    depends_on:
      - usb-pd-parser

networks:
  internal:
    driver: bridge
    internal: true
  external:
    driver: bridge
```

### 3. Secrets Management

```python
# secrets_manager.py
import os
from typing import Optional

class SecretsManager:
    """Manage secrets from environment or external services."""
    
    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> str:
        """Get secret from environment or external service."""
        
        # Try environment variable first
        value = os.getenv(key, default)
        
        if value is None:
            # Try AWS Secrets Manager
            try:
                import boto3
                client = boto3.client('secretsmanager')
                response = client.get_secret_value(SecretId=key)
                value = response['SecretString']
            except:
                pass
        
        if value is None:
            raise ValueError(f"Secret {key} not found")
        
        return value

# Usage
database_url = SecretsManager.get_secret('DATABASE_URL')
api_key = SecretsManager.get_secret('API_KEY')
```

## Backup and Recovery

### 1. Data Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/usb-pd-parser"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup outputs
tar -czf "$BACKUP_DIR/$DATE/outputs.tar.gz" outputs/

# Backup configuration
cp application.yml "$BACKUP_DIR/$DATE/"

# Backup database (if applicable)
if [ -f "parser.db" ]; then
    cp parser.db "$BACKUP_DIR/$DATE/"
fi

# Clean old backups (keep last 30 days)
find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR/$DATE"
```

### 2. Disaster Recovery

```python
# disaster_recovery.py
import shutil
from pathlib import Path
import logging

class DisasterRecovery:
    """Handle disaster recovery scenarios."""
    
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.logger = logging.getLogger(__name__)
    
    def create_checkpoint(self, checkpoint_name: str):
        """Create a recovery checkpoint."""
        checkpoint_dir = self.backup_dir / checkpoint_name
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup critical files
        critical_files = [
            'application.yml',
            'outputs/',
            'parser.db'
        ]
        
        for file_path in critical_files:
            source = Path(file_path)
            if source.exists():
                if source.is_file():
                    shutil.copy2(source, checkpoint_dir)
                else:
                    shutil.copytree(source, checkpoint_dir / source.name, dirs_exist_ok=True)
        
        self.logger.info(f"Checkpoint created: {checkpoint_name}")
    
    def restore_from_checkpoint(self, checkpoint_name: str):
        """Restore from a checkpoint."""
        checkpoint_dir = self.backup_dir / checkpoint_name
        
        if not checkpoint_dir.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_name}")
        
        # Restore files
        for item in checkpoint_dir.iterdir():
            target = Path(item.name)
            
            if item.is_file():
                shutil.copy2(item, target)
            else:
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
        
        self.logger.info(f"Restored from checkpoint: {checkpoint_name}")

# Usage
recovery = DisasterRecovery("/backups/usb-pd-parser")
recovery.create_checkpoint("before_upgrade")
```

This comprehensive deployment guide covers all aspects of deploying the USB PD Parser in various environments, from development to production, with proper security, monitoring, and disaster recovery considerations.