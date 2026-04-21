---
title: Segurança
description: Medidas de segurança e proteção de dados no BSFM
---

# 🔒 Segurança

Arquitetura de segurança robusta implementada no BSFM para proteger dados dos usuários e garantir conformidade com regulamentações de privacidade.

## 🎯 Visão Geral

O BSFM implementa uma abordagem de segurança em camadas, incluindo:
- **Autenticação e Autorização** - Controle de acesso granular
- **Criptografia** - Dados protegidos em trânsito e em repouso  
- **Proteção de Dados** - Privacidade do usuário como prioridade
- **Monitoramento** - Detecção e resposta a incidentes
- **Conformidade** - Adequação a regulamentações de proteção de dados

## 🏗️ Arquitetura de Segurança

### **Camadas de Proteção**
```
🔐 Autenticação & Identidade
├── JWT tokens com assinatura digital
├── OAuth 2.0 / OpenID Connect
├── MFA (Multi-Factor Authentication)
└── Gerenciamento de sessões seguro

🔒 Criptografia
├── TLS 1.3 para dados em trânsito
├── AES-256 para dados em repouso  
├── Hashing bcrypt para senhas
└── Chaves gerenciadas por KMS

🛡️ Proteção de Aplicação
├── CORS configurado corretamente
├── CSRF tokens protection
├── Rate limiting e DDoS protection
└── Input validation e sanitização

📊 Monitoramento
├── Logging centralizado
├── Detecção de anomalias
├── Alertas em tempo real
└── Auditoria de segurança
```

## 🔐 Autenticação e Autorização

### **Sistema de Autenticação JWT**
```python
from datetime import datetime, timedelta
import jwt
from bcrypt import hashpw, gensalt, checkpw

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_token(self, user_id: str, email: str, roles: List[str]) -> str:
        """Cria JWT token com claims"""
        payload = {
            'sub': user_id,
            'email': email,
            'roles': roles,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
            'iss': 'bsfm-app'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Dict:
        """Verifica e decodifica JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationError('Token inválido')
    
    def hash_password(self, password: str) -> str:
        """Hash de senha com bcrypt"""
        salt = gensalt(rounds=12)
        return hashpw(password.encode(), salt).decode()
    
    def check_password(self, password: str, hashed: str) -> bool:
        """Verifica senha contra hash"""
        return checkpw(password.encode(), hashed.encode())
```

### **Middleware de Autenticação**
```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Esquema de autenticação inválido")
        
        try:
            payload = auth_service.verify_token(credentials.credentials)
            return payload
        except AuthenticationError as e:
            raise HTTPException(status_code=403, detail=str(e))

# Uso em endpoints
@app.get("/profile")
async def get_user_profile(
    credentials: Dict = Depends(JWTBearer())
):
    user_id = credentials['sub']
    return await get_profile(user_id)
```

### **Controle de Acesso Baseado em Roles**
```python
from functools import wraps

def require_role(required_role: str):
    """Decorator para exigir role específica"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials = kwargs.get('credentials')
            
            if not credentials or required_role not in credentials.get('roles', []):
                raise HTTPException(
                    status_code=403, 
                    detail=f"Role {required_role} requerida"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso em endpoints administrativos
@app.get("/admin/users")
@require_role('admin')
async def get_all_users(credentials: Dict = Depends(JWTBearer())):
    return await get_users()
```

## 🔒 Criptografia

### **Criptografia de Dados Sensíveis**
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class EncryptionService:
    def __init__(self, master_key: str):
        self.master_key = master_key.encode()
    
    def derive_key(self, salt: bytes) -> bytes:
        """Deriva chave usando PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key))
    
    def encrypt_data(self, data: str) -> Dict[str, str]:
        """Criptografa dados sensíveis"""
        salt = os.urandom(16)
        key = self.derive_key(salt)
        fernet = Fernet(key)
        
        encrypted_data = fernet.encrypt(data.encode())
        
        return {
            'encrypted_data': base64.urlsafe_b64encode(encrypted_data).decode(),
            'salt': base64.urlsafe_b64encode(salt).decode()
        }
    
    def decrypt_data(self, encrypted_data: str, salt: str) -> str:
        """Descriptografa dados"""
        salt_bytes = base64.urlsafe_b64decode(salt)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
        
        key = self.derive_key(salt_bytes)
        fernet = Fernet(key)
        
        return fernet.decrypt(encrypted_bytes).decode()
```

### **Gerenciamento de Chaves**
```python
# Configuração de chaves por ambiente
class KeyManager:
    def __init__(self):
        self.keys = {
            'jwt_secret': os.getenv('JWT_SECRET_KEY'),
            'encryption_key': os.getenv('ENCRYPTION_MASTER_KEY'),
            'database_url': os.getenv('DATABASE_URL')
        }
        
        self.validate_keys()
    
    def validate_keys(self):
        """Valida que todas as chaves necessárias estão presentes"""
        required_keys = ['jwt_secret', 'encryption_key', 'database_url']
        
        for key in required_keys:
            if not self.keys.get(key):
                raise ConfigurationError(f"Chave {key} não configurada")
            
            # Valida força das chaves
            if key == 'jwt_secret' and len(self.keys[key]) < 32:
                raise ConfigurationError("JWT secret muito curta")
```

## 🛡️ Proteção de Aplicação

### **Configuração de CORS**
```python
from fastapi.middleware.cors import CORSMiddleware

# Configuração segura de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bsfm-app.railway.app",
        "https://bsfm-admin.railway.app",
        "http://localhost:3000"  # Apenas desenvolvimento
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining"],
    max_age=600  # 10 minutos
)
```

### **Rate Limiting**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)

# Aplicar rate limiting global
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Limites específicos por endpoint
@app.get("/api/foods/search")
@limiter.limit("10/minute")  # 10 requests por minuto
async def search_foods(request: Request, q: str):
    return await search_food_items(q)

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # 5 tentativas de login por minuto  
async def login(request: Request, credentials: LoginCredentials):
    return await authenticate_user(credentials)
```

### **Input Validation e Sanitização**
```python
from pydantic import BaseModel, constr, EmailStr, validator
import html

class UserRegistration(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    name: constr(min_length=2, max_length=100)
    
    @validator('name')
    def sanitize_name(cls, v):
        """Sanitiza nome para prevenir XSS"""
        # Remove tags HTML e caracteres especiais
        sanitized = html.escape(v.strip())
        
        # Valida que não contém scripts
        if '<script' in sanitized.lower():
            raise ValueError('Nome contém conteúdo inválido')
            
        return sanitized
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Valida força da senha"""
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        
        if not any(char.isdigit() for char in v):
            raise ValueError('Senha deve conter pelo menos um número')
            
        if not any(char.isupper() for char in v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
            
        return v
```

## 📊 Monitoramento e Logging

### **Logging de Segurança**
```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logger de segurança
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# File handler com rotação
handler = RotatingFileHandler(
    'logs/security.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)

# Funções de logging
log_security_event('login_failed', {
    'email': 'user@example.com',
    'ip': '192.168.1.1',
    'user_agent': 'Mozilla/5.0...',
    'reason': 'invalid_password'
})

def log_security_event(event_type: str, details: Dict):
    """Log eventos de segurança"""
    security_logger.info(
        f"Security event: {event_type}",
        extra={'details': details}
    )
```

### **Detecção de Anomalias**
```python
class AnomalyDetector:
    def __init__(self):
        self.failed_login_attempts = {}
        self.request_patterns = {}
    
    def detect_failed_login_attack(self, email: str, ip: str) -> bool:
        """Detecta tentativas de força bruta"""
        key = f"{email}:{ip}"
        
        # Incrementar contador
        self.failed_login_attempts[key] = self.failed_login_attempts.get(key, 0) + 1
        
        # Se mais de 5 tentativas em 5 minutos, possível ataque
        if self.failed_login_attempts[key] > 5:
            log_security_event('brute_force_attempt', {
                'email': email,
                'ip': ip,
                'attempts': self.failed_login_attempts[key]
            })
            return True
        
        return False
    
    def cleanup_old_attempts(self):
        """Limpa tentativas antigas"""
        # Implementar limpeza periódica
        pass
```

## 📝 Políticas de Segurança

### **Política de Senhas**
```markdown
# Política de Senhas BSFM

## Requisitos Mínimos
- **Comprimento**: Mínimo 8 caracteres
- **Complexidade**: Pelo menos:
  - 1 letra maiúscula
  - 1 letra minúscula  
  - 1 número
  - 1 caractere especial (!@#$%^&*)

## Validação
- Verificação em tempo real durante registro
- Feedback claro sobre requisitos não atendidos
- Sugestões para melhorar a segurança

## Expiração
- Senhas expiram a cada 90 dias
- Notificação 15 dias antes da expiração
- Histórico das últimas 5 senhas para prevenir reuso

## Recuperação
- Link de recuperação com expiração de 1 hora
- Verificação de identidade por email
- Redefinição segura com confirmação
```

### **Política de Privacidade**
```markdown
# Política de Privacidade BSFM

## Dados Coletados
- **Dados de perfil**: Nome, email, informações de saúde
- **Dados nutricionais**: Alimentos consumidos, metas
- **Dados técnicos**: IP, user agent, logs de acesso

## Finalidade
- Fornecer serviços de análise nutricional personalizada
- Melhorar a experiência do usuário
- Desenvolver novos recursos e funcionalidades

## Compartilhamento
- **Nunca** vendemos dados dos usuários
- Dados agregados e anonimizados para analytics
- Parceiros apenas com acordos de proteção de dados

## Retenção
- Dados mantidos enquanto conta ativa
- Exclusão completa upon request
- Backups criptografados com retenção limitada
```

## 🚦 Resposta a Incidentes

### **Plano de Resposta**
```python
class IncidentResponse:
    def __init__(self):
        self.incident_handlers = {
            'data_breach': self.handle_data_breach,
            'dos_attack': self.handle_dos_attack,
            'unauthorized_access': self.handle_unauthorized_access
        }
    
    def handle_incident(self, incident_type: str, details: Dict):
        """Coordena resposta a incidentes"""
        handler = self.incident_handlers.get(incident_type)
        
        if handler:
            # Log do incidente
            log_security_event(f'incident_{incident_type}', details)
            
            # Executar handler específico
            handler(details)
            
            # Notificar equipe
            self.notify_team(incident_type, details)
        
    def handle_data_breach(self, details: Dict):
        """Resposta a violação de dados"""
        # 1. Isolar sistemas afetados
        self.isolate_affected_systems(details)
        
        # 2. Notificar usuários impactados
        self.notify_affected_users(details)
        
        # 3. Reportar às autoridades
        self.report_to_authorities(details)
        
        # 4. Investigar causa raiz
        self.investigate_root_cause(details)
    
    def handle_dos_attack(self, details: Dict):
        """Resposta a ataques DoS"""
        # 1. Ativar modo de proteção
        self.activate_dos_protection()
        
        # 2. Bloquear IPs maliciosos
        self.block_malicious_ips(details.get('attacker_ips', []))
        
        # 3. Escalar para provedor
        self.escalate_to_provider()
        
        # 4. Monitorar tráfego
        self.monitor_traffic_patterns()
```

### **Checklist de Incidentes**
```markdown
# Checklist de Resposta a Incidentes

## Imediato (0-15 minutos)
- [ ] Identificar escopo do incidente
- [ ] Isolar sistemas afetados
- [ ] Notificar equipe de segurança
- [ ] Iniciar logging forense

## Curto Prazo (15-60 minutos)  
- [ ] Avaliar impacto nos usuários
- [ ] Implementar medidas de contenção
- [ ] Comunicar-se com stakeholders
- [ ] Preservar evidências

## Médio Prazo (1-24 horas)
- [ ] Investigar causa raiz
- [ ] Remediar vulnerabilidades
- [ ] Restaurar serviços
- [ ] Notificar autoridades se necessário

## Longo Prazo (1-7 dias)
- [ ] Post-mortem completo
- [ ] Atualizar políticas e procedimentos
- [ ] Treinamento adicional da equipe
- [ ] Monitoramento reforçado
```

## 📋 Conformidade e Auditoria

### **LGPD (Lei Geral de Proteção de Dados)**
```python
class GDPRCompliance:
    def __init__(self):
        self.data_processing_activities = []
        self.data_protection_impact_assessments = []
    
    def register_processing_activity(self, activity: Dict):
        """Registra atividade de processamento"""
        self.data_processing_activities.append(activity)
    
    def conduct_dpia(self, processing_activity: Dict) -> Dict:
        """Realiza avaliação de impacto"""
        assessment = {
            'activity': processing_activity,
            'risks_identified': [],
            'mitigation_measures': [],
            'approval_status': 'pending',
            'conducted_at': datetime.now()
        }
        
        self.data_protection_impact_assessments.append(assessment)
        return assessment
    
    def handle_user_rights_request(self, request: Dict) -> Dict:
        """Processa direitos do usuário"""
        right_type = request['right_type']
        user_id = request['user_id']
        
        if right_type == 'access':
            return self.provide_data_access(user_id)
        elif right_type == 'erasure':
            return self.process_erasure_request(user_id)
        elif right_type == 'rectification':
            return self.process_rectification_request(user_id, request['data'])
        elif right_type == 'portability':
            return self.provide_data_portability(user_id)
```

### **Auditoria de Segurança**
```python
def conduct_security_audit() -> Dict:
    """Realiza auditoria completa de segurança"""
    audit_report = {
        'timestamp': datetime.now(),
        'auditor': 'BSFM Security Team',
        'findings': [],
        'recommendations': [],
        'risk_level': 'low'
    }
    
    # Verificar configurações de segurança
    findings += check_security_configurations()
    
    # Testar vulnerabilidades comuns
    findings += test_for_common_vulnerabilities()
    
    # Revisar logs de segurança
    findings += review_security_logs()
    
    # Verificar conformidade com políticas
    findings += check_policy_compliance()
    
    audit_report['findings'] = findings
    audit_report['risk_level'] = calculate_risk_level(findings)
    audit_report['recommendations'] = generate_recommendations(findings)
    
    return audit_report
```

## 🚀 Melhores Práticas Implementadas

### **OWASP Top 10 Protection**
```markdown
# Proteções contra OWASP Top 10

## 1. Injection
- ✅ Prepared statements parametrizados
- ✅ Input validation e sanitização
- ✅ ORM com proteção built-in

## 2. Broken Authentication  
- ✅ JWT com assinatura forte
- ✅ Rate limiting em login
- ✅ Senhas hasheadas com bcrypt

## 3. Sensitive Data Exposure
- ✅ TLS 1.3 em todas as conexões
- ✅ Dados sensíveis criptografados
- ✅ Headers de segurança HTTP

## 4. XML External Entities (XXE)
- ✅ Desabilitado parsing XML
- ✅ Validação strict de content-type

## 5. Broken Access Control
- ✅ Controle de acesso baseado em roles
- ✅ Validação de permissões no backend
- ✅ Princípio do menor privilégio

## 6. Security Misconfiguration
- ✅ Configurações hardened por padrão
- ✅ Scanning automatizado de configurações
- ✅ Ambiente específico para produção

## 7. Cross-Site Scripting (XSS)
- ✅ Content Security Policy (CSP)
- ✅ Sanitização de output
- ✅ Headers X-XSS-Protection

## 8. Insecure Deserialization
- ✅ Deserialização apenas de fontes confiáveis
- ✅ Validação de integridade de dados

## 9. Using Components with Known Vulnerabilities  
- ✅ Dependências escaneadas regularmente
- ✅ Atualizações automáticas de segurança
- ✅ SBOM (Software Bill of Materials)

## 10. Insufficient Logging & Monitoring
- ✅ Logging centralizado de segurança
- ✅ Detecção de anomalias em tempo real
- ✅ Alertas proativos
```

## 📊 Métricas de Segurança

### **Dashboard de Segurança**
```python
class SecurityDashboard:
    def __init__(self):
        self.metrics = {
            'failed_login_attempts': 0,
            'successful_logins': 0,
            'security_incidents': 0,
            'blocked_ips': 0,
            'audit_findings': []
        }
    
    def update_metrics(self, event_type: str, data: Dict = None):
        """Atualiza métricas baseado em eventos"""
        if event_type == 'login_failed':
            self.metrics['failed_login_attempts'] += 1
        elif event_type == 'login_success':
            self.metrics['successful_logins'] += 1
        elif event_type == 'security_incident':
            self.metrics['security_incidents'] += 1
        elif event_type == 'ip_blocked':
            self.metrics['blocked_ips'] += 1
        elif event_type == 'audit_finding':
            self.metrics['audit_findings'].append(data)
    
    def get_security_score(self) -> float:
        """Calcula score de segurança (0-100)"""
        total_events = self.metrics['successful_logins'] + self.metrics['failed_login_attempts']
        
        if total_events == 0:
            return 100.0
        
        failure_rate = self.metrics['failed_login_attempts'] / total_events
        incident_score = min(self.metrics['security_incidents'] * 10, 50)
        
        base_score = 100 - (failure_rate * 50)
        final_score = max(base_score - incident_score, 0)
        
        return round(final_score, 2)
```

## 🔮 Roadmap de Segurança

### **Próximas Implementações**
- [ ] **MFA (Multi-Factor Authentication)** - Autenticação em dois fatores
- [ ] **Web Application Firewall** - Proteção adicional de camada 7
- [ ] **Security Headers** - Headers de segurança adicionais
- [ ] **Certificate Pinning** - Proteção contra MITM
- [ ] **Bug Bounty Program** - Programa de recompensas por bugs

### **Melhorias Contínuas**
- [ ] **Pentesting Regular** - Testes de penetração trimestrais
- [ ] **Security Training** - Treinamento contínuo da equipe  
- [ ] **Threat Modeling** - Modelagem de ameaças para novos features
- [ ] **Compliance Automation** - Automação de auditorias

---

*🔒 Segurança como prioridade fundamental no design do sistema*  
*🛡️ Proteção multicamada contra ameaças modernas*  
*📊 Monitoramento contínuo e resposta proativa*  
*📝 Conformidade completa com regulamentações de proteção de dados*