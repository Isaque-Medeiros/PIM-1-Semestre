---
title: Stack DevOps
description: Ferramentas e práticas para desenvolvimento, deployment e operações de software
---

# Stack DevOps

## Visão Geral

Esta stack abrange as ferramentas e práticas de DevOps que utilizo para automatização, deployment, monitoramento e operação de aplicações.

## Version Control

### Git ⭐⭐⭐⭐⭐
**Nível**: Expert
**Experiência**: 2+ anos
**Recursos Dominados**:
- Branching strategies (GitFlow)
- Rebasing vs merging
- Interactive staging
- Submodules
- Hooks

**Comandos Essenciais**:
```bash
# Setup e configuração
git init
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Trabalho diário
git status
git add .
git commit -m "mensagem descritiva"
git push origin main

# Branching
git checkout -b feature/nova-funcionalidade
git merge feature/nova-funcionalidade
git rebase main

# Histórico
git log --oneline --graph --all
git diff
git show
```

### GitHub ⭐⭐⭐⭐⭐
**Plataforma**:
- Repository hosting
- Pull requests
- Issues tracking
- Actions (CI/CD)
- Projects
- Pages

**Workflow**:
1. Feature branches
2. Pull requests com review
3. CI/CD automation
4. Deployment automático

## Containerização

### Docker ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Conceitos**:
- Images e containers
- Dockerfile
- Docker Compose
- Volumes
- Networks

**Dockerfile Exemplo**:
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

**Docker Compose**:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
    
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Docker Hub ⭐⭐⭐
**Registry**:
- Image storage
- Automated builds
- Version tagging
- Public/private repos

## CI/CD (Continuous Integration/Deployment)

### GitHub Actions ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Workflows**:
- Automated testing
- Build automation
- Deployment pipelines
- Scheduled jobs

**Exemplo Workflow**:
```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
        
    - name: Run tests
      env:
        DATABASE_URL: postgresql://test_user:test_pass@postgres:5432/test_db
      run: |
        pytest --cov=app --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Jenkins ⭐⭐⭐
**CI Server**:
- Pipeline as code
- Plugin ecosystem
- Distributed builds
- Enterprise features

## Infrastructure as Code

### Terraform ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 6+ meses
**Conceitos**:
- Resource management
- State management
- Modules
- Provisioners

**Exemplo AWS**:
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-app-data-bucket"
  acl    = "private"
  
  versioning {
    enabled = true
  }
}
```

### Ansible ⭐⭐
**Configuration Management**:
- Playbooks
- Roles
- Inventory management
- Ad-hoc commands

## Cloud Platforms

### AWS ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Serviços Utilizados**:
- EC2 (Elastic Compute)
- S3 (Simple Storage)
- Lambda (Serverless)
- RDS (Relational Database)
- IAM (Identity Access)
- CloudFront (CDN)

### Microsoft Azure ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Serviços**:
- App Service
- Functions
- Storage Accounts
- SQL Database
- DevOps Pipelines

### Google Cloud Platform ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 6+ meses
**Serviços**:
- Compute Engine
- Cloud Storage
- Cloud Functions
- BigQuery

## Monitoring & Logging

### Prometheus ⭐⭐⭐
**Monitoring**:
- Time-series data
- Metrics collection
- Alerting rules
- Exporters

**Exemplo Config**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'webapp'
    static_configs:
      - targets: ['localhost:5000']
```

### Grafana ⭐⭐⭐
**Visualization**:
- Dashboards
- Data sources
- Alerting
- Templates

### ELK Stack ⭐⭐
**Logging**:
- Elasticsearch
- Logstash
- Kibana
- Filebeat

## Web Servers & Proxies

### Nginx ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Configurações**:
- Reverse proxy
- Load balancing
- SSL termination
- Static file serving
- Caching

**Exemplo Config**:
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /app/static/;
        expires 30d;
    }
}
```

### Apache ⭐⭐⭐
**Web Server**:
- .htaccess
- Virtual hosts
- Modules
- CGI scripts

## Security

### SSL/TLS ⭐⭐⭐⭐
**Encryption**:
- Certificate management
- Let's Encrypt
- HTTPS configuration
- HSTS headers

### Security Best Practices ⭐⭐⭐⭐
**Práticas**:
- Principle of least privilege
- Regular updates
- Security scanning
- Access controls

**Tools**:
- snyk (vulnerability scanning)
- trivy (container scanning)
- bandit (Python security)

## Database Management

### Backup Strategies ⭐⭐⭐⭐
**Estratégias**:
- Automated backups
- Point-in-time recovery
- Off-site storage
- Backup verification

**Ferramentas**:
- pg_dump (PostgreSQL)
- mysqldump (MySQL)
- mongodump (MongoDB)

### Database Migration ⭐⭐⭐⭐
**Ferramentas**:
- Alembic (SQLAlchemy)
- Django migrations
- Flyway
- Liquibase

## Performance Optimization

### Caching Strategies ⭐⭐⭐⭐
**Técnicas**:
- CDN caching
- Browser caching
- Database caching
- Application caching

**Ferramentas**:
- Redis
- Memcached
- Varnish

### Load Testing ⭐⭐⭐
**Ferramentas**:
- k6
- Locust
- JMeter
- Artillery

## Development Tools

### VS Code ⭐⭐⭐⭐⭐
**IDE Principal**:
- Extensions
- Debugging
- Integrated terminal
- Git integration

**Extensions Úteis**:
- Docker
- Terraform
- Python
- GitLens
- Remote - Containers

### Command Line Tools ⭐⭐⭐⭐⭐
**Ferramentas**:
- curl
- jq (JSON processing)
- ssh
- rsync
- tmux
- htop

## Project Management

### Agile Methodology ⭐⭐⭐⭐
**Metodologias**:
- Scrum
- Kanban
- Sprint planning
- Retrospectives

### Tools ⭐⭐⭐⭐
**Plataformas**:
- Jira
- Trello
- Asana
- GitHub Projects

## Documentation

### MkDocs ⭐⭐⭐⭐
**Documentation**:
- Markdown-based
- Theme customization
- GitHub Pages deployment
- Search functionality

### ReadTheDocs ⭐⭐⭐
**Documentation Hosting**:
- Automated builds
- Versioning
- PDF generation

## Learning Path

### Concluído ✅
- Git & GitHub mastery
- Docker fundamentals
- CI/CD basics
- Cloud basics (AWS/Azure)
- Web server configuration

### Em Progresso 🚧
- Advanced Docker
- Kubernetes fundamentals
- Terraform infrastructure
- Advanced CI/CD pipelines
- Monitoring stack

### Próximos Steps 📅
- Kubernetes certification
- Advanced cloud architecture
- Service mesh (Istio/Linkerd)
- GitOps practices
- Security scanning automation

## Projetos em Destaque

### Automated Deployment Pipeline
**Tecnologias**: GitHub Actions, Docker, AWS
**Features**:
- Automated testing
- Container builds
- Deployment to staging/production
- Rollback capabilities

### Infrastructure as Code
**Tecnologias**: Terraform, AWS
**Recursos**:
- VPC configuration
- EC2 instances
- S3 buckets
- Security groups
- IAM roles

### Monitoring Stack
**Tecnologias**: Prometheus, Grafana, Docker
**Métricas**:
- Application performance
- Resource usage
- Error rates
- Business metrics

## Estatísticas de Uso

### Pipeline Efficiency
```python
ci_cd_metrics = {
    "build_time": "3-5 minutes",
    "test_coverage": "85%+",
    "deployment_frequency": "Daily",
    "change_failure_rate": "< 5%"
}
```

### Resource Usage
```python
resource_usage = {
    "containers_running": 15,
    "cloud_services": 8,
    "monitored_endpoints": 25,
    "automated_tests": 200+
}
```

### Availability
```python
availability = {
    "uptime": "99.9%",
    "response_time": "< 200ms",
    "incidents_monthly": "0-1",
    "recovery_time": "< 15 minutes"
}
```

## Best Practices

### Infrastructure as Code
- Version control all infrastructure
- Use modules for reusability
- Regular terraform fmt
- State file management

### Containerization
- Use multi-stage builds
- Keep images small
- Use .dockerignore
- Security scanning

### CI/CD
- Fast feedback loops
- Comprehensive testing
- Deployment strategies
- Environment parity

### Monitoring
- Monitor business metrics
- Set meaningful alerts
- Regular review of dashboards
- Capacity planning

---

*Última atualização: Abril 2026*

🚀 **DevOps Stack**: Automatizada e confiável  
🎯 **Foco Atual**: Kubernetes e GitOps  
📊 **Nível Geral**: Intermediário-Avançado