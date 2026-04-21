---
title: Deployment Guide - BSFM
description: Guia completo de deployment e operação do sistema BodySmart Food Monitor
---

# Deployment Guide - BSFM

## Visão Geral do Deployment

Este guia cobre os processos de deployment, configuração e operação do sistema BSFM em diferentes ambientes.

## Pré-requisitos

### Requisitos do Sistema

#### Hardware Minimum
- **CPU**: 4 cores modernos (8+ cores recomendado)
- **RAM**: 16GB (32GB+ recomendado)
- **Storage**: 100GB SSD (200GB+ para produção)
- **GPU**: NVIDIA GPU com 8GB+ VRAM para ML inference

#### Software Requirements
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Kubernetes**: 1.24+ (para produção)
- **Python**: 3.9+
- **Node.js**: 18+ (para frontend)

### Contas de Cloud Necessárias
- AWS Account (para S3, RDS, EKS)
- Docker Hub Account (para image registry)
- GitHub Account (para CI/CD)

## Ambientes de Deployment

### 1. Ambiente de Desenvolvimento Local

#### Setup com Docker Compose
```bash
# Clone o repositório
git clone https://github.com/bsfm/body-smart-food-monitor.git
cd body-smart-food-monitor

# Configure environment variables
cp .env.example .env
# Edite .env com suas configurações

# Inicie os serviços
docker-compose up -d
```

#### Serviços Locais
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: bsfm
      POSTGRES_USER: bsfm
      POSTGRES_PASSWORD: bsfm123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  ml-service:
    build: ./ml-service
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
```

### 2. Ambiente de Staging

#### Kubernetes Setup
```bash
# Create staging cluster
eksctl create cluster --name bsfm-staging --nodes 3 --node-type t3.medium

# Deploy to staging
kubectl apply -f k8s/staging/
```

#### Staging Configuration
```yaml
# k8s/staging/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bsfm-api
  namespace: staging
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: api
        image: bsfm/api:staging
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "staging"
```

### 3. Ambiente de Produção

#### Production Cluster Setup
```bash
# Create production cluster
eksctl create cluster --name bsfm-production --nodes 5 --node-type m5.large

# Setup monitoring
helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana
```

#### High Availability Configuration
```yaml
# k8s/production/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bsfm-api
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bsfm-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Configuração de Serviços

### Configuração do Database

#### PostgreSQL Configuration
```sql
-- Configure database parameters
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- Create database and user
CREATE DATABASE bsfm;
CREATE USER bsfm WITH ENCRYPTED PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE bsfm TO bsfm;
```

#### Database Migrations
```bash
# Run migrations
alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### Configuração do Redis

#### Redis Configuration
```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Configuração do Nginx

#### Nginx Config
```nginx
# nginx.conf
upstream api {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
    }
}
```

## Deploy Automation

### GitHub Actions CI/CD

#### Build and Test
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: bsfm_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest --cov=app
```

#### Deploy to Staging
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name bsfm-staging
        kubectl apply -f k8s/staging/
```

### Production Deployment

#### Blue-Green Deployment
```bash
# Deploy new version
eksctl create cluster --name bsfm-blue --nodes 3
kubectl apply -f k8s/blue/

# Test new version
curl https://blue.bsfm.com/health

# Switch traffic
eksctl create cluster --name bsfm-green --nodes 3
kubectl apply -f k8s/green/

# Update route53 to point to green
aws route53 change-resource-record-sets --hosted-zone-id Z1XXX --change-batch file://dns-update.json
```

#### Canary Deployment
```yaml
# k8s/canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: bsfm-api
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bsfm-api
  service:
    port: 8000
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      threshold: 99
    - name: request-duration
      threshold: 500
```

## Monitoring and Observability

### Prometheus Configuration

#### Service Monitoring
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'bsfm-api'
    static_configs:
      - targets: ['api1:8000', 'api2:8000', 'api3:8000']
    metrics_path: /metrics

  - job_name: 'bsfm-db'
    static_configs:
      - targets: ['postgres:9187']
```

#### Custom Metrics
```python
# metrics.py
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@REQUEST_DURATION.time()
def handle_request():
    REQUEST_COUNT.inc()
    # Process request
```

### Grafana Dashboards

#### API Dashboard
- Request rate
- Error rate
- Response time
- CPU/Memory usage

#### Database Dashboard
- Query performance
- Connection count
- Cache hit ratio
- Replication lag

#### ML Service Dashboard
- Inference latency
- GPU utilization
- Model performance
- Batch processing metrics

## Backup and Disaster Recovery

### Database Backup

#### Automated Backups
```bash
# PostgreSQL backup
pg_dump -h postgres -U bsfm bsfm > backup.sql

# Upload to S3
aws s3 cp backup.sql s3://bsfm-backups/daily/backup-$(date +%Y%m%d).sql
```

#### Backup Schedule
```yaml
# cron schedule
0 2 * * * /scripts/backup.sh  # Daily at 2AM
0 2 * * 0 /scripts/full-backup.sh  # Weekly full backup
```

### Disaster Recovery Plan

#### Recovery Procedures
1. **Identify failure** - Monitoring alerts
2. **Failover** - Switch to standby database
3. **Restore** - Restore from latest backup
4. **Validate** - Verify data consistency
5. **Failback** - Return to primary

#### Recovery Time Objectives (RTO)
- Database: 15 minutes
- API Services: 5 minutes
- ML Service: 30 minutes

#### Recovery Point Objectives (RPO)
- Database: 5 minutes
- User data: 1 hour
- ML models: 24 hours

## Security Configuration

### Network Security

#### Kubernetes Network Policies
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: bsfm-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### Security Groups
```json
// AWS Security Group
{
  "GroupName": "bsfm-api",
  "IpPermissions": [
    {
      "IpProtocol": "tcp",
      "FromPort": 443,
      "ToPort": 443,
      "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    }
  ]
}
```

### Secret Management

#### Kubernetes Secrets
```bash
# Create secrets
kubectl create secret generic database-secret \
  --from-literal=username=bsfm \
  --from-literal=password='securepassword'
```

#### Environment Variables
```yaml
# deployment.yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: database-secret
      key: connection-string
```

## Performance Optimization

### Database Optimization

#### Indexing Strategy
```sql
-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_foods_name ON foods(name);
CREATE INDEX idx_analyses_timestamp ON analyses(created_at DESC);
```

#### Query Optimization
```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE 
SELECT * FROM users WHERE email = 'user@example.com';
```

### Cache Optimization

#### Redis Configuration
```bash
# Redis tuning
redis-cli config set maxmemory 2gb
redis-cli config set maxmemory-policy allkeys-lru
```

#### Cache Strategies
```python
# Python caching
from redis import Redis
from functools import wraps

redis = Redis()

def cache_response(ttl=300):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = f"cache:{f.__name__}:{args}:{kwargs}"
            cached = redis.get(key)
            if cached:
                return json.loads(cached)
            result = f(*args, **kwargs)
            redis.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

## Scaling Strategies

### Horizontal Scaling

#### Auto-scaling Configuration
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bsfm-api
spec:
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 70
        type: Utilization
```

#### Load Testing
```bash
# Run load test
k6 run --vus 100 --duration 30s script.js
```

### Vertical Scaling

#### Resource Requests
```yaml
# deployment.yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
```

## Maintenance Procedures

### Routine Maintenance

#### Database Maintenance
```sql
-- Weekly maintenance
VACUUM ANALYZE;
REINDEX DATABASE bsfm;
```

#### Log Rotation
```bash
# Logrotate configuration
/var/log/bsfm/*.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

### Update Procedures

#### Software Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt
npm update

# Update base images
FROM python:3.9-slim@sha256:latest
```

#### Security Updates
```bash
# Scan for vulnerabilities
trivy image bsfm/api:latest
snyk test
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connection
psql -h postgres -U bsfm -d bsfm -c "SELECT 1"
```

#### Service Health Checks
```bash
# Check service health
curl http://localhost:8000/health
```

#### Log Analysis
```bash
# View logs
kubectl logs deployment/bsfm-api
journalctl -u bsfm-api
```

### Debug Procedures

#### Performance Debugging
```bash
# CPU profiling
py-spy record -o profile.svg --pid 1234

# Memory profiling
fil-profile run app.py
```

#### Network Debugging
```bash
# Network tracing
tcpdump -i any port 5432
curl -v http://localhost:8000/health
```

---

*Última atualização: Abril 2026*

🚀 **Deployment Status**: Production Ready  
📊 **Environments**: Development, Staging, Production  
🔧 **Automation**: CI/CD Complete