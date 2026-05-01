# Changelog

Todas as mudanças notáveis no projeto BSFM serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e o projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.3.5] - 2026-05-01 - CoreAnalytics

### Adicionado
- **BSFM.CoreAnalytics**: Módulo de análise de rótulos nutricionais com Split Architecture
- **Analisador de Rótulos (OCR)**: Escaneamento de tabelas nutricionais com Tesseract.js
- **Groq LLM Integration**: Motor NutriBrainService com Llama 3 para feedback personalizado
- **Context Injector**: SystemPrompt com dados biométricos do usuário
- **Health Score**: Pontuação de saúde (0-10) com feedback restritivo
- **Dados de Saúde do Usuário**: Cadastro de diabetes e intolerâncias alimentares
- **App Mobile - Login como Página Inicial**: App inicia diretamente no login

### Alterado
- **AnaliseIA**: Novos campos (PodeConsumir, PontuacaoSaude, AnaliseEmRelacaoAMeta, DicaBSFM)
- **Usuarios**: Novas colunas (Diabetes, Intolerancia)
- **Migrações automáticas**: Adiciona colunas sem scripts SQL manuais
- **Documentação MkDocs**: Atualizada com informações do CoreAnalytics

### Corrigido
- **Navegação mobile**: App não fica mais na landing page, inicia no login

---

## [1.3.0] - 2026-04-29 - Atualização Pré-Definitiva

### Adicionado
- **PWA (Progressive Web App)**: Aplicação instalável em dispositivos móveis
- **Service Worker**: Cache offline com estratégia network-first
- **Ícone SVG do BSFM**: Logotipo otimizado para PWA
- **Meta tags PWA**: Adicionadas em todas as páginas HTML

### Alterado
- **Documentação MkDocs atualizada**: Conteúdo realista de protótipo
- **Correção de navegação**: Links rápidos da home page corrigidos
- **Paleta de cores ajustada**: Barra de navegação preta com detalhes em laranja

---

## [1.2.0] - 2026-04-28 - Remasterização Final

### Adicionado
- **Consumo de água**: Registro diário e semanal de hidratação
- **Plano de refeições semanal**: Agendamento de refeições por dia da semana
- **Perfil do usuário**: Edição de dados pessoais
- **Gráficos de evolução**: Chart.js para visualização de progresso
- **Mapa SOS Saúde**: Leaflet para localização de UPAs e hospitais
- **Central LIBRAS**: Conteúdo em Língua Brasileira de Sinais

### Alterado
- **Refatoração do tema**: Light-mode como padrão
- **Animações e melhorias de UI/UX**: Transições suaves e feedback visual
- **Configuração de deploy no Render**: Dockerfile e render.yaml
- **Documentação revisada**: Transparência sobre status de protótipo

---

## [1.1.0] - 2026-04-08 - Versão Remaster SDD

### Adicionado
- **Arquitetura refinada**: Baseada em metodologia SDD
- **Melhorias na documentação técnica**

### Alterado
- **Refatoração do código**: Melhor organização e separação de responsabilidades

---

## [1.0.0] - 2026-03-20 - Primeira Versão Funcional

### Adicionado
- **Backend .NET 8.0**: Rotas de API RESTful
- **Sistema de cadastro e login**: Autenticação com verificação por email
- **Dashboard**: Métricas básicas (IMC, TMB, TDEE)
- **Análise de alimentos por IA**: YOLO Object Detection com modelo ONNX
- **Integração com USDA API**: Consulta de dados nutricionais
- **Diário alimentar**: Registro de refeições analisadas
- **Banco de dados PostgreSQL**: Modelagem inicial

---

## [0.1.0] - 2026-02-29 - Início do Projeto

### Adicionado
- Definição do tema da ONG de nutrição
- Criação do grupo de desenvolvimento
- Divisão das tarefas entre os 4 integrantes
- Planejamento dos RF (Requisitos Funcionais) e RNF (Requisitos Não Funcionais)
- Identificação dos Stakeholders
- Definição dos termos de contrato

---

## Notas de Versão

### Compatibilidade
- **v1.3.5**: Requer .NET 8.0+, PostgreSQL 15+ ou SQLite
- **v1.3.0**: Requer .NET 8.0+, PostgreSQL 15+ ou SQLite
- **v1.2.0**: Requer .NET 8.0+, PostgreSQL 15+ ou SQLite
- **v1.0.0**: Requer .NET 8.0+, PostgreSQL 15+

### Atualização
Para atualizar de uma versão anterior:
1. Faça backup do banco de dados
2. Atualize o código fonte
3. Execute `dotnet run` (migrações automáticas)
4. Verifique o health check

---

**Última atualização:** 01 de Maio de 2026
