---
title: API Reference - BSFM
description: Documentação completa da API RESTful do BodySmart Food Monitor
---

# API Reference - BSFM

## Visão Geral da API

O BSFM oferece uma API RESTful completa para integração com sistemas externos, aplicações móveis e frontend web. Todas as APIs retornam JSON e seguem os padrões REST.

## Autenticação

### Authentication Methods

#### JWT Bearer Token
```http
Authorization: Bearer <jwt_token>
```

#### OAuth2 Flow
```
1. Redirect to /oauth/authorize
2. User authentication
3. Redirect with code
4. Exchange code for tokens
```

### Endpoints de Autenticação

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Endpoints Principais

### Users

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Response**:
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "profile": {
    "age": 30,
    "weight": 75.5,
    "height": 180,
    "goal": "weight_loss"
  }
}
```

#### Update User Profile
```http
PATCH /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "profile": {
    "weight": 72.0
  }
}
```

### Food Analysis

#### Analyze Food Image
```http
POST /api/v1/food/analyze
Authorization: Bearer <token>
Content-Type: multipart/form-data

-- Form Data --
image: <binary image data>
additional_data: {"meal_type": "lunch", "timestamp": "2024-01-15T12:30:00Z"}
```

**Response**:
```json
{
  "analysis_id": "analysis_123",
  "status": "completed",
  "results": {
    "food_items": [
      {
        "name": "Apple",
        "confidence": 0.95,
        "quantity": 1,
        "unit": "unit",
        "nutrition": {
          "calories": 95,
          "protein": 0.5,
          "carbs": 25,
          "fat": 0.3
        }
      }
    ],
    "total_nutrition": {
      "calories": 95,
      "protein": 0.5,
      "carbs": 25,
      "fat": 0.3
    }
  }
}
```

#### Get Analysis History
```http
GET /api/v1/food/history
Authorization: Bearer <token>
Query Parameters:
  page: 1
  limit: 20
  start_date: 2024-01-01
  end_date: 2024-01-31
```

### Meals & Nutrition

#### Create Meal Entry
```http
POST /api/v1/meals
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Lunch",
  "type": "lunch",
  "timestamp": "2024-01-15T12:30:00Z",
  "food_items": [
    {
      "food_id": "food_123",
      "quantity": 1,
      "unit": "unit"
    }
  ]
}
```

#### Get Daily Nutrition Summary
```http
GET /api/v1/nutrition/daily/2024-01-15
Authorization: Bearer <token>
```

**Response**:
```json
{
  "date": "2024-01-15",
  "total_calories": 1850,
  "total_protein": 75,
  "total_carbs": 250,
  "total_fat": 45,
  "meals": [
    {
      "name": "Breakfast",
      "calories": 450,
      "foods": ["Oatmeal", "Banana"]
    }
  ]
}
```

### Goals & Progress

#### Set Nutrition Goals
```http
POST /api/v1/goals
Authorization: Bearer <token>
Content-Type: application/json

{
  "target_calories": 2000,
  "target_protein": 100,
  "target_carbs": 250,
  "target_fat": 65,
  "goal_type": "weight_loss",
  "target_weight": 70.0
}
```

#### Get Progress Overview
```http
GET /api/v1/progress
Authorization: Bearer <token>
Query Parameters:
  period: "week"  // day, week, month
```

## Status Codes e Erros

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

### Error Response Format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `invalid_token` | JWT token is invalid or expired |
| `rate_limit_exceeded` | Too many requests |
| `image_too_large` | Image exceeds size limit |
| `analysis_failed` | Food analysis failed |
| `invalid_credentials` | Login credentials are invalid |

## Rate Limiting

### Limits por Plano

| Plano | Requests/min | Uploads/min |
|-------|-------------|-------------|
| Free | 60 | 10 |
| Pro | 300 | 60 |
| Enterprise | 1000 | 200 |

### Headers de Rate Limiting
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1627841234
Retry-After: 60
```

## Paginação

### Query Parameters
```http
GET /api/v1/resources
?page=2
&limit=20
&sort=created_at
&order=desc
```

### Response Format
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

## Filtros e Busca

### Filtering
```http
GET /api/v1/foods
?calories__gte=100
&calories__lte=500
&category=fruit
```

### Searching
```http
GET /api/v1/foods
?q=apple
```

### Sorting
```http
GET /api/v1/foods
?sort=calories
&order=desc
```

## Upload de Imagens

### Formatos Suportados
- JPEG, PNG, WebP
- Tamanho máximo: 10MB
- Resolução recomendada: 1024x1024px

### Exemplo de Upload
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('metadata', JSON.stringify({
  meal_type: 'lunch',
  timestamp: new Date().toISOString()
}));

const response = await fetch('/api/v1/food/analyze', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

## Webhooks

### Eventos Suportados
- `analysis.completed` - Análise de comida concluída
- `meal.created` - Nova refeição criada
- `goal.achieved` - Meta nutricional alcançada

### Configuração de Webhook
```http
POST /api/v1/webhooks
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com/webhooks",
  "events": ["analysis.completed", "meal.created"],
  "secret": "your_secret_here"
}
```

### Payload do Webhook
```json
{
  "event": "analysis.completed",
  "data": {
    "analysis_id": "analysis_123",
    "user_id": "user_123",
    "timestamp": "2024-01-15T12:30:00Z"
  }
}
```

## SDKs e Client Libraries

### Python SDK
```python
from bfsm import Client

client = Client(api_key='your_api_key')

# Analyze food image
result = client.analyze_food(image_path='food.jpg')
print(result['calories'])

# Get user profile
profile = client.get_user_profile()
```

### JavaScript SDK
```javascript
import { BSFMClient } from 'bsfm-sdk';

const client = new BSFMClient({
  apiKey: 'your_api_key'
});

// Analyze food from browser
const result = await client.analyzeFood(imageFile);
console.log(result.calories);
```

### cURL Examples

#### Authentication
```bash
curl -X POST https://api.bsfm.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

#### Food Analysis
```bash
curl -X POST https://api.bsfm.com/api/v1/food/analyze \
  -H "Authorization: Bearer <token>" \
  -F "image=@food.jpg" \
  -F "metadata={\"meal_type\":\"lunch\"}"
```

## Versioning

### API Versions
- `v1` - Current stable version
- `v0` - Deprecated (use v1)

### Version Header
```http
Accept: application/vnd.bsfm.v1+json
```

### Deprecation Policy
- APIs são suportadas por pelo menos 12 meses após depreciação
- Versões deprecadas recebem headers de warning
- Migration guides são fornecidos

## Testing

### Sandbox Environment
```
Base URL: https://sandbox.bsfm.com/api/v1
API Key: sb_xxxxxxxxxxxxxxxx
```

### Test Data
- Use images de teste fornecidas
- Mock responses disponíveis
- Rate limits relaxados

## Suporte

### Documentação Adicional
- [Configuração de Ambiente](setup.md)
- [Arquitetura do Sistema](architecture.md)
- [Perguntas Frequentes (FAQ)](../user-guide/faq.md)

### Suporte Técnico
- Email: api-support@bsfm.com
- Slack: #api-support
- Documentation: https://docs.bsfm.com

---

*Última atualização: Abril 2026*

🚀 **API Version**: v1 (Stable)  
📊 **Status**: Production Ready  
🔐 **Authentication**: JWT & OAuth2