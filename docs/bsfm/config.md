# Configuração do Projeto

Esta página centraliza os parâmetros básicos para executar e manter o BSFM.

## 🗄️ Configuração do Banco de Dados

### Estrutura do Banco
O BSFM utiliza PostgreSQL (produção) ou SQLite (desenvolvimento) com as seguintes tabelas principais:
- **Usuarios**: Dados dos usuários e métricas nutricionais (inclui Diabetes e Intolerancia)
- **Refeicoes**: Catálogo de refeições completas
- **Comidas**: Alimentos individuais e seus valores nutricionais
- **CronogramaAlimentar**: Planos alimentares dos usuários
- **Hospitais**: Instituições de saúde parceiras
- **AnaliseIA**: Análises de alimentos realizadas por IA (inclui campos de feedback: PodeConsumir, PontuacaoSaude, AnaliseEmRelacaoAMeta, DicaBSFM)
- **HistoricoProgresso**: Evolução temporal dos usuários
- **ConsumoAgua**: Registro de hidratação diária
- **RefeicoesAgendadas**: Refeições agendadas por dia da semana

### Configuração de Desenvolvimento

Crie `appsettings.Development.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=bsfm_dev;Username=bsfm_user;Password=senha_segura"
  },
  "Database": {
    "Provider": "PostgreSQL",
    "Version": "15.0",
    "Timeout": 30,
    "Pooling": true,
    "MaxPoolSize": 100
  },
  "ApiKeys": {
    "UsdaApiKey": "SUA_CHAVE_USDA",
    "BrevoApiKey": "SUA_CHAVE_BREVO",
    "GroqApiKey": "SUA_CHAVE_GROQ"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning"
    }
  }
}
```

### Variáveis de Ambiente Recomendadas

```bash
# Banco de dados
DATABASE_URL=Host=localhost;Database=bsfm_dev;Username=bsfm_user;Password=senha_segura
DB_PROVIDER=PostgreSQL
DB_TIMEOUT=30

# APIs Externas
USDA_API_KEY=sua_chave_usda_aqui
BREVO_API_KEY=sua_chave_brevo_aqui
GROQ_API_KEY=sua_chave_groq_aqui

# Ambiente
ASPNETCORE_ENVIRONMENT=Development
ASPNETCORE_URLS=http://localhost:5000

# Logging
LOG_LEVEL=Information
DB_LOG_LEVEL=Warning
```

### Configuração de Produção (Render)

Para produção no Render, utilize variáveis de ambiente no painel do Web Service:

| Variável | Descrição |
|----------|-----------|
| `DATABASE_URL` | Connection string do PostgreSQL (fornecido pelo Render) |
| `USDA_API_KEY` | Chave da API USDA FoodData Central |
| `BREVO_API_KEY` | Chave da API Brevo (Sendinblue) |
| `GROQ_API_KEY` | Chave da API Groq (para feedback IA) |
| `ASPNETCORE_ENVIRONMENT` | `Production` |
| `PORT` | Porta atribuída pelo Render (automático) |

## Configuração de Tema/Documentação

A documentação MkDocs está com:

- Tema escuro como padrão
- Tema claro opcional via toggle
- Paleta personalizada em vermelho, verde e laranja
- CSS principal em `docs/stylesheets/custom.css`
- Script de tema em `docs/js/custom.js`

## Configuração de Deploy

### Produção
- **Render**: Hospedagem principal da aplicação (backend + frontend)
- **Vercel**: Hospedagem da documentação MkDocs

### Arquivos de Configuração
- `render.yaml`: Configuração Infrastructure as Code
- `Dockerfile`: Containerização da aplicação .NET
- `mkdocs.yml`: Configuração da documentação

## Migrações Automáticas

O sistema realiza migrações automáticas no startup para adicionar colunas necessárias sem precisar de scripts SQL manuais:

- **Diabetes** (VARCHAR(50)) na tabela Usuarios
- **Intolerancia** (TEXT) na tabela Usuarios
- **PodeConsumir** (BOOLEAN) na tabela AnalisesIA
- **PontuacaoSaude** (INTEGER) na tabela AnalisesIA
- **AnaliseEmRelacaoAMeta** (TEXT) na tabela AnalisesIA
- **DicaBSFM** (TEXT) na tabela AnalisesIA

## Boas Práticas

- Não commitar chaves reais no repositório
- Usar variáveis de ambiente/secrets no deploy
- Revisar configurações antes de cada release
- Manter o `appsettings.json` com valores padrão seguros
- A GROQ_API_KEY é opcional - sem ela, o feedback IA não estará disponível
