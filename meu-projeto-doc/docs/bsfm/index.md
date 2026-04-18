---
title: BSFM - Brazilian System of Food Metric
description: Plataforma completa de nutrição inteligente com IA para análise de alimentos e acompanhamento nutricional personalizado
---

# BSFM - Brazilian System of Food Metric

<div class="grid cards" markdown>

-   :material-brain:{ .lg .middle } **Visão Geral**
    
    ---
    
    Conheça a plataforma revolucionária de nutrição inteligente que combina IA, análise nutricional em tempo real e acompanhamento personalizado.

    [:octicons-arrow-right-24: Visão e Missão](#visão-e-missão)

-   :material-rocket-launch:{ .lg .middle } **Primeiros Passos**
    
    ---
    
    Comece a usar o BSFM com nosso guia completo de introdução e configuração inicial.

    [:octicons-arrow-right-24: Guia do Usuário](/bsfm/user-guide/)

-   :material-code-braces:{ .lg .middle } **Desenvolvimento**
    
    ---
    
    Documentação técnica completa para desenvolvedores, incluindo arquitetura, API e deployment.

    [:octicons-arrow-right-24: Guia do Desenvolvedor](/bsfm/developer-guide/)

-   :material-shield-check:{ .lg .middle } **Tecnologia**
    
    ---
    
    Stack tecnológico, IA, banco de dados e segurança implementados na plataforma.

    [:octicons-arrow-right-24: Tecnologias](/bsfm/technology/)

</div>

---

## :material-check-circle: Status do Projeto

| Componente | Status | Versão | Notas |
| :--- | :--- | :--- | :--- |
| **Backend (.NET 8.0)** | :material-check-circle:{ style="color: #10b981" } Produção | v2.0.0 | API completa com autenticação |
| **Frontend (Tailwind)** | :material-check-circle:{ style="color: #10b981" } Produção | v2.0.0 | Interface responsiva PWA-ready |
| **IA (YOLO Model)** | :material-check-circle:{ style="color: #10b981" } Produção | bsfmv1_yolo_final | 452 alimentos reconhecidos |
| **Banco de Dados** | :material-check-circle:{ style="color: #10b981" } Produção | PostgreSQL 15 | Railway hosting |
| **Documentação** | :material-progress-check:{ style="color: #3b82f6" } Em expansão | v1.0.0 | Esta documentação |

---

## :material-target: Visão e Missão

### Visão
Ser o sistema de referência em métricas alimentares no Brasil, democratizando o acesso à nutrição de qualidade através da tecnologia.

### Missão
Utilizar inteligência artificial para fornecer análises nutricionais precisas, acompanhamento personalizado e educação alimentar acessível a todos os brasileiros.

---

## :material-star: Funcionalidades Principais

### 1. :material-camera: Análise de Alimentos por IA
- **Detecção visual** de alimentos em tempo real com YOLO Object Detection
- **Tradução automática** EN → PT para 452 alimentos
- **Análise nutricional completa** por 100g via USDA API
- **Suporte a porções** (pequeno, médio, grande) com cálculo automático

### 2. :material-chart-bar: Dashboard Personalizado
- **Métricas de saúde** (IMC, TMB, Gasto Calórico) com cálculos científicos
- **Evolução histórica** de peso/altura com gráficos interativos
- **Progresso nutricional** com visualizações claras e intuitivas
- **Metas personalizadas** com acompanhamento e notificações

### 3. :material-account: Sistema de Usuários
- **Cadastro seguro** com verificação por email via Brevo API
- **Autenticação robusta** com BCrypt hashing e salt automático
- **Redefinição de senha** com tokens únicos de 6 dígitos
- **Aceitação de termos** com registro de data e versão

### 4. :material-hospital: Integração Hospitalar
- **Diretório de hospitais** parceiros com informações completas
- **Informações de contato** e endereços para acesso rápido
- **Serviços de saúde** integrados à plataforma

### 5. :material-calendar: Cronograma Alimentar
- **Planos alimentares** personalizados baseados em perfil metabólico
- **Refeições diárias** programadas com sugestões inteligentes
- **Acompanhamento nutricional** semanal com ajustes automáticos

---

## :material-cog: Arquitetura Técnica

### Stack Tecnológico Principal

#### Backend (.NET 8.0)
- **Framework:** ASP.NET Core 8.0 (Minimal APIs)
- **Banco de Dados:** PostgreSQL (Railway) + SQLite (desenvolvimento)
- **ORM:** Entity Framework Core 8.0 (Code-First)
- **Autenticação:** BCrypt.Net-Next para hash de senhas
- **Email:** MailKit + MimeKit + Brevo API
- **IA:** YoloDotNet + ONNX Runtime

#### Frontend (HTML/CSS/JS)
- **Framework CSS:** Tailwind CSS 3.0+
- **Fontes:** Google Fonts (Inter + Outfit)
- **Ícones:** Font Awesome 6.4.0 + Material Design Icons
- **Design System:** Glassmorphism + Gradients + Animations

#### APIs Externas Integradas
- **USDA FoodData Central API** - Dados nutricionais científicos
- **Brevo API** - Serviços de email transacional
- **YOLO Object Detection** - Reconhecimento de alimentos

---

## :material-chart-line: Impacto e Métricas

### KPIs do Produto
- **Usuários ativos:** 10,000/mês (meta)
- **Análises realizadas:** 50,000/mês (meta)
- **Precisão da IA:** >80% em testes
- **Satisfação do usuário:** >4.5/5 (meta)

### Impacto na Saúde
- **Redução de IMC:** 15% dos usuários (meta)
- **Melhoria alimentar:** 70% dos usuários (meta)
- **Adesão ao tratamento:** 40% aumento (meta)

---

## :material-book-open: Documentação por Tipo de Usuário

<div class="grid" markdown>

- **Usuários Finais**
    
    ---
    
    Aprenda a usar todas as funcionalidades da plataforma para melhorar sua saúde alimentar.
    
    [:octicons-arrow-right-24: Guia do Usuário](/bsfm/user-guide/)

- **Desenvolvedores**
    
    ---
    
    Implemente, estenda ou integre o BSFM em seus projetos com nossa documentação técnica completa.
    
    [:octicons-arrow-right-24: Guia do Desenvolvedor](/bsfm/developer-guide/)

- **Profissionais de Saúde**
    
    ---
    
    Utilize o BSFM como ferramenta de apoio em consultas e acompanhamento de pacientes.
    
    [:octicons-arrow-right-24: Casos de Uso](/bsfm/user-guide/cases/)

- **Parceiros**
    
    ---
    
    Integre o BSFM em sua instituição ou produto através de nossa API pública.
    
    [:octicons-arrow-right-24: API Reference](/bsfm/developer-guide/api/)

</div>

---

## :material-history: Roadmap

### Fase 1 - MVP Atual ✅
- [x] Análise básica de alimentos com IA
- [x] Sistema de usuários completo
- [x] Dashboard simples com métricas
- [x] Integração USDA API

### Fase 2 - Aprimoramentos 🚧
- [ ] App mobile nativo (React Native/Flutter)
- [ ] Reconhecimento de porções automático
- [ ] Planos alimentares gerados por IA
- [ ] Integração com wearables (Apple Health/Google Fit)

### Fase 3 - Expansão 📅
- [ ] API pública para desenvolvedores
- [ ] Marketplace de profissionais de nutrição
- [ ] Análise de receitas completas
- [ ] Integração com supermercados e delivery

---

## :material-download: Comece Agora

<div class="grid" markdown>

-   **Para Usuários**
    
    ---
    
    Acesse a plataforma e comece sua jornada de saúde alimentar hoje mesmo.
    
    [:material-rocket-launch: Acessar BSFM](https://bsfm-app.railway.app/){ .md-button .md-button--primary }

-   **Para Desenvolvedores**
    
    ---
    
    Clone o repositório e configure o ambiente de desenvolvimento local.
    
    [:material-code-braces: Setup Local](/bsfm/developer-guide/setup.md){ .md-button }

-   **Para Contribuidores**
    
    ---
    
    Contribua com o projeto open source através de issues e pull requests.
    
    [:material-github: GitHub Repository](https://github.com/Isaque-Medeiros/BSFM){ .md-button }

</div>

---

## :material-help-circle: Suporte

- **Documentação:** Esta documentação completa com FAQ
- **GitHub Issues:** [Reportar bugs](https://github.com/Isaque-Medeiros/BSFM/issues)
- **Email:** suporte@bsfm.com.br (contato direto)
- **Comunidade:** Discord para desenvolvedores e usuários

---

*Documentação atualizada em Abril 2026 - BSFM Team*  
*Plataforma em constante evolução com atualizações semanais*