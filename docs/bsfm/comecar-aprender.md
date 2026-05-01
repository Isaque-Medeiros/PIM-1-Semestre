---
title: "Começar a Aprender"
description: "Primeiros passos para usar a plataforma BSFM"
---

# Começar a Aprender

Este guia foi criado para acelerar sua entrada na plataforma BSFM.

## O que você vai fazer primeiro

1. Criar sua conta
2. Configurar perfil e metas
3. Registrar sua primeira refeição
4. Acompanhar resultados no dashboard

## Passo 1 - Criar conta

- Cadastre email e senha forte
- Confirme o email para liberar acesso
- Complete dados básicos do perfil

## Passo 2 - Definir objetivo

Escolha seu foco inicial:

- Perda de peso
- Ganho de massa
- Reeducação alimentar
- Manutenção de resultados

## Passo 3 - Registrar alimentação

No primeiro dia, registre:

- Café da manhã
- Almoço
- Jantar
- Lanches

Com isso, o sistema começa a calcular indicadores como consumo calórico, distribuição de macronutrientes e progresso de meta.

## Passo 4 - Ler o dashboard

No dashboard você acompanha:

- Calorias consumidas x meta do dia
- Evolução de peso e histórico
- Indicadores de performance da rotina alimentar

## Funcionalidades Avançadas

### Analisador de Rótulos (OCR)
1. Acesse o **Analisador de Rótulos**
2. Aponte a câmera para a tabela nutricional de um produto
3. O Tesseract.js extrai o texto automaticamente
4. A IA do Groq analisa e retorna:
   - **Health Score** (0-10)
   - **Pode Consumir** (sim/não/moderado)
   - **Análise personalizada** baseada no seu perfil
   - **Dica BSFM** com sugestões

### Dados de Saúde
1. Acesse **Perfil** > **Dados de Saúde**
2. Informe se possui:
   - **Diabetes** (Tipo 1, Tipo 2, Pré-diabetes, Gestacional)
   - **Intolerâncias Alimentares** (Lactose, Glúten, etc.)
3. A IA considera esses dados nas análises nutricionais

## Fluxo sugerido de uso semanal

- Segunda a sexta: registrar refeições diariamente
- Sábado: revisar relatório da semana
- Domingo: ajustar metas para a próxima semana

## Linha do tempo do projeto

- Início do desenvolvimento: 29 de fevereiro de 2026
- Primeira versão (v1.0): 20 de março de 2026
- Versão remaster com metodologia SDD: 08 de abril de 2026
- Remasterização final (v1.2.0): 28 de abril de 2026
- Atualização PWA (v1.3.0): 29 de abril de 2026
- CoreAnalytics (v1.3.5): 01 de maio de 2026

## Infraestrutura e deploy

- **Produção**: Render (backend + frontend)
- **Documentação**: Vercel (MkDocs)

## Próximas leituras

- [Instalação](instalacao.md)
- [Configuração](config.md)
- [Guia do Usuário](../guia-usuario/introducao.md)
- [Roadmap](../roadmap/index.md)
