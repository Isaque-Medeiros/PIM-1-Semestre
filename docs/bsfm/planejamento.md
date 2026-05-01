---
title: "Planejamento de Gerenciamento do Projeto"
date: 2026
layout: default
---

# Planejamento de Gerenciamento do Projeto

## Organização das Atividades

**Analisando** o documento de guia do trabalho semestral do 3° semestre, decidimos o tema da nossa ONG, qual área ela irá abordar, qual dificuldade e o impacto que gerará.

Após isso, foi criado um grupo no *WhatsApp* para realizar a divisão das atividades e ter fácil comunicação entre todos os integrantes do grupo.

### Divisão das Tarefas

A divisão das tarefas ficou assim:

- **Todos** ficaram responsáveis por planejar os *RF e RNF*, identificar os *Stakeholders* e definir os *termos de contrato* com o sistema e o cliente final.
- **Isaque de Medeiros** ficou responsável por desenvolver as Funcionalidades em <b style="color: #512bd4;">C#</b>
- **Gustavo** responsável pelo banco de Dados
- **Yuri** responsável pela documentação do Projeto
- **Giovana** responsável pelo design do site
- **Todos** responsáveis pelo desenvolvimento e críticas de melhorias.
- **Libras** a critério da IA para o melhor modo de ensino e distribuir informação para o usuário.

### Cronograma de Desenvolvimento

| Período | Atividade | Responsável |
|---------|-----------|-------------|
| 29/02 - 07/03 | Planejamento e definição do tema | Equipe BSFM |
| 08/03 - 20/03 | Desenvolvimento v1.0 (backend + frontend) | Desenvolvedor |
| 21/03 - 08/04 | Remasterização SDD | Designer e Desenvolvedor |
| 09/04 - 28/04 | Remasterização final e deploy | Equipe BSFM |
| 28/04 - 30/04 | Correções de bugs, implementando APK e Deploy | Desenvolvedor |
| 01/05 | CoreAnalytics v1.3.5 - Motor de insights nutricionais | Equipe de Qualidade |

### Tecnologias Utilizadas

- **Backend**: C# com ASP.NET Core 8.0
- **Frontend**: HTML, CSS, JavaScript (Tailwind CSS)
- **Banco de Dados**: PostgreSQL / SQLite
- **IA (Visão)**: YOLO Object Detection (ONNX)
- **IA (Texto)**: Groq Llama 3 para feedback nutricional
- **OCR**: Tesseract.js (processamento no navegador)
- **Deploy**: Render
- **Documentação**: MkDocs (Vercel)

### Funcionalidades Implementadas

1. ✅ Cadastro e login de usuários
2. ✅ Dashboard com métricas (IMC, TMB, TDEE)
3. ✅ Análise de alimentos por IA (YOLO + USDA)
4. ✅ Diário alimentar
5. ✅ Plano de refeições semanal
6. ✅ Consumo de água
7. ✅ Mapa SOS Saúde (Leaflet)
8. ✅ Central LIBRAS
9. ✅ Perfil do usuário
10. ✅ Gráficos de evolução (Chart.js)
11. ✅ PWA (Progressive Web App)
12. ✅ Analisador de Rótulos (OCR + Groq LLM)
13. ✅ Dados de Saúde (Diabetes e Intolerâncias)
14. ✅ Health Score com feedback personalizado
15. ✅ App mobile inicia no login (não na landing page)
