---
title: Setup de Desenvolvimento
description: Guia completo para configurar o ambiente de desenvolvimento do BSFM
---

# Setup de Desenvolvimento

Este guia orienta você através da configuração completa do ambiente de desenvolvimento para o projeto BSFM (Brazilian System of Food Metric).

## :material-check-circle: Pré-requisitos

### Software Necessário
| Software | Versão | Link |
| :--- | :--- | :--- |
| **.NET SDK** | 8.0+ | [Download](https://dotnet.microsoft.com/download) |
| **Node.js** | 18+ | [Download](https://nodejs.org/) |
| **Git** | 2.40+ | [Download](https://git-scm.com/) |
| **PostgreSQL** | 15+ | [Download](https://www.postgresql.org/download/) |
| **Visual Studio 2022** ou **VS Code** | Latest | [VS Code](https://code.visualstudio.com/) |

### Contas e APIs Necessárias
| Serviço | Propósito | Como obter |
| :--- | :--- | :--- |
| **USDA API Key** | Dados nutricionais | [FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html) |
| **Brevo API Key** | Email transacional | [Brevo](https://www.brevo.com/) |
| **Railway Account** | Deployment | [Railway](https://railway.app/) |

## :material-folder: Estrutura do Projeto

```
MobileRepositorio/
├── Controllers/          # Controladores ASP.NET Core
├── Models/              # Modelos de dados e entidades
├── Services/            # Serviços de negócio e lógica
├── wwwroot/             # Frontend estático (HTML/CSS/JS)
├── ClassesBSFM.cs       # Classes principais do domínio
├── PonteDB.cs           # Contexto do Entity Framework
├── Program.cs           # Ponto de entrada da aplicação
└── MeusApp.csproj       # Configuração do projeto .NET
```

## :material-play: Passo a Passo

### 1. Clone o Repositório

```bash
# Clone o repositório principal
git clone https://github.com/Isaque-Medeiros/BSFM.git
cd BSFM/MobileRepositorio
```

### 2. Configure Variáveis de Ambiente

Crie um arquivo `appsettings.Development.json` na raiz do projeto:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=bsfm_dev;Username=postgres;Password=senha_local"
  },
  "ApiKeys": {
    "UsdaApiKey": "SUA_CHAVE_USDA_AQUI",
    "BrevoApiKey": "SUA_CHAVE_BREVO_AQUI"
  },
  "AppSettings": {
    "JwtSecret": "SUA_CHAVE_SECRETA_JWT_AQUI",
    "FrontendUrl": "http://localhost:3000",
    "BackendUrl": "http://localhost:8080"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

**Windows (PowerShell):**
```powershell
$env:USDA_API_KEY = "sua_chave_aqui"
$env:BREVO_API_KEY = "sua_chave_aqui"
$env:DATABASE_URL = "postgresql://postgres:senha@localhost:5432/bsfm_dev"
```

**Linux/macOS:**
```bash
export USDA_API_KEY="sua_chave_aqui"
export BREVO_API_KEY="sua_chave_aqui"
export DATABASE_URL="postgresql://postgres:senha@localhost:5432/bsfm_dev"
```

### 3. Configure o Banco de Dados

```sql
-- Crie o banco de dados
CREATE DATABASE bsfm_dev;

-- Conecte ao banco
\c bsfm_dev;

-- Execute as migrations (serão criadas automaticamente)
-- Ou execute o script inicial se preferir
```

Ou use o Entity Framework para criar o banco:

```bash
# Instale as ferramentas do EF Core
dotnet tool install --global dotnet-ef

# Execute as migrations
dotnet ef database update
```

### 4. Restaure Dependências

```bash
# Restaure pacotes .NET
dotnet restore

# Instale dependências do frontend (se houver package.json)
npm install
```

### 5. Execute a Aplicação

```bash
# Desenvolvimento com hot reload
dotnet watch run

# Ou execute normalmente
dotnet run
```

A aplicação estará disponível em:
- **Backend:** http://localhost:8080
- **Frontend:** http://localhost:3000 (se configurado)

## :material-cog: Configuração Detalhada

### Banco de Dados

#### PostgreSQL Local
```bash
# Instalação no Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Inicie o serviço
sudo systemctl start postgresql

# Acesse o PostgreSQL
sudo -u postgres psql

# Crie usuário e banco
CREATE USER bsfm_user WITH PASSWORD 'senha_segura';
CREATE DATABASE bsfm_dev OWNER bsfm_user;
GRANT ALL PRIVILEGES ON DATABASE bsfm_dev TO bsfm_user;
```

#### SQLite (Alternativa para desenvolvimento)
Altere a connection string no `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=bsfm.db"
  }
}
```

### Configuração do .NET

#### MeusApp.csproj
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.*" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.*">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.*" />
    <PackageReference Include="YoloDotNet" Version="2.0.0" />
    <PackageReference Include="BCrypt.Net-Next" Version="4.0.3" />
    <PackageReference Include="MailKit" Version="4.3.0" />
    <PackageReference Include="MimeKit" Version="4.3.0" />
  </ItemGroup>
</Project>
```

### Configuração do Frontend

#### Tailwind CSS
```bash
# Instale o Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### Configuração do tailwind.config.js
```javascript
module.exports = {
  content: [
    "./wwwroot/**/*.{html,js}",
    "./**/*.cshtml"
  ],
  theme: {
    extend: {
      colors: {
        emerald: {
          50: '#ecfdf5',
          100: '#d1fae5',
          // ... até 900
        }
      }
    }
  },
  plugins: [],
}
```

## :material-test-tube: Testando a Configuração

### 1. Verifique as Dependências
```bash
# .NET SDK
dotnet --version
# Deve retornar: 8.0.100 ou superior

# Node.js
node --version
# Deve retornar: v18.0.0 ou superior

# PostgreSQL
psql --version
# Deve retornar: psql (PostgreSQL) 15.0 ou superior
```

### 2. Teste a Conexão com o Banco
```csharp
// Execute no Package Manager Console ou terminal:
dotnet ef migrations add InitialCreate
dotnet ef database update
```

### 3. Execute os Testes
```bash
# Execute testes unitários
dotnet test

# Ou execute testes específicos
dotnet test --filter "Category=Unit"
```

### 4. Acesse a Aplicação
1. Execute `dotnet run`
2. Acesse http://localhost:8080
3. Você deve ver a página inicial do BSFM
4. Teste a API em http://localhost:8080/swagger (se configurado)

## :material-alert: Solução de Problemas Comuns

### Erro: "Cannot connect to database"
```bash
# Verifique se o PostgreSQL está rodando
sudo systemctl status postgresql

# Verifique as credenciais
psql -h localhost -U postgres -d bsfm_dev
```

### Erro: "Missing API keys"
```powershell
# No PowerShell, configure as variáveis:
$env:USDA_API_KEY = "obtenha_em_https://fdc.nal.usda.gov/api-key-signup.html"
$env:BREVO_API_KEY = "obtenha_em_https://www.brevo.com/"
```

### Erro: "Port already in use"
```bash
# Encontre o processo usando a porta
netstat -ano | findstr :8080

# Ou no Linux/macOS:
lsof -i :8080

# Mate o processo ou use outra porta
# Altere no appsettings.json:
# "BackendUrl": "http://localhost:5000"
```

### Erro: "YOLO model not found"
```bash
# Verifique se o modelo está no lugar correto
ls Models/bsfmv1_yolo_final.onnx

# Se não estiver, baixe-o:
# O modelo está incluído no repositório, verifique o commit history
```

## :material-rocket: Configuração para Produção

### Railway Deployment
```bash
# Instale a CLI do Railway
npm i -g @railway/cli

# Login
railway login

# Inicialize o projeto
railway init

# Configure variáveis
railway variables set USDA_API_KEY=suachave
railway variables set BREVO_API_KEY=suachave
railway variables set DATABASE_URL=postgresql://...

# Deploy
railway up
```

### Docker (Opcional)
```dockerfile
# Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "MeusApp.dll"]
```

## :material-book: Próximos Passos

1. **Explore a Arquitetura:** [Arquitetura do Sistema](/bsfm/developer-guide/architecture.md)
2. **Conheça a API:** [API Reference](/bsfm/developer-guide/api.md)
3. **Aprenda sobre Deployment:** [Deploy em Produção](/bsfm/developer-guide/deployment.md)
4. **Contribua:** [Guidelines de Contribuição](https://github.com/Isaque-Medeiros/BSFM/blob/main/CONTRIBUTING.md)

## :material-help-circle: Suporte

- **Issues do GitHub:** [Reportar problemas](https://github.com/Isaque-Medeiros/BSFM/issues)
- **Documentação:** Esta documentação e comentários no código
- **Comunidade:** [Discord do projeto](https://discord.gg/bsfm)

---

:material-lightbulb: **Dica de Desenvolvimento:** Use `dotnet watch run` durante o desenvolvimento para hot reload automático quando arquivos forem modificados.

*Guia atualizado em Abril 2026 - Equipe BSFM*