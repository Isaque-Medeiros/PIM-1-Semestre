---
title: Stack Database
description: Tecnologias e estratégias para gestão e otimização de bancos de dados
---

# Stack Database

## Visão Geral

Esta stack abrange as tecnologias de banco de dados que utilizo, desde sistemas relacionais SQL até bancos NoSQL, incluindo ORMs, ferramentas de migração e otimização.

## Sistemas de Banco de Dados

### SQLite ⭐⭐⭐⭐⭐
**Nível**: Expert
**Experiência**: 2+ anos
**Características**:
- Serverless architecture
- Zero configuration
- File-based storage
- ACID compliant

**Casos de Uso**:
- Desenvolvimento local
- Prototyping rápido
- Aplicações simples
- Testing environments

**Exemplo de Uso**:
```python
import sqlite3

# Conexão com database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Inserir dados
cursor.execute(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    ('João Silva', 'joao@email.com')
)

conn.commit()
conn.close()
```

### PostgreSQL ⭐⭐⭐⭐
**Nível**: Avançado
**Experiência**: 1+ ano
**Recursos Avançados**:
- JSONB data type
- Full-text search
- Geographic objects
- Advanced indexing

**Vantagens**:
- Enterprise features
- Extensibility
- Performance
- Reliability

### MySQL ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 6+ meses
**Uso**:
- Web applications
- Content management
- E-commerce systems

### MongoDB ⭐⭐⭐
**Nível**: Intermediário
**Experiência**: 6+ meses
**Características NoSQL**:
- Document-oriented
- Flexible schema
- Horizontal scaling
- Aggregation framework

## ORMs (Object-Relational Mappers)

### SQLAlchemy ⭐⭐⭐⭐⭐
**Python ORM**:
- SQL expression language
- ORM patterns
- Database abstraction
- Session management

**Core Features**:
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Database setup
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
```

### Django ORM ⭐⭐⭐⭐
**ORM Integrado**:
- Django integration
- Migrations automáticas
- QuerySet API
- Admin interface

**Exemplo**:
```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

### Mongoose ⭐⭐⭐
**MongoDB ODM**:
- Schema validation
- Middleware hooks
- Population
- Query building

## Ferramentas de Migração

### Alembic ⭐⭐⭐⭐
**Database Migrations**:
- Version control
- Schema changes
- Data migrations
- Downgrade support

**Comandos Principais**:
```bash
# Inicializar alembic
alembic init migrations

# Criar nova migration
alembic revision -m "create_users_table"

# Aplicar migrations
alembic upgrade head

# Reverter migration
alembic downgrade -1
```

### Django Migrations ⭐⭐⭐⭐
**Sistema Integrado**:
- Automatic migration generation
- Dependency tracking
- Schema evolution

**Uso**:
```bash
# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Migration status
python manage.py showmigrations
```

## Design de Banco de Dados

### Normalização ⭐⭐⭐⭐⭐
**Princípios**:
- 1NF: Atomic values
- 2NF: No partial dependencies
- 3NF: No transitive dependencies
- BCNF: Boyce-Codd Normal Form

### Modelagem de Dados
**Entidade-Relacionamento**:
- Entities and attributes
- Relationships (1:1, 1:N, M:N)
- Cardinality
- Optionality

**Exemplo Diagrama**:
```
USER (Entity)
├── id (PK)
├── name
├── email
└── created_at

POST (Entity) 
├── id (PK)
├── title
├── content
├── user_id (FK → USER.id)
└── created_at

1 USER : N POSTS (Relationship)
```

### Indexação ⭐⭐⭐⭐
**Estratégias**:
- Primary keys
- Foreign keys
- Unique indexes
- Composite indexes
- Full-text indexes

**Performance Considerations**:
- Read vs write tradeoffs
- Index maintenance
- Query optimization

## Query Optimization

### SQL Optimization ⭐⭐⭐⭐
**Técnicas**:
- EXPLAIN queries
- Index usage analysis
- Query rewriting
- Join optimization

**Exemplo EXPLAIN**:
```sql
EXPLAIN ANALYZE 
SELECT * FROM users 
WHERE email = 'joao@email.com';
```

### ORM Optimization ⭐⭐⭐⭐
**Best Practices**:
- Eager loading
- Select only needed fields
- Batch operations
- Connection pooling

**Exemplo Otimizado**:
```python
# Ruim: N+1 queries
users = session.query(User).all()
for user in users:
    print(user.posts)  # Nova query para cada user

# Bom: Eager loading
users = session.query(User).options(joinedload(User.posts)).all()
for user in users:
    print(user.posts)  # Todos os posts carregados de uma vez
```

## Transações e Concorrência

### ACID Properties ⭐⭐⭐⭐⭐
**Garantias**:
- Atomicity: Todas ou nenhuma operação
- Consistency: Restrições mantidas
- Isolation: Execução isolada
- Durability: Dados persistentes

### Níveis de Isolamento ⭐⭐⭐⭐
**SQL Standard**:
- Read Uncommitted
- Read Committed
- Repeatable Read
- Serializable

### Locking Strategies ⭐⭐⭐
**Tipos de Lock**:
- Row-level locking
- Table-level locking
- Optimistic locking
- Pessimistic locking

## Backup e Recovery

### Estratégias de Backup ⭐⭐⭐⭐
**Tipos**:
- Full backup
- Incremental backup
- Differential backup
- Point-in-time recovery

**Ferramentas**:
- pg_dump (PostgreSQL)
- mysqldump (MySQL)
- MongoDB dump tools

### Recovery Procedures ⭐⭐⭐⭐
**Procedimentos**:
- Backup verification
- Recovery testing
- Disaster recovery plans
- High availability setups

## Monitoramento e Performance

### Monitoring Tools ⭐⭐⭐
**Ferramentas**:
- pgAdmin (PostgreSQL)
- MySQL Workbench
- MongoDB Compass
- Custom dashboards

### Key Metrics ⭐⭐⭐⭐
**Métricas**:
- Query response time
- Connection count
- Cache hit ratio
- Disk I/O
- Lock contention

**Exemplo Monitoring**:
```sql
-- PostgreSQL performance queries
SELECT * FROM pg_stat_database;
SELECT * FROM pg_stat_user_tables;
SELECT * FROM pg_locks;
```

## Segurança de Dados

### Authentication ⭐⭐⭐⭐
**Métodos**:
- Password authentication
- Certificate-based auth
- LDAP integration
- OAuth integration

### Authorization ⭐⭐⭐⭐
**Controle de Acesso**:
- Role-based access control
- Row-level security
- Column privileges
- Schema permissions

### Encryption ⭐⭐⭐
**Técnicas**:
- Data-at-rest encryption
- Data-in-transit encryption
- Column-level encryption
- Transparent data encryption

## Ferramentas e Utilities

### Admin Interfaces ⭐⭐⭐⭐
**Ferramentas**:
- Django Admin
- pgAdmin
- MySQL Workbench
- MongoDB Compass
- SQLite Browser

### CLI Tools ⭐⭐⭐⭐
**Comandos**:
- psql (PostgreSQL)
- mysql (MySQL)
- mongo (MongoDB)
- sqlite3 (SQLite)

### GUI Clients ⭐⭐⭐
**Aplicações**:
- DBeaver
- TablePlus
- DataGrip
- Navicat

## Projetos em Destaque

### SysAcad Database Design
**Tecnologias**: SQLite, File-based storage
**Design**:
- Normalized schema
- Relationships: Students, Courses, Grades
- Transaction management
- Data integrity constraints

### E-commerce Database
**Tecnologias**: PostgreSQL, SQLAlchemy
**Features**:
- User management
- Product catalog
- Order processing
- Payment integration
- Inventory management

### Analytics Platform
**Tecnologias**: MongoDB, Mongoose
**Características**:
- Flexible schema for event data
- High write throughput
- Aggregation pipelines
- Real-time analytics

## Best Practices

### Naming Conventions ⭐⭐⭐⭐⭐
**Padrões**:
- snake_case para tabelas e colunas
- Plural table names (users, products)
- Singular column names (first_name, email)
- Consistent naming across system

### Schema Design ⭐⭐⭐⭐⭐
**Princípios**:
- Use appropriate data types
- Set NOT NULL constraints
- Define primary and foreign keys
- Add indexes strategically
- Document schema decisions

### Data Validation ⭐⭐⭐⭐
**Validação**:
- Database constraints
- Application-level validation
- Input sanitization
- Type checking

## Learning Path

### Concluído ✅
- SQL Fundamentals
- Database Design
- Basic Optimization
- Transaction Management
- ORM Patterns

### Em Progresso 🚧
- Advanced PostgreSQL Features
- Database Scaling
- High Availability
- Advanced Indexing
- Performance Tuning

### Próximos Steps 📅
- Database Sharding
- Replication Strategies
- Data Warehousing
- Big Data Technologies
- Cloud Database Services

## Estatísticas de Uso

### Projetos por Tecnologia
```python
database_usage = {
    "SQLite": 12,
    "PostgreSQL": 5,
    "MySQL": 3,
    "MongoDB": 4,
    "In-memory": 2
}
```

### Performance Metrics
- **Query Time**: < 100ms (95% queries)
- **Cache Hit Ratio**: > 90%
- **Uptime**: 99.9%
- **Backup Frequency**: Daily

### Schema Statistics
- **Tables Designed**: 50+
- **Relationships**: 100+
- **Indexes Created**: 80+
- **Migrations Executed**: 200+

---

*Última atualização: Abril 2026*

🚀 **Database Stack**: Robusta e performática  
🎯 **Foco Atual**: Otimização e scaling  
📊 **Nível Geral**: Intermediário-Avançado