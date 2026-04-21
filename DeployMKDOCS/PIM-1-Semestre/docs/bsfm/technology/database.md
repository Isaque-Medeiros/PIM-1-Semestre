---
title: Banco de Dados
description: Arquitetura e gerenciamento de dados no BSFM
---

# 🗄️ Banco de Dados

Arquitetura de dados robusta e escalável para armazenamento de informações nutricionais, perfis de usuários e análises do sistema BSFM.

## 🎯 Visão Geral

O BSFM utiliza uma arquitetura de banco de dados híbrida combinando:
- **PostgreSQL** - Dados estruturados e transacionais  
- **JSON Documents** - Dados semi-estruturados e flexíveis
- **Cache Redis** - Performance e sessões em tempo real
- **Armazenamento de Arquivos** - Uploads e recursos estáticos

## 🏗️ Arquitetura de Dados

### **Modelo Entidade-Relacionamento**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Users       │    │     Foods       │    │    Meals        │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ email           │    │ name           │    │ user_id (FK)    │
│ password_hash   │    │ category       │    │ date_time       │
│ profile_data    │    │ nutrients_json │    │ foods_json      │
│ created_at      │    │ created_at     │    │ total_nutrients  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        └───────────────────────────────────────────────┘
                        ┌─────────────────┐
                        │   Goals         │
                        ├─────────────────┤
                        │ id (PK)         │
                        │ user_id (FK)    │
                        │ target_nutrients│
                        │ progress_data   │
                        │ created_at      │
                        └─────────────────┘
```

### **Esquema Principal - PostgreSQL**

#### **Tabela Users**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_data JSONB DEFAULT '{}',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
```

#### **Tabela Foods**  
```sql
CREATE TABLE foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    nutrients JSONB NOT NULL,  -- {calories: 52, protein: 0.3, ...}
    portion_sizes JSONB DEFAULT '{}',
    barcode VARCHAR(100),
    source VARCHAR(100) DEFAULT 'usda',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para buscas
CREATE INDEX idx_foods_name ON foods(name);
CREATE INDEX idx_foods_category ON foods(category);
CREATE INDEX idx_foods_barcode ON foods(barcode);
```

#### **Tabela Meals**
```sql
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    meal_type VARCHAR(50) NOT NULL,  -- breakfast, lunch, dinner, snack
    meal_date DATE NOT NULL,
    meal_time TIME,
    foods JSONB NOT NULL,  -- [{food_id: 123, quantity: 100, unit: 'g'}]
    total_nutrients JSONB NOT NULL,  -- Calculated nutrients sum
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices compostos para queries eficientes
    CREATE INDEX idx_meals_user_date ON meals(user_id, meal_date);
    CREATE INDEX idx_meals_date_type ON meals(meal_date, meal_type);
);
```

#### **Tabela Goals**
```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    goal_type VARCHAR(50) NOT NULL,  -- weight_loss, muscle_gain, maintenance
    start_date DATE NOT NULL,
    end_date DATE,
    target_values JSONB NOT NULL,   -- {calories: 2000, protein: 150, ...}
    current_progress JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Fluxo de Dados

### **Processo de Ingestão**
```
📥 Novos Dados
├── Validação de schema
├── Limpeza e formatação
├── Enriquecimento com metadados
└── Inserção no banco

⚡ Processamento em Tempo Real
├── Cálculo de nutrientes totais
├── Atualização de progresso de metas
├── Geração de insights
└── Cache de resultados frequentes

💾 Armazenamento
├── PostgreSQL (dados estruturados)
├── Redis (cache e sessões)
├── Sistema de arquivos (uploads)
└── Backup automático
```

## 🛠️ Tecnologias Utilizadas

### **Sistema de Banco de Dados**
- **PostgreSQL 15+** - Banco relacional principal
- **Redis 7+** - Cache em memória e sessões
- **SQLAlchemy 2.0** - ORM e gerenciamento de conexões
- **Alembic** - Migrations e versionamento de schema

### **Ferramentas de Gerenciamento**
- **pgAdmin** - Interface gráfica para PostgreSQL
- **Redis CLI** - Console para gerenciamento Redis
- **DBeaver** - IDE universal de banco de dados
- **VS Code Database Tools** - Extensões para desenvolvimento

### **Monitoramento e Performance**
- **pg_stat_statements** - Análise de queries PostgreSQL
- **Redis Monitor** - Monitoramento em tempo real
- **Custom Dashboards** - Métricas personalizadas
- **Alerting System** - Notificações de performance

## 📊 Estrutura de Dados JSONB

### **Exemplo: Perfil de Usuário**
```json
{
  "personal_info": {
    "name": "João Silva",
    "age": 28,
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 70
  },
  "health_info": {
    "activity_level": "moderate",
    "goal": "weight_loss", 
    "dietary_restrictions": ["lactose"],
    "medical_conditions": []
  },
  "preferences": {
    "theme": "dark",
    "language": "pt-BR",
    "notifications": {
      "meal_reminders": true,
      "goal_updates": true
    }
  }
}
```

### **Exemplo: Dados Nutricionais**
```json
{
  "calories": {
    "value": 52,
    "unit": "kcal"
  },
  "protein": {
    "value": 0.3,
    "unit": "g",
    "percent_daily": 1
  },
  "carbohydrates": {
    "value": 14.0,
    "unit": "g",
    "breakdown": {
      "sugars": 10.0,
      "fiber": 2.4,
      "other": 1.6
    }
  },
  "fats": {
    "value": 0.2,
    "unit": "g",
    "breakdown": {
      "saturated": 0.0,
      "unsaturated": 0.2
    }
  },
  "vitamins": {
    "vitamin_c": {
      "value": 4.6,
      "unit": "mg",
      "percent_daily": 8
    }
  }
}
```

## ⚡ Otimizações de Performance

### **Índices Estratégicos**
```sql
-- Índices para queries frequentes
CREATE INDEX idx_users_email ON users USING gin (email gin_trgm_ops);
CREATE INDEX idx_foods_search ON foods USING gin (name gin_trgm_ops);
CREATE INDEX idx_meals_user_date ON meals(user_id, meal_date DESC);

-- Índices para JSONB
CREATE INDEX idx_users_profile ON users USING gin (profile_data);
CREATE INDEX idx_foods_nutrients ON foods USING gin (nutrients);
```

### **Particionamento de Tabelas**
```sql
-- Particionamento por data para tabela de meals
CREATE TABLE meals_2024 PARTITION OF meals
    FOR VALUES FROM ('2024-01-01') TO ('2024-12-31');

CREATE TABLE meals_2025 PARTITION OF meals
    FOR VALUES FROM ('2025-01-01') TO ('2025-12-31');
```

### **Cache Strategy**
```python
# Exemplo de implementação de cache com Redis
from redis import Redis
import json

redis = Redis(host='localhost', port=6379, db=0)

def get_user_meals_cached(user_id: int, date: str) -> List[Dict]:
    cache_key = f"user:{user_id}:meals:{date}"
    
    # Tentar obter do cache primeiro
    cached_data = redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Se não estiver em cache, buscar do banco
    meals = get_user_meals_from_db(user_id, date)
    
    # Armazenar no cache por 1 hora
    redis.setex(cache_key, 3600, json.dumps(meals))
    
    return meals
```

## 🔒 Segurança de Dados

### **Proteção de Dados Sensíveis**
```sql
-- Hash de senhas com bcrypt
UPDATE users SET password_hash = crypt('new_password', gen_salt('bf', 12))
WHERE id = 1;

-- Máscara de dados pessoais
CREATE VIEW masked_users AS
SELECT 
    id,
    mask_email(email) as email,  -- jo***@example.com
    mask_name(personal_info->>'name') as name,  -- J*** S***
    personal_info->>'age' as age
FROM users;
```

### **Controle de Acesso**
```sql
-- Roles e permissions
CREATE ROLE api_user NOLOGIN;
CREATE ROLE app_user INHERIT;

-- Grants específicos
GRANT SELECT ON foods TO api_user;
GRANT SELECT, INSERT ON meals TO app_user;
GRANT SELECT ON users TO nobody;  -- Restrito

-- Row Level Security
CREATE POLICY user_data_policy ON users
    USING (id = current_user_id());
```

## 📈 Migrations e Versionamento

### **Sistema de Migrations com Alembic**
```bash
# Inicializar alembic
alembic init migrations

# Criar nova migration
alembic revision -m "add_user_preferences_column"

# Aplicar migrations
alembic upgrade head

# Reverter migration
alembic downgrade -1
```

### **Exemplo de Migration**
```python
# migrations/versions/001_add_preferences.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', 
        sa.Column('preferences', sa.JSON(), nullable=True, server_default='{}')
    )
    
    # Criar índice para JSONB
    op.create_index('idx_users_preferences', 'users', ['preferences'], 
                   postgresql_using='gin')

def downgrade():
    op.drop_index('idx_users_preferences', 'users')
    op.drop_column('users', 'preferences')
```

## 🧪 Testing e Qualidade

### **Testes de Banco de Dados**
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    # Banco de dados em memória para testes
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    
    # Criar schema
    Base.metadata.create_all(engine)
    
    return Session()

def test_user_creation(test_db):
    """Teste de criação de usuário"""
    user = User(email='test@example.com', password_hash='hashed')
    test_db.add(user)
    test_db.commit()
    
    assert user.id is not None
    assert user.email == 'test@example.com'
```

### **Testes de Performance**
```python
def test_query_performance():
    """Teste de performance de queries frequentes"""
    start_time = time.time()
    
    # Query que deve ser rápida
    results = session.query(Meal).filter(
        Meal.user_id == 1,
        Meal.meal_date == '2024-01-15'
    ).all()
    
    end_time = time.time()
    
    # Assert que a query leva menos de 100ms
    assert (end_time - start_time) < 0.1
    assert len(results) > 0
```

## 🚀 Deployment e DevOps

### **Configuração de Produção**
```yaml
# docker-compose.prod.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bsfm_prod
      POSTGRES_USER: bsfm_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./backups:/backups
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

### **Backup Automático**
```bash
#!/bin/bash
# backup.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/bsfm_${TIMESTAMP}.dump"

# Backup completo
pg_dump -Fc -U bsfm_user bsfm_prod > $BACKUP_FILE

# Manter apenas últimos 7 backups
find /backups -name "*.dump" -mtime +7 -delete
```

### **Monitoramento**
```python
# Monitoramento de saúde do banco
from prometheus_client import Gauge

db_connections = Gauge('db_connections', 'Active database connections')
db_query_time = Gauge('db_query_time_seconds', 'Query execution time')

def monitor_database_health():
    while True:
        # Verificar conexões ativas
        active_conns = get_active_connections()
        db_connections.set(active_conns)
        
        # Verificar performance
        query_time = measure_query_performance()
        db_query_time.set(query_time)
        
        time.sleep(60)  # A cada minuto
```

## 📊 Estatísticas e Métricas

### **Métricas de Performance**
| Métrica | Valor | Limite | Status |
|---------|-------|--------|--------|
| **Query Response Time** | 45ms | < 100ms | ✅ Saudável |
| **Active Connections** | 12 | < 50 | ✅ Normal |
| **Cache Hit Rate** | 92% | > 85% | ✅ Excelente |
| **Disk Usage** | 65% | < 80% | ✅ Controlado |

### **Estatísticas de Dados**
```sql
-- Estatísticas do banco
SELECT 
    COUNT(*) as total_users,
    (SELECT COUNT(*) FROM foods) as total_foods,
    (SELECT COUNT(*) FROM meals) as total_meals,
    pg_size_pretty(pg_database_size('bsfm')) as db_size;
```

## 🔮 Roadmap Futuro

### **Melhorias Planejadas**
- [ ] **TimescaleDB** - Para dados temporais de metrics
- [ ] **Elasticsearch** - Busca full-text em alimentos
- [ ] **Data Warehouse** - Analytics e business intelligence  
- [ ] **Graph Database** - Para relações complexas entre alimentos

### **Otimizações**
- [ ] **Connection Pooling** - PgBouncer para melhor escalabilidade
- [ ] **Read Replicas** - Para distribuir carga de leitura
- [ ] **Sharding** - Particionamento horizontal para escala
- [ ] **Compression** - Compactação de dados históricos

---

*🗄️ Arquitetura de dados robusta para suportar crescimento*  
*⚡ Performance otimizada para experiência do usuário*  
*🔒 Segurança como prioridade máxima*  
*📈 Preparado para escala e evolução do sistema*