# Instalação do BSFM

Este guia mostra como executar o projeto localmente e como fazer deploy em produção.

## Visão Rápida

- **Backend**: .NET 8 (ASP.NET Core)
- **Frontend**: HTML/CSS/JS servido estaticamente pelo backend
- **Banco de dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Deploy**: Render (produção)
- **Documentação**: Vercel (MkDocs)

## Pré-requisitos

- .NET SDK 8+
- Git
- PostgreSQL 15+ (ou SQLite para desenvolvimento)
- Visual Studio 2022 ou VS Code

## Instalação Local

### 1. Clonar Repositório

```bash
git clone https://github.com/Brazilian-System-of-Food-Metric/BSFM-APP.git
cd BSFM-APP
```

### 2. Restaurar Dependências

```bash
dotnet restore
```

### 3. Configurar Banco de Dados

#### Opção A - PostgreSQL (Recomendado para produção)
```bash
# Criar container PostgreSQL
docker run -d --name bsfm-postgres \
  -p 5432:5432 \
  -e POSTGRES_DB=bsfm_dev \
  -e POSTGRES_USER=bsfm_user \
  -e POSTGRES_PASSWORD=senha_segura \
  -v bsfm-data:/var/lib/postgresql/data \
  postgres:15-alpine
```

#### Opção B - SQLite (Desenvolvimento rápido)
O projeto já está configurado para usar SQLite como fallback. Basta configurar a variável de ambiente:
```bash
set DATABASE_URL=Data Source=bsfm.db
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto ou configure no sistema:

```bash
# Banco de dados (PostgreSQL)
DATABASE_URL=Host=localhost;Database=bsfm_dev;Username=bsfm_user;Password=senha_segura

# APIs Externas
USDA_API_KEY=sua-chave-usda-aqui
BREVO_API_KEY=sua-chave-brevo-aqui
GROQ_API_KEY=sua-chave-groq-aqui

# Ambiente
ASPNETCORE_ENVIRONMENT=Development
ASPNETCORE_URLS=http://localhost:5000
```

### 5. Executar a Aplicação

```bash
dotnet run
```

A aplicação estará disponível em: **http://localhost:5000**

Para desenvolvimento com hot reload:
```bash
dotnet watch run
```

## Deploy no Render

### Pré-requisitos para Deploy

1. Conta no [Render](https://render.com)
2. Repositório no GitHub conectado ao Render
3. Banco PostgreSQL (Render oferece PostgreSQL gratuito)

### Passo a Passo

#### 1. Criar Banco PostgreSQL no Render
1. Acesse o Dashboard do Render
2. Clique em **New +** > **PostgreSQL**
3. Configure:
   - **Name**: `bsfm-db`
   - **Database**: `bsfm_prod`
   - **User**: `bsfm_user`
   - **Region**: `São Paulo (South America)`
4. Após criar, copie a **Internal Database URL**

#### 2. Criar Web Service no Render
1. Clique em **New +** > **Web Service**
2. Conecte seu repositório GitHub
3. Configure:
   - **Name**: `bsfm-api`
   - **Runtime**: `Docker` (ou `.NET 8` se disponível)
   - **Build Command**: `dotnet publish -c Release -o output`
   - **Start Command**: `dotnet output/MobileRepositorio.dll`
   - **Plan**: Free

#### 3. Configurar Variáveis de Ambiente no Render

No painel do Web Service, vá em **Environment** e adicione:

| Variável | Valor |
|----------|-------|
| `ASPNETCORE_ENVIRONMENT` | `Production` |
| `DATABASE_URL` | `Host=...;Database=bsfm_prod;Username=bsfm_user;Password=...` |
| `USDA_API_KEY` | Sua chave da API USDA |
| `BREVO_API_KEY` | Sua chave da API Brevo |
| `GROQ_API_KEY` | Sua chave da API Groq |

#### 4. Deploy Automático
- O Render faz deploy automático a cada push na branch principal
- Para deploy manual: clique em **Manual Deploy** > **Deploy latest commit**

### Arquivos de Configuração para Deploy

O projeto inclui:

- **render.yaml**: Configuração Infrastructure as Code para o Render
- **Dockerfile**: Containerização da aplicação
- **Program.cs**: Configurado para ler PORT, DATABASE_URL e outras variáveis

### Health Check

Após o deploy, acesse: `https://seu-app.onrender.com/health`

Retorno esperado:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-28T...",
  "database": "connected"
}
```

## Checklist de Deploy

- [ ] Repositório no GitHub
- [ ] Conta no Render criada
- [ ] Banco PostgreSQL criado no Render
- [ ] Variáveis de ambiente configuradas (incluindo GROQ_API_KEY)
- [ ] Build passando no Render
- [ ] Health check respondendo
- [ ] Funcionalidades testadas em produção

## Solução de Problemas

### Erro de Conexão com Banco
```bash
# Verifique se a DATABASE_URL está correta
# O sistema tenta reconectar automaticamente até 3 vezes
```

### Porta em Uso
```bash
# Mude a porta no Render ou localmente
ASPNETCORE_URLS=http://localhost:5001
```

### Build Falhando
```bash
# Verifique se o .NET SDK 8 está instalado
dotnet --version
# Deve retornar 8.x.x
```

### Groq API não funciona
```bash
# Verifique se a GROQ_API_KEY está configurada
# O serviço funciona sem ela, mas o feedback IA não estará disponível
```
