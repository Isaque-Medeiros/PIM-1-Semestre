---
title: Stack Backend
description: Tecnologias e frameworks para desenvolvimento backend e APIs
---

# Stack Backend

## Visão Geral

Esta stack representa as tecnologias backend que domino para desenvolvimento de APIs, serviços web e aplicações server-side.

## Linguagens Principais

### Python ⭐⭐⭐⭐⭐
**Nível**: Expert
**Experiência**: 2+ anos
**Frameworks**:
- Flask (Microframework)
- Django (Full-stack)
- FastAPI (Modern APIs)

**Bibliotecas Chave**:
```python
# Web Development
flask, django, fastapi, requests

# Data Processing  
pandas, numpy, matplotlib

# AI/ML
tensorflow, sklearn, nltk

# Utilities
os, sys, json, datetime
```

**Exemplo Flask**:
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = [
        {'id': 1, 'name': 'João', 'email': 'joao@email.com'},
        {'id': 2, 'name': 'Maria', 'email': 'maria@email.com'}
    ]
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # Lógica de criação de usuário
    return jsonify({'message': 'User created', 'data': data}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

### Node.js ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 1+ ano
**Frameworks**:
- Express.js (Web framework)
- Nest.js (Em aprendizado)

**Características**:
- Non-blocking I/O
- Event-driven architecture
- NPM ecosystem

### C++ ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 1+ ano
**Uso**:
- Sistemas acadêmicos
- Algoritmos complexos
- Performance-critical code

## Frameworks Web

### Flask ⭐⭐⭐⭐
**Microframework Python**:
- Simplicidade e flexibilidade
- Extensível com extensions
- Ideal para APIs e microservices

**Extensions Utilizadas**:
- Flask-SQLAlchemy (ORM)
- Flask-Marshmallow (Serialization)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-origin)

### Django ⭐⭐⭐
**Full-stack Framework**:
- Batteries included
- ORM poderoso
- Admin interface
- Security features

**Recursos**:
- Django REST Framework (APIs)
- Django Templates
- Authentication system
- Database migrations

### FastAPI ⭐⭐⭐
**Modern API Framework**:
- High performance
- Automatic docs (Swagger)
- Type hints integration
- Async support

**Vantagens**:
- Fast development
- Data validation
- Dependency injection
- OpenAPI standard

## Bancos de Dados

### SQLite ⭐⭐⭐⭐
**Database Embarcado**:
- Ideal para desenvolvimento
- Zero configuration
- File-based storage

**Uso em Projetos**:
- Prototyping rápido
- Aplicações simples
- Testing environments

### PostgreSQL ⭐⭐⭐
**Database Relacional**:
- Enterprise features
- JSON support
- Advanced data types

**Recursos**:
- Transactions ACID
- Foreign keys
- Stored procedures
- Full-text search

### MongoDB ⭐⭐
**NoSQL Database**:
- Document-oriented
- Flexible schema
- Horizontal scaling

**Casos de Uso**:
- Dados não estruturados
- High write throughput
- Rapid prototyping

## ORMs e Database Tools

### SQLAlchemy ⭐⭐⭐⭐
**Python ORM**:
- SQL expression language
- Object-relational mapping
- Database abstraction

**Exemplo**:
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

# Database setup
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

### Mongoose ⭐⭐
**MongoDB ODM**:
- Schema definition
- Data validation
- Middleware support

### Alembic ⭐⭐⭐
**Database Migrations**:
- Version control for database
- Schema changes tracking
- Automatic migration generation

## Autenticação e Segurança

### JWT (JSON Web Tokens) ⭐⭐⭐⭐
**Authentication**:
- Stateless authentication
- Token-based security
- Refresh tokens

**Implementação**:
```python
from flask_jwt_extended import JWTManager, create_access_token

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Create token
def login():
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
```

### OAuth2 ⭐⭐⭐
**Authorization Framework**:
- Third-party authentication
- Social login integration
- Scope-based permissions

### HTTPS/SSL ⭐⭐⭐⭐
**Security**:
- Encrypted communication
- Certificate management
- Secure headers

## APIs e Microservices

### REST APIs ⭐⭐⭐⭐
**Design Principles**:
- Resource-based URLs
- HTTP methods semantics
- Stateless communication
- JSON responses

**Best Practices**:
- Versioning (/api/v1/)
- Pagination
- Filtering and sorting
- Error handling

### GraphQL ⭐⭐
**Query Language**:
- Single endpoint
- Client-defined responses
- Strong typing
- Introspection

### gRPC ⭐
**High-performance RPC**:
- Protocol Buffers
- HTTP/2 transport
- Streaming support

## Message Queues e Background Jobs

### Celery ⭐⭐⭐
**Distributed Task Queue**:
- Async task execution
- Periodic tasks
- Result backend

**Exemplo**:
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_data(data):
    # Processamento demorado
    return result
```

### Redis ⭐⭐⭐
**In-memory Data Store**:
- Caching
- Session storage
- Message broker
- Rate limiting

## Deployment e DevOps

### Docker ⭐⭐⭐
**Containerization**:
- Application packaging
- Environment consistency
- Microservices deployment

**Dockerfile Example**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Nginx ⭐⭐⭐
**Web Server**:
- Reverse proxy
- Load balancing
- Static file serving
- SSL termination

### Gunicorn ⭐⭐⭐
**WSGI Server**:
- Python application server
- Process management
- Performance optimization

## Monitoramento e Logging

### Logging ⭐⭐⭐⭐
**Application Logs**:
- Structured logging
- Log levels
- Log rotation
- Centralized logging

**Python Logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info('Application started')
```

### Metrics ⭐⭐⭐
**Performance Monitoring**:
- Response times
- Error rates
- Resource usage
- Business metrics

## Projetos em Destaque

### SysAcad Management System
**Tecnologias**: C++, File-based storage
**Features**:
- Complete academic management
- Student/teacher/course management
- Grade tracking
- Report generation

### Intelligent Assistant API
**Tecnologias**: Python, Flask, SQLite
**Features**:
- RESTful API
- JWT authentication
- AI integration
- Database persistence

### Cloud Deployment Projects
**Tecnologias**: Python, FastAPI, PostgreSQL
**Features**:
- High-performance APIs
- Database migrations
- Container deployment
- Cloud integration

## Fluxo de Desenvolvimento

### Setup Projeto Python
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows

# Install dependencies
pip install flask flask-sqlalchemy flask-jwt-extended

# Run application
python app.py
```

### Estrutura de Projeto
```
project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   └── utils.py
├── tests/
│   ├── test_models.py
│   └── test_routes.py
├── requirements.txt
├── config.py
└── app.py
```

### API Design Guidelines
```python
# Good REST practices
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.from_dict(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

## Learning Path

### Concluído ✅
- Python Fundamentals
- Flask Web Development
- REST API Design
- Basic Database Design
- Authentication Systems

### Em Progresso 🚧
- Advanced Django
- FastAPI Performance
- PostgreSQL Advanced Features
- Docker Containerization
- Microservices Architecture

### Próximos Steps 📅
- Kubernetes Orchestration
- Message Queues (RabbitMQ)
- GraphQL Implementation
- Serverless Functions
- Advanced Security Practices

## Estatísticas de Uso

### Projetos por Tecnologia
```python
backend_projects = {
    "Flask": 8,
    "Django": 3,
    "FastAPI": 2,
    "C++ Systems": 5,
    "Other": 4
}
```

### Linhas de Código
```python
loc_backend = {
    "Python": 12000,
    "C++": 5000,
    "SQL": 2000,
    "Configuration": 1000
}
```

### Performance Metrics
- **API Response Time**: < 200ms
- **Database Queries**: < 50ms
- **Error Rate**: < 1%
- **Uptime**: 99.9% (development)

---

*Última atualização: Abril 2026*

🚀 **Backend Stack**: Robusta e escalável  
🎯 **Foco Atual**: APIs de alta performance  
📊 **Nível Geral**: Intermediário-Avançado